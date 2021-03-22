from __future__ import annotations

# Standard library imports.
from typing import Generator, Optional

# Project imports.
import disruptive as dt
import disruptive.requests as dtrequests
import disruptive.events as dtevents
import disruptive.errors as dterrors
import disruptive.outputs as dtoutputs
from disruptive.authentication import BasicAuth, OAuth


class Device(dtoutputs.OutputBase):
    """
    Represents sensors and cloud connectors.

    When the REST API endpoint response contains a device object, the
    content is unpacked and set to the related attributes.

    Attributes
    ----------
    raw : dict
        Unmodified device object received from the REST API.
    id : str
        Device ID.
    project_id : str
        Project in which the device resides.
    type : str
        Device type.
    labels : dict
        Label keys and values.
    reported : Reported
        Object containing the data from the most recent events.

    """

    def __init__(self, device: dict) -> None:
        """
        Constructs the Device class by unpacking the raw device object.

        Parameters
        ----------
        device : dict
            Dictionary of device data returned by an endpoint.

        """

        # Inherit from Response parent.
        dtoutputs.OutputBase.__init__(self, device)

        # Unpack attributes from dictionary.
        self.id = self.raw['name'].split('/')[-1]
        self.project_id = self.raw['name'].split('/')[1]
        self.type = self.raw['type']
        self.labels = self.raw['labels']
        self.reported = Reported(self.raw['reported'])

    @classmethod
    def get_device(cls,
                   project_id: str,
                   device_id: str,
                   auth: Optional[BasicAuth | OAuth] = None,
                   ) -> Device:
        """
        Gets a device specified by its project and id.

        Parameters
        ----------
        project_id : str
            Unique project ID.
        device_id : str
            Unique device ID.
        auth: BasicAuth, OAuth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be priotized over global authentication.

        Returns
        -------
        device : Device
            Object representing the specified device.

        """

        # Construct URL
        url = dt.base_url
        url += '/projects/{}/devices/{}'.format(project_id, device_id)

        # Return Device object of GET request response.
        return cls(dtrequests.get(
            url=url,
            auth=auth
        ))

    @classmethod
    def list_devices(cls,
                     project_id: str,
                     query: Optional[str] = None,
                     device_ids: Optional[list[str]] = None,
                     device_types: Optional[list[str]] = None,
                     label_filters: Optional[list[str]] = None,
                     order_by: Optional[str] = None,
                     auth: Optional[BasicAuth | OAuth] = None,
                     ) -> list[Device]:
        """
        Gets a list of devices specified by a project id.

        Parameters
        ----------
        project_id : str
            Unique project ID.
        query : str, optional
            Keyword based search for device display name.
        device_ids : list[str], optional
            Specify devices by their unique IDs.
        device_types : list[str], optional
            Specify devices by type.
        label_filters : list[str], optional
            Specify devices by label keys and values.
            Each entry takes the form "label_key=label_value".
        order_by : str, optional
            The field name you want to order the response by.
            Referred to using dot notation, e.g. reported.temperature.value.
            Default order is ascending, but can be flipped by prefixing a "~".
        auth: BasicAuth, OAuth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be priotized over global authentication.
        """

        # Construct parameters dictionary.
        params: dict = dict()
        if query is not None:
            params['query'] = query
        if device_ids is not None:
            params['device_ids'] = device_ids
        if device_types is not None:
            params['device_types'] = device_types
        if label_filters is not None:
            params['label_filters'] = label_filters
        if order_by is not None:
            params['order_by'] = order_by

        # Return list of Device objects of paginated GET response.
        devices = dtrequests.auto_paginated_list(
            url=dt.base_url + '/projects/{}/devices'.format(project_id),
            pagination_key='devices',
            params=params,
            auth=auth,
        )
        return [cls(device) for device in devices]

    @classmethod
    def generator(cls,
                  project_id: str,
                  page_size: int = 100,
                  auth: Optional[BasicAuth | OAuth] = None,
                  ) -> Generator:
        """
        Gets devices by ;d
        """

        # Construct URL
        url = dt.base_url + '/projects/{}/devices'.format(project_id)

        # Relay generator output, yielding Device objects of response.
        for devices in dtrequests.generator_list(
                url=url,
                pagination_key='devices',
                params={},
                page_size=page_size,
                auth=auth
                ):
            for device in devices:
                yield cls(device)

    @staticmethod
    def batch_update_labels(project_id: str,
                            device_ids: list[str],
                            add_labels: Optional[dict[str, str]] = None,
                            remove_labels: Optional[list[str]] = None,
                            auth: Optional[BasicAuth | OAuth] = None,
                            ) -> None:

        # Construct list of devices.
        name = 'projects/{}/devices/{}'
        devices = [name.format(project_id, xid) for xid in device_ids]

        # Construct request body dictionary.
        body: dict = dict()
        body['devices'] = devices
        if add_labels is not None:
            body['addLabels'] = add_labels
        if remove_labels is not None:
            body['removeLabels'] = remove_labels

        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/devices:batchUpdate'.format(project_id)

        # Sent POST request, but return nothing.
        dtrequests.post(
            url=url,
            body=body,
            auth=auth,
        )

    @staticmethod
    def add_label(project_id: str,
                  device_id: str,
                  key: str,
                  value: str,
                  auth: Optional[BasicAuth | OAuth] = None,
                  ) -> None:

        # Use batch_update_labels for safer call.
        Device.batch_update_labels(
            project_id=project_id,
            device_ids=[device_id],
            add_labels={key: value},
            auth=auth,
        )

    @staticmethod
    def update_label(project_id: str,
                     device_id: str,
                     key: str,
                     value: str,
                     auth: Optional[BasicAuth | OAuth] = None,
                     ) -> None:

        # Use batch_update_labels for safer call.
        Device.batch_update_labels(
            project_id=project_id,
            device_ids=[device_id],
            add_labels={key: value},
            auth=auth,
        )

    @staticmethod
    def remove_label(project_id: str,
                     device_id: str,
                     label: str,
                     auth: Optional[BasicAuth | OAuth] = None,
                     ) -> None:

        # Use batch_update_labels for safer call.
        Device.batch_update_labels(
            project_id=project_id,
            device_ids=[device_id],
            remove_labels=[label],
            auth=auth,
        )

    @staticmethod
    def transfer_device(source_project_id: str,
                        target_project_id: str,
                        device_ids: list[str],
                        auth: Optional[BasicAuth | OAuth] = None,
                        ) -> None:

        # Construct list of devices.
        name = 'projects/{}/devices/{}'
        devices = [name.format(source_project_id, xid) for xid in device_ids]

        # Construct request body dictionary.
        body = {
            "devices": devices
        }

        # Sent POST request, but return nothing.
        dtrequests.post(
            url=dt.base_url + '/projects/{}/devices:transfer'.format(
                target_project_id
            ),
            body=body,
            auth=auth,
        )


class Reported(dtoutputs.OutputBase):

    def __init__(self, reported_dict: dict) -> None:
        # Inherit parent Event class init.
        dtoutputs.OutputBase.__init__(self, reported_dict)

        # Set default attribute values.
        for key in dtevents.EVENTS_MAP:
            setattr(self, str(dtevents.EVENTS_MAP[key]['attr']), None)

        # Unpack the reported dictionary data.
        self.__unpack()

    def __unpack(self) -> None:
        # Iterate keys in reported dictionary.
        for key in self.raw.keys():
            # Fields can be None on emulated devices. Skip if that is the case.
            if self.raw[key] is None:
                continue

            # Repack the data field in expected format.
            repacked = {key: self.raw[key]}

            # Initialize appropriate data instance.
            data = dtevents.DataClass.from_event_type(repacked, key)

            # Set attribute according to event type.
            if key in dtevents.EVENTS_MAP:
                setattr(self, str(dtevents.EVENTS_MAP[key]['attr']), data)
            else:
                raise dterrors.NotFound('Unknown event type {}.'.format(key))
