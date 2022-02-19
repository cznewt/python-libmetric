#!/usr/bin/env python

import click

from libmetric.engine.prometheus import PrometheusQuery, PrometheusSearch
from libmetric.engine.influxdb import InfluxdbQuery, InfluxdbSearch
from libmetric.engine.graphite import GraphiteQuery, GraphiteSearch


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
        search = InfluxdbSearch(**data)
    elif engine == "graphite":
        search = GraphiteSearch(**data)
    else:
        raise Exception("Unsupported engine {}".format(engine))

    print(search.get())


def libmetric_metadata():
    _libmetric_metadata(auto_envvar_prefix="LIBMETRIC")
