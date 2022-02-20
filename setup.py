# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

VERSION = '0.6.3'

with open('README.md') as readme:
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
        'Jinja2',
        'urllib3',
        'requests',
        'pandas',
        'numpy',
        'elasticsearch-dsl'
    ],
    entry_points='''
[console_scripts]
libmetric_query=libmetric.cli:libmetric_query
    ''',
)
