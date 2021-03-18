# Standard-library imports.
import json

# Project imports.
import disruptive.transforms as dttrans


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


class Member(OutputBase):

    def __init__(self, member):
        # Inherit from Response parent.
        OutputBase.__init__(self, member)

        # Unpack organization json.
        self.__unpack()

    def __unpack(self) -> None:
        self.display_name = self.raw['displayName']
        self.roles = [r.split('/')[-1] for r in self.raw['roles']]
        self.status = self.raw['status']
        self.email = self.raw['email']
        self.account_type = self.raw['accountType']
        self.create_time = dttrans.iso8601_to_datetime(self.raw['createTime'])
