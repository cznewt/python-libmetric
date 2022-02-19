
import pandas as pd
import numpy as np
import datetime
from libmetric.query import Query, InstantQuery, RangeQuery



class ElasticSearchRangeQuery(RangeQuery):

    def __init__(self, **kwargs):
        super(ElasticSearchRangeQuery, self).__init__(**kwargs)

    def get(self):
        data = self._http_get_data()
        return self._process(data)

    def _url(self):
        url = '/_search'
        return self.base_url + url

    def _params(self):
        return {
            'query': self.queries[0]
        }

    def _process(self, data):
        np_data = [(series['query'],
                    np.array(series['datapoints'])) for series in data]
        series = [pd.DataFrame(series[:, 0],
                               index=series[:, 1],
                               columns=[query]) for query, series in np_data if series.any()]
        if len(series) > 0:
            return pd.concat(series, axis=1, join='inner')
        else:
            return None

