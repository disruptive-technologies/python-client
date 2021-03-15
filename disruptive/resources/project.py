import disruptive as dt
import disruptive.requests as dtrequests
import disruptive.outputs as dtoutputs


class Project(dtoutputs.OutputBase):

    def __init__(self, project_dict):
        # Inherit from Response parent.
        dtoutputs.OutputBase.__init__(self, project_dict)

        # Unpack organization json.
        self.__unpack()

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
    def list(cls):
        # Construct URL.
        url = dt.base_url + '/projects'

        # Get responses by auto-paginating.
        responses = dtrequests.auto_paginated_list(
            url=url,
            pagination_key='projects',
        )

        return [cls(r) for r in responses]

    def __unpack(self):
        self.display_name = self.raw['displayName']
        self.organization_id = self.raw['organization'].split('/')[-1]
        self.organization_display_name = self.raw['organizationDisplayName']
        self.sensor_count = self.raw['sensorCount']
        self.cloud_connector_count = self.raw['cloudConnectorCount']
        self.is_inventory = self.raw['inventory']
