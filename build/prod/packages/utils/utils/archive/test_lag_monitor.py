import instadataeng as de
import sys
import time


def getQuery(db_name, schema_name, table_name, column_name):
    column_name = column_name.upper()
    fq_table_name = "%s.%s.%s" % (db_name, schema_name, table_name)
    fq_table_name_up = fq_table_name.upper()
    sql = """
    select 
        '%s' as db_name,
        '%s' as schema_name,
        '%s' as table_name,
        '%s' as col_name,
        EXTRACT(EPOCH FROM (max(%s))) as last_unix_ts, 
        EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP)) as current_unix_ts,  
        (current_unix_ts-last_unix_ts)/60 as lag_mins 
        FROM %s """ % (
        db_name,
        schema_name,
        table_name.upper(),
        column_name,
        column_name,
        fq_table_name_up,
    )
    return sql


config = {
    "snowflake": {
        "INSTADATA": {
            "DWH": {
                "fact_order_item": {
                    "metrics": {"lag_mins": {"col": "order_date_time_utc"}}
                },
                "fact_order": {"metrics": {"lag_mins": {"col": "created_at"}}},
                "fact_order_delivery": {
                    "metrics": {"lag_mins": {"col": "delivery_created_date_time_utc"}}
                },
                "fact_event": {"metrics": {"lag_mins": {"col": "EVENT_DATE_TIME_UTC"}}},
                "fact_event_search": {
                    "metrics": {"lag_mins": {"col": "SEARCH_EVENT_DATE_TIME_UTC"}}
                },
                "fact_event_replacement_impression": {
                    "metrics": {"lag_mins": {"col": "REPLACEMENT_IMPRESSION_DATE_UTC"}}
                },
                "FACT_EVENT_BROWSE_IMPRESSION": {
                    "metrics": {"lag_mins": {"col": "BROWSE_IMPRESSION_DATE_TIME_UTC"}}
                },
                "FACT_EVENT_SEARCH_IMPRESSION": {
                    "metrics": {"lag_mins": {"col": "SEARCH_IMPRESSION_DATE_TIME_UTC"}}
                },
                "DIM_ITEM": {
                    "metrics": {"lag_mins": {"col": "ITEM_CREATED_DATE_TIME_UTC"}}
                },
                "fact_in_store_transaction": {
                    "metrics": {"lag_mins": {"col": "TRANSACTION_DATE_TIME_UTC"}}
                },
                "FACT_BATCH": {
                    "metrics": {"lag_mins": {"col": "BATCH_CREATED_DATE_UTC"}}
                },
            },
            "RDS_DATA": {
                "ORDER_RECONCILIATIONS": {
                    "metrics": {"lag_mins": {"col": "CREATED_AT"}}
                },
                "ORDER_DELIVERY_RECONCILIATIONS": {
                    "metrics": {"lag_mins": {"col": "CREATED_AT"}}
                },
                "ORDER_ITEM_RECONCILIATIONS": {
                    "metrics": {"lag_mins": {"col": "CREATED_AT"}}
                },
            },
        }
    }
}


"""

Retailers

mvw_transaction_logs,
DELIVERED_AT

Shoppers

DWH.FACT_AVAILABILITY_METRIC
no created date

DWH.DIM_BATCH_ORDER_DELIVERY_MAP
DWH_CREATED_DATE_TIME_UTC

DWH.FACT_BATCH_STATE
STATE_STARTED_DATE_TIME_UTC

DWH.DIM_SHOPPER_SHIFT
SHIFT_CREATED_DATE_TIME_UTC

DWH.DIM_SHOPPER
SHOPPER_CREATED_DATE_TIME_UTC

DWH.DIM_SHOPPER_MILESTONE
DWH.DIM_APPLICANT
APPLIED_DATE_TIME_UTC

DWH.FACT_SHOPPER_COHORT


DIM_PRODUCT
PRODUCT_CREATED_DATE_TIME_UTC

FACT_EVENT_CPG_COUPON
EVENT_DATE_TIME_PT

FACT_EVENT_DELIVERY_PROMOTION
EVENT_DATE_TIME_UTC
"""


def queryLag(config):
    selects = []
    for wh, wconfig in config.items():
        for db, dconfig in wconfig.items():
            for schema, sconfig in dconfig.items():
                for table, tconfig in sconfig.items():
                    for metrics, msconfig in tconfig.items():
                        for metric, mconfig in msconfig.items():
                            if metric is "lag_mins":
                                column = mconfig["col"]
                                print(wh, db, schema, table, metric, column)
                                sql = getQuery(db, schema, table, column)
                                selects.append(sql)

    sql = "\nunion all\n".join(selects)
    print(sql)

    sf = de.SnowflakeClient()
    df = sf.execute_query_to_df(sql)
    return df


def updateLag(config):

    ts = time.time()
    df = queryLag(config)
    print(df)

    dd = de.DataDogAPIClient()
    for idx, row in df.iterrows():
        metric = "dataeng.snowflake.lag_mins"
        db = row["DB_NAME"]
        schema = row["SCHEMA_NAME"]
        table = row["TABLE_NAME"]
        value = row["LAG_MINS"]
        tags = [
            "db:%s" % db,
            "schema:%s.%s" % (db, schema),
            "table:%s.%s.%s" % (db, schema, table),
        ]
        dd.sendGauge(metric, ts, value, tags)


# -----------------
# MAIN
# -----------------

while True:
    updateLag(config)
    time.sleep(10 * 60)
