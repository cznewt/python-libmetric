from setuptools import setup, find_packages

VERSION = '0.3.0'

with open('README.rst') as readme:
    LONG_DESCRIPTION = ''.join(readme.readlines())


setup(
    name='libmetric',
    version=VERSION,
    description='Python library for querying metrics into Pandas DataFrames',
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    license='Apache License, Version 2.0',
    url='https://github.com/cznewt/python-libmetric',
    install_requires=[
        'click',
        'requests',
        'pandas',
        'numpy'
    ],
    entry_points='''
[console_scripts]
range_meter=libmetric.cli:range_meter
instant_meter=libmetric.cli:instant_meter
range_alarm=libmetric.cli:range_alarm
instant_alarm=libmetric.cli:instant_alarm
    ''',
)
