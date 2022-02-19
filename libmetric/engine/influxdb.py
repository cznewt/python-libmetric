import pandas as pd
import numpy as np
import datetime
from libmetric.query import Query, InstantQuery, RangeQuery
from libmetric.search import Search


class InfluxdbQuery(Query):
    def __init__(self, **kwargs):
        if kwargs.get("moment", None) == None:
            self.collector = InfluxdbRangeQuery(**kwargs)
        else:
            self.collector = InfluxdbInstantQuery(**kwargs)
        super(InfluxdbQuery, self).__init__(**kwargs)


class InfluxdbRangeQuery(RangeQuery):
    def __init__(self, **kwargs):
        super(InfluxdbRangeQuery, self).__init__(**kwargs)
        self.partition = kwargs["partition"]

    def get(self):
        data = self._http_get_params()
        return self._process(data)

    def _params(self):
        params = {"db": self.partition, "epoch": "s", "q": self.queries[0]}
        if self.user is not None:
            params["u"] = self.user
            params["p"] = self.password
        return params

    def _url(self):
        url = "/query"
        return self.base_url + url

    def _process(self, response):
        data = response["results"][0]["series"]
        np_data = [(series["name"], np.array(series["values"])) for series in data]
        series = []
        for query, serie in np_data:
            frame = pd.DataFrame(serie[:, 1], index=serie[:, 0], columns=[query])
            series.append(frame)
        if len(series) > 0:
            return pd.concat(series, axis=1, join="inner")
        else:
            return None


class InfluxdbInstantQuery(InstantQuery):
    def __init__(self, **kwargs):
        super(InfluxdbInstantQuery, self).__init__(**kwargs)
        self.partition = kwargs["partition"]

    def _url(self):
        params = ["q={}".format(query) for query in self.queries]
        if self.user is not None:
            params += ["u={}".format(self.user), "p={}".format(self.password)]
        url = "/query?db={}&epoch=s&{}".format(self.partition, "&".join(params))
        return self.base_url + url


class InfluxdbSearch(Search):
    def __init__(self, **kwargs):
        super(InfluxdbSearch, self).__init__(**kwargs)
        self.partition = kwargs["partition"]

    def _url(self):
        params = ["q={}".format(search) for search in self.search]
        if self.user is not None:
            params += ["u={}".format(self.user), "p={}".format(self.password)]
        url = "/search?db={}&epoch=s&{}".format(self.partition, "&".join(params))
        return self.base_url + url
