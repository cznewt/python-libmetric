
================
python-libmetric
================

Python library for querying metrics from several time-series databases into
Pandas DataFrames.

It support two types of metric queries, the first is ``instant`` metric,
returning the value in precise moment in time. The second is the ``range``
metric, giving you the series of values for given time range and step.


Installation
============

Install the required dependencies on Debian based systems.

.. code-block:: bash

    apt-get -y install librrd-dev libpython-dev

Install library from ``pip`` package.

.. code-block:: bash

    pip install libmetric

Install library from source.

.. code-block:: bash

    git clone https://github.com/cznewt/python-libmetric.git
    cd python-libmetric
    python setup.py install


Input Parameters
================

Parameters can be either set by environmental parameters or passed as command
arguments.

For example passing the parameters as environmental parameters.

.. code-block:: bash

    export LIBMETRIC_ENGINE='prometheus'
    export LIBMETRIC_URL='https://metric01:9090'
    export LIBMETRIC_QUERY='alertmanager_notifications_total'

    export LIBMETRIC_START='2017-11-12T00:00:00Z'
    export LIBMETRIC_END='2017-11-16T00:00:00Z'
    export LIBMETRIC_STEP='3600s'

    range_metric

And the example of passing parameters as command arguments.

.. code-block:: bash

    range_metric --engine prometheus --url 'https://metric01:9090' --query '...'


Common Parameters
-----------------

**LIBMETRIC_ENGINE**
  Type of the endpoint to make query.

**LIBMETRIC_URL**
  URL of the endpoint service.

**LIBMETRIC_PARTITION**
  Data partition on target service endopoint.

**LIBMETRIC_QUERY**
  Query to get the metric time-series or value.


Range Parameters
----------------

Parameters that apply only for the ``range`` meters.

**LIBMETRIC_START**
  Time range start.

**LIBMETRIC_END**
  Time range end.

**LIBMETRIC_STEP**
  Query resolution step width.


Instant Parameters
------------------

Parameters that apply only for the ``intant`` meters.

**LIBMETRIC_MOMENT**
  Single moment in time.


Alarm Parameters
----------------

Parameters that apply only for the all meters/alarms. Except the
``LIBMETRIC_AGGREGATION`` is applicable only for ``range`` meters.

**LIBMETRIC_ALARM_THRESHOLD**
  Threshold for the alarms.

**LIBMETRIC_ALARM_OPERATOR**
  Arithmetic operator for alarm evaluation. [gt, lt, gte, lte, eq]

**LIBMETRIC_AGGREGATION**
  Aggregation function for the given time-series [min, max, sum, avg]


Supported Endpoints
===================

The ``libmetric`` supports several major time-series databases to get the
results in normalised way. The endpoints are queried thru HTTP API calls.


Graphite
--------

Example configuration to query the Graphite server.

.. code-block:: bash

    export LIBMETRIC_ENGINE='graphite'
    export LIBMETRIC_URL='http://graphite.host:80'
    export LIBMETRIC_QUERY='averageSeries(server.web*.load)'
    ...


InfluxDb
--------

Example configuration to query the InfluxDb server.

.. code-block:: bash

    export LIBMETRIC_ENGINE='influxdb'
    export LIBMETRIC_URL='http://influxdb.host:8086'
    export LIBMETRIC_USER='user'
    export LIBMETRIC_PASSWORD='password'
    export LIBMETRIC_PARTITION='prometheus'
    export LIBMETRIC_QUERY='SELECT mean("value") FROM "alertmanager_notifications_total"'
    ...


Prometheus
----------

Example configuration to query the Prometheus server.

.. code-block:: bash

    export LIBMETRIC_ENGINE='prometheus'
    export LIBMETRIC_URL='https://prometheus.host:9090'
    export LIBMETRIC_QUERY='alertmanager_notifications_total'
    ...


Round-Robin Database
--------------------

Example configuration to query the RRD file. The query is the ``consolidation
function`` and the partition is the ``data set``.

.. code-block:: bash

    export LIBMETRIC_ENGINE='rrd'
    export LIBMETRIC_URL='file:///tmp/port.rrd'
    export LIBMETRIC_PARTITION='INOCTETS'
    export LIBMETRIC_QUERY='AVERAGE'
    ...


Alarm Options
=============

Following lists show allowed values for alarm functions, the alarm arithmetic
operators and aggregation function for ``range`` meters.


Supported Alarm Operators
-------------------------

**gt**
  Greater than ``>``.

**gte**
  Greater or equal than ``>=``.

**lt**
  Lower than ``<``.

**lte**
  Lower or equal than ``<=``.

**eq**
  Equals to ``==``.


Supported Time-series Aggregations
----------------------------------

**avg**
  Arithmetic average of the series values.

**min**
  Use the minimal value from series.

**max**
  Use the maximal value from series.

**sum**
  Sum the values together.


More Information
================

* https://prometheus.io/docs/prometheus/latest/querying/api/
* http://graphite.readthedocs.io/en/latest/render_api.html
* https://docs.influxdata.com/influxdb/v1.3/guides/querying_data/
* https://oss.oetiker.ch/rrdtool/doc/rrdtool.en.html
