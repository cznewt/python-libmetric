import json
import requests


class Search(object):
    def __init__(self, **kwargs):
        self.base_url = kwargs["url"]
        self.user = kwargs["user"]
        self.password = kwargs["password"]
        self.search = kwargs["search"]

    def _url(self):
        raise NotImplementedError

    def _process(self, data):
        raise NotImplementedError

    def get(self):
        data = json.loads(requests.get(self._url(), verify=False).text)
        return self._process(data)
