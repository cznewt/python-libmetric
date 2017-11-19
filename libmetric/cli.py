#!/usr/bin/env python

import click
from libmetric.query_range import (InfluxRangeQuery, GraphiteRangeQuery,
                                   PrometheusRangeQuery, RrdRangeQuery)
from libmetric.query_instant import (InfluxInstantQuery, GraphiteInstantQuery,
                                     PrometheusInstantQuery, RrdInstantQuery)
from libmetric.search import (GraphiteSearch, PrometheusSearch, InfluxSearch,
                              RrdSearch)
from libmetric.alarm import RangeAlarm, InstantAlarm


@click.command()
@click.option('--engine', default='prometheus',
              help="Engine [prometheus, elasticsearch, influxdb]")
@click.option('--url', default=None,
              help="Server URL")
@click.option('--user', default=None,
              help="Authentication username")
@click.option('--password', default=None,
              help="Authentication password")
@click.option('--partition', default=None,
              help="Data partition")
@click.option('--query', default=None,
              help="Time-series query")
@click.option('--start', default=None,
              help="Time range start")
@click.option('--end', default=None,
              help="Time range end")
@click.option('--step', default=None,
              help="Query resolution step width")
def _range_metric(engine, url, user, password, partition, query,
                  start, end, step):
    data = {
        'queries': [query],
        'url': url,
        'user': user,
        'password': password,
        'partition': partition,
        'step': step,
        'start': start,
        'end': end
    }

    if engine == 'prometheus':
        query = PrometheusRangeQuery(**data)
    elif engine == 'influxdb':
        query = InfluxRangeQuery(**data)
    elif engine == 'graphite':
        query = GraphiteRangeQuery(**data)
    elif engine == 'rrd':
        query = RrdRangeQuery(**data)
    else:
        raise Exception("Unsupported engine {}.".format(engine))

    print query.get()


def range_metric():
    _range_metric(auto_envvar_prefix='LIBMETRIC')


@click.command()
@click.option('--engine', default='prometheus',
              help="Engine [prometheus, elasticsearch, influxdb]")
@click.option('--url', default=None,
              help="Server URL")
@click.option('--user', default=None,
              help="Authentication username")
@click.option('--password', default=None,
              help="Authentication password")
@click.option('--partition', default=None,
              help="Data partition")
@click.option('--query', default=None,
              help="Time-series query")
@click.option('--start', default=None,
              help="Time range start")
@click.option('--end', default=None,
              help="Time range end")
@click.option('--step', default=None,
              help="Query resolution step width")
@click.option('--alarm-threshold', default=None,
              help="Threshold value for the alarm")
@click.option('--alarm-operator', default=None,
              help="Arithmetic operator for alarm evaluation")
@click.option('--aggregation', default=None,
              help="Aggregation function for the given time-series")
def _range_alarm(engine, url, user, password, partition, query, start, end,
                 step, alarm_operator, alarm_threshold, aggregation):
    data = {
        'queries': [query],
        'url': url,
        'user': user,
        'password': password,
        'partition': partition,
        'step': step,
        'start': start,
        'end': end
    }

    if engine == 'prometheus':
        query = PrometheusRangeQuery(**data)
    elif engine == 'influxdb':
        query = InfluxRangeQuery(**data)
    elif engine == 'graphite':
        query = GraphiteRangeQuery(**data)
    elif engine == 'rrd':
        query = RrdRangeQuery(**data)
    else:
        raise Exception("Unsupported engine {}.".format(engine))

    time_series = query.get()
    alarm = {
        'alarm_operator': alarm_operator,
        'alarm_threshold': alarm_threshold,
        'aggregation': aggregation,
        'time_series': time_series
    }
    result = RangeAlarm(**alarm).evaluate()
    print result


def range_alarm():
    _range_alarm(auto_envvar_prefix='LIBMETRIC')


@click.command()
@click.option('--engine', default='prometheus',
              help="Engine [prometheus, elasticsearch, influxdb]")
@click.option('--url', default=None,
              help="Server URL")
