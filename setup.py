from setuptools import setup, find_packages

version = '0.1.0'

setup(
    name='libmetric',
    version=version,
    description='Python library for querying metrics into Pandas DataFrames',
    packages=find_packages(),
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
