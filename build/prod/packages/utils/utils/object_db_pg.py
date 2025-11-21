import json
import os
import pandas as pd
from peewee import (
    Model,
    CharField,
    IntegerField,
    BlobField,
    DatabaseProxy,
    OperationalError,
    fn,
)
from peewee import SQL
import datetime
import pickle
from pydantic import BaseModel, ValidationError
from typing import Optional


class ObjectDBEntry(Model):

    key = CharField(index=True, unique=True)
    format = IntegerField(index=False, unique=False)
    object = BlobField(index=False, unique=False)
    added_ts = IntegerField(index=False, unique=False)

    class Meta:
        table_name = "objects"
        database = DatabaseProxy()


class ObjectDBPostgres:

    FORMAT_DATAFRAME = 1
    FORMAT_JSON = 2

    def __init__(self):

        try:
            ObjectDBEntry.create_table()
        except OperationalError:
            print("ERROR: Failed to create documents table")

    def _get_obj_type(self, obj):
        if type(obj) == pd.DataFrame:
            return ObjectDBPostgres.FORMAT_DATAFRAME
        elif type(obj) == dict:
            return ObjectDBPostgres.FORMAT_JSON
        else:
            assert False, "Invalid object type"

    def _get_current_time_ts(self):
        return int(datetime.datetime.now().timestamp())

    def save(self, key, obj, format=None):

        key = key.lower()
        print("ObjectDBPostgres.save(%s)" % key)

        """Save an object to the database with specified format.
        If an object with the same key exists, it will be overwritten.
        
        Args:
            key: Unique identifier for the object
            obj: The object to save (DataFrame or dict)
            format: ObjectDBEntry.FORMAT_DATAFRAME or ObjectDBEntry.FORMAT_JSON
        """

        if format is None:
            format = self._get_obj_type(obj)

        if format == ObjectDBPostgres.FORMAT_DATAFRAME:
            object_bytes = pickle.dumps(obj)
        elif format == ObjectDBPostgres.FORMAT_JSON:
            object_bytes = pickle.dumps(obj)
        else:
            assert False, "Invalid format specified"


        
        try:
            # Try to update existing entry with database current timestamp
            entry = ObjectDBEntry.get(ObjectDBEntry.key == key)
            # Update the entry's values - let Peewee generate SQL with DB timestamp
            ObjectDBEntry.update(
                format=format,
                object=object_bytes,
                added_ts=SQL("EXTRACT(EPOCH FROM NOW())"),
            ).where(ObjectDBEntry.key == key).execute()
            # print("Updated %s in DB" % key)
            return True
        except ObjectDBEntry.DoesNotExist:
            # Create new entry if it doesn't exist - use DB timestamp
            ObjectDBEntry.insert(
                key=key,
                format=format,
                object=object_bytes,
                added_ts=SQL("EXTRACT(EPOCH FROM NOW())"),
            ).execute()
            # print("Saved %s in DB" % key)
            return True

    def get_all_keys_df(self):
        query_results = [
            (entry.key, entry.added_ts)
            for entry in ObjectDBEntry.select(
                ObjectDBEntry.key, ObjectDBEntry.added_ts
            ).order_by(ObjectDBEntry.added_ts.desc())
        ]
        return pd.DataFrame(query_results, columns=["key", "added_ts"])
    
    def get_all_keys_starts_with_df(self, starts_with):
        query_results = [
            (entry.key, entry.added_ts)
            for entry in ObjectDBEntry.select(
                ObjectDBEntry.key, ObjectDBEntry.added_ts
            ).where(ObjectDBEntry.key.startswith(starts_with))
            .order_by(ObjectDBEntry.added_ts.desc())
        ]
        return pd.DataFrame(query_results, columns=["key", "added_ts"])

    # # Find the latest record that matches the partial key.
    # # This is used when all we know is the partial key and not the actual key.
    def lookup_partial_key(self, partial_key):
        """Find the latest record that matches the partial key.

        Args:
            partial_key: A string to match against the beginning of keys

        Returns:
            The key of the latest matching entry, or None if no match found
        """
        partial_key = partial_key.lower()
        try:
            # Find all matching entries, ordered by timestamp descending
            matching_entry = (
                ObjectDBEntry.select()
                .where(ObjectDBEntry.key.startswith(partial_key))
                .order_by(ObjectDBEntry.added_ts.desc())
                .get()
            )

            return matching_entry.key

        except ObjectDBEntry.DoesNotExist:
            return None

    # def search_keys(self, partial_key, limit):
    #     # print("ObjectDBPostgres.search_keys(%s, %s)" % (partial_key, limit))
    #     partial_key = partial_key.lower()
    #     try:
    #         matching_entries = (
    #             ObjectDBEntry.select()
    #             .where(ObjectDBEntry.key.startswith(partial_key))
    #             .order_by(ObjectDBEntry.added_ts.desc())
    #             .limit(limit)
    #         )
    #         return [entry.key for entry in matching_entries]
    #     except ObjectDBEntry.DoesNotExist:
    #         return []

    def get_key_ts(self, key):
        key = key.lower()
        try:
            entry = ObjectDBEntry.get(ObjectDBEntry.key == key)
            return entry.added_ts
        except ObjectDBEntry.DoesNotExist:
            return None

    def get(self, key):
        key = key.lower()
        try:
            entry = ObjectDBEntry.get(ObjectDBEntry.key == key)
            return self._deserialize_object(entry.format, entry.object)
        except ObjectDBEntry.DoesNotExist:
            return None

    def get_with_ts(self, key):
        key = key.lower()
        try:
            entry = ObjectDBEntry.get(ObjectDBEntry.key == key)
            return entry.added_ts, self._deserialize_object(entry.format, entry.object)
        except ObjectDBEntry.DoesNotExist:
            return None, None

    def _deserialize_object(self, format, object_bytes):
        if format == ObjectDBPostgres.FORMAT_DATAFRAME:
            try:
                return pickle.loads(object_bytes)
            except:
                print("Error deserializing dataframe object: ", object_bytes)
                return None
        elif format == ObjectDBPostgres.FORMAT_JSON:
            try:
                # Use pickle.loads for both formats now
                return pickle.loads(object_bytes)
            except:
                print("Error deserializing json object: ", object_bytes)
                return None
        return None

if __name__ == "__main__":

    pass
