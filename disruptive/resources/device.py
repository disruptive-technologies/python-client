# Project imports.
import disruptive as dt
import disruptive.requests as dtrequests
import disruptive.events as dtevents
import disruptive.errors as dterrors
import disruptive.datas as dtdatas
import disruptive.outputs as dtoutputs


class Device(dtoutputs.OutputBase):

    def __init__(self, device_dict):
        # Inherit from Response parent.
        dtoutputs.OutputBase.__init__(self, device_dict)

        # Unpack device json.
        self.__unpack()

    def __unpack(self):
        self.device_id = self.raw['name'].split('/')[-1]
        self.project_id = self.raw['name'].split('/')[1]
        self.type = self.raw['type']
        self.labels = self.raw['labels']
        self.reported = Reported(self.raw['reported'])

    @classmethod
    def get(cls, project_id: str, device_id: str, auth=None):
        # Construct URL
        url = dt.base_url
        url += '/projects/{}/devices/{}'.format(project_id, device_id)

        # Return simple GET request instance.
        return cls(dtrequests.get(
            url=url,
            auth=auth
        ))

    @classmethod
    def list(cls,
             project_id,
             query=None,
             device_ids=[],
             device_types=[],
             label_filters=[],
             order_by='',
             auth=None):

        # Construct parameters dictionary.
        params = {}
        if query is not None:
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
        devices = dtrequests.auto_paginated_list(
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
        for devices in dtrequests.generator_list(
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
        dtrequests.post(
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
        dtrequests.post(
            url=dt.base_url + '/projects/{}/devices:transfer'.format(
                target_project_id
            ),
            body=body,
            auth=auth,
        )


class Reported(dtoutputs.OutputBase):

    def __init__(self, reported_dict):
        # Inherit parent Event class init.
        dtoutputs.OutputBase.__init__(self, reported_dict)

        # Set default attribute values.
        for key in dtevents.EVENTS_MAP:
            setattr(self, dtevents.EVENTS_MAP[key]['attr'], None)

        # Unpack the reported dictionary data.
        self.__unpack()

    def __unpack(self):
        # Iterate keys in reported dictionary.
        for key in self.raw.keys():
            # Fields can be None on emulated devices. Skip if that is the case.
            if self.raw[key] is None:
                continue

            # Repack the data field in expected format.
            repacked = {key: self.raw[key]}

            # Initialize appropriate data instance.
            data = dtdatas.DataClass.from_event_type(repacked, key)

            # Set attribute according to event type.
            if key in dtevents.EVENTS_MAP:
                setattr(self, dtevents.EVENTS_MAP[key]['attr'], data)
            else:
                raise dterrors.NotFound('Unknown event type {}.'.format(key))
