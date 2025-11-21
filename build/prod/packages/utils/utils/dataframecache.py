import os
import pandas as pd
import hashlib
import datetime
import time
from abc import ABC, abstractmethod
from utils.pgfilestore import PGFileStore

# A simple class to save and retrieve a dataframe to disk

class DataFrameCache(ABC):

    def __init__(self, cache_name):
        self.cache_name = cache_name

    @abstractmethod
    def get_df(self, id):
        pass

    @abstractmethod
    def save_df(self, id, df):
        pass

    # @abstractmethod
    # def is_stale(self, id, max_age_secs=3600):
    #     pass

    # @abstractmethod
    # def exists(self, id):
    #     pass

    # def _get_data_type_dir(self, data_type_name, create_dir=False):
    #     dir = os.path.join(self.data_dir, data_type_name)
    #     if not os.path.exists(dir) and create_dir:
    #         os.mkdir(dir)
    #     return dir
    
    
    # def is_stale(self, id, data_type_name, max_age_secs=3600):
    #     fn = self._get_fn(id, data_type_name)
    #     age = DataFrameCache._file_age_secs(fn)
    #     if age is None:
    #         return True
    #     if age > max_age_secs:
    #         return True
    #     return False




    # # def get_df_min_ts(self, id, min_ts):
    # #     fn = self._get_fn(id)
    # #     ts = DataFrameCache._file_ts(fn)
    # #     if ts is None:
    # #         return None
    # #     if ts < min_ts:
    # #         return None
    # #     return self.get_df(id)



    # # def delete_df(self, id, data_type_name):
    # #     fn = self._get_fn(id, data_type_name)
    # #     if os.path.exists(fn):
    # #         os.unlink(fn)

    # # def get_last_update_dt(self, id):
    # #     fn = self._get_fn(id)
    # #     ts = DataFrameCache._file_ts(fn)
    # #     if ts is None:
    # #         return None
    # #     return datetime.datetime.fromtimestamp(ts)


class LocalDataFrameCache(DataFrameCache):

    def __init__(self, file_cache_dir, max_age_secs=None):
        super().__init__(NotImplementedError)    
        self.data_dir = file_cache_dir
        self.max_age_secs = max_age_secs
        if not os.path.exists(file_cache_dir):
            os.makedirs(file_cache_dir, exist_ok=True)

    def _get_fn(self, id):
        file = "%s.pkl" % (id)
        return os.path.join(self.data_dir, file)

    def get_df(self, id):
        if self.max_age_secs is not None:
            if self.is_stale(id, self.max_age_secs):
                return None
        fn = self._get_fn(id)
        if os.path.exists(fn):
            df = pd.read_pickle(fn)
            return df
        return None

    def save_df(self, id, df):
        if df is None:
            return False
        fn = fn = self._get_fn(id)
        df.to_pickle(fn)
        print("Wrote dataframe to ", fn)

    def exists(self, id):
        fn = self._get_fn(id)
        return os.path.exists(fn)

    def _file_ts(fn):
        if not os.path.exists(fn):
            return 0
        else:
            return os.path.getmtime(fn)

    def _file_age_secs(fn):
        current_ts = time.time()
        file_ts = LocalDataFrameCache._file_ts(fn)
        diff = current_ts - file_ts
        return diff

    def get_last_modified_ts(self, id):
        fn = self._get_fn(id)
        ts = LocalDataFrameCache._file_ts(fn)
        return ts

    def is_stale(self, id, max_age_secs=3600):
        fn = self._get_fn(id)
        age = LocalDataFrameCache._file_age_secs(fn)
        if age is None:
            return True
        if age > max_age_secs:
            return True
        return False

    def list_ids(self):
        """
        Returns a list of all IDs for which dataframes are stored in the cache.
        """
        try:
            # Get all .pkl files in the data directory
            file_list = [f for f in os.listdir(self.data_dir) if f.endswith('.pkl')]
            # Extract ID from each filename
            ids = [os.path.splitext(file)[0] for file in file_list]
            return ids
        except Exception as e:
            print(f"Failed to list cached IDs: {e}")
            return []


# class PGStoreDataFrameCache(DataFrameCache):

#     def __init__(self, app, collection, pg_connect_config, local_dest_dir, disable_pg_writes):
#         name = "%s_%s" % (app, collection)
#         super().__init__(name)
#         self.pg_store = PGFileStore(app, collection, pg_connect_config)
#         self.local_dest_dir = local_dest_dir
#         self.local_cache = LocalDataFrameCache(local_dest_dir)

#         # In dev situations I dont want to mess up PG
#         self.disable_pg_writes = disable_pg_writes

#     # We're asumming that a sync was done before this.
#     # Local data has everything that is in PG.
#     def get_df(self, id):
#         df = self.local_cache.get_df(id)
#         return df

#     # Any updates to an id should write through to PG
#     def save_df(self, id, df):
#         if df is None:
#             return False
#         self.local_cache.save_df(id, df)
#         local_fn = self.local_cache._get_fn(id)
#         if not self.disable_pg_writes:
#             self.pg_store.save_file(id, local_fn)

    # def sync(self):

    #     local_ids = self.local_cache.list_ids()
    #     pg_ids = self.pg_store.list_file_ids()

    #     # Convert lists to sets for set operations
    #     local_id_set = set(local_ids)
    #     pg_id_set = set(pg_ids)

    #     local_only_ids = list(local_id_set - pg_id_set)  # IDs that are only in the local cache
    #     pg_only_ids = list(pg_id_set - local_id_set)     # IDs that are only in the PostgreSQL database
    #     common_ids = list(local_id_set & pg_id_set)      # IDs that are common to both

    #     print("Local Only IDs:", local_only_ids)
    #     print("PostgreSQL Only IDs:", pg_only_ids)
    #     print("Common IDs:", common_ids)

    #     for id in pg_only_ids:
    #         print("Pulling ID ", id)
    #         local_fn = self.local_cache._get_fn(id)
    #         self.pg_store.pull_file(id, local_fn)

    #     if not self.disable_pg_writes:
    #         for id in local_only_ids:
    #             print("Uploading ID ", id)
    #             local_fn = self.local_cache._get_fn(id)
    #             self.pg_store.save_file(id, local_fn)

    #     for id in common_ids:
    #         print("Checking ID ", id)
    #         local_fn = self.local_cache._get_fn(id)
    #         local_last_modified_ts = int(os.path.getmtime(local_fn))
    #         details = self.pg_store.get_file_details(id)
    #         remote_last_modified_ts = details.get('last_mod_ts', 0)
    #         print("Local Last Modified ", local_last_modified_ts)
    #         if local_last_modified_ts == remote_last_modified_ts:
    #             print("Local file is the same as in PG. Skipping.")
    #         else:
    #             if local_last_modified_ts > remote_last_modified_ts:
    #                 if not self.disable_pg_writes:
    #                     print("Local file is more recent than in PG. Upload it to PG")
    #                     self.pg_store.save_file(id, local_fn)
    #             else:
    #                 print("Local file is older than in PG. Pulling from PG.")
    #                 self.pg_store.pull_file(id, local_fn)
