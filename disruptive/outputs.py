# Standard-library imports.
import json


class OutputBase():

    def __init__(self, raw: dict) -> None:
        self.raw = raw

    def pprint(self, n: int = 4) -> None:
        print(json.dumps(self.raw, indent=n))


class Metric(OutputBase):

    def __init__(self, metric: dict) -> None:
        # Inherit attributes from ResponseBase parent.
        OutputBase.__init__(self, metric)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self) -> None:
        self.success_count = self.raw['metrics']['successCount']
        self.error_count = self.raw['metrics']['errorCount']
        self.latency = self.raw['metrics']['latency99p']
