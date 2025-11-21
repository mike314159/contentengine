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


class SubscriptionDBEntry(peewee.Model):

    id = peewee.PrimaryKeyField(primary_key=True)

    user_guid = peewee.CharField(null=False)

    event_name = peewee.CharField(null=True)
    purchase_type = peewee.CharField(null=True)

    order_id = peewee.IntegerField(null=True)
    store_id = peewee.IntegerField(null=True)
    customer_email = peewee.CharField(null=True)
    customer_id = peewee.IntegerField(null=True)
    customer_portal_url = peewee.CharField(null=True)
    update_payment_method_url = peewee.CharField(null=True)
    customer_portal_update_subscription_url = peewee.CharField(null=True)

    status = peewee.CharField(null=True)

    product_name = peewee.CharField(null=True)
    variant_name = peewee.CharField(null=True)
    product_id = peewee.IntegerField(null=True)
    variant_id = peewee.IntegerField(null=True)

    price_id = peewee.IntegerField(null=True)
    quantity = peewee.IntegerField(null=True)
    subscription_id = peewee.IntegerField(null=True)
    pause = peewee.IntegerField(null=True)
    renews_at = peewee.DateTimeField(null=True)
    cancelled = peewee.IntegerField(null=True)

    added_ts = peewee.IntegerField(null=True)

    class Meta:

        table_name = "subscriptions"
        database = peewee.DatabaseProxy()


class SubscriptionsDBLemonSqueezy:

    # If no worker uuid is specified, one is generated
    # In cases where we have multiple users of the queue, we may want some to ignore doing maintenance
    # because it will be taken care of my the other.
    def __init__(self):

        try:
            SubscriptionDBEntry.create_table()
        except peewee.OperationalError:
            print("ERROR: Failed to create SubscriptionDBEntry table")

    # This is unix timestampe
    def _get_now_ts(self):
        return int(time.time())

    def query_to_df(self, query):
        return pd.DataFrame(list(query.dicts()))

    def get_all_df(self):
        query = SubscriptionDBEntry.select()
        return self.query_to_df(query)

    def add_event(self, user_guid, event_obj):
        added_ts = self._get_now_ts()

        # cancelled = info_dct.get("cancelled", None)
        # try:
        #     cancelled = int(cancelled)
        # except Exception as e:
        #     cancelled = None

        # Extract all fields from info_dct
        subscription_data = {
            "event_name": event_obj.event_name,
            "purchase_type": event_obj.purchase_type,
            "status": event_obj.status,
            "order_id": event_obj.order_id,
            "store_id": event_obj.store_id,
            "customer_email": event_obj.customer_email,
            "customer_id": event_obj.customer_id,
            "customer_portal_url": event_obj.customer_portal_url,
            "product_name": event_obj.product_name,
            "variant_name": event_obj.variant_name,
            "product_id": event_obj.product_id,
            "variant_id": event_obj.variant_id,
            "price_id": event_obj.price_id,
            "added_ts": added_ts,
        }

        try:
            # # Try to update existing subscription
            # rows_updated = (SubscriptionDBEntry
            #                .update(**subscription_data)
            #                .where(SubscriptionDBEntry.user_guid == user_guid)
            #                .execute())

            # if rows_updated == 0:
            # If no rows were updated, create new subscription
            subscription_data["user_guid"] = user_guid
            SubscriptionDBEntry.create(**subscription_data)
            return True, ""

        except Exception as e:
            print("Exception: ", e)
            return False, f"Error adding/updating subscription: {str(e)}"

    def get_lemon_squeezy_events_for_user_df(self, user_guid):
        query = (
            SubscriptionDBEntry.select()
            .where(SubscriptionDBEntry.user_guid == user_guid)
            .order_by(SubscriptionDBEntry.added_ts.desc())
        )
        return self.query_to_df(query)

    def get_subscription_plan_info(self, user_guid):
        query = (
            SubscriptionDBEntry.select()
            .where(SubscriptionDBEntry.user_guid == user_guid)
            .order_by(SubscriptionDBEntry.added_ts.desc())
            .limit(1)
        )
        df = self.query_to_df(query)
        if len(df) == 0:
            return {}
        return df.iloc[0].to_dict()

    def get_customer_portal_url(self, user_guid):
        query = (
            SubscriptionDBEntry.select()
            .where(SubscriptionDBEntry.user_guid == user_guid)
            .order_by(SubscriptionDBEntry.added_ts.desc())
            .limit(1)
        )
        df = self.query_to_df(query)
        if len(df) == 0:
            return None
        return df.iloc[0].to_dict().get("customer_portal_url", None)
