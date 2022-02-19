import json
import rrdtool
import pandas as pd
import numpy as np
import datetime
from libmetric.query import Query, InstantQuery, RangeQuery


class RrdRangeQuery(RangeQuery):
    def __init__(self, **kwargs):
        super(RrdRangeQuery, self).__init__(**kwargs)
        self.url = kwargs["url"]

    def get(self):
        result = rrdtool.fetch(self._url(), str(self.queries[0]))

        start, end, step = result[0]
        ds = result[1]
        rows = result[2]

    #        return self._process(data)

    def _url(self):
        return str(self.base_url.replace("file://", ""))


class RrdInstantQuery(InstantQuery):
    def __init__(self, **kwargs):
        super(RrdInstantQuery, self).__init__(**kwargs)
        self.url = kwargs["url"]

    def get(self):
        data = json.loads(requests.get(self._url(), verify=False).text)
        return self._process(data)


class RrdSearch(Search):
    def __init__(self, **kwargs):
        super(RrdSearch, self).__init__(**kwargs)

    def _url(self):
        return str(self.base_url.replace("file://", ""))

    def get(self):
        data_sources = set()
        info = rrdtool.info(self._url())
        for datum, real_value in info.items():
            if datum.startswith("ds"):
                value = datum.replace("ds[", "").split("].")
                # if value[0] not in data_source:
                #     data_source[value[0]] = {}
                # data_source[value[0]][value[1]] = real_value
                data_sources.add(value[0])
        return list(data_sources)
