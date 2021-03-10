

class OutputBase():

    def __init__(self, raw):
        self.raw = raw


class Metric(OutputBase):

    def __init__(self, metric_dict):
        # Inherit attributes from ResponseBase parent.
        OutputBase.__init__(self, metric_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        self.success_count = self.raw['metrics']['successCount']
        self.error_count = self.raw['metrics']['errorCount']
        self.latency = self.raw['metrics']['latency99p']