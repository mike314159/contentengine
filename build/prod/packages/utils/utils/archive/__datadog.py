from packages.utils.utils.__datadog import initialize
from packages.utils.utils.__datadog import api
import time


class DataDogAPIClient:
    def __init__(self):

        options = {
            #'api_key': '783f4892814b50b0b5fd0d81791e4ff9',
            "api_key": "c9113a59ea00be7718b7e7211389dbb2",
            "app_key": "783fd4878864e2435290a5af9cee6e0fa90f6b0d",
        }
        initialize(**options)

    # Submit a single point with a timestamp of `now`
    def sendGauge(self, metric_name, ts, value, tags):
        print("%d: gauge %s=%f, %s" % (ts, metric_name, value, tags))
        response = api.Metric.send(
            metric=metric_name, points=[(ts, value)], tags=tags, type="gauge"
        )
        print(response)
