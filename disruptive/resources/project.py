from __future__ import annotations

# Project imports.
import disruptive as dt
import disruptive.requests as dtrequests
import disruptive.outputs as dtoutputs
from disruptive.authentication import BasicAuth, OAuth


class Project(dtoutputs.OutputBase):

    def __init__(self, project: dict) -> None:
        # Inherit from Response parent.
        dtoutputs.OutputBase.__init__(self, project)

        # Unpack organization json.
        self.__unpack()

    def __unpack(self) -> None:
        self.display_name = self.raw['displayName']
        self.organization_id = self.raw['organization'].split('/')[-1]
        self.organization_display_name = self.raw['organizationDisplayName']
        self.sensor_count = self.raw['sensorCount']
        self.cloud_connector_count = self.raw['cloudConnectorCount']
        self.is_inventory = self.raw['inventory']

    @classmethod
    def get(cls,
            project_id: str,
            auth: BasicAuth | OAuth | None = None
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
    def get_list(cls,
                 organization_id: str = '',
                 query: str = '',
                 auth: BasicAuth | OAuth | None = None
                 ) -> list[Project]:

        # Construct URL.
        url = dt.base_url + '/projects'

        # Construct parameters dictionary.
        params = {}
        if len(organization_id) > 0:
            params['organization'] = 'organizations/' + organization_id
        if len(query) > 0:
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
               auth: BasicAuth | OAuth | None = None
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
               auth: BasicAuth | OAuth | None = None
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
               auth: BasicAuth | OAuth | None = None
               ) -> None:

        # Construct URL.
        url = dt.base_url + '/projects/' + project_id

        # Send DELETE request, but return nothing.
        dtrequests.delete(
            url=url,
            auth=auth,
        )
