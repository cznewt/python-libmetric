from libmetric.engine.prometheus import PrometheusQuery
import os

url = os.getenv("LIBMETRIC_URL", "https://prometheus.monlab.newt.cz")

query = PrometheusQuery(
    **{
        "query": "node_load15",
        "url": url,
        "step": 60,
        "start": 1645173343,
        "end": 1645194943,
    }
)

print(query.info)
print(query.data)

query = PrometheusQuery(
    **{
        "query": "node_load15",
        "url": url,
        "step": 120,
        "start": 1645173343,
        "end": 1645194943,
    }
)

print(query.info)
print(query.data)

query = PrometheusQuery(
    **{
        "query": "node_load15",
        "url": url,
        "step": 60,
        "moment": 1645173343,
    }
)

print(query.info)
print(query.data)
