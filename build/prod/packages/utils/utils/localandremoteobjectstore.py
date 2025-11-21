import os
import pandas as pd
import pickle
import json
import time

"""
This class implements a key value object storage which has local storage
and remote storage. 
The local storage is a simple pickle file store. 
The remote storage is a postgres database.

If the local key is not found, it looks for the remote object. 
If the remote object is found it saves it locally. 

No expiration is done. 

"""


class LocalAndRemoteObjectStore:

    FORMAT_DATAFRAME = "df"
    FORMAT_JSON = "json"

    def __init__(self, local_cache_dir, remote_object_db):
        #print("Initializing LocalAndRemoteObjectStore with local cache dir %s" % local_cache_dir)
        self.data_dir = local_cache_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self.remote_object_db = remote_object_db

    # ----------------------
    # Private Methods
    # ----------------------

    def _get_local_fn(self, key, format):
        if format == LocalAndRemoteObjectStore.FORMAT_DATAFRAME:
            file = "%s.pkl" % (key)
        elif format == LocalAndRemoteObjectStore.FORMAT_JSON:
            file = "%s.json" % (key)
        else:
            raise ValueError("Invalid format specified")
        return os.path.join(self.data_dir, file)

    def _find_local_fn(self, key):
        df_fn = self._get_local_fn(key, LocalAndRemoteObjectStore.FORMAT_DATAFRAME)
        if os.path.exists(df_fn):
            return df_fn
        json_fn = self._get_local_fn(key, LocalAndRemoteObjectStore.FORMAT_JSON)
        if os.path.exists(json_fn):
            return json_fn
        return None

    def _save_obj_local(self, key, obj, ts):
        if obj is None:
            return False
        format = self._get_obj_type(obj)
        fn = self._get_local_fn(key, format)
        if format == LocalAndRemoteObjectStore.FORMAT_DATAFRAME:
            print("Saving %s to %s" % (key, fn))
            obj.to_pickle(fn)
        elif format == LocalAndRemoteObjectStore.FORMAT_JSON:
            print("Saving %s to %s" % (key, fn))
            with open(fn, "w") as f:
                json.dump(obj, f)

        os.utime(fn, (ts, ts))

    def _get_obj_local(self, key):
        #print("Getting object from local for %s" % key)
        fn = self._get_local_fn(key, format=LocalAndRemoteObjectStore.FORMAT_DATAFRAME)
        if os.path.exists(fn):
            #print("Found object in local for %s" % key)
            return pd.read_pickle(fn)
        fn = self._get_local_fn(key, format=LocalAndRemoteObjectStore.FORMAT_JSON)
        if os.path.exists(fn):
            with open(fn, "r") as f:
                return json.load(f)
        return None

    def _save_obj_remote(self, key, obj):
        self.remote_object_db.save(key, obj)
        return self.remote_object_db.get_key_ts(key)

    def _get_obj_remote_with_ts(self, key):
        ts, obj = self.remote_object_db.get_with_ts(key)
        return ts, obj

    def _get_obj_type(self, obj):
        if type(obj) == pd.DataFrame:
            return LocalAndRemoteObjectStore.FORMAT_DATAFRAME
        elif type(obj) == dict:
            return LocalAndRemoteObjectStore.FORMAT_JSON
        else:
            raise ValueError("Invalid object type")

    # ----------------------
    # Public Methods
    # ----------------------

    # def exists_local(self, key):
    #     fn = self._find_local_fn(key)
    #     return fn is not None

    def get_all_remote_keys_df(self, starts_with=None):
        return self.remote_object_db.get_all_keys_starts_with_df(starts_with)

    # Always use the PG to find a partial key.
    # Since on reboot the local cache is cleared.
    def lookup_partial_key(self, partial_key):
        found_key = self.remote_object_db.lookup_partial_key(partial_key)
        #print("Found key remote : %s" % found_key)
        return found_key

    # def search_keys(self, partial_key, limit):
    #     return self.remote_object_db.search_keys(partial_key, limit)

    def get_remote_keys_starts_with_df(self, starts_with):
        return self.remote_object_db.get_all_keys_starts_with_df(starts_with)

    def local_key_exists(self, key):
        fn = self._find_local_fn(key)
        return fn is not None
    
    def _get_local_last_mod_ts(self, key):
        fn = self._find_local_fn(key)
        if fn is None:
            return None
        return os.path.getmtime(fn)

    # def is_stale(self, key, max_age_secs=3600):
    #     fn = self._find_local_fn(key)
    #     if fn is None:
    #         return True
    #     last_mod_ts = os.path.getmtime(fn)
    #     now_ts = time.time()
    #     return (now_ts - last_mod_ts) > max_age_secs

    def save(self, key, obj):
        print("Saving %s to remote and local" % key)
        remote_ts = self._save_obj_remote(key, obj)
        self._save_obj_local(key, obj, remote_ts)
        return True

    # def get_remote_save_local(self, key):
    #     remote_obj = self._get_obj_remote(key)
    #     if remote_obj is not None:
    #         self._save_obj_local(key, remote_obj)
    #         print("Saved remote object to local for %s" % key)
    #     else:
    #         print("No remote object found for %s" % key)
        
    
    def get(self, key):
        obj = self._get_obj_local(key)
        if obj is not None:
            return obj
        remote_ts, remote_obj = self._get_obj_remote_with_ts(key)
        if remote_obj is not None:
            self._save_obj_local(key, remote_obj, remote_ts)
        return remote_obj


    def _is_local_stale(self, key, remote_last_mod_ts):
        local_last_mod_ts = self._get_local_last_mod_ts(key)
        if local_last_mod_ts is None:
            print("Local object is None for %s" % key)
            return True
        if local_last_mod_ts <  remote_last_mod_ts:
            print("Local object older than remote for %s" % key)
            return True
        if local_last_mod_ts ==  remote_last_mod_ts:
            print("Local object ts is same as remote for %s" % key)
            return False
        if local_last_mod_ts >  remote_last_mod_ts:
            print("Local object ts is newer than remote for %s" % key)
            return False
        assert False, "Should not happen"
    
    def update_local_with_remote(self, key_starts_with=None):

        if key_starts_with is None:
            remote_keys_df = self.remote_object_db.get_all_keys_df()
        else:
            remote_keys_df = self.remote_object_db.get_all_keys_starts_with_df(key_starts_with)

        print("Updating local with remote for %s keys" % len(remote_keys_df))
        for idx, row in remote_keys_df.iterrows():
            key = row['key']
            remote_last_mod_ts = row['added_ts']
            if self._is_local_stale(key, remote_last_mod_ts):
                print("Local object is stale for %s" % key)
                remote_ts, remote_obj = self.remote_object_db.get_with_ts(key)
                if remote_obj is not None:
                    print("Saving remote object to local for %s, set ts to %s" % (key, remote_ts))
                    self._save_obj_local(key, remote_obj, remote_ts)
                else:
                    print("No remote object found for %s" % key)

        print("Done Updating local with remote")
