#!/usr/bin/env python

import json
import requests
import rrdtool
import pandas as pd
import numpy as np


PROMETHEUS_REPLY = 'Prometheus API replied with error {}: {}'


class RangeQuery(object):
    def __init__(self, **kwargs):
        self.base_url = kwargs['url']
        self.user = kwargs['user']
        self.password = kwargs['password']
        self.queries = kwargs['queries']
        self.start = kwargs['start']
        self.end = kwargs['end']
        self.step = kwargs['step']

    def _url(self):
        raise NotImplementedError

    def _process(self, data):
        raise NotImplementedError

    def get(self):
        data = json.loads(requests.get(self._url(), verify=False).text)
        return self._process(data)


class GraphiteRangeQuery(RangeQuery):
    def __init__(self, **kwargs):
        super(GraphiteRangeQuery, self).__init__(**kwargs)

    def _url(self):
        params = ["target={}".format(query) for query in self.queries]
        params += ["from={}".format(self.start),
                   "until={}".format(self.end)]
        url = '/render?format=json&{}'.format('&'.join(params))
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

    def _url(self):
        params = ["q={}".format(query) for query in self.queries]
        if self.user is not None:
            params += ["u={}".format(self.user), "p={}".format(self.password)]
        url = '/query?db={}&epoch=s&{}'.format(self.partition, '&'.join(params))
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

    def _url(self):
        params = ["query={}".format(query) for query in self.queries]
        params += ["start={}".format(self.start),
                   "end={}".format(self.end),
                   "step={}".format(self.step)]
        url = '/api/v1/query_range?{}'.format('&'.join(params))
        return self.base_url + url

    def _process(self, response):
        if response['status'] == 'error':
            raise Exception(PROMETHEUS_REPLY.format(response['errorType'],
                                                    response['error']))
        data = response['data']['result']
        np_data = [('{}_{}'.format(series['metric']['__name__'],
                                   series['metric']['instance']),
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
        super(RrdRangeQuery, self).__init__(**kwargs)
        self.url = kwargs['url']

    def _url(self):
        return str(self.base_url.replace('file://', ''))

    def get(self):
        result = rrdtool.fetch(self._url(), str(self.queries[0]))

        start, end, step = result[0]
        ds = result[1]
        rows = result[2]
        print start, end, step
        print ds
        print rows

#        return self._process(data)
