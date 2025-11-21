import datetime
import pandas as pd
from peewee import (
    Model,
    PrimaryKeyField,
    CharField,
    TextField,
    IntegerField,
    DatabaseProxy,
    OperationalError,
)


class PromptDBEntry(Model):
    """
    Prompt table entry.

    Fields:
        id: Primary key
        project: Project name (string)
        prompt_id: Prompt identifier (string)
        prompt_desc: Prompt description/content (text)
        created_ts: Timestamp when the prompt was created
    """

    id = PrimaryKeyField(index=True, unique=True)
    project = CharField(max_length=255, index=True, null=False)
    prompt_id = CharField(max_length=255, index=True, null=False)
    prompt_desc = TextField(null=True)
    created_ts = IntegerField(null=False)

    class Meta:
        table_name = "prompt"
        database = DatabaseProxy()


class PromptDBPostgres:
    """
    Postgres-backed implementation of the prompt store.

    Pattern mirrors `WorkQueueTaskDBPostgres` and other DB classes:
    - Uses a Peewee `Model` with a `DatabaseProxy`
    - Actual Postgres database is bound elsewhere (e.g. via ObjectFactory)
    """

    def __init__(self):
        # Try to create the table if it does not exist.
        try:
            PromptDBEntry.create_table()
        except OperationalError:
            # Table likely already exists or database is not yet bound.
            print("INFO: Failed to create prompt table (it may already exist).")

    def query_to_df(self, query):
        """Convert a Peewee query to a pandas DataFrame."""
        rows = list(query.dicts())
        if not rows:
            return pd.DataFrame()
        return pd.DataFrame(rows)

    def get_all_df(self):
        """Return all prompts as a DataFrame."""
        query = PromptDBEntry.select(
            PromptDBEntry.id,
            PromptDBEntry.project,
            PromptDBEntry.prompt_id,
            PromptDBEntry.prompt_desc,
            PromptDBEntry.created_ts
        )
        df = self.query_to_df(query)
        return df

    def add_prompt(self, project, prompt_id, prompt_desc=None):
        """
        Add a prompt to the prompt table.

        Args:
            project: Project name
            prompt_id: Prompt identifier
            prompt_desc: Optional prompt description/content

        Returns:
            id (int) on success, or None on failure.
        """
        created_ts = int(datetime.datetime.now().timestamp())

        entry = PromptDBEntry(
            project=project,
            prompt_id=prompt_id,
            prompt_desc=prompt_desc,
            created_ts=created_ts,
        )

        try:
            entry.save()
            return entry.id
        except Exception as e:
            print(f"ERROR: Failed to add prompt to prompt table: {e}")
            import traceback
            traceback.print_exc()
            return None

    def get_prompt_by_id(self, prompt_id):
        """
        Get a prompt by its prompt_id.

        Args:
            prompt_id: Prompt identifier.

        Returns:
            Dictionary with prompt data if found, None otherwise.
        """
        try:
            prompt = PromptDBEntry.get(PromptDBEntry.prompt_id == prompt_id)
            
            r = {
                "id": prompt.id,
                "project": prompt.project,
                "prompt_id": prompt.prompt_id,
                "prompt_desc": prompt.prompt_desc,
                "created_ts": prompt.created_ts,
            }
            return r

        except PromptDBEntry.DoesNotExist:
            return None
        except Exception as e:
            print(f"ERROR: Failed to get prompt by prompt_id: {e}")
            import traceback
            traceback.print_exc()
            return None

    def get_prompts_by_project(self, project):
        """
        Get all prompts for a specific project.

        Args:
            project: Project name.

        Returns:
            DataFrame with all prompts for the project.
        """
        query = PromptDBEntry.select().where(PromptDBEntry.project == project)
        return self.query_to_df(query)

    def update_prompt(self, prompt_id, project=None, prompt_desc=None):
        """
        Update a prompt by its prompt_id.

        Args:
            prompt_id: Prompt identifier.
            project: Optional new project name.
            prompt_desc: Optional new prompt description/content.

        Returns:
            True on success, False on failure.
        """
        try:
            prompt = PromptDBEntry.get(PromptDBEntry.prompt_id == prompt_id)
            
            if project is not None:
                prompt.project = project
            if prompt_desc is not None:
                prompt.prompt_desc = prompt_desc
            
            prompt.save()
            return True

        except PromptDBEntry.DoesNotExist:
            return False
        except Exception as e:
            print(f"ERROR: Failed to update prompt by prompt_id: {e}")
            import traceback
            traceback.print_exc()
            return False

    def delete_prompt(self, prompt_id):
        """
        Delete a prompt by its prompt_id.

        Args:
            prompt_id: Prompt identifier.

        Returns:
            True on success, False on failure.
        """
        try:
            prompt = PromptDBEntry.get(PromptDBEntry.prompt_id == prompt_id)
            prompt.delete_instance()
            return True

        except PromptDBEntry.DoesNotExist:
            return False
        except Exception as e:
            print(f"ERROR: Failed to delete prompt by prompt_id: {e}")
            import traceback
            traceback.print_exc()
            return False

