import instadataeng as de


def example1():
    sf = de.SnowflakeClient()
    query = "select * from SNOWFLAKE.ACCOUNT_USAGE.warehouse_metering_history limit 10"
    df = sf.execute_query_to_df(query)
    print(df.head())


def example2():
    key = "SNOWFLAKE_USER"
    sf_user = de.get_secret(key)
    print("%s = %s" % (key, sf_user))


example1()
example2()
