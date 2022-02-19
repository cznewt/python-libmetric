#!/usr/bin/env python

import json
import requests
import urllib3

urllib3.disable_warnings()


class Query(object):
    def __init__(self, **kwargs):
        pass

    def get(self):
        return self.collector.get()


class InstantQuery(object):
    def __init__(self, **kwargs):
        self.base_url = kwargs["url"]
        self.user = kwargs.get("user", None)
        self.password = kwargs.get("password", None)
        self.queries = kwargs["queries"]
        self.moment = kwargs.get("moment", None)
        self.verify = False

    def _process(self, data):
        raise NotImplementedError

    def _url(self):
        raise NotImplementedError

    def get(self):
        data = json.loads(requests.get(self._url(), verify=False).text)
        return self._process(data)

    def _http_get_params(self):
        return json.loads(
            requests.get(self._url(), params=self._params(), verify=self.verify).text
        )

    def _http_get_data(self):
        return json.loads(
            requests.get(
                self._url(), data=json.dumps(self._params()), verify=self.verify
            ).text
        )


class GraphiteInstantQuery(InstantQuery):
    def __init__(self, **kwargs):
        super(GraphiteInstantQuery, self).__init__(**kwargs)

    def _url(self):
        params = ["from={}".format(self.start), "until={}".format(self.end)]
        params += ["target={}".format(query) for query in self.queries]
        url = "/render?format=json&{}".format("&".join(params))
        return self.base_url + url


class RangeQuery(object):
    def __init__(self, **kwargs):
        self.base_url = kwargs["url"]
        self.user = kwargs.get("user", None)
        self.password = kwargs.get("password")
        self.queries = kwargs["queries"]
        self.start = kwargs["start"]
        self.end = kwargs["end"]
        self.step = kwargs["step"]
        self.verify = False

    def _process(self, data):
        raise NotImplementedError

    def _url(self):
        raise NotImplementedError

    def _http_get_params(self):
        return json.loads(
            requests.get(self._url(), params=self._params(), verify=self.verify).text
        )

    def _http_get_data(self):
        return json.loads(
            requests.get(
                self._url(), data=json.dumps(self._params()), verify=self.verify
            ).text
        )
