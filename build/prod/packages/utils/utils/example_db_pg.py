import json
import os
import pandas as pd
from peewee import *
import datetime

from pydantic import BaseModel, ValidationError
from typing import Optional

"""
This is an example for how to create a Postgres DB table using Peewee Model.

In this example I want to store example objects. 

So the naming is as follows. 

ExampleDBEntry: Is the Peewee Model, singular for each row in the DB
ExampleDBPostgres: The class that manages the database
The table_name is the plural version of the objects name

"""


class ExampleDBEntry(Model):

    # All rows should have a primary key
    id = PrimaryKeyField(index=True, unique=True)

    # These are the fields relevant to the object
    name = CharField(index=True, unique=False, null=True)
    email = CharField(index=True, unique=False, null=False)

    # All entries should have added and last_updated timestamps
    added_ts = IntegerField(index=False, unique=False, null=False)
    last_updated_ts = IntegerField(index=False, unique=False, null=False)

    class Meta:
        # The table name is always the prefix before DBEntry and lowercase and plural
        table_name = "examples"
        database = DatabaseProxy()


class ExampleDBPostgres:

    def __init__(self):

        try:
            ExampleDBEntry.create_table()
        except OperationalError:
            print("ERROR: Failed to create %s table" % ExampleDBEntry._meta.table_name)

    def add(self, name, email):

        added_ts = int(datetime.datetime.now().timestamp())
        item = ExampleDBEntry(
            name=name,
            email=email,
            added_ts=added_ts,
            last_updated_ts=added_ts,
            added_ts=added_ts,
        )
        try:
            item.save()
            return True
        except Exception:
            return False

    def update(self, id, name, email):
        last_updated_ts = int(datetime.datetime.now().timestamp())
        item = ExampleDBEntry.get(ExampleDBEntry.id == id)
        item.name = name
        item.email = email
        item.last_updated_ts = last_updated_ts
        item.save()
        return True

    def delete(self, id):
        item = ExampleDBEntry.get(ExampleDBEntry.id == id)
        item.delete_instance()
        return True

    def get(self, id):
        return ExampleDBEntry.select().where(ExampleDBEntry.id == id).first()

    def query_to_df(self, query):
        lst = list(query.dicts())
        if len(lst) == 0:
            return pd.DataFrame()
        return pd.DataFrame(lst)

    def get_all_df(self):
        query = ExampleDBEntry.select()
        return self.query_to_df(query)
