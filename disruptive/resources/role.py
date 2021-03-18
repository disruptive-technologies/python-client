
# Project imports.
import disruptive as dt
import disruptive.requests as dtrequests
from disruptive.outputs import OutputBase


class Role(OutputBase):

    def __init__(self, role: dict) -> None:
        # Inherit from Response parent.
        OutputBase.__init__(self, role)

        # Unpack organization json.
        self.__unpack()

    def __unpack(self) -> None:
        self.role = self.raw['name'].split('/')[-1]
        self.display_name = self.raw['displayName']
        self.description = self.raw['description']
        self.permissions = self.raw['permissions']

    @classmethod
    def list(cls):
        # Return list of Role objects.
        response = dtrequests.auto_paginated_list(
            url=dt.base_url + '/roles',
            pagination_key='roles',
        )
        return [cls(r) for r in response]
