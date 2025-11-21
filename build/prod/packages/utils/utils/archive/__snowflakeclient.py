import snowflake.connector
import base64
import pandas as pd
from snowflake.connector import NotSupportedError

class SnowflakeClient:
    def __init__(self, account, username, password, role, database, warehouse, schema, pkey):
        self.username = username
        self.role = role
        self.password = password
        self.account = account
        self.database = database
        self.warehouse = warehouse
        self.schema = schema
        self.fetch_size = 10000
        self.private_key_text = base64.b64decode(pkey)

    def _get_connection(self):
        return snowflake.connector.connect(
            user=self.username,
            password=self.password,
            account=self.account,
            warehouse=self.warehouse,
            database=self.database,
            schema=self.schema,
            role=self.role,
            private_key=self.private_key_text,
        )

    def fetch_df(self, query):
        conn = self._get_connection()
        try:
            cur = conn.cursor()
            cur.execute(query)
            df = cur.fetch_pandas_all()
        except NotSupportedError:
            df = pd.DataFrame()
        finally:
            cur.close()

        conn.close()
        return df
        
    def execute_query(self, query):

        ctx = self._get_connection()
        cs = ctx.cursor()
        try:
            cs.execute("USE WAREHOUSE %s" % self.warehouse)
            cs.execute(query)

        finally:
            cs.close()
        ctx.close()