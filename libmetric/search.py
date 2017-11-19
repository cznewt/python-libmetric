
import json
import requests
import rrdtool


class Search(object):
    def __init__(self, **kwargs):
        self.base_url = kwargs['url']
        self.user = kwargs['user']
        self.password = kwargs['password']
        self.search = kwargs['search']

    def _url(self):
        raise NotImplementedError

    def _process(self, data):
        raise NotImplementedError

    def get(self):
        data = json.loads(requests.get(self._url(), verify=False).text)
        return self._process(data)


class GraphiteSearch(Search):
    def __init__(self, **kwargs):
        super(GraphiteSearch, self).__init__(**kwargs)

    def _url(self):
        params = ["from={}".format(self.start),
                  "until={}".format(self.end)]
        params += ["target={}".format(search) for search in self.search]
        url = '/render?format=json&{}'.format('&'.join(params))
        return self.base_url + url


class InfluxSearch(Search):
    def __init__(self, **kwargs):
        super(InfluxSearch, self).__init__(**kwargs)
        self.partition = kwargs['partition']

    def _url(self):
        params = ["q={}".format(search) for search in self.search]
        if self.user is not None:
            params += ["u={}".format(self.user), "p={}".format(self.password)]
        url = '/search?db={}&epoch=s&{}'.format(self.partition,
                                                '&'.join(params))
        return self.base_url + url


class PrometheusSearch(Search):
    def __init__(self, **kwargs):
        super(PrometheusSearch, self).__init__(**kwargs)

    def _url(self):
        params = []
        params += ["match[]={}".format(search) for search in self.search]
        if self.start is not None:
            params += ["start={}".format(self.start),
                       "end={}".format(self.end)]
        url = '/api/v1/series?' + '&'.join(params)
        return self.base_url + url

    def _process(self, response):
        print response


class RrdSearch(Search):
    def __init__(self, **kwargs):
        super(RrdSearch, self).__init__(**kwargs)

    def _url(self):
        return str(self.base_url.replace('file://', ''))

    def get(self):
        data_sources = set()
        info = rrdtool.info(self._url())
        for datum, real_value in info.items():
            if datum.startswith('ds'):
                value = datum.replace('ds[', '').split('].')
                # if value[0] not in data_source:
                #     data_source[value[0]] = {}
                # data_source[value[0]][value[1]] = real_value
                data_sources.add(value[0])
        return list(data_sources)
