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



class SnippetDBEntry(Model):

    id = PrimaryKeyField(index=True, unique=True)
    uuid = CharField(max_length=36, index=True, unique=True, null=False)
    project = CharField(max_length=255, index=True, null=False)
    category = CharField(max_length=255, index=True, null=False)
    text = TextField(null=False)
    approval_state = IntegerField(null=False, default=0)
    added_ts = IntegerField(null=False)
    deleted = IntegerField(null=False, default=0)
    published = CharField(max_length=255, null=True)
    published_ts = IntegerField(null=True)

    class Meta:
        table_name = "snippet"
        database = DatabaseProxy()


class SnippetDBPostgres():

    def __init__(self):

        try:
            SnippetDBEntry.create_table()
        except OperationalError:
            print("ERROR: Failed to create snippet table")



        """ This state transition table shows the label and choices for each state.
        The choices list contains tuples where the first element is the button label, 
        and the second element is the new state value.
        """
        self.approved_states = {
            "pending": {
                "id": 0,
                "choices": [
                    ("approve", "approved"),
                    ("reject", "rejected")
                ]
            },
            "approved": {
                "id": 1,
                "choices": [
                    ("reject", "rejected")
                ]
            },
            "rejected": {
                "id": 2,
                "choices": [
                    ("approve", "approved")
                ]
            },
        }

        self.map_approved_state_label_to_id = {}
        for (label, details) in self.approved_states.items():
            self.map_approved_state_label_to_id[label] = details["id"]


    def get_approved_state_choices(self, approved_state_id):
        for (label, details) in self.approved_states.items():
            if details["id"] == approved_state_id:
                return details["choices"]
        return None

    def add(
            self,
            project,
            category,
            text,
            approval_state=0,
            deleted=0,
            published=None,
            published_ts=None):

        added_ts = int(datetime.datetime.now().timestamp())
        snippet_uuid = str(uuid.uuid4())
        item = SnippetDBEntry(
            uuid=snippet_uuid,
            project=project,
            category=category,
            text=text,
            approval_state=approval_state,
            added_ts=added_ts,
            deleted=deleted,
            published=published,
            published_ts=published_ts
        )
        try:
            item.save()
            return True
        except Exception as e:
            print(f"ERROR: Failed to save snippet: {e}")
            import traceback
            traceback.print_exc()
            return False

    def query_to_df(self, query):
        lst = list(query.dicts())
        if len(lst) == 0:
            return pd.DataFrame()
        return pd.DataFrame(lst)

    def get_all_df(self):
        query = SnippetDBEntry.select()
        return self.query_to_df(query)

    def get_filtered_df(self, project=None, category=None, approval_state=None, published=None):
        """
        Get snippets filtered by the provided criteria.
        
        Args:
            project: Filter by exact project name
            category: Filter by exact category name
            approval_state: Filter by exact approval_state (int)
            published: Filter by published status (0 = unpublished, 1 = published)
                - 0: published_ts <= 0 or None
                - 1: published_ts > 0
        
        Returns:
            pandas.DataFrame with filtered snippets
        """
        query = SnippetDBEntry.select()
        
        if project is not None:
            query = query.where(SnippetDBEntry.project == project)
        
        if category is not None:
            query = query.where(SnippetDBEntry.category == category)
        
        if approval_state is not None:
            query = query.where(SnippetDBEntry.approval_state == approval_state)
        
        if published is not None:
            if published == 0:
                # published_ts <= 0 or None
                query = query.where(
                    (SnippetDBEntry.published_ts.is_null()) | 
                    (SnippetDBEntry.published_ts <= 0)
                )
            elif published == 1:
                # published_ts > 0
                query = query.where(
                    (~SnippetDBEntry.published_ts.is_null()) & 
                    (SnippetDBEntry.published_ts > 0)
                )
        
        return self.query_to_df(query)

    def update_approval_state(self, snippet_id, approval_state):
        """Update the approval_state of a snippet by ID."""
        try:
            snippet = SnippetDBEntry.get_by_id(snippet_id)
            snippet.approval_state = approval_state
            snippet.save()
            return True
        except Exception as e:
            print(f"ERROR: Failed to update snippet approval_state: {e}")
            import traceback
            traceback.print_exc()
            return False

    def publish_snippet(self, uuid_prefix, published_value):
        """
        Publish a snippet by UUID prefix (first 7 characters).
        
        Args:
            uuid_prefix: First 7 characters of the UUID
            published_value: Value to set for the published field
        
        Returns:
            Tuple of (success: bool, error_code: str, error_message: str)
            - success: True if successful, False otherwise
            - error_code: Error code if failed (e.g., "NOT_FOUND", "NOT_APPROVED", "ALREADY_PUBLISHED")
            - error_message: Human-readable error message
        """
        try:
            # Find snippet by UUID prefix (first 7 characters)
            # Use LIKE to match the first 7 characters
            query = SnippetDBEntry.select().where(
                SnippetDBEntry.uuid.like(f"{uuid_prefix}%")
            )
            
            snippets = list(query)
            
            if len(snippets) == 0:
                error_msg = f"No snippet found with UUID prefix: {uuid_prefix}"
                print(f"ERROR: {error_msg}")
                return (False, "NOT_FOUND", error_msg)
            
            if len(snippets) > 1:
                error_msg = f"Multiple snippets found with UUID prefix: {uuid_prefix}"
                print(f"ERROR: {error_msg}")
                return (False, "MULTIPLE_MATCHES", error_msg)
            
            snippet = snippets[0]
            
            # Check if snippet is approved (approval_state == 1)
            approved_state_id = self.map_approved_state_label_to_id.get("approved")
            if snippet.approval_state != approved_state_id:
                error_msg = f"Snippet is not approved (current state: {snippet.approval_state})"
                print(f"ERROR: {error_msg}")
                return (False, "NOT_APPROVED", error_msg)
            
            # Check if snippet is already published (published_ts > 0)
            if snippet.published_ts is not None and snippet.published_ts > 0:
                error_msg = f"Snippet is already published (published_ts: {snippet.published_ts})"
                print(f"ERROR: {error_msg}")
                return (False, "ALREADY_PUBLISHED", error_msg)
            
            # Publish the snippet
            snippet.published = published_value
            snippet.published_ts = int(datetime.datetime.now().timestamp())
            snippet.save()
            return (True, None, None)
        except Exception as e:
            error_msg = f"Failed to publish snippet: {e}"
            print(f"ERROR: {error_msg}")
            import traceback
            traceback.print_exc()
            return (False, "INTERNAL_ERROR", error_msg)
