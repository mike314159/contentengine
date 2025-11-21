import numpy as np
import pandas as pd

class DataFrameFormatter:


    def format_none(value):
        return value

    def format_date(value):
        #print(value, type(value))
        if pd.isna(value):
            return ""
        return pd.to_datetime(value).strftime("%Y-%m-%d")

    def format_pct(value):
        #print(value, type(value))
        if pd.isna(value):
            return ""
        value = value * 100
        absvalue = np.abs(value)
        if absvalue > 100:
            return "%0.0f%s" % (value, "")
        if absvalue > 1:
            return "%0.1f%s" % (value, "")
        else:
            return "%0.2f%s" % (value, "")


    def format_pct100(value):
        if np.isnan(value):
            return ""
        absvalue = np.abs(value)
        if absvalue > 100:
            return "%0.0f%s" % (value, "")
        if absvalue > 1:
            return "%0.1f%s" % (value, "")
        else:
            return "%0.2f%s" % (value, "")


    def format_value(value):
        if np.isnan(value):
            return ""
        absvalue = np.abs(value)
        if absvalue > 1000:
            return "%0.0f" % (value)
        if absvalue > 100:
            return "%0.1f" % (value)
        if absvalue > 1:
            return "%0.2f" % (value)
        else:
            return "%f" % (value)


    def format_value_usd(value):
        if np.isnan(value):
            return ""
        return "%s%0.2f" % ("", value)

    def format_two_sig_digits(value):
        if np.isnan(value):
            return ""
        return "%0.2f" % (value)
    

    def apply_formats(df, fmts):
        funcs = {
            'format_pct': DataFrameFormatter.format_pct,
            'format_date': DataFrameFormatter.format_date
        }
        #df = df.copy()
        #cols = []
        for col, func_name in fmts.items():
            if col in df.columns:
                func = funcs.get(func_name, None)
                if func is not None:
                    df[col] = df[col].apply(func)
         #       cols.append(col)
        #return df

    def apply_color_formats(self, colors_df, data_df, fmts):
        funcs = {
            'format_color_pos_neg': DataFrameFormatter.format_color_pos_neg
        }
        for col, func_name in fmts.items():
            if col in data_df.columns:
                func = funcs.get(func_name, None)
                if func is not None:
                    colors_df[col] = data_df[col].apply(func)
         #       cols.append(col)
        #return df

    def format_df_col(src_df, dest_df, col_name, func):
        for idx, row in src_df.iterrows():
            value = row[col_name]
            format_value = func(value)
            dest_df.set_value(idx, col_name, format_value)


    def format_colors_df_col(table_df, colors_df, col_name, func):
        for idx, row in table_df.iterrows():
            value = row[col_name]
            format_value = func(value)
            colors_df.set_value(idx, col_name, format_value)


    def format_color_pos_neg(value):
        #print(type(value))
        if np.isnan(value):
            return ""
        if value < 0:
            return "#8B0000"
        else:
            return "#006400"

    def cell_fmt_pos_neg_color(value):
        if value < 0:
            return "red_cell"
        if value > 0:
            return "green_cell"
        return np.nan

    def format_pass_thru(value):
        return value


    def format_no_color(value):
        return ""



