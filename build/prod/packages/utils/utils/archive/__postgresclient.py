import os
import pandas as pd
from packages.utils.utils import __secrets
from sqlalchemy import create_engine


class PostgresClient:
    def __init__(self, connection_str):
        self.connection_str = connection_str

    def execute_query_to_df(self, sql):
        db = create_engine(self.connection_str)
        df = pd.read_sql_query(sql, con=db)
        return df
