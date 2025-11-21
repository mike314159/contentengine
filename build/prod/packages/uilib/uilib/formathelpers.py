import numpy as np


# def format_none(value):
#     return value


# def format_pct(value):
#     if np.isnan(value):
#         return ""
#     value = value * 100
#     absvalue = np.abs(value)
#     if absvalue > 100:
#         return "%0.0f%s" % (value, "")
#     if absvalue > 1:
#         return "%0.1f%s" % (value, "")
#     else:
#         return "%0.2f%s" % (value, "")


# def format_pct100(value):
#     if np.isnan(value):
#         return ""
#     absvalue = np.abs(value)
#     if absvalue > 100:
#         return "%0.0f%s" % (value, "")
#     if absvalue > 1:
#         return "%0.1f%s" % (value, "")
#     else:
#         return "%0.2f%s" % (value, "")


def format_float_value(value):
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
    
def format_int_value(value):
    if np.isnan(value):
        return ""
    try:
        return "%d" % (value)
    except:
        return ""
    

# def format_value_usd(value):
#     if np.isnan(value):
#         return ""
#     return "%s%0.2f" % ("", value)


# def apply_formats(df, fmts):
#     df = df.copy()
#     cols = []
#     for col in fmts.keys():
#         if col in df.columns:
#             func = fmts[col]
#             df[col] = df[col].apply(func)
#             cols.append(col)
#     return (df, cols)


# def format_df_col(src_df, dest_df, col_name, func):
#     for idx, row in src_df.iterrows():
#         value = row[col_name]
#         format_value = func(value)
#         dest_df.set_value(idx, col_name, format_value)


# def format_colors_df_col(table_df, colors_df, col_name, func):
#     for idx, row in table_df.iterrows():
#         value = row[col_name]
#         format_value = func(value)
#         colors_df.set_value(idx, col_name, format_value)


# def format_color_pos_neg(value):
#     if np.isnan(value):
#         return ""
#     if value < 0:
#         return "#F5B7B1"
#     else:
#         return "#ABEBC6"


# def format_pass_thru(value):
#     return value


# def format_no_color(value):
#     return ""

