import pandas as pd
import numpy as np
import datetime
from libmetric.query import Query, InstantQuery, RangeQuery

PROMETHEUS_REPLY = "Prometheus API replied with error {}: {}"


class PrometheusQuery(Query):
    def __init__(self, **kwargs):
        if kwargs.get("moment", None) == None:
            self.collector = PrometheusRangeQuery(**kwargs)
        else:
            self.collector = PrometheusInstantQuery(**kwargs)
        super(PrometheusQuery, self).__init__(**kwargs)


class PrometheusRangeQuery(RangeQuery):
    def __init__(self, **kwargs):
        super(PrometheusRangeQuery, self).__init__(**kwargs)

    def get(self):
        data = self._http_get_params()
        return self._process(data)

    def _params(self):
        return {
            "query": self.queries,
            "start": self.start,
            "end": self.end,
            "step": self.step,
        }

    def _url(self):
        url = "/api/v1/query_range"
        if self.step:
            return self.base_url + url + "?step=%s" % self.step
        return self.base_url + url

    def _process(self, response):
        if response["status"] == "error":
            raise Exception(
                PROMETHEUS_REPLY.format(response["errorType"], response["error"])
            )
        data = response["data"]["result"]

        for series in data:
            for values in series["values"]:
                values[0] = pd.Timestamp(datetime.datetime.fromtimestamp(values[0]))
                values[1] = float(values[1])

        np_data = [
            (
                "{}_{}".format(
                    series["metric"].get("__name__", "name"),
                    series["metric"].get("instance", "instance"),
                ),
                np.array(series["values"]),
            )
            for series in data
        ]

        series = []
        for query, serie in np_data:
            frame = pd.DataFrame(serie[:, 1], index=serie[:, 0], columns=[query])
            series.append(frame)
        if len(series) > 0:
            return pd.concat(series, axis=1, join="inner")
        else:
            return None


class PrometheusInstantQuery(InstantQuery):
    def __init__(self, **kwargs):
        super(PrometheusInstantQuery, self).__init__(**kwargs)

    def get(self):
        data = self._http_get_params()
        return self._process(data)

    def _params(self):
        return {"query": self.queries, "time": self.moment}

    def _url(self):
        url = "/api/v1/query"
        return self.base_url + url

    def _process(self, response):
        if response["status"] == "error":
            raise Exception(
                PROMETHEUS_REPLY.format(response["errorType"], response["error"])
            )
        data = response["data"]["result"]
        for series in data:
            for values in [series["value"]]:
                values[0] = pd.Timestamp(datetime.datetime.fromtimestamp(values[0]))
                values[1] = float(values[1])
        np_data = [
            (
                "{}_{}".format(
                    series["metric"]["__name__"], series["metric"]["instance"]
                ),
                np.array([series["value"]]),
            )
            for series in data
        ]
        series = []
        for query, serie in np_data:
            frame = pd.DataFrame(serie[:, 1], index=serie[:, 0], columns=[query])
            series.append(frame)
        if len(series) > 0:
            return pd.concat(series, axis=1, join="inner")
        else:
            return None
