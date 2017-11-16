
export LIBMETRIC_ENGINE='graphite'
export LIBMETRIC_URL='http://metric02:80'
export LIBMETRIC_QUERY='averageSeries(server.web*.load)'

export LIBMETRIC_START='2017-11-12T00:00:00Z'
export LIBMETRIC_END='2017-11-16T00:00:00Z'
export LIBMETRIC_STEP='3600s'

range_meter
