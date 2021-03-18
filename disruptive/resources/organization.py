from __future__ import annotations

# Standard library imports
from typing import List, Optional, Sequence

# Project imports.
import disruptive as dt
import disruptive.requests as dtrequests
from disruptive.outputs import OutputBase, Member
from disruptive.authentication import BasicAuth, OAuth


class Organization(OutputBase):

    def __init__(self, org: dict) -> None:
        # Inherit from OutputBase parent.
        OutputBase.__init__(self, org)

        # Unpack organization json.
        self.__unpack()

    def __unpack(self) -> None:
        self.id = self.raw['name'].split('/')[-1]
        self.display_name = self.raw['displayName']

    @classmethod
    def get(cls,
            organization_id: str,
            auth: Optional[BasicAuth | OAuth] = None,
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
    def list(cls,
             auth: Optional[BasicAuth | OAuth] = None,
             ) -> List[Organization]:

        # Return list of Organization objects of paginated GET response.
        orgs = dtrequests.auto_paginated_list(
            url=dt.base_url + '/organizations',
            pagination_key='organizations',
            auth=auth,
        )
        return [cls(org) for org in orgs]

    @staticmethod
    def list_members(organization_id: str,
                     auth: Optional[BasicAuth | OAuth] = None,
                     ) -> List[Member]:

        # Construct URL
        url = dt.base_url
        url += '/organizations/{}/members'.format(organization_id)

        # Return list of Member objects of paginated GET response.
        members = dtrequests.auto_paginated_list(
            url=url,
            pagination_key='members',
            auth=auth,
        )
        return [Member(m) for m in members]

    @staticmethod
    def add_member(organization_id: str,
                   email: str,
                   roles: Sequence[str],
                   auth: Optional[BasicAuth | OAuth] = None,
                   ) -> Member:

        # Construct URL
        url = dt.base_url
        url += '/organizations/{}/members'.format(organization_id)

        # Construct request body.
        body: dict = dict()
        body['roles'] = ['roles/' + r for r in roles]
        body['email'] = email

        # Return list of Member objects of paginated GET response.
        return Member(dtrequests.post(
            url=url,
            body=body,
            auth=auth,
        ))

    @staticmethod
    def get_member(organization_id: str,
                   member_id: str,
                   auth: Optional[BasicAuth | OAuth] = None,
                   ) -> Member:

        # Construct URL
        url = dt.base_url
        url += '/organizations/{}/members/{}'.format(
            organization_id,
            member_id,
        )

        # Return list of Member objects of paginated GET response.
        return Member(dtrequests.get(
            url=url,
            auth=auth,
        ))

    @staticmethod
    def remove_member(organization_id: str,
                      member_id: str,
                      auth: Optional[BasicAuth | OAuth] = None,
                      ) -> None:

        # Construct URL
        url = dt.base_url
        url += '/organizations/{}/members/{}'.format(
            organization_id,
            member_id,
        )

        # Send DELETE reuqest, but return nothing.
        dtrequests.delete(
            url=url,
            auth=auth,
        )

    @staticmethod
    def get_member_invite_url(organization_id: str,
                              member_id: str,
                              auth: Optional[BasicAuth | OAuth] = None,
                              ) -> None:

        # Construct URL
        url = dt.base_url
        url += '/organizations/{}/members/{}'.format(
            organization_id,
            member_id,
        ) + ':getInviteUrl'

        # Send DELETE reuqest, but return nothing.
        return dtrequests.get(
            url=url,
            auth=auth,
        )['inviteUrl']
