from __future__ import annotations

# Project imports.
import disruptive as dt
import disruptive.requests as dtrequests
import disruptive.outputs as dtoutputs
from disruptive.authentication import BasicAuth, OAuth


class Organization(dtoutputs.OutputBase):

    def __init__(self, org: dict) -> None:
        # Inherit from Response parent.
        dtoutputs.OutputBase.__init__(self, org)

        # Unpack organization json.
        self.__unpack()

    def __unpack(self) -> None:
        self.organization_id = self.raw['name'].split('/')[-1]
        self.display_name = self.raw['displayName']

    @classmethod
    def get(cls,
            organization_id: str,
            auth: BasicAuth | OAuth | None = None
            ) -> Organization:

        # Construct URL
        url = dt.base_url
        url += '/organizations/{}'.format(organization_id)

        # Return Organization object of GET request response.
        return cls(dtrequests.get(
            url=url,
            auth=auth
        ))

    @classmethod
    def get_list(cls,
                 auth: BasicAuth | OAuth | None = None,
                 ) -> list[Organization]:

        # Return list of Organization objects of paginated GET response.
        orgs = dtrequests.auto_paginated_list(
            url=dt.base_url + '/organizations',
            pagination_key='organizations',
            auth=auth,
        )
        return [cls(org) for org in orgs]
