#!/usr/bin/env python

import click

from libmetric.engine.prometheus import PrometheusQuery
from libmetric.engine.influxdb import InfluxdbQuery
from libmetric.engine.graphite import GraphiteQuery

from libmetric.search import GraphiteSearch, PrometheusSearch, InfluxSearch, RrdSearch
from libmetric.alarm import RangeAlarm, InstantAlarm


@click.command()
@click.option(
    "--engine", default="prometheus", help="Engine [prometheus, graphite, influxdb]"
)
@click.option("--url", default=None, help="Server URL")
@click.option("--user", default=None, help="Authentication username")
@click.option("--password", default=None, help="Authentication password")
@click.option("--partition", default=None, help="Data partition")
@click.option("--query", default=None, help="Time-series query")
@click.option("--start", default=None, help="Time range start")
@click.option("--end", default=None, help="Time range end")
@click.option("--moment", default=None, help="Moment in time")
@click.option("--step", default=None, help="Query resolution step width")
def _libmetric_query(
    engine, url, user, password, partition, query, start, end, moment, step
):

    data = {
        "queries": [query],
        "url": url,
        "user": user,
        "password": password,
        "partition": partition,
        "step": step,
        "start": start,
        "end": end,
        "moment": moment,
    }
    print(data)

    if engine == "prometheus":
        query = PrometheusQuery(**data)
    elif engine == "influxdb":
        query = InfluxdbQuery(**data)
    elif engine == "graphite":
        query = GraphiteQuery(**data)
    else:
        raise Exception("Unsupported engine {}.".format(engine))

    print(query.get())


def libmetric_query():
    _libmetric_query(auto_envvar_prefix="LIBMETRIC")


@click.command()
@click.option(
    "--engine",
    default="prometheus",
    help="Engine [prometheus, elasticsearch, influxdb]",
)
@click.option("--url", default=None, help="Server URL")
@click.option("--user", default=None, help="Authentication username")
@click.option("--password", default=None, help="Authentication password")
@click.option("--partition", default=None, help="Data partition")
@click.option("--query", default=None, help="Time-series query")
@click.option("--start", default=None, help="Time range start")
@click.option("--end", default=None, help="Time range end")
@click.option("--moment", default=None, help="Moment in time")
@click.option("--step", default=None, help="Query resolution step width")
@click.option("--alert-threshold", default=None, help="Threshold value for the alert")
@click.option(
    "--alert-operator", default=None, help="Arithmetic operator for alert evaluation"
)
@click.option("--alert-series", default=None, help="Series to perform alert against")
@click.option(
    "--aggregation", default=None, help="Aggregation function for the given time-series"
)
def _libmetric_alert(
    engine,
    url,
    user,
    password,
    partition,
    query,
    start,
    end,
    moment,
    step,
    alert_operator,
    alert_threshold,
    alert_series,
    aggregation,
):
    data = {
        "queries": [query],
        "url": url,
        "user": user,
        "password": password,
        "partition": partition,
        "step": step,
        "start": start,
        "end": end,
        "moment": moment,
    }

    if engine == "prometheus":
        query = PrometheusRangeQuery(**data)
    elif engine == "influxdb":
        query = InfluxRangeQuery(**data)
    elif engine == "graphite":
        query = GraphiteRangeQuery(**data)
    elif engine == "rrd":
        query = RrdRangeQuery(**data)
    else:
        raise Exception("Unsupported engine {}.".format(engine))

    data_frame = query.get()
    alarm = {
        "alarm_operator": alert_operator,
        "alarm_threshold": alert_threshold,
        "aggregation": aggregation,
        "series": alert_series,
        "data_frame": data_frame,
    }
    result = RangeAlarm(**alarm).evaluate()
    print("{}".format(result))


def libmetric_alert():
    _libmetric_alert(auto_envvar_prefix="LIBMETRIC")


@click.command()
@click.option(
    "--engine",
    default="prometheus",
    help="Engine [prometheus, elasticsearch, influxdb]",
)
@click.option("--url", default=None, help="Server URL")
@click.option("--user", default=None, help="Authentication username")
@click.option("--password", default=None, help="Authentication password")
@click.option("--partition", default=None, help="Data partition")
@click.option("--search", default=None, help="Search time-series")
@click.option("--start", default=None, help="Time range start")
@click.option("--end", default=None, help="Time range end")
def _libmetric_metadata(engine, url, user, password, partition, search, start, end):
    data = {
        "search": [search],
        "url": url,
        "user": user,
        "password": password,
        "partition": partition,
        "start": start,
        "end": end,
    }

    if engine == "prometheus":
        search = PrometheusSearch(**data)
    elif engine == "influxdb":
        search = InfluxSearch(**data)
    elif engine == "graphite":
        search = GraphiteSearch(**data)
    elif engine == "rrd":
        search = RrdSearch(**data)
    else:
        raise Exception("Unsupported engine {}".format(engine))

    print(search.get())


def libmetric_metadata():
    _libmetric_metadata(auto_envvar_prefix="LIBMETRIC")
