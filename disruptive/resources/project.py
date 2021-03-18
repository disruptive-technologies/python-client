from __future__ import annotations

# Standard library imports.
from typing import List, Optional, Sequence

# Project imports.
import disruptive as dt
import disruptive.requests as dtrequests
from disruptive.outputs import OutputBase, Member
from disruptive.authentication import BasicAuth, OAuth


class Project(OutputBase):

    def __init__(self, project: dict) -> None:
        # Inherit from Response parent.
        OutputBase.__init__(self, project)

        # Unpack organization json.
        self.__unpack()

    def __unpack(self) -> None:
        self.id = self.raw['name'].split('/')[-1]
        self.display_name = self.raw['displayName']
        self.organization_id = self.raw['organization'].split('/')[-1]
        self.organization_display_name = self.raw['organizationDisplayName']
        self.sensor_count = self.raw['sensorCount']
        self.cloud_connector_count = self.raw['cloudConnectorCount']
        self.is_inventory = self.raw['inventory']

    @classmethod
    def get(cls,
            project_id: str,
            auth: Optional[BasicAuth | OAuth] = None
            ) -> Project:

        # Construct URL.
        url = dt.base_url
        url += '/projects/{}'.format(project_id)

        # Return Project object of GET request response.
        return cls(dtrequests.get(
            url=url,
            auth=auth
        ))

    @classmethod
    def list(cls,
             organization_id: Optional[str] = None,
             query: Optional[str] = None,
             auth: Optional[BasicAuth | OAuth] = None
             ) -> List[Project]:

        # Construct URL.
        url = dt.base_url + '/projects'

        # Construct parameters dictionary.
        params = {}
        if organization_id is not None:
            params['organization'] = 'organizations/' + organization_id
        if query is not None:
            params['query'] = query

        # Return list of Project objects of paginated GET response.
        responses = dtrequests.auto_paginated_list(
            url=url,
            pagination_key='projects',
            params=params,
            auth=auth,
        )
        return [cls(r) for r in responses]

    @classmethod
    def create(cls,
               organization_id: str,
               display_name: str,
               auth: Optional[BasicAuth | OAuth] = None
               ) -> Project:

        # Construct URL.
        url = dt.base_url + '/projects'

        # Construct request body.
        body = {
            'organization': 'organizations/' + organization_id,
            'displayName': display_name,
        }

        # Return Project object of POST request response.
        return cls(dtrequests.post(
            url=url,
            body=body,
            auth=auth,
        ))

    @staticmethod
    def update(project_id: str,
               display_name: str,
               auth: Optional[BasicAuth | OAuth] = None
               ) -> None:

        # Construct URL.
        url = dt.base_url + '/projects/' + project_id

        # Construct request body.
        body = {}
        if display_name is not None:
            body['displayName'] = display_name

        # Send PATCH request, but return nothing.
        dtrequests.patch(
            url=url,
            body=body,
            auth=auth,
        )

    @staticmethod
    def delete(project_id: str,
               auth: Optional[BasicAuth | OAuth] = None
               ) -> None:

        # Construct URL.
        url = dt.base_url + '/projects/' + project_id

        # Send DELETE request, but return nothing.
        dtrequests.delete(
            url=url,
            auth=auth,
        )

    @staticmethod
    def list_members(project_id: str,
                     auth: Optional[BasicAuth | OAuth] = None,
                     ) -> List[Member]:

        # Construct URL
        url = dt.base_url
        url += '/projects/{}/members'.format(project_id)

        # Return list of Member objects of paginated GET response.
        members = dtrequests.auto_paginated_list(
            url=url,
            pagination_key='members',
            auth=auth,
        )
        return [Member(m) for m in members]

    @staticmethod
    def add_member(project_id: str,
                   email: str,
                   roles: Sequence[str],
                   auth: Optional[BasicAuth | OAuth] = None,
                   ) -> Member:

        # Construct URL
        url = dt.base_url
        url += '/projects/{}/members'.format(project_id)

        # Construct request body.
        body: dict = dict()
        body['roles'] = ['roles/' + r for r in roles]
        body['email'] = email

        # Return Member object of POST request response.
        return Member(dtrequests.post(
            url=url,
            body=body,
            auth=auth,
        ))

    @staticmethod
    def get_member(project_id: str,
                   member_id: str,
                   auth: Optional[BasicAuth | OAuth] = None,
                   ) -> Member:

        # Construct URL
        url = dt.base_url
        url += '/projects/{}/members/{}'.format(
            project_id,
            member_id,
        )

        # Return Member object of GET request response.
        return Member(dtrequests.get(
            url=url,
            auth=auth,
        ))
