import disruptive as dt
import disruptive.requests as req
from disruptive.outputs import OutputBase


class Project(OutputBase):

    def __init__(self, project_dict):
        # Inherit from Response parent.
        OutputBase.__init__(self, project_dict)

        # Unpack organization json.
        self.__unpack()

    @classmethod
    def get(cls, project_id: str, auth=None):
        # Construct URL
        url = dt.base_url
        url += '/projects/{}'.format(project_id)

        # Return simple GET request instance.
        return cls(req.get(
            url=url,
            auth=auth
        ))

    def __unpack(self):
        self.display_name = self.raw['displayName']
        self.organization_id = self.raw['organization'].split('/')[-1]
        self.organization_display_name = self.raw['organizationDisplayName']
        self.sensor_count = self.raw['sensorCount']
        self.cloud_connector_count = self.raw['cloudConnectorCount']
        self.is_inventory = self.raw['inventory']
