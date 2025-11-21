import datetime
import uuid
import pandas as pd
import json
from peewee import (
    Model,
    PrimaryKeyField,
    CharField,
    TextField,
    BlobField,
    IntegerField,
    DatabaseProxy,
    OperationalError,
)


class WorkQueueTaskDBEntry(Model):
    """
    Work queue task table entry.

    Fields:
        id: Primary key
        task_uuid: Task UUID (string)
        task_type: Task type (e.g. 'text', 'json', 'image')
        text: Text payload (raw text or JSON string)
        image: Binary payload for images
        created_ts: Timestamp when the task was created
    """

    id = PrimaryKeyField(index=True, unique=True)
    task_uuid = CharField(max_length=255, index=True, null=False)
    task_type = CharField(max_length=255, index=True, null=False)
    text = TextField(null=True)
    image = BlobField(null=True)
    created_ts = IntegerField(null=False)

    class Meta:
        table_name = "work_queue_task"
        database = DatabaseProxy()


class WorkQueueTaskDBPostgres:
    """
    Postgres-backed implementation of the work queue task store.

    Pattern mirrors `SnippetDBPostgres` and `WorkQueueDBPostgres`:
    - Uses a Peewee `Model` with a `DatabaseProxy`
    - Actual Postgres database is bound elsewhere (e.g. via ObjectFactory)
    """

    def __init__(self):
        # Try to create the table if it does not exist.
        try:
            WorkQueueTaskDBEntry.create_table()
        except OperationalError:
            # Table likely already exists or database is not yet bound.
            print("INFO: Failed to create work_queue_task table (it may already exist).")

    def query_to_df(self, query):
        """Convert a Peewee query to a pandas DataFrame."""
        rows = list(query.dicts())
        if not rows:
            return pd.DataFrame()
        return pd.DataFrame(rows)

    def get_all_df(self):
        """Return all work queue tasks as a DataFrame (excluding image column)."""
        # Select all columns except image to avoid loading large binary data
        query = WorkQueueTaskDBEntry.select(
            WorkQueueTaskDBEntry.id,
            WorkQueueTaskDBEntry.task_uuid,
            WorkQueueTaskDBEntry.task_type,
            WorkQueueTaskDBEntry.text,
            WorkQueueTaskDBEntry.created_ts
        )
        df = self.query_to_df(query)
        #print(f"DEBUG: DataFrame: \n{df}")
        return df

    def add_task(self, task_type, text=None, image=None):
        """
        Add a task to the work queue task table.

        Args:
            task_type: Type of task ('text', 'json', 'image', etc.)
            text: Optional text payload (raw text or JSON string)
            image: Optional binary payload for images

        Returns:
            task_uuid (str) on success, or None on failure.
        """
        task_uuid = uuid.uuid4().hex
        created_ts = int(datetime.datetime.now().timestamp())

        entry = WorkQueueTaskDBEntry(
            task_uuid=task_uuid,
            task_type=task_type,
            text=text,
            image=image,
            created_ts=created_ts,
        )

        try:
            entry.save()
            return task_uuid
        except Exception as e:
            print(f"ERROR: Failed to add task to work_queue_task: {e}")
            import traceback

            traceback.print_exc()
            return None


    def get_task_by_uuid(self, task_uuid):
        """
        Get a task by its UUID.

        Args:
            task_uuid: Task UUID.

        Returns:
            WorkQueueDBEntry object if found, None otherwise.
        """
        try:
            task = WorkQueueTaskDBEntry.get(WorkQueueTaskDBEntry.task_uuid == task_uuid)
            #print(f"Task: {json.dumps(task, indent=4)}")
            task_type = task.task_type

            r = {
                "uuid": task.task_uuid,
                "task_type": task.task_type,
                "text": task.text,
                "created_ts": task.created_ts,
                "image": task.image  # Include image data
            }

            if task_type == "json":
                r["json"] = json.loads(task.text)
            else:
                r["json"] = { 'text': task.text }
            return r

        except WorkQueueTaskDBEntry.DoesNotExist:
            return None
        except Exception as e:
            print(f"ERROR: Failed to get task by UUID: {e}")
            import traceback
            traceback.print_exc()
            return None

