
import json
import os
import pandas as pd
import peewee
import datetime
#from loggerfactory import LoggerFactory
import uuid
import pickle
import sys
import hashlib
import glob
import re
import time
import pytz
#queue_database_proxy = peewee.DatabaseProxy()
from ua_parser import user_agent_parser
from flask import request


class EventDBEntry(peewee.Model):

    id = peewee.PrimaryKeyField(primary_key=True)

    # deployment = peewee.CharField()
    # host = peewee.CharField()
    # env = peewee.CharField()

    # user, script

    event_name = peewee.CharField(index=True)



    #actor_type = peewee.IntegerField(index=True) # user or script
    user_id = peewee.CharField(index=True)  # user id, script name
    resource = peewee.CharField(index=True)


    # EventName     ActorType     ActorID             Resource      Properties
    # pageview      user          guid or bcookie     /blog         { 'browser': 'chrome', 'referrer': 'https://google.com' }
    # signin        user          guid                None          { 'browser': 'chrome', 'referrer': 'https://google.com' }

    properties = peewee.TextField(null=True)
    added_ts = peewee.IntegerField(null=False)

    #obj_id = peewee.CharField(index=True)


    # Obj Type      Obj ID              Action          Subject
    # script        system              started         app
    # user          email               signed_up       newsletter
    # user          email               unsubscribed    newsletter
    # user          email               submitted       contact-msg
    # script        run_perf_reports    symbol_updated  VPL
    # script        run_perf_reports    symbol_fresh    IBM
    # script        run_perf_reports    report_updated  asset_classes

    #action = peewee.CharField(index=True)
    #subject = peewee.CharField(index=True)
    


    #msg = peewee.TextField()

    #added_pt_dt = peewee.CharField()
    #deleted_ts = peewee.IntegerField(null=True)

    # When the worker reserved it and the uinique id of the worker
    # reserved_ts = peewee.IntegerField()
    # worker_uuid = peewee.CharField(null=True, index=True)

    # Worker periodically "pings" the message to indicate in progress.
    # If current ts > (last_ping_ts + last_ping_timeout_secs) worker is unresponsive.
    # clear the reservation and let another worker try it.
    # last_ping_ts = peewee.IntegerField(null=True)
    # last_ping_timeout_secs = peewee.IntegerField()

    class Meta:

        table_name = "events"
        #database = peewee.SqliteDatabase('workqueue.db')
        #database = queue_database_proxy 
        database = peewee.DatabaseProxy() 

        # older stuff
        #database = queue_database_proxy 
        #database = work_queue_db_proxy
        #schema = os.getenv("POSTGRES_SALSA_SCHEMA")
        #db_table = "queue"



