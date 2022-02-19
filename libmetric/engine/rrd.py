
import rrdtool

class RrdRangeQuery(RangeQuery):

    def __init__(self, **kwargs):
        super(RrdRangeQuery, self).__init__(**kwargs)
        self.url = kwargs['url']

    def get(self):
        result = rrdtool.fetch(self._url(), str(self.queries[0]))

        start, end, step = result[0]
        ds = result[1]
        rows = result[2]
#        return self._process(data)

    def _url(self):
        return str(self.base_url.replace('file://', ''))


class RrdInstantQuery(InstantQuery):
    def __init__(self, **kwargs):
        super(RrdInstantQuery, self).__init__(**kwargs)
        self.url = kwargs['url']

    def get(self):
        data = json.loads(requests.get(self._url(), verify=False).text)
        return self._process(data)
