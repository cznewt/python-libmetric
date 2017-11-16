
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

    apt-get -y install build-dep python-lxml

Intall library from ``pip`` package.

.. code-block:: bash

    pip install libmetric

Intall library from source.

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
    export LIBMETRIC_URL='https://metric01:15010'
    export LIBMETRIC_QUERY='alertmanager_notifications_total'

    export LIBMETRIC_START='2017-11-12T00:00:00Z'
    export LIBMETRIC_END='2017-11-16T00:00:00Z'
    export LIBMETRIC_STEP='3600s'

    range_meter

And the example of passing parameters as command arguments.

.. code-block:: bash

    export LIBMETRIC_ENGINE='prometheus'
    export LIBMETRIC_URL='https://metric01:15010'
    export LIBMETRIC_QUERY='alertmanager_notifications_total'

    export LIBMETRIC_START='2017-11-12T00:00:00Z'
    export LIBMETRIC_END='2017-11-16T00:00:00Z'
    export LIBMETRIC_STEP='3600s'

    range_meter


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
  Moment in time.


Supported MetaData Endpoints
============================

The ``libmetric`` supports several major time-series databases to get the
results in normalised way. The endpoints are queried thru HTTP API calls.


Graphite
--------


InfluxDB
--------


Prometheus
----------


More Information
================

* https://prometheus.io/docs/prometheus/latest/querying/api/
* http://graphite.readthedocs.io/en/latest/render_api.html
* https://docs.influxdata.com/influxdb/v1.3/guides/querying_data/