class EventsDB():

    # ACTOR_TYPE_USER = 1
    # ACTOR_TYPE_SYSTEM = 2

    #DEFAULT_PING_TIMEOUT = 800

    # If no worker uuid is specified, one is generated
    # In cases where we have multiple users of the queue, we may want some to ignore doing maintenance 
    # because it will be taken care of my the other. 
    def __init__(self): #, worker_uuid, ignore_maintenance=False):

        # Every user of this work queue gets a unique id
        # if worker_uuid is None:
        #     self.worker_uuid = str(uuid.uuid4())
        # else:
        #     self.worker_uuid = worker_uuid

        # self.deployment = deployment
        # self.host = host
        # self.env = env

        try:
            #print("WorkQueue: Create table")
            EventDBEntry.create_table()
        except peewee.OperationalError:
            print("ERROR: Failed to create EventDBEntry table")

        # self.message_classes = {}
        # self.last_maintenance_ts = None
        # self.ignore_maintenance = ignore_maintenance
        # self._do_maintenance()

    # This is unix timestampe
    def _get_now_ts(self):
        return int(time.time())

    # def register_msg_class(self, msg_class):
    #     name = msg_class.__name__
    #     self.message_classes[name] = msg_class


    # # Function to convert Unix timestamp to California time
    # def convert_to_california_time(unix_timestamp):
    #     california_tz = pytz.timezone('America/Los_Angeles')
    #     utc_time = datetime.datetime.utcfromtimestamp(unix_timestamp).replace(tzinfo=pytz.utc)
    #     return utc_time.astimezone(california_tz)

    # user, email, signed_up, newsletter
    # user, email, submitted, contact-us
    # app, email, submitted, contact-us


    # def log_user_app_action(self, url, email, action, event_json):
    #     self.log_event(
    #         obj_type='script',
    #         event_source='app',
    #         entity_id=email,
    #         attr_id=action,
    #         value_id=url,
    #         event_json=event_json
    #     )

    # def log_app_event(self, action):
    #     self.log_event(
    #         event_source='app',
    #         entity_id=None,
    #         attr_id=action,
    #         value_id=None,
    #         event_json=None
    #    )

    #def log_event(self, event_source, event_desc):
    def log_event(self, event_name, user_id, resource, properties):

        try:
            properties_str = json.dumps(properties, indent=4)
        except Exception as e:
            print("ERROR: Failed to convert event_dict to json: ", e)
            properties_str = None

        # if False:
        #     print("Send Msg: ", type(msg))
        added_ts = self._get_now_ts()
        # added_pt_dt = EventStore.convert_to_california_time(added_ts)
        # added_pt_dt_str = added_pt_dt.strftime("%Y-%m-%d %H:%M:%S")
        
        #if timeout is None:
        #    timeout = WorkQueue.DEFAULT_PING_TIMEOUT
        item = EventDBEntry(
            event_name=event_name,
            #actor_type=actor_type,
            user_id=user_id,
            resource=resource,
            properties=properties_str,
            added_ts=added_ts,
        )
        item.save()
        return item.id


    # def get_request_properties(self, request):
    #     properties = {}
    #     if request is not None:
    #         #properties["request_url"] = request.url
    #         properties["full_path"] = request.full_path
    #         #properties["current_url"] = request.path
    #         properties["referrer"] = request.referrer
    #         properties["ip"] = request.remote_addr
    #         properties["host"] = request.host

    #         ua = request.user_agent.string
    #         result_dict = user_agent_parser.Parse(ua)
    #         browser = result_dict.get("user_agent", {}).get("family", "Unknown")
    #         os = result_dict.get("os", {}).get("family", "Unknown")
    #         properties["browser"] = browser
    #         properties["os"] = os
    #     return properties


    def log_pageview(self, properties, user_id):
        url = request.path
        #properties = self.get_request_properties(request)
        self.log_event(
            event_name='pageview',
            #actor_type=self.ACTOR_TYPE_USER,
            user_id=user_id,
            resource=url,
            properties=properties
        )
    # def _run_query(self, query):
    #     df = pd.DataFrame()
    #     for row in query.objects():
    #         idx = row.id
    #         df.at[idx, "tube"] = row.tube
    #         df.at[idx, "worker_uuid"] = str(row.worker_uuid)
    #         df.at[idx, "msg_class"] = row.msg_class
    #         df.at[idx, "msg"] = row.msg
    #         df.at[idx, "added_ts"] = row.added_ts
    #         df.at[idx, "last_ping_timeout_secs"] = row.last_ping_timeout_secs
    #         df.at[idx, "reserved_ts"] = row.reserved_ts
    #         df.at[idx, "last_ping_ts"] = row.last_ping_ts
    #         df.at[idx, "deleted_ts"] = row.deleted_ts
    #     return df

    # def get_info(self):
    #     query = EventStoreEntry.select()
    #     return self._run_query(query)
    
    def query_to_df(self, query):
        return pd.DataFrame(list(query.dicts()))

    def get_all_df(self, sort_desc=True, limit=500, since_ts=None):
        query = EventDBEntry.select()
        if since_ts is not None:
            query = query.where(EventDBEntry.added_ts >= since_ts)
        if sort_desc:
            query = query.order_by(EventDBEntry.id.desc())
        if limit is not None:
            query = query.limit(limit)
        return self.query_to_df(query)
    
    def get_user_events_df(self, user_id, limit=500):
        query = EventDBEntry.select().where(EventDBEntry.user_id == user_id).order_by(EventDBEntry.added_ts.desc()).limit(limit)
        return self.query_to_df(query)
    
    # def get_events_df(self, obj_type=None, obj_id=None, action=None, subject=None, limit=500):

    #     query = EventStoreEntry.select().order_by(EventStoreEntry.added_ts.desc()).limit(limit)

    #     # Add conditions to the query if action or subject is specified
    #     if action:
    #         query = query.where(EventStoreEntry.action == action)
    #     if subject:
    #         query = query.where(EventStoreEntry.subject == subject)
    #     if obj_type:
    #         query = query.where(EventStoreEntry.obj_type == obj_type)
    #     if obj_id:
    #         query = query.where(EventStoreEntry.obj_id == obj_id)

    #     # if action is not None:
        #     query = (
        #         EventStoreEntry.select()
        #         .where(EventStoreEntry.action == action)
        #         .order_by(EventStoreEntry.added_ts)
        #         .limit(limit)
        #     )
        # elif subject is not None:
        #     query = (
        #         EventStoreEntry.select()
        #         .where(EventStoreEntry.subject == subject)
        #         .order_by(EventStoreEntry.added_ts)
        #         .limit(limit)
        #     )
        # else:

        # query = (
        #     EventStoreEntry.select()
        #     #.where(EventStoreEntry.event_type == event_type)
        #     .order_by(EventStoreEntry.added_ts)
        #     .limit(limit)
        # )
        # df = self.query_to_df(query)
        # if df is not None and len(df) > 0:
        #     df['tmp_added_ts'] = pd.to_datetime(df['added_ts'], unit='s', utc=True)

        #     # add a column for current utc time
        #     df['current_utc_dt'] = pd.to_datetime('now', utc=True)
        #     df['ago'] = df['current_utc_dt'] - df['tmp_added_ts']
        #     df['ago'] = df['ago'].dt.floor('s')

        #     california_tz = pytz.timezone('America/Los_Angeles')
        #     df['added_pt_dt'] = df['tmp_added_ts'].dt.tz_convert(california_tz)
        #     df.drop(columns=['tmp_added_ts', 'current_utc_dt'], inplace=True)
        #     df.sort_values(by='id', ascending=False, inplace=True)
        # return df    
