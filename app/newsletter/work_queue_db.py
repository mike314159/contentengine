import datetime
import pandas as pd
from peewee import (
    Model,
    PrimaryKeyField,
    CharField,
    IntegerField,
    DatabaseProxy,
    OperationalError,
    fn,
)


class WorkQueueDBEntry(Model):
    """
    Work queue table entry.

    Fields:
        id: Primary key
        project: Project name
        queue: Queue name
        task_uuid: Task UUID
        added_to_queue_ts: Timestamp when task was added to the queue
    """

    id = PrimaryKeyField(index=True, unique=True)
    project = CharField(max_length=255, index=True, null=False)
    queue = CharField(max_length=255, index=True, null=False)
    task_uuid = CharField(max_length=255, index=True, null=False)
    added_to_queue_ts = IntegerField(null=False)

    class Meta:
        table_name = "work_queue"
        database = DatabaseProxy()


class WorkQueueDBPostgres:
    """
    Postgres-backed implementation of the work queue.

    This follows the same pattern as `SnippetDBPostgres` in `snippet_db_pg.py`:
    - Uses a Peewee `Model` with a `DatabaseProxy`
    - The actual Postgres database is bound elsewhere (e.g. via ObjectFactory)
    """

    def __init__(self):
        # Try to create the table if it does not exist.
        try:
            WorkQueueDBEntry.create_table()
        except OperationalError:
            # Table likely already exists or database is not yet bound.
            print("INFO: Failed to create work_queue table (it may already exist).")

    def query_to_df(self, query):
        """Convert a Peewee query to a pandas DataFrame."""
        rows = list(query.dicts())
        if not rows:
            return pd.DataFrame()
        return pd.DataFrame(rows)

    def get_all_df(self):
        """Return all work queue entries as a DataFrame."""
        query = WorkQueueDBEntry.select()
        return self.query_to_df(query)

    def get_queue_summary_df(self):
        """
        Return an aggregated DataFrame with the number of items in each queue.

        Columns: project, queue, count
        """
        query = (
            WorkQueueDBEntry.select(
                WorkQueueDBEntry.project,
                WorkQueueDBEntry.queue,
                fn.COUNT(WorkQueueDBEntry.id).alias("count"),
            )
            .group_by(WorkQueueDBEntry.project, WorkQueueDBEntry.queue)
            .order_by(WorkQueueDBEntry.project, WorkQueueDBEntry.queue)
        )
        return self.query_to_df(query)

    def add_task(self, project, queue, task_uuid):
        """
        Add a task to the work queue.

        Args:
            project: Project name
            queue: Queue name
            task_uuid: Task UUID

        Returns:
            True on success, False on failure.
        """
        added_ts = int(datetime.datetime.now().timestamp())
        entry = WorkQueueDBEntry(
            project=project,
            queue=queue,
            task_uuid=task_uuid,
            added_to_queue_ts=added_ts,
        )
        try:
            entry.save()
            return True
        except Exception as e:
            print(f"ERROR: Failed to add task to work_queue: {e}")
            import traceback

            traceback.print_exc()
            return False

    def move_task_queue(self, id, dest_queue):
        """
        Move a task to a different queue.

        Args:
            id: Primary key of the work queue entry.
            dest_queue: Destination queue name.

        Returns:
            True on success, False on failure.
        """
        try:
            entry = WorkQueueDBEntry.get_by_id(id)
            entry.queue = dest_queue
            entry.save()
            return True
        except WorkQueueDBEntry.DoesNotExist:
            print(f"ERROR: WorkQueueDBEntry with id {id} does not exist.")
            return False
        except Exception as e:
            print(f"ERROR: Failed to move task in work_queue: {e}")
            import traceback

            traceback.print_exc()
            return False



