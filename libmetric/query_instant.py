#!/usr/bin/env python

import json
import requests
import rrdtool
import pandas as pd
import numpy as np
import datetime

PROMETHEUS_REPLY = 'Prometheus API replied with error {}: {}'


class InstantQuery(object):
    def __init__(self, **kwargs):
        self.base_url = kwargs['url']
        self.user = kwargs['user']
        self.password = kwargs['password']
        self.queries = kwargs['queries']
        self.moment = kwargs['moment']
        self.verify = False

    def _process(self, data):
        raise NotImplementedError

    def _url(self):
        raise NotImplementedError

    def get(self):
        data = json.loads(requests.get(self._url(), verify=False).text)
        return self._process(data)

    def _http_get_params(self):
        return json.loads(requests.get(self._url(),
                                       params=self._params(),
                                       verify=self.verify).text)

    def _http_get_data(self):
        return json.loads(requests.get(self._url(),
                                       data=json.dumps(self._params()),
                                       verify=self.verify).text)


class GraphiteInstantQuery(InstantQuery):
    def __init__(self, **kwargs):
        super(GraphiteInstantQuery, self).__init__(**kwargs)

    def _url(self):
        params = ["from={}".format(self.start),
                  "until={}".format(self.end)]
        params += ["target={}".format(query) for query in self.queries]
        url = '/render?format=json&{}'.format('&'.join(params))
        return self.base_url + url


class InfluxInstantQuery(InstantQuery):
    def __init__(self, **kwargs):
        super(InfluxInstantQuery, self).__init__(**kwargs)
        self.partition = kwargs['partition']

    def _url(self):
        params = ["q={}".format(query) for query in self.queries]
        if self.user is not None:
            params += ["u={}".format(self.user), "p={}".format(self.password)]
        url = '/query?db={}&epoch=s&{}'.format(self.partition,
                                               '&'.join(params))
        return self.base_url + url


class PrometheusInstantQuery(InstantQuery):

    def __init__(self, **kwargs):
        super(PrometheusInstantQuery, self).__init__(**kwargs)

    def get(self):
        data = self._http_get_params()
        return self._process(data)

    def _params(self):
        return {
            "query": self.queries,
            "time": self.moment
        }

    def _url(self):
        url = '/api/v1/query'
        return self.base_url + url

    def _process(self, response):
        if response['status'] == 'error':
            raise Exception(PROMETHEUS_REPLY.format(response['errorType'],
                                                    response['error']))
        data = response['data']['result']
        for series in data:
            for values in [series['value']]:
                values[0] = pd.Timestamp(datetime.datetime.fromtimestamp(values[0]))
                values[1] = float(values[1])
        np_data = [('{}_{}'.format(series['metric']['__name__'],
                                   series['metric']['instance']),
                                   np.array([series['value']])) for series in data]
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


class RrdInstantQuery(InstantQuery):
    def __init__(self, **kwargs):
        super(RrdInstantQuery, self).__init__(**kwargs)
        self.url = kwargs['url']

    def get(self):
        data = json.loads(requests.get(self._url(), verify=False).text)
        return self._process(data)
