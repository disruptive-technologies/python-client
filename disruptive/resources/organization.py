import disruptive as dt
import disruptive.requests as req
from disruptive.outputs import OutputBase


class Organization(OutputBase):

    def __init__(self, org_dict):
        # Inherit from Response parent.
        OutputBase.__init__(self, org_dict)

        # Unpack organization json.
        self.__unpack()

    def __unpack(self):
        self.display_name = self.raw['displayName']

    @classmethod
    def get(cls, organization_id: str, auth=None):
        # Construct URL
        url = dt.base_url
        url += '/organizations/{}'.format(organization_id)

        # Return simple GET request instance.
        return cls(req.get(
            url=url,
            auth=auth
        ))

    @classmethod
    def list(cls, auth=None):
        # Return paginated GET request instance.
        orgs = req.auto_paginated_list(
            url=dt.base_url + '/organizations',
            pagination_key='organizations',
            auth=auth,
        )
        return [cls(org) for org in orgs]
