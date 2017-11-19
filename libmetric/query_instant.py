#!/usr/bin/env python

import json
import requests
import rrdtool
import pandas as pd
import numpy as np

PROMETHEUS_REPLY = 'Prometheus API replied with error {}: {}'


class InstantQuery(object):
    def __init__(self, **kwargs):
        self.base_url = kwargs['url']
        self.user = kwargs['user']
        self.password = kwargs['password']
        self.queries = kwargs['queries']
        self.moment = kwargs['moment']

    def _url(self):
        raise NotImplementedError

    def _process(self, data):
        raise NotImplementedError

    def get(self):
        data = json.loads(requests.get(self._url(), verify=False).text)
        return self._process(data)


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

    def _url(self):
        params = []
        params += ["query={}".format(query) for query in self.queries]
        params += ["time={}".format(self.moment)]
        url = '/api/v1/query?' + '&'.join(params)
        return self.base_url + url

    def _process(self, response):
        if response['status'] == 'error':
            raise Exception(PROMETHEUS_REPLY.format(response['errorType'],
                                                    response['error']))

class RrdInstantQuery(InstantQuery):
    def __init__(self, **kwargs):
        super(RrdInstantQuery, self).__init__(**kwargs)
        self.url = kwargs['url']

    def get(self):
        data = json.loads(requests.get(self._url(), verify=False).text)
        return self._process(data)
