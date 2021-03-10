import disruptive as dt
import disruptive.requests as req
from disruptive.outputs import OutputBase


class Device(OutputBase):

    def __init__(self, device_dict):
        # Inherit from Response parent.
        OutputBase.__init__(self, device_dict)

        # Unpack device json.
        self.__unpack()

    @classmethod
    def get(cls, project_id: str, device_id: str, auth=None):
        # Construct URL
        url = dt.base_url
        url += '/projects/{}/devices/{}'.format(project_id, device_id)

        # Return simple GET request instance.
        return cls(req.get(
            url=url,
            auth=auth
        ))

    @classmethod
    def list(cls,
             project_id,
             query='',
             device_ids=[],
             device_types=[],
             label_filters=[],
             order_by='',
             auth=None):

        # Construct parameters dictionary.
        params = {}
        if len(query) > 0:
            params['query'] = query
        if len(device_ids) > 0:
            params['device_ids'] = device_ids
        if len(device_types) > 0:
            params['device_types'] = device_types
        if len(label_filters) > 0:
            params['label_filters'] = label_filters
        if len(order_by) > 0:
            params['order_by'] = order_by

        # Return paginated GET request instance.
        devices = req.auto_paginated_list(
            url=dt.base_url + '/projects/{}/devices'.format(project_id),
            pagination_key='devices',
            params=params,
            auth=auth,
        )
        return [cls(device) for device in devices]

    @classmethod
    def generator(cls, project_id, page_size=100, auth=None):
        # Construct URL
        url = dt.base_url + '/projects/{}/devices'.format(project_id)

        # Relay generator output, converting the responses to Device instances.
        for devices in req.generator_list(
                url,
                'devices',
                {},
                page_size,
                auth=auth
                ):
            yield [cls(device) for device in devices]

    @staticmethod
    def batch_update_labels(
                project_id,
                device_ids,
                add_labels={},
                remove_keys=[],
                auth=None):

        # Construct list of devices.
        name = 'projects/{}/devices/{}'
        devices = [name.format(project_id, xid) for xid in device_ids]

        # Construct request body dictionary.
        body = {
            'devices': devices,
            'addLabels': add_labels,
            'removeLabels': remove_keys,
        }

        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/devices:batchUpdate'.format(project_id)

        # Send POST request to API.
        req.post(
            url=url,
            body=body,
            auth=auth,
        )

    @staticmethod
    def set_label(project_id, device_id, key, value, auth=None):
        Device.batch_update_labels(
            project_id=project_id,
            device_ids=[device_id],
            add_labels={key: value},
            auth=auth,
        )

    @staticmethod
    def update_label(project_id, device_id, key, value, auth=None):
        Device.batch_update_labels(
            project_id=project_id,
            device_ids=[device_id],
            add_labels={key: value},
            auth=auth,
        )

    @staticmethod
    def remove_label(project_id, device_id, key, auth=None):
        Device.batch_update_labels(
            project_id=project_id,
            device_ids=[device_id],
            remove_keys=[key],
            auth=auth,
        )

    @staticmethod
    def transfer(source_project_id, target_project_id, device_ids, auth=None):
        # Construct list of devices.
        name = 'projects/{}/devices/{}'
        devices = [name.format(source_project_id, xid) for xid in device_ids]

        # Construct request body dictionary.
        body = {
            "devices": devices
        }

        # Send POST request to API.
        req.post(
            url=dt.base_url + '/projects/{}/devices:transfer'.format(
                target_project_id
            ),
            body=body,
            auth=auth,
        )

    def __unpack(self):
        self.id = self.raw['name'].split('/')[-1]
        self.type = self.raw['type']
