

import pandas as pd

class MagnitudeTableCellStyler:

    def __init__(self, df, cols):
        self.colors_df = pd.DataFrame()
        self.positive_range = ["#D4FFCF", "#81FF75", "#4CFF3B"]
        self.negative_range = ["#FFA8A8", "#FF4444", "#FF1212"]
        self.num_buckets = len(self.positive_range)
        self._build_colors_df(df, cols)

    def _get_color(self, value, bucket_idx):
        if bucket_idx is None:
            return "#FFFFFF"
        if value < 0:
            return self.negative_range[bucket_idx]
        if value > 0:
            return self.positive_range[bucket_idx]
        else:
            return "#FFFFFF"
        
    def _build_colors_df(self, df, cols):
        for col in cols:
            if col not in df.columns:
                continue
            col_values = df[col].dropna()
            if len(col_values) == 0:
                continue
            min_value = min(col_values)
            max_value = max(col_values)
            #print("Col ", col, " min ", min_value, " max ", max_value)
            buckets = self._get_bucket_ranges(min_value, max_value, self.num_buckets)
            for idx, row in df.iterrows():
                value = row[col]
                bucket_idx = self._get_bucket(value, buckets)
                #print("Value %f, Bucket %d" % (value, bucket_idx))
                color = self._get_color(value, bucket_idx)
                self.colors_df.at[idx, col] = color
        #print("Colors DF\n", self.colors_df)
        return self.colors_df
    
    def _get_bucket(self, value, buckets):
        if buckets is None:
            return None
        if type(value) is str:
            return None
        if pd.isna(value):
            return None
        value = abs(value)
        idx = 0
        #print("Find Bucket %f" % value)
        for bucket in buckets:
            bucket_min = bucket[0]
            bucket_max = bucket[1]
            #print("\tTest %f, (%f, %f)" % (value, bucket_min, bucket_max))
            if (value >= bucket_min) and (value < bucket_max):
                #print("\tFound")
                return idx
            idx += 1
        print("Bucket Not found")
        print("Buckets ", buckets)
        print("Value = ", value)
        assert False
        return idx
    
    def _get_bucket_ranges(self, min_value, max_value, num_buckets):
        if type(min_value) is str:
            return None
        #if math.isnan(min_value) or math.isnan(max_value):
        #    return None
        largest = max(abs(min_value), abs(max_value)) + 0.0001
        bucket_width = largest / num_buckets
        start = 0
        buckets = []
        for i in range(0, num_buckets):
            end = start + bucket_width
            buckets.append((start, end))
            start = end
        return buckets


    def get_style(self, row_idx, col, value):
        #return "style='background: gray;'"
        if row_idx in self.colors_df.index:
            if col in self.colors_df.columns:
                color = self.colors_df.at[row_idx, col]
                return "style='background: %s;'" % color
        return None