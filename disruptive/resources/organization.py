import disruptive as dt
import disruptive.requests as req
from disruptive.responses import ResponseBase


class Organization(ResponseBase):

    def __init__(self, org_dict):
        # Inherit from Response parent.
        ResponseBase.__init__(self, org_dict)

        # Unpack organization json.
        self.__unpack()

    def __unpack(self):
        self.display_name = self.raw['displayName']

    @classmethod
    def get(cls, organization_id: str, auth=None):
        # Construct endpoint url
        url = dt.base_url
        url += '/organizations/{}'.format(organization_id)

        # Return simple GET request instance.
        return cls(req.get(
            endpoint=url,
            auth=auth
        ))

    @classmethod
    def list(cls, auth=None):
        # Return paginated GET request instance.
        orgs = req.auto_paginated_list(
            endpoint=dt.base_url + '/organizations',
            pagination_key='organizations',
            auth=auth,
        )
        return [cls(org) for org in orgs]
