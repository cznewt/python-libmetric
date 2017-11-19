

class InstantAlarm(object):
    def __init__(self, **kwargs):
        self.alarm_operator = kwargs['alarm_operator']
        self.alarm_threshold = kwargs['alarm_threshold']
        self.value = kwargs['value']

    def evaluate(self):
        if self.alarm_operator == 'gt':
            response = (self.alarm_threshold > self.value)
        elif self.alarm_operator == 'gte':
            response = (self.alarm_threshold >= self.value)
        elif self.alarm_operator == 'lt':
            response = (self.alarm_threshold < self.value)
        elif self.alarm_operator == 'lte':
            response = (self.alarm_threshold <= self.value)
        elif self.alarm_operator == 'eq':
            response = (self.alarm_threshold == self.value)
        return response


class RangeAlarm(object):
    def __init__(self, **kwargs):
        self.alarm_operator = kwargs['alarm_operator']
        self.alarm_threshold = kwargs['alarm_threshold']
        self.time_series = kwargs['time_series']
        self.aggregation = kwargs['aggregation']

    def evaluate(self):
        self.value = self.time_series[-1]
        if self.alarm_operator == 'gt':
            response = (self.alarm_threshold > self.value)
        elif self.alarm_operator == 'gte':
            response = (self.alarm_threshold >= self.value)
        elif self.alarm_operator == 'lt':
            response = (self.alarm_threshold < self.value)
        elif self.alarm_operator == 'lte':
            response = (self.alarm_threshold <= self.value)
        elif self.alarm_operator == 'eq':
            response = (self.alarm_threshold == self.value)
        return response
