#!/usr/bin/env python

import click
from libmetric.query import PrometheusRangeQuery, PrometheusInstantQuery, \
    GraphiteRangeQuery, GraphiteInstantQuery 


@click.command()
@click.option('--engine', default='prometheus',
              help="Engine [prometheus, elasticsearch, influxdb]")
@click.option('--url', default=None,
              help="Server URL")
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
def _range_meter(engine, url, partition, query, start, end, step):

    data = {
        'queries': [query],
        'url': url,
        'partition': partition,
        'step': step,
        'start': start,
        'end': end
    }

    if engine == 'prometheus':
        query = PrometheusRangeQuery(**data)
    elif engine == 'graphite':
        query = GraphiteRangeQuery(**data)
    else:
        raise Exception("Unsupported engine {}.".format(engine))

    print query.get()


@click.command()
@click.option('--engine', default='prometheus',
              help="Engine [prometheus, elasticsearch, influxdb]")
@click.option('--url', default=None,
              help="Server URL")
@click.option('--partition', default=None,
              help="Data partition")
@click.option('--query', default=None,
              help="Time-series query")
@click.option('--moment', default=None,
              help="Moment in time")
def _instant_meter(engine, partition, url, query, moment):

    data = {
        'queries': [query],
        'url': url,
        'partition': partition,
        'moment': moment,
    }

    if engine == 'prometheus':
        query = PrometheusInstantQuery(**data)
    elif engine == 'graphite':
        query = GraphiteInstantQuery(**data)
    else:
        raise Exception("Unsupported engine {}.".format(engine))

    print query.get()


def range_meter():
    _range_meter(auto_envvar_prefix='LIBMETRIC')


def instant_meter():
    _instant_meter(auto_envvar_prefix='LIBMETRIC')


def instant_alarm():
    _instant_meter(auto_envvar_prefix='LIBMETRIC')


def range_alarm():
    _range_meter(auto_envvar_prefix='LIBMETRIC')
