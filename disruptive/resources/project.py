# Project imports.
import disruptive as dt
import disruptive.requests as dtrequests
import disruptive.outputs as dtoutputs


class Project(dtoutputs.OutputBase):

    def __init__(self, project_dict):
        # Inherit from Response parent.
        dtoutputs.OutputBase.__init__(self, project_dict)

        # Unpack organization json.
        self.__unpack()

    def __unpack(self):
        self.display_name = self.raw['displayName']
        self.organization_id = self.raw['organization'].split('/')[-1]
        self.organization_display_name = self.raw['organizationDisplayName']
        self.sensor_count = self.raw['sensorCount']
        self.cloud_connector_count = self.raw['cloudConnectorCount']
        self.is_inventory = self.raw['inventory']

    @classmethod
    def get(cls, project_id: str, auth=None):
        # Construct URL.
        url = dt.base_url
        url += '/projects/{}'.format(project_id)

        # Return class instance from GET request response.
        return cls(dtrequests.get(
            url=url,
            auth=auth
        ))

    @classmethod
    def list(cls, organization_id: str = None, query: str = None, auth=None):
        # Construct URL.
        url = dt.base_url + '/projects'

        # Construct parameters dictionary.
        params = {}
        if organization_id is not None:
            params['organization'] = 'organizations/' + organization_id
        if query is not None:
            params['query'] = query

        # Get responses by auto-paginating.
        responses = dtrequests.auto_paginated_list(
            url=url,
            pagination_key='projects',
            params=params,
            auth=auth,
        )

        return [cls(r) for r in responses]

    @classmethod
    def create(cls, organization_id, display_name, auth=None):
        # Construct URL.
        url = dt.base_url + '/projects'

        # Construct request body.
        body = {
            'organization': 'organizations/' + organization_id,
            'displayName': display_name,
        }

        # Send POST request and return Project object of it.
        return cls(dtrequests.post(
            url=url,
            body=body,
            auth=auth,
        ))

    @staticmethod
    def update(project_id, display_name, auth=None):
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
