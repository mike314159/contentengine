

import pandas as pd


class CellValueFormatter:

    '''
        col_fmts = {
            '1d': [CellValueFormatter.format_pct],
        }
    '''
    def __init__(self, col_fmts):
        self.col_fmts = col_fmts

    def format_currency(value):
        if pd.isna(value):
            return ""
        return "%0.2f" % value

    def format_float(value):
        if pd.isna(value):
            return ""
        try:
            v = float(value)
            return "%0.2f" % (v)
        except:
            #print("Error formatting %s" % value)
            return ""
        
    def format_pct(value):
        if pd.isna(value):
            return ""
        try:
            v = float(value)
            return "%0.2f%%" % (v)
        except:
            #print("Error formatting %s" % value)
            return ""
    
    def format(self, col, value):
        if col in self.col_fmts.keys():
            funcs = self.col_fmts[col]
            for func in funcs:
                return func(value)
        return value