import disruptive as dt
import disruptive.requests as req
from disruptive.outputs import Metric


class Dataconnector():

    def __init__(self, dataconnector_dict):
        # Inherit everything from Response parent.
        self.raw = dataconnector_dict

        # Unpack device json.
        self.__unpack()

    @classmethod
    def get(cls, project_id, dataconnector_id, auth=None):
        # Construct URL
        url = dt.base_url
        url += '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)

        # Return simple GET request instance.
        return cls(req.get(
            url=url,
            auth=auth
        ))

    @classmethod
    def list(cls, project_id):
        # Return paginated GET request instance.
        devices = req.auto_paginated_list(
            url=dt.base_url + '/projects/{}/dataconnectors'.format(project_id),
            pagination_key='dataConnectors',
        )
        return [cls(device) for device in devices]

    @classmethod
    def create(cls,
               project_id,
               url,
               display_name=None,
               status='ACTIVE',
               events=[],
               http_type='HTTP_PUSH',
               signature_secret=None,
               headers={},
               labels=[],
               auth=None,
               ):
        # Construct request body dictionary.
        body = {
            'type': http_type,
            'status': status,
            'events': [],
            'labels': labels,
            'httpConfig': {
                'url': url,
                'headers': {}
            }
        }
        if display_name is not None:
            body['displayName'] = display_name
        if signature_secret is not None:
            body['httpConfig']['signatureSecret'] = signature_secret

        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/dataconnectors'.format(project_id)

        # Send POST request to API.
        return cls(req.post(
            url=url,
            body=body,
            auth=auth,
        ))

    @classmethod
    def update(cls,
               project_id,
               dataconnector_id,
               display_name=None,
               status=None,
               events=None,
               labels=None,
               url=None,
               signature_secret=None,
               headers=None,
               auth=None,
               ):
        # Construct request body dictionary.
        body = {'httpConfig': {}}
        if display_name is not None:
            body['displayName'] = display_name
        if status is not None:
            body['status'] = status
        if events is not None:
            body['events'] = events
        if labels is not None:
            body['labels'] = labels
        if url is not None:
            body['httpConfig']['url'] = url
        if signature_secret is not None:
            body['httpConfig']['signatureSecret'] = signature_secret
        if headers is not None:
            body['headers'] = headers

        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)

        # Send POST request to API.
        return cls(req.patch(
            url=url,
            body=body,
            auth=auth,
        ))

    @classmethod
    def delete(cls, project_id, dataconnector_id, auth=None):
        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)

        # Send DELETE request to API.
        req.delete(
            url=url,
            auth=auth,
        )

    @classmethod
    def metrics(cls, project_id, dataconnector_id, auth=None):
        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)
        url += ':metrics'

        # Send GET request to API.
        return Metric(req.get(
            url=url,
            auth=auth,
        ))

    @classmethod
    def sync(cls, project_id, dataconnector_id, auth=None):
        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)
        url += ':sync'

        # Send GET request to API.
        return req.post(
            url=url,
            auth=auth,
        )

    def __unpack(self):
        self.id = self.raw['name'].split('/')[-1]
        self.type = self.raw['type']
        self.status = self.raw['status']
        self.display_name = self.raw['displayName']
