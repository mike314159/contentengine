import instadataeng as de
from instadataeng import postgresclient as pgc
from instadataeng import secrets


def get_client():
    conn_str = secrets.get_secret("POSTGRES_CONN_STRING", required=True)
    return pgc.PostgresClient(conn_str)


def test_instantiate_class():
    pg = get_client()
    assert isinstance(pg, pgc.PostgresClient)


def test_query():
    pg = get_client()
    sql = "select process_name, cron_schedule from etl_metadata.etl_data_extract_config LIMIT 10"
    df = pg.execute_query_to_df(sql)
    # print(df)
    assert len(df.index) > 0


# test_query()
