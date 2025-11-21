import json
import os
import pandas as pd
import peewee
import datetime

# from loggerfactory import LoggerFactory
import uuid
import pickle
import sys
import hashlib
import glob
import re
import time
import pytz
import hashlib
import bcrypt
import hmac
from pydantic import BaseModel, ValidationError
from typing import Optional


class EmailEventDBEntry(peewee.Model):

    id = peewee.PrimaryKeyField(primary_key=True)

    event_type = peewee.CharField(null=True)
    email_address = peewee.CharField(null=True)
    user_guid = peewee.CharField(null=True)
    
    email_type = peewee.CharField(null=True)
    email_provider_id = peewee.CharField(null=True)
    email_delivery_status = peewee.CharField(null=True)
    email_subject = peewee.CharField(null=True)
    email_content = peewee.TextField(null=True)

    # purchase_type = peewee.CharField(null=True)

    # order_id = peewee.IntegerField(null=True)
    # store_id = peewee.IntegerField(null=True)
    # customer_email = peewee.CharField(null=True)
    # customer_id = peewee.IntegerField(null=True)
    # customer_portal_url = peewee.CharField(null=True)
    # update_payment_method_url = peewee.CharField(null=True)
    # customer_portal_update_subscription_url = peewee.CharField(null=True)

    # status = peewee.CharField(null=True)

    # product_name = peewee.CharField(null=True)
    # variant_name = peewee.CharField(null=True)
    # product_id = peewee.IntegerField(null=True)
    # variant_id = peewee.IntegerField(null=True)

    # price_id = peewee.IntegerField(null=True)
    # quantity = peewee.IntegerField(null=True)
    # subscription_id = peewee.IntegerField(null=True)
    # pause = peewee.IntegerField(null=True)
    # renews_at = peewee.DateTimeField(null=True)
    # cancelled = peewee.IntegerField(null=True)

    added_ts = peewee.IntegerField(null=True)

    class Meta:

        table_name = "email_events"
        database = peewee.DatabaseProxy()


class EmailEventsDB:

    EVENT_TYPE_SEND_EMAIL = 'send'
    EVENT_TYPE_UNSUBSCRIBE = 'unsubscribe'

    EMAIL_PROVIDER_STATUS_DELIVERED = 'delivered'
    EMAIL_PROVIDER_STATUS_BOUNCED = 'bounced'

    # If no worker uuid is specified, one is generated
    # In cases where we have multiple users of the queue, we may want some to ignore doing maintenance
    # because it will be taken care of my the other.
    def __init__(self):

        try:
            EmailEventDBEntry.create_table()
        except peewee.OperationalError:
            print("ERROR: Failed to create EmailEventDBEntry table")

    # This is unix timestampe
    def _get_now_ts(self):
        return int(time.time())

    def query_to_df(self, query):
        return pd.DataFrame(list(query.dicts()))

    def get_all_df(self):
        query = EmailEventDBEntry.select()
        return self.query_to_df(query)

    def add_event(self, email_address, user_guid, event_type, email_type, email_provider_id, email_subject, email_content):
        added_ts = self._get_now_ts()

        # cancelled = info_dct.get("cancelled", None)
        # try:
        #     cancelled = int(cancelled)
        # except Exception as e:
        #     cancelled = None

        # Extract all fields from info_dct
        email_event_data = {
            "event_type": event_type,
            "email_address": email_address,
            "user_guid": user_guid,
            "email_type": email_type,
            "email_provider_id": email_provider_id,
            "email_subject": email_subject,
            "email_content": email_content,
            "added_ts": added_ts,
        }

        try:
            EmailEventDBEntry.create(**email_event_data)
            return True, ""

        except Exception as e:
            print("Exception: ", e)
            return False, f"Error adding/updating email event: {str(e)}"

    def update_delivery_status(self, email_provider_id, email_delivery_status):
        query = (
            EmailEventDBEntry.update(email_delivery_status=email_delivery_status)
            .where(EmailEventDBEntry.email_provider_id == email_provider_id)
        )
        query.execute()

    def get_null_delivery_status_events(self):
        query = (
            EmailEventDBEntry.select()
            .where(EmailEventDBEntry.email_delivery_status == None)
        )
        return self.query_to_df(query)

    def get_events_for_user_df(self, user_guid):
        query = (
            EmailEventDBEntry.select()
            .where(EmailEventDBEntry.user_guid == user_guid)
            .order_by(EmailEventDBEntry.added_ts.desc())
        )
        return self.query_to_df(query)

    def get_events_for_user_email_df(self, email_address):
        query = (
            EmailEventDBEntry.select()
            .where(EmailEventDBEntry.email_address == email_address)
            .order_by(EmailEventDBEntry.added_ts.desc())
        )
        return self.query_to_df(query)
    
    def email_already_sent(self, email_address, email_type):
        query = (
            EmailEventDBEntry.select()
            .where(EmailEventDBEntry.email_address == email_address)
            .where(EmailEventDBEntry.email_type == email_type)
        )
        return len(self.query_to_df(query)) > 0
    
    def prior_email_has_bounced(self, email_address):
        query = (
            EmailEventDBEntry.select()
                .where(EmailEventDBEntry.email_address == email_address)
                .where(EmailEventDBEntry.email_delivery_status == EmailEventsDB.EMAIL_PROVIDER_STATUS_BOUNCED)
        )
        return len(self.query_to_df(query)) > 0

    def get_send_stats(self, email_address=None):
        base_query = (
            EmailEventDBEntry.select(
                EmailEventDBEntry.email_address,
                EmailEventDBEntry.email_type,
                EmailEventDBEntry.user_guid,
                peewee.fn.MIN(EmailEventDBEntry.added_ts).alias('first_sent_ts'),
                peewee.fn.MAX(EmailEventDBEntry.added_ts).alias('last_sent_ts'),
                peewee.fn.COUNT(EmailEventDBEntry.id).alias('total_sent')
            )
            .where(EmailEventDBEntry.event_type == EmailEventsDB.EVENT_TYPE_SEND_EMAIL)
            .group_by(EmailEventDBEntry.email_type, EmailEventDBEntry.email_address, EmailEventDBEntry.user_guid)
        )
        
        if email_address is not None:
            email_address = email_address.lower()
            base_query = base_query.where(EmailEventDBEntry.email_address == email_address)

        df = self.query_to_df(base_query)
        if len(df) == 0:
            return pd.DataFrame()
        return df


