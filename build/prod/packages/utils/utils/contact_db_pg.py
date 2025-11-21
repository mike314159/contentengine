import json
import os
import pandas as pd
from peewee import *
#import peewee
import datetime
import uuid
import pickle
import sys
import hashlib
import glob
import re

#from globals import *


from pydantic import BaseModel, ValidationError
from typing import Optional



class ContactDBEntry(Model):

    id = PrimaryKeyField(index=True, unique=True)
    name = CharField(index=True, unique=False, null=True)
    email = CharField(index=True, unique=False, null=False)
    message = TextField(index=False, unique=False, null=False)
    added_ts = IntegerField(index=False, unique=False, null=False)

    class Meta:
        table_name = "contact"
        database = DatabaseProxy() 


class ContactDBPostgres():


    def __init__(self):

        try:
            ContactDBEntry.create_table()
        except OperationalError:
            print("ERROR: Failed to create contact table")


    def add(
            self,
            name,
            email,
            message):

        added_ts = int(datetime.datetime.now().timestamp())
        item = ContactDBEntry(
            name=name,
            email=email,
            message=message,
            added_ts=added_ts
        )
        try:
            item.save()
            return True
        except Exception:
            return False



    # def get(self, key):
    #     query = DocumentDBEntry.select().where(DocumentDBEntry.key == key)
    #     df = self.query_to_df(query)
    #     if len(df) == 0:
    #         return None
    #     #print("Explanation Cache Hit")
    #     #print(df)
    #     format = df.iloc[0]["format"]
    #     document_str = df.iloc[0]["document"]
    #     return self._deserialize_document(format, document_str)

    # def get_by_id(self, id):
    #     query = DocumentDBEntry.select().where(DocumentDBEntry.id == id)
    #     df = self.query_to_df(query)
    #     if len(df) == 0:
    #         return None
    #     format = df.iloc[0]["format"]
    #     document_str = df.iloc[0]["document"]
    #     return self._deserialize_document(format, document_str)


    # def get_key_list(self, since_id, prefix, limit=100):
    #     query = DocumentDBEntry.select(
    #         DocumentDBEntry.id,
    #         DocumentDBEntry.key,
    #         DocumentDBEntry.added_ts,
    #     ).where(DocumentDBEntry.id > since_id)
    #     if prefix:
    #         query = query.where(DocumentDBEntry.key.startswith(prefix))
    #     query = query.limit(limit)
    #     df = self.query_to_df(query)
    #     if len(df) == 0:
    #         return []
    #     key_list = []
    #     for idx, row in df.iterrows():
    #         key = row["key"]
    #         added_ts = row["added_ts"]
    #         key_list.append(
    #             {
    #                 "id": row["id"],
    #                 "key": key,
    #                 "ts": added_ts
    #             }
    #         )
    #     return key_list

    def query_to_df(self, query):
        lst = list(query.dicts())
        if len(lst) == 0:
            return pd.DataFrame()
        return pd.DataFrame(lst)
    
    def get_all_df(self):
        query = ContactDBEntry.select()
        return self.query_to_df(query)

