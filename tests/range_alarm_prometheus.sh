
export LIBMETRIC_ENGINE='prometheus'
export LIBMETRIC_URL='https://metric01:15010'
export LIBMETRIC_QUERY='alertmanager_notifications_total'

export LIBMETRIC_START='2017-11-12T00:00:00Z'
export LIBMETRIC_END='2017-11-16T00:00:00Z'
export LIBMETRIC_STEP='3600s'
export LIBMETRIC_AGGREGATION='avg'

export LIBMETRIC_ALARM_THRESHOLD='500'
export LIBMETRIC_ALARM_OPERATOR='gt'
export LIBMETRIC_ALARM_SERIES='alertmanager_notifications_total_10.0.0.6:9093'

range_alarm
