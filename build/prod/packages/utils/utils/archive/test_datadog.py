import instadataeng as de
import sys
import random
import time

dd = de.DataDogAPIClient()

metric = "dataeng.snowflake.lag_mins"
db = "instadata"
schema = "dwh"
table = "fact_event_replacement_impression"
tags = [
    "db:%s" % db,
    "schema:%s.%s" % (db, schema),
    "table:%s.%s.%s" % (db, schema, table),
]

value = 500
for j in range(1, 500):
    ts = time.time()
    incr = random.randrange(-20, +20)
    value = value + incr
    if value < 0:
        value = 0
    dd.sendCount(metric, ts, value, tags)
    time.sleep(5)

sys.exit()

#   python /app/scripts/test_datadog.py


# sdb = statsdb.StatsDB()

# initialize(**options)
#
# title = "Data Eng Test"
# text = 'And let me tell you all about it here!'
# tags = ['dataeng:1', 'application:cli']

# api.Event.create(title=title, text=text, tags=tags)

# Submit a single point with a timestamp of `now`
# for i in range(1,20):
#     for j in range(1,10):
#         value = random.randrange(1000)
#         metric_name = 'test.dataeng.metric1'
#         tags = ['wh:%d' % j]
#         #api.Metric.send(metric=metric_name, points=v, tags=tags)
#         ts = time.time()
#         sdb.sendCount(metric_name, ts, value, tags)
#         #print("%s=%d" % (metric_name, value))
#         time.sleep(1)
#     time.sleep(60)