@click.option('--user', default=None,
              help="Authentication username")
@click.option('--password', default=None,
              help="Authentication password")
@click.option('--partition', default=None,
              help="Data partition")
@click.option('--query', default=None,
              help="Time-series query")
@click.option('--moment', default=None,
              help="Moment in time")
def _instant_metric(engine, url, user, password, partition, query, moment):
    data = {
        'queries': [query],
        'url': url,
        'user': user,
        'password': password,
        'partition': partition,
        'moment': moment,
    }

    if engine == 'prometheus':
        query = PrometheusInstantQuery(**data)
    elif engine == 'influxdb':
        query = InfluxInstantQuery(**data)
    elif engine == 'graphite':
        query = GraphiteInstantQuery(**data)
    elif engine == 'rrd':
        query = RrdInstantQuery(**data)
    else:
        raise Exception("Unsupported engine {}.".format(engine))

    print query.get()


def instant_metric():
    _instant_metric(auto_envvar_prefix='LIBMETRIC')


@click.command()
@click.option('--engine', default='prometheus',
              help="Engine [prometheus, elasticsearch, influxdb]")
@click.option('--url', default=None,
              help="Server URL")
@click.option('--user', default=None,
              help="Authentication username")
@click.option('--password', default=None,
              help="Authentication password")
@click.option('--partition', default=None,
              help="Data partition")
@click.option('--query', default=None,
              help="Time-series query")
@click.option('--start', default=None,
              help="Time range start")
@click.option('--end', default=None,
              help="Time range end")
@click.option('--step', default=None,
              help="Query resolution step width")
@click.option('--alarm-threshold', default=None,
              help="Threshold value for the alarm")
@click.option('--alarm-operator', default=None,
              help="Arithmetic operator for alarm evaluation")
def _instant_alarm(engine, url, user, password, partition, query, start, end,
                   step, alarm_operator, alarm_threshold):
    data = {
        'queries': [query],
        'url': url,
        'user': user,
        'password': password,
        'partition': partition,
        'step': step,
        'start': start,
        'end': end
    }

    if engine == 'prometheus':
        query = PrometheusRangeQuery(**data)
    elif engine == 'influxdb':
        query = InfluxRangeQuery(**data)
    elif engine == 'graphite':
        query = GraphiteRangeQuery(**data)
    elif engine == 'rrd':
        query = RrdRangeQuery(**data)
    else:
        raise Exception("Unsupported engine {}.".format(engine))

    value = query.get()
    alarm = {
        'alarm_operator': alarm_operator,
        'alarm_threshold': alarm_threshold,
        'value': value
    }
    result = InstantAlarm(**alarm).evaluate()
    print result


def instant_alarm():
    _instant_metric(auto_envvar_prefix='LIBMETRIC')


@click.command()
@click.option('--engine', default='prometheus',
              help="Engine [prometheus, elasticsearch, influxdb]")
@click.option('--url', default=None,
              help="Server URL")
@click.option('--user', default=None,
              help="Authentication username")
@click.option('--password', default=None,
              help="Authentication password")
@click.option('--partition', default=None,
              help="Data partition")
@click.option('--search', default=None,
              help="Search time-series")
@click.option('--start', default=None,
              help="Time range start")
@click.option('--end', default=None,
              help="Time range end")
def _search_metrics(engine, url, user, password, partition, search,
                    start, end):
    data = {
        'search': [search],
        'url': url,
        'user': user,
        'password': password,
        'partition': partition,
        'start': start,
        'end': end
    }

    if engine == 'prometheus':
        search = PrometheusSearch(**data)
    elif engine == 'influxdb':
        search = InfluxSearch(**data)
    elif engine == 'graphite':
        search = GraphiteSearch(**data)
    elif engine == 'rrd':
        search = RrdSearch(**data)
    else:
        raise Exception("Unsupported engine {}".format(engine))

    print search.get()


def search_metrics():
    _search_metrics(auto_envvar_prefix='LIBMETRIC')
