import pandas as pd
import numpy as np
import datetime
from libmetric.query import Query, InstantQuery, RangeQuery
from libmetric.search import Search

PROMETHEUS_REPLY = "Prometheus API replied with error {}: {}"


class PrometheusQuery(Query):
    def __init__(self, **kwargs):
        kwargs["queries"] = [kwargs["query"]]
        if kwargs.get("moment", None) == None:
            self._collector = PrometheusRangeQuery(**kwargs)
        else:
            self._collector = PrometheusInstantQuery(**kwargs)
        super(PrometheusQuery, self).__init__(**kwargs)

    def _render_info(self):
        info = "Query info:\n".format(**self._info)
        info += "  Server URL: {url}\n".format(**self._info)
        if self._info.get("moment", None) == None:
            info += "  Type: Range PromQL query\n".format(**self._info)
        else:
            info += "  Type: Instant PromQL query\n".format(**self._info)
        info += "  Query: {query}\n".format(**self._info)
        if self._info.get("moment", None) == None:
            info += "  Duration: {start} - {end}\n".format(**self._info)
        else:
            info += "  Moment: {moment}\n".format(**self._info)
        info += "  Step: {step}\n".format(**self._info)
        return info


class PrometheusRangeQuery(RangeQuery):
    def __init__(self, **kwargs):
        super(PrometheusRangeQuery, self).__init__(**kwargs)

    def data(self):
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
            title_list = []
            for key, value in series["metric"].items():
                title_list.append(f"{key}={value}")
            series["header"] = "{" + ",".join(title_list) + "}"

        np_data = [
            (
                series["header"],
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

    def data(self):
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

            title_list = []
            for key, value in series["metric"].items():
                title_list.append(f"{key}={value}")
            series["header"] = "{" + ",".join(title_list) + "}"

        np_data = [
            (
                series["header"],
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


class PrometheusSearch(Search):
    def __init__(self, **kwargs):
        super(PrometheusSearch, self).__init__(**kwargs)

    def _url(self):
        params = []
        params += ["match[]={}".format(search) for search in self.search]
        if self.start is not None:
            params += ["start={}".format(self.start), "end={}".format(self.end)]
        url = "/api/v1/series?" + "&".join(params)
        return self.base_url + url

    def _process(self, response):
        print(response)