#    # Mostly used for testing
#     def delete_items(self):
#         delete_query = WorkQueueEntry.delete()
#         delete_query.execute()

#     def _get_available_items(self, tubes, limit=3):
#         query = (
#             WorkQueueEntry.select()
#             .where((WorkQueueEntry.worker_uuid.is_null()) & (WorkQueueEntry.tube.in_(tubes)))
#             .order_by(WorkQueueEntry.added_ts)
#             .limit(limit)
#         )
#         return self._run_query(query)

#     def _reserve(self, item_id, worker_uuid):
#         ts = self._get_now_ts()
#         query = WorkQueueEntry.update(
#             reserved_ts=ts, last_ping_ts=ts, worker_uuid=worker_uuid
#         ).where((WorkQueueEntry.id == item_id) & (WorkQueueEntry.worker_uuid.is_null()))
#         rows = query.execute()
#         if rows > 0:
#             return True
#         else:
#             # with multiple workers, there will be expected failures to reserve.
#             return False
        
#     # Get a few items and try and reserve ONLY one.
#     def reserve(self, tubes):
#         df = self._get_available_items(tubes)
#         for item_id, row in df.iterrows():
#             class_name = row["msg_class"]
#             if class_name in self.message_classes:
#                 success = self._reserve(item_id, self.worker_uuid)
#                 if success:
#                     msg_class = self.message_classes[class_name]
#                     msg_obj = msg_class.deserialize(row["msg"])
#                     return (item_id, msg_obj)
#             else:
#                 print("ERROR: WorkQueue failed to find class %s" % class_name)
#                 print("Message Classes", self.message_classes)
#         return (None, None)
    
#     def delete(self, item_id):
#         self._do_maintenance()
#         ts = self._get_now_ts()
#         query = WorkQueueEntry.update(
#             deleted_ts=ts
#         ).where((WorkQueueEntry.id == item_id))
#         rows_deleted = query.execute()
#         if rows_deleted == 1:
#             return True
#         else:
#             print("ERROR: Failed to delete item %d" % item_id)
#             return False
        
#     # Release any job which has been reserved beyond the expected time
#     def release_expired_reservations(self):
#         ts = int(datetime.datetime.now().timestamp())
#         try:
#             query = WorkQueueEntry.update(reserved_ts=0, last_ping_ts=0, worker_uuid=None).where(
#                 (WorkQueueEntry.worker_uuid.is_null()==False)
#                 & (WorkQueueEntry.deleted_ts.is_null())
#                 & ((ts - WorkQueueEntry.last_ping_ts) > WorkQueueEntry.last_ping_timeout_secs)
#             )
#             rows = query.execute()
#             print("Released expired %d rows " % rows)
#         except peewee.OperationalError:
#             print("ERROR: Failed to release expired reservations")

    
#     # Delete any old items which have been deleted to keep the db size down
#     def permanently_delete_old_entries(self):
#         ts = self._get_now_ts()
#         #delete_from_ts = ts - (60 * 60 * 24 * 7) # 7 days
#         delete_from_ts = ts - 300 # 5 minutes
#         try:
#             query = WorkQueueEntry.delete().where(
#             (WorkQueueEntry.deleted_ts.is_null()==False) & (WorkQueueEntry.deleted_ts < delete_from_ts)
#             )
#             rows = query.execute()
#             print("Permanently deleted %d rows " % rows)
#         except peewee.OperationalError:
#             print("ERROR: Failed to permanently delete old entries")
        
#     def _do_maintenance(self):
#         if self.ignore_maintenance:
#             return
#         now_ts = self._get_now_ts()
#         if (self.last_maintenance_ts is None) or (now_ts - self.last_maintenance_ts) > 60:
#             self.release_expired_reservations()
#             self.permanently_delete_old_entries()
#             self.last_maintenance_ts = now_ts



    

if __name__ == '__main__':
    pass


