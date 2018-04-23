#!/usr/bin/env python

import json
import requests
import pandas as pd
import numpy as np
import datetime

PROMETHEUS_REPLY = 'Prometheus API replied with error {}: {}'


class RangeQuery(object):

    def __init__(self, **kwargs):
        self.base_url = kwargs['url']
        self.user = kwargs.get('user', None)
        self.password = kwargs.get('password')
        self.queries = kwargs['queries']
        self.start = kwargs['start']
        self.end = kwargs['end']
        self.step = kwargs['step']
        self.verify = False

    def _process(self, data):
        raise NotImplementedError

    def _url(self):
        raise NotImplementedError

    def _http_get_params(self):
        return json.loads(requests.get(self._url(),
                                       params=self._params(),
                                       verify=self.verify).text)

    def _http_get_data(self):
        return json.loads(requests.get(self._url(),
                                       data=json.dumps(self._params()),
                                       verify=self.verify).text)


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


class GraphiteRangeQuery(RangeQuery):

    def __init__(self, **kwargs):
        super(GraphiteRangeQuery, self).__init__(**kwargs)

    def get(self):
        data = self._http_get_params()
        return self._process(data)

    def _params(self):
        return {
            'target': self.queries,
            'from': self.start,
            'until': self.end,
            'format': 'json'
        }

    def _url(self):
        url = '/render'
        return self.base_url + url

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


class InfluxRangeQuery(RangeQuery):

    def __init__(self, **kwargs):
        super(InfluxRangeQuery, self).__init__(**kwargs)
        self.partition = kwargs['partition']

    def get(self):
        data = self._http_get_params()
        return self._process(data)

    def _params(self):
        params = {
            'db': self.partition,
            'epoch': 's',
            'q': self.queries[0]
        }
        if self.user is not None:
            params['u'] = self.user
            params['p'] = self.password
        return params

    def _url(self):
        url = '/query'
        return self.base_url + url

    def _process(self, response):
        data = response['results'][0]['series']
        np_data = [(series['name'],
                    np.array(series['values'])) for series in data]
        series = []
        for query, serie in np_data:
            frame = pd.DataFrame(serie[:, 1],
                                 index=serie[:, 0],
                                 columns=[query])
            series.append(frame)
        if len(series) > 0:
            return pd.concat(series, axis=1, join='inner')
        else:
            return None


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
            "step": self.step
        }

    def _url(self):
        url = '/api/v1/query_range'
        if self.step:
            return self.base_url + url + '?step=%s' % self.step
        return self.base_url + url

    def _process(self, response):
        if response['status'] == 'error':
            raise Exception(PROMETHEUS_REPLY.format(response['errorType'],
                                                    response['error']))
        data = response['data']['result']

        for series in data:
            for values in series['values']:
                values[0] = pd.Timestamp(
                    datetime.datetime.fromtimestamp(values[0]))
                values[1] = float(values[1])

        np_data = [('{}_{}'.format(
            series['metric'].get('__name__', 'name'),
            series['metric'].get('instance', 'instance')),
            np.array(series['values'])) for series in data]

        series = []
        for query, serie in np_data:
            frame = pd.DataFrame(serie[:, 1],
                                 index=serie[:, 0],
                                 columns=[query])
            series.append(frame)
        if len(series) > 0:
            return pd.concat(series, axis=1, join='inner')
        else:
            return None


class RrdRangeQuery(RangeQuery):

    def __init__(self, **kwargs):
        try:
            import rrdtool  # noqa
        except ImportError:
            raise Exception("pip install python-rrdtool")
        super(RrdRangeQuery, self).__init__(**kwargs)
        self.url = kwargs['url']

    def get(self):
        import rrdtool
        result = rrdtool.fetch(self._url(), str(self.queries[0]))

        start, end, step = result[0]
        ds = result[1]
        rows = result[2]
        print(start, end, step)
        print(ds)
        print(rows)
#        return self._process(data)

    def _url(self):
        return str(self.base_url.replace('file://', ''))
