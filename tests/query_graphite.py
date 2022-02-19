

from libmetric.engine.prometheus import PrometheusQuery
import os

query = os.getenv('LIBMETRIC_URL', 'http://metric:80')
url = os.getenv('LIBMETRIC_QUERY', 'averageSeries(server.web*.load)')

data = {
    'queries': [query],
    'url': url,
    'step': 60,
    'start': 1645173343,
    'end': 1645194943
}

query = PrometheusQuery(**data)

print(data)
print(query.get())

data = {
    'queries': [query],
    'url': url,
    'step': 60,
    'moment': 1645173343,
}

query = PrometheusQuery(**data)

print(data)
print(query.get())