import os
import pandas as pd
import hashlib
import datetime

# A simple class to save and retrieve a dataframe to disk

class DataFrameCache:
    def __init__(self, data_dir="/data/dataframes"):

        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)

    def _get_fn(self, id):
        return os.path.join(self.data_dir, "%s.pkl" % (id))

    def _file_ts(fn):
        if not os.path.exists(fn):
            return None
        else:
            return os.path.getmtime(fn)

    def get_df(self, id):
        fn = self._get_fn(id)
        if os.path.exists(fn):
            print("DataFrameStore Loading ", fn)
            df = pd.read_pickle(fn)
            # print("Done loading")
            return df
        else:
            print("ERROR: Dataframe not found ", fn)
        return None

    def get_df_min_ts(self, id, min_ts):
        fn = self._get_fn(id)
        ts = DataFrameStore._file_ts(fn)
        if ts is None:
            return None
        if ts < min_ts:
            return None
        return self.get_df(id)

    def save_df(self, id, df):
        if df is None:
            return False
        if len(df.index) == 0:
            return False
        fn = self._get_fn(id)
        df.to_pickle(fn)
        print("Wrote dataframe to ", fn)

    def delete_df(self, id):
        fn = self._get_fn(id)
        if os.path.exists(fn):
            os.unlink(fn)

    def get_last_update_dt(self, id):
        fn = self._get_fn(id)
        ts = DataFrameStore._file_ts(fn)
        return datetime.datetime.fromtimestamp(ts)