import pandas as pd
import numpy as np
import datetime
from libmetric.query import Query, InstantQuery, RangeQuery
from libmetric.search import Search


class GraphiteQuery(Query):
    def __init__(self, **kwargs):
        if kwargs.get("moment", None) == None:
            self._collector = GraphiteRangeQuery(**kwargs)
        else:
            self._collector = GraphiteInstantQuery(**kwargs)
        super(GraphiteQuery, self).__init__(**kwargs)

    def _render_info(self):
        return self._info


class GraphiteRangeQuery(RangeQuery):
    def __init__(self, **kwargs):
        super(GraphiteRangeQuery, self).__init__(**kwargs)

    def data(self):
        data = self._http_get_params()
        return self._process(data)

    def _params(self):
        return {
            "target": self.queries,
            "from": self.start,
            "until": self.end,
            "format": "json",
        }

    def _url(self):
        url = "/render"
        return self.base_url + url

    def _process(self, data):
        np_data = [(series["query"], np.array(series["datapoints"])) for series in data]
        series = [
            pd.DataFrame(series[:, 0], index=series[:, 1], columns=[query])
            for query, series in np_data
            if series.any()
        ]
        if len(series) > 0:
            return pd.concat(series, axis=1, join="inner")
        else:
            return None


class GraphiteInstantQuery(InstantQuery):
    def __init__(self, **kwargs):
        super(GraphiteInstantQuery, self).__init__(**kwargs)

    def _url(self):
        params = ["from={}".format(self.start), "until={}".format(self.end)]
        params += ["target={}".format(query) for query in self.queries]
        url = "/render?format=json&{}".format("&".join(params))
        return self.base_url + url


class GraphiteSearch(Search):
    def __init__(self, **kwargs):
        super(GraphiteSearch, self).__init__(**kwargs)

    def _url(self):
        params = ["from={}".format(self.start), "until={}".format(self.end)]
        params += ["target={}".format(search) for search in self.search]
        url = "/render?format=json&{}".format("&".join(params))
        return self.base_url + url
