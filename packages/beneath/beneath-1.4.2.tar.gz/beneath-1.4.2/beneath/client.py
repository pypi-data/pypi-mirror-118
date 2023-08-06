from collections.abc import Mapping
from datetime import timedelta
import json
import logging
import os
import sys
from typing import Dict, Iterable, List, Union

import pandas as pd

from beneath import config
from beneath.admin.client import AdminClient
from beneath.checkpointer import Checkpointer, PrefixedCheckpointer
from beneath.config import DEFAULT_READ_BATCH_SIZE
from beneath.connection import Connection, GraphQLError
from beneath.consumer import Consumer
from beneath.instance import TableInstance
from beneath.job import Job
from beneath.table import Table
from beneath.utils import infer_avro, ProjectIdentifier, TableIdentifier, SubscriptionIdentifier
from beneath.writer import DryWriter, Writer


class Client:
    """
    The main class for interacting with Beneath.
    Data-related features (like defining tables and reading/writing data) are implemented
    directly on `Client`, while control-plane features (like creating projects) are isolated in
    the `admin` member.

    Args:
        secret (str):
            A beneath secret to use for authentication. If not set, uses the
            ``BENEATH_SECRET`` environment variable, and if that is not set either, uses the secret
            authenticated in the CLI (stored in ``~/.beneath``).
        dry (bool):
            If true, the client will not perform any mutations or writes, but generally perform
            reads as usual. It's useful for testing.

            The exact implication differs for different operations: Some mutations will be mocked,
            such as creating a table, others will fail with an exception. Write operations log
            records to the logger instead of transmitting to the server. Reads generally work, but
            throw an exception when called on mocked resources.
        write_delay_ms (int):
            The maximum amount of time to buffer written records before sending
            a batch write request over the network. Defaults to 1 second (1000 ms).
            Writing records in batches reduces the number of requests, which leads to lower cost
            (Beneath charges at least 1kb per request).
    """

    def __init__(
        self,
        secret: str = None,
        dry: bool = False,
        write_delay_ms: int = config.DEFAULT_WRITE_DELAY_MS,
    ):
        self.connection = Connection(secret=self._get_secret(secret=secret))
        self.admin = AdminClient(connection=self.connection, dry=dry)
        self.dry = dry
        self.logger = self._make_default_logger()

        if dry:
            self._writer = DryWriter(client=self, max_delay_ms=write_delay_ms)
        else:
            self._writer = Writer(client=self, max_delay_ms=write_delay_ms)

        self._start_count = 0
        self._checkpointers: Dict[ProjectIdentifier, Checkpointer] = {}
        self._consumers: Dict[SubscriptionIdentifier, Consumer] = {}

    @classmethod
    def _get_secret(cls, secret=None):
        if not secret:
            secret = os.getenv("BENEATH_SECRET", default=None)
        if not secret:
            secret = config.read_secret()
        if not secret:
            raise ValueError(
                "You are not authenticated (either run 'beneath auth' in the CLI, set the "
                "BENEATH_SECRET environment variable, or pass a secret to the Client constructor)"
            )
        if not isinstance(secret, str):
            raise TypeError("secret must be a string")
        return secret.strip()

    @classmethod
    def _make_default_logger(cls):
        h1 = logging.StreamHandler(sys.stdout)
        h1.setLevel(logging.INFO)
        h1.addFilter(lambda record: record.levelno <= logging.INFO)

        h2 = logging.StreamHandler(sys.stderr)
        h2.setLevel(logging.WARNING)

        logging.basicConfig(handlers=[h1, h2])
        logger = logging.getLogger("beneath")
        logger.setLevel(logging.INFO)
        return logger

    # FINDING AND STAGING TABLES

    async def find_table(self, table_path: str) -> Table:
        """
        Finds an existing table and returns an object that you can use to
        read and write from/to the table.

        Args:
            path (str):
                The path to the table in the format of "USERNAME/PROJECT/TABLE"
        """
        identifier = TableIdentifier.from_path(table_path)
        table = await Table._make(client=self, identifier=identifier)
        return table

    async def create_table(
        self,
        table_path: str,
        schema: str,
        description: str = None,
        meta: bool = None,
        use_index: bool = None,
        use_warehouse: bool = None,
        retention: timedelta = None,
        log_retention: timedelta = None,
        index_retention: timedelta = None,
        warehouse_retention: timedelta = None,
        schema_kind: str = "GraphQL",
        indexes: str = None,
        update_if_exists: bool = None,
    ) -> Table:
        """
        Creates (or optionally updates if ``update_if_exists=True``) a table and returns it.

        Args:
            table_path (str):
                The (desired) path to the table in the format of "USERNAME/PROJECT/TABLE".
                The project must already exist. If the table doesn't exist yet, it creates it.
            schema (str):
                The GraphQL schema for the table. To learn about the schema definition language,
                see https://about.beneath.dev/docs/reading-writing-data/schema-definition/.
            description (str):
                The description shown for the table in the web console. If not set, tries to infer
                a description from the schema.
            retention (timedelta):
                The amount of time to retain records written to the table.
                If not set, records will be stored forever.
            schema_kind (str):
                The parser to use for ``schema``. Currently must be "GraphQL" (default).
            update_if_exists (bool):
                If true and the table already exists, the provided info will be used to update
                the table (only supports non-breaking schema changes) before returning it.
        """
        identifier = TableIdentifier.from_path(table_path)
        if self.dry:
            data = await self.admin.tables.compile_schema(
                schema_kind=schema_kind,
                schema=schema,
            )
            table = await Table._make_dry(
                client=self,
                identifier=identifier,
                avro_schema=data["canonicalAvroSchema"],
            )
        else:
            data = await self.admin.tables.create(
                organization_name=identifier.organization,
                project_name=identifier.project,
                table_name=identifier.table,
                schema_kind=schema_kind,
                schema=schema,
                indexes=indexes,
                description=description,
                meta=meta,
                use_index=use_index,
                use_warehouse=use_warehouse,
                log_retention_seconds=self._timedelta_to_seconds(
                    log_retention if log_retention else retention
                ),
                index_retention_seconds=self._timedelta_to_seconds(
                    index_retention if index_retention else retention
                ),
                warehouse_retention_seconds=self._timedelta_to_seconds(
                    warehouse_retention if warehouse_retention else retention
                ),
                update_if_exists=update_if_exists,
            )
            table = await Table._make(client=self, identifier=identifier, admin_data=data)
        return table

    @staticmethod
    def _timedelta_to_seconds(td: timedelta):
        if not td:
            return None
        secs = int(td.total_seconds())
        if secs == 0:
            return None
        return secs

    # WAREHOUSE QUERY

    async def query_warehouse(
        self,
        query: str,
        analyze: bool = False,
        max_bytes_scanned: int = config.DEFAULT_QUERY_WAREHOUSE_MAX_BYTES_SCANNED,
        timeout_ms: int = config.DEFAULT_QUERY_WAREHOUSE_TIMEOUT_MS,
    ):
        """
        Starts a warehouse (OLAP) SQL query, and returns a job for tracking its progress

        Args:
            query (str):
                The analytical SQL query to run. To learn about the query language,
                see https://about.beneath.dev/docs/reading-writing-data/warehouse-queries/.
            analyze (bool):
                If true, analyzes the query and returns info about referenced tables
                and expected bytes scanned, but doesn't actually run the query.
            max_bytes_scanned (int):
                Sets a limit on the number of bytes the query can scan.
                If exceeded, the job will fail with an error.
        """
        resp = await self.connection.query_warehouse(
            query=query,
            dry_run=analyze,
            max_bytes_scanned=max_bytes_scanned,
            timeout_ms=timeout_ms,
        )
        job_data = resp.job
        return Job(client=self, job_id=job_data.job_id, job_data=job_data)

    # WRITING

    async def start(self):
        """
        Opens the client for writes.
        Can be called multiple times, but make sure to call ``stop`` correspondingly.
        """
        self._start_count += 1
        if self._start_count != 1:
            return

        await self.connection.ensure_connected()
        await self._writer.start()

        for checkpointer in self._checkpointers.values():
            await checkpointer._start()

    async def stop(self):
        """
        Closes the client for writes, ensuring buffered writes are flushed.
        If ``start`` was called multiple times, only the last corresponding call
        to ``stop`` triggers a flush.
        """

        if self._start_count == 0:
            raise Exception("Called stop more times than start")

        if self._start_count == 1:
            for checkpointer in self._checkpointers.values():
                await checkpointer._stop()
            await self._writer.stop()

        self._start_count -= 1

    async def write(self, instance: TableInstance, records: Union[Mapping, Iterable[Mapping]]):
        """
        Writes one or more records to ``instance``. By default, writes are buffered for up to
        ``write_delay_ms`` milliseconds before being transmitted to the server. See the Client
        constructor for details.

        To enabled writes, make sure to call ``start`` on the client (and ``stop`` before
        terminating).

        Args:
            instance (TableInstance):
                The instance to write to. You can also call ``instance.write`` as a convenience
                wrapper.
            records:
                The records to write. Can be a single record (dict) or a list of records (iterable
                of dict).
        """
        if self._start_count == 0:
            raise Exception("Cannot call write because the client is stopped")
        await self._writer.write(instance, records)

    async def force_flush(self):
        """Forces the client to flush buffered writes without stopping"""
        await self._writer.force_flush()

    async def write_full(
        self,
        table_path: str,
        records: Union[Iterable[dict], pd.DataFrame],
        key: Union[str, List[str]] = None,
        description: str = None,
        recreate_on_schema_change=False,
    ):
        """
        Infers a schema, creates a table, and writes a full dataset to Beneath.
        Each call will create a new primary version for the table, and delete the old primary
        version if/when the write completes succesfully.

        Args:
            table_path (str):
                The (desired) path to the table in the format of "USERNAME/PROJECT/TABLE".
                The project must already exist.
            records (list(dict) | pandas.DataFrame):
                The full dataset to write, either as a list of records or as a Pandas DataFrame.
                This function uses ``beneath.infer_avro`` to infer a schema for the table based
                on the records.
            key (str | list(str)):
                The fields to use as the table's key. If not set, will default to the dataframe
                index if ``records`` is a Pandas DataFrame, or add a column of incrementing numbers
                if ``records`` is a list.
            description (str):
                A description for the table.
            recreate_on_schema_change (bool):
                If true, and there's an existing table at ``table_path`` with a schema that is
                incompatible with the inferred schema for ``records``, it will delete the existing
                table and create a new one instead of throwing an error. Defaults to false.
        """
        if self._start_count == 0:
            raise Exception("Cannot call write_full because the client is stopped")
        if len(records) == 0:
            return
        # hairy defaults for `key`
        if isinstance(key, str):
            key = [key]
        if not key:
            if isinstance(records, pd.DataFrame):
                index_named = None
                for name in records.index.names:
                    if index_named is None:
                        index_named = name is not None
                    elif index_named == (name is None):
                        raise ValueError(
                            "Cannot write DataFrame with mixed null and non-null"
                            f" index names {records.index.names}"
                        )
                if index_named:
                    key = records.index.names
                    records = records.reset_index()
                else:
                    if len(records.index.names) > 1:
                        key = [f"key{idx}" for idx, name in enumerate(records.index.names)]
                    else:
                        key = ["key"]
                    records.index.names = key
                    records = records.reset_index()
            else:
                for idx, record in enumerate(records):
                    if "key" not in record:
                        record["key"] = idx
                    key = ["key"]

        # infer schema and indexes
        schema = infer_avro(records)
        indexes = json.dumps([{"key": True, "fields": key}])

        # create the table
        try:
            table = await self.create_table(
                table_path=table_path,
                schema=schema,
                description=description,
                schema_kind="Avro",
                indexes=indexes,
                update_if_exists=True,
            )
        except GraphQLError as e:
            if "Schema error:" not in str(e):
                raise
            if not recreate_on_schema_change:
                raise ValueError(
                    "Cannot create table because an existing table *with a different schema* "
                    f"already exists at '{table_path}'. To delete the existing table and all its"
                    " versions and records, pass recreate_on_schema_change=True."
                )
            # recreate
            table = await self.find_table(table_path)
            await self.admin.tables.delete(table_id=str(table.table_id))
            table = await self.create_table(
                table_path=table_path,
                schema=schema,
                description=description,
                schema_kind="Avro",
                indexes=indexes,
                update_if_exists=True,
            )

        # get instance
        next_instance = None
        previous_instance = None
        if table.primary_instance is None:
            next_instance = await table.create_instance()
        elif table.primary_instance.is_final:
            next_instance = await table.create_instance()
            previous_instance = table.primary_instance
        else:
            next_instance = table.primary_instance

        # write records
        if isinstance(records, pd.DataFrame):
            records = records.to_dict(orient="records")
        await next_instance.write(records)

        # make primary and final, and delete previous instance
        await next_instance.update(make_primary=True, make_final=True)
        if previous_instance:
            await previous_instance.delete()

        return table

    # CHECKPOINTERS

    async def checkpointer(
        self,
        project_path: str,
        key_prefix: str = None,
        metatable_name="checkpoints",
        metatable_create: bool = True,
        metatable_description="Stores checkpointed state for consumers, pipelines, and more",
    ) -> Checkpointer:
        """
        Returns a checkpointer for the given project.
        Checkpointers store (small) key-value records useful for maintaining consumer and pipeline
        state. State is stored in a meta-table called "checkpoints" in the given project.

        Args:
            project_path (str):
                Path to the project in which to store the checkpointer's state
            key_prefix (str):
                If set, any ``get`` or ``set`` call on the checkpointer will prepend the prefix
                to the key.
            metatable_name (str):
                Name of the meta table in which to save checkpointed data
            metatable_create (bool):
                If true, the checkpointer will create the checkpoints meta-table if it does not
                already exists. If false, the checkpointer will throw an exception if the
                meta-table does not already exist. Defaults to True.
            metatable_description (str):
                An optional description to apply to the checkpoints meta-table. Defaults to a
                sensible description of checkpointing.
        """
        project_identifier = ProjectIdentifier.from_path(project_path)
        identifier = TableIdentifier(
            organization=project_identifier.organization,
            project=project_identifier.project,
            table=metatable_name,
        )

        if identifier not in self._checkpointers:
            checkpointer = Checkpointer(
                client=self,
                metatable_identifier=identifier,
                metatable_create=metatable_create,
                metatable_description=metatable_description,
            )
            self._checkpointers[identifier] = checkpointer
            if self._start_count != 0:
                await checkpointer._start()

        checkpointer = self._checkpointers[identifier]
        if key_prefix:
            checkpointer = PrefixedCheckpointer(checkpointer, key_prefix)
        return checkpointer

    # CONSUMERS

    async def consumer(
        self,
        table_path: str,
        version: int = None,
        batch_size: int = DEFAULT_READ_BATCH_SIZE,
        subscription_path: str = None,
        checkpointer: Checkpointer = None,
        metatable_create: bool = True,
    ):
        """
        Creates a consumer for the given table.
        Consumers make it easy to replay the history of a table and/or subscribe to new changes.

        Args:
            table_path (str):
                Path to the table to subscribe to. The consumer will subscribe to the table's
                primary version.
            version (int):
                The instance version to use for table. If not set, uses the primary instance.
            batch_size (int):
                Sets the max number of records to load in each network request. Defaults to 1000.
            subscription_path (str):
                Format "ORGANIZATION/PROJECT/NAME". If set, the consumer will use a checkpointer
                to save cursors. That means processing will not restart from scratch if the process
                ends or crashes (as long as you use the same subscription name). To reset a
                subscription, call ``reset`` on the consumer.
            checkpointer (Checkpointer):
                Only applies if ``subscription_path`` is set. Provides a specific checkpointer to
                use for consumer state. If not set, will create one in the subscription's project.
            metatable_create (bool):
                Only applies if ``subscription_path`` is set and ``checkpointer`` is not set.
                Passed through to ``client.checkpointer``.
        """
        table_identifier = TableIdentifier.from_path(table_path)
        if not subscription_path:
            consumer = Consumer(
                client=self,
                table_identifier=table_identifier,
                batch_size=batch_size,
            )
            await consumer._init()
            return consumer

        sub_identifier = SubscriptionIdentifier.from_path(subscription_path)
        if sub_identifier not in self._consumers:
            if checkpointer is None:
                checkpointer = await self.checkpointer(
                    f"{sub_identifier.organization}/{sub_identifier.project}",
                    metatable_create=metatable_create,
                )
            consumer = Consumer(
                client=self,
                table_identifier=table_identifier,
                version=version,
                batch_size=batch_size,
                checkpointer=checkpointer,
                subscription_name=sub_identifier.subscription,
            )
            await consumer._init()
            self._consumers[sub_identifier] = consumer

        return self._consumers[sub_identifier]
