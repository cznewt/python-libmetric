# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

VERSION = '0.6.0'

with open('README.rst') as readme:
    LONG_DESCRIPTION = ''.join(readme.readlines())

setup(
    name='libmetric',
    version=VERSION,
    description='Python library for querying metrics into Pandas DataFrames',
    long_description=LONG_DESCRIPTION,
    author='Aleš Komárek',
    author_email='ales.komarek@newt.cz',
    packages=find_packages(),
    license='Apache License, Version 2.0',
    url='https://github.com/cznewt/python-libmetric',
    install_requires=[
        'click',
        'urllib3==1.21.1',
        'requests',
        'pandas',
        'numpy',
        'elasticsearch-dsl'
    ],
    entry_points='''
[console_scripts]
search_metrics=libmetric.cli:search_metrics
range_metric=libmetric.cli:range_metric
instant_metric=libmetric.cli:instant_metric
range_alarm=libmetric.cli:range_alarm
instant_alarm=libmetric.cli:instant_alarm
    ''',
)
