from instadataeng import snowflakeclient as sfc
from instadataeng import secrets


def get_client():
    warehouse = secrets.get_secret("SNOWFLAKE_WAREHOUSE", required=True)
    account = secrets.get_secret("SNOWFLAKE_ACCOUNT", required=True)
    username = secrets.get_secret("SNOWFLAKE_USERNAME", required=True)
    password = secrets.get_secret("SNOWFLAKE_PASSWORD", required=False, default=None)
    pkey = secrets.get_secret("SNOWFLAKE_PRIVATE_KEY", required=False, default=None)
    role = secrets.get_secret("SNOWFLAKE_ROLE", required=True)
    database = secrets.get_secret("SNOWFLAKE_DATABASE", required=False, default=None)
    schema = secrets.get_secret("SNOWFLAKE_SCHEMA", required=False, default=None)
    return sfc.SnowflakeClient(account, username, password, role, database, warehouse, schema, pkey)

def test_instantiate_class():
    sf = get_client()
    assert isinstance(sf, sfc.SnowflakeClient)


def test_query():
    sf = get_client()
    sql = "select * from rds_data.users limit 15"
    df = sf.fetch_df(sql)
    assert len(df.index) == 15
    print(df.head())


test_query()

