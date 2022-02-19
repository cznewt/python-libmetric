# Library python-libmetric

Python library for querying metrics from popular time-series databases into
Pandas DataFrames.

It support two types of metric queries, the first is `instant` metric, 
returning the value in precise moment in time. The second is the `range`
metric, giving you the series of values for given time range and step.

## Installation

Install the required dependencies on Debian based systems.

```bash
apt-get -y install librrd-dev libpython-dev
```

Install library from `pip` package.

```bash
pip install libmetric
```

Install library from source.

```bash
git clone https://github.com/cznewt/python-libmetric.git
cd python-libmetric
python setup.py install
```

## Input Parameters

Parameters can be either set by environmental parameters or passed as command
arguments.

For example passing the parameters as environmental parameters.

```bash
export LIBMETRIC_ENGINE='prometheus'
export LIBMETRIC_URL='https://metric01:9090'
export LIBMETRIC_QUERY='alertmanager_notifications_total'

export LIBMETRIC_START='2017-11-12T00:00:00Z'
export LIBMETRIC_END='2017-11-16T00:00:00Z'
export LIBMETRIC_STEP='3600s'

libmetric_query
```

And the example of passing parameters as command arguments.

```bash
libmetric_query --engine prometheus --url 'https://metric01:9090' --query '...'
```

### Common Parameters

**LIBMETRIC_ENGINE**
  Type of the endpoint to make query.

**LIBMETRIC_URL**
  URL of the endpoint service.

**LIBMETRIC_PARTITION**
  Data partition on target service endopoint.

**LIBMETRIC_QUERY**
  Query to get the metric time-series or value.

### Range Query Parameters

Parameters that apply only for the `range` meters.

**LIBMETRIC_START**
  Time range start.

**LIBMETRIC_END**
  Time range end.

**LIBMETRIC_STEP**
  Query resolution step width.

### Instant Query Parameters

Parameters that apply only for the `intant` meters.

**LIBMETRIC_MOMENT**
  Single moment in time.

### Alert Parameters

Parameters that apply only for the all meters/alarms. Except the
`LIBMETRIC_AGGREGATION`  ` is applicable only for `  `range` meters.

**LIBMETRIC_ALARM_THRESHOLD**
  Threshold for the alarms.

**LIBMETRIC_ALARM_OPERATOR**
  Arithmetic operator for alarm evaluation. [gt, lt, gte, lte, eq]

**LIBMETRIC_AGGREGATION**
  Aggregation function for the given time-series [min, max, sum, avg]

## Supported Endpoints

The ``libmetric`` supports several major time-series databases to get the
results in normalised way. The endpoints are queried thru HTTP API calls.

### Graphite

Example configuration to query the Graphite server.

```bash
export LIBMETRIC_ENGINE='graphite'
export LIBMETRIC_URL='http://graphite.host:80'
export LIBMETRIC_QUERY='averageSeries(server.web*.load)'
```

### InfluxDB

Example configuration to query the InfluxDb server.

```bash
export LIBMETRIC_ENGINE='influxdb'
export LIBMETRIC_URL='http://influxdb.host:8086'
export LIBMETRIC_USER='user'
export LIBMETRIC_PASSWORD='password'
export LIBMETRIC_PARTITION='prometheus'
export LIBMETRIC_QUERY='SELECT mean("value") FROM "alertmanager_notifications_total"'
```

### Prometheus

Example configuration to query the Prometheus server.

```bash
export LIBMETRIC_ENGINE='prometheus'
export LIBMETRIC_URL='https://prometheus.host:9090'
export LIBMETRIC_QUERY='alertmanager_notifications_total'
```

### Round-Robin Database (RRD)

Example configuration to query the RRD file. The query is the `consolidation function` and the partition is the `data set`.

```bash
export LIBMETRIC_ENGINE='rrd'
export LIBMETRIC_URL='file:///tmp/port.rrd'
export LIBMETRIC_PARTITION='INOCTETS'
export LIBMETRIC_QUERY='AVERAGE'
```

## Usage from python

```python
from libmetric.engine.prometheus import PrometheusQuery

query = PrometheusQuery(**{
    'queries': ['cpu{metric="load"}'],
    'url': 'http://localhost:9090',
    'step': 3600,
    'start': 1645173343,
    'end': 1645273343
})

print(
  query.get()
)
```

## More Information

* https://prometheus.io/docs/prometheus/latest/querying/api/
* http://graphite.readthedocs.io/en/latest/render_api.html
* https://docs.influxdata.com/influxdb/v1.3/guides/querying_data/
* https://oss.oetiker.ch/rrdtool/doc/rrdtool.en.html
