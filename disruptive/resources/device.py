from __future__ import annotations

# Standard library imports.
from typing import Optional

# Project imports.
import disruptive as dt
import disruptive.requests as dtrequests
import disruptive.events as dtevents
import disruptive.errors as dterrors
import disruptive.outputs as dtoutputs


class Device(dtoutputs.OutputBase):
    """
    Represents sensors and cloud connectors.

    When a device response is received, the content is
    unpacked and the related attributes are updated.

    Attributes
    ----------
    raw : dict
        Unmodified device response dictionary.
    id : str
        Unique device ID.
    project_id : str
        Project in which the device resides.
    type : str
        Device type.
    labels : dict
        Label keys and values.
    emulated : bool
        True if the device is emulated, otherwise False.
    reported : Reported, None
        Object containing the data from the most recent events.
        If emulated is True, reported is None.

    """

    def __init__(self, device: dict, emulated: bool = False) -> None:
        """
        Constructs the Device object by unpacking the raw device response.

        Parameters
        ----------
        device : dict
            Unmodified device response dictionary.

        """

        # Inherit from OutputBase parent.
        dtoutputs.OutputBase.__init__(self, device)

        # Unpack attributes from dictionary.
        self.id = device['name'].split('/')[-1]
        self.project_id = device['name'].split('/')[1]
        self.type = device['type']
        self.labels = device['labels']
        self.emulated = emulated
        if emulated:
            self.reported = None
        else:
            self.reported = Reported(device['reported'])

    @classmethod
    def get_device(cls,
                   project_id: str,
                   device_id: str,
                   **kwargs,
                   ) -> Device:
        """
        Gets a device specified by its project and ID.

        Parameters
        ----------
        project_id : str
            Unique ID of the target project.
        device_id : str
            Unique ID of the target device.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        device : Device
            Object representing the specified device.

        Examples
        --------
        >>> device = dt.Device.get_device(project_id='...', device_id='...')

        """

        # Construct URL
        url = dt.api_url
        url += '/projects/{}/devices/{}'.format(project_id, device_id)

        # Return Device object of GET request response.
        return cls(dtrequests.generic_request(
            method='GET',
            url=url,
            **kwargs,
        ))

    @classmethod
    def list_devices(cls,
                     project_id: str,
                     query: Optional[str] = None,
                     device_ids: Optional[list[str]] = None,
                     device_types: Optional[list[str]] = None,
                     label_filters: Optional[list[str]] = None,
                     order_by: Optional[str] = None,
                     **kwargs,
                     ) -> list[Device]:
        """
        List all available devices in the specified project.

        Parameters
        ----------
        project_id : str
            Unique ID of the target project.
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
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        page_size: int, optional
            Number of devices [1, 100] to get per request. Defaults to 100.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        devices : list[Device]
            List of objects each representing a device.

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
            url=dt.api_url + '/projects/{}/devices'.format(project_id),
            pagination_key='devices',
            params=params,
            **kwargs,
        )
        return [cls(device) for device in devices]

    @staticmethod
    def batch_update_labels(project_id: str,
                            device_ids: list[str],
                            set_labels: Optional[dict[str, str]] = None,
                            remove_labels: Optional[list[str]] = None,
                            **kwargs,
                            ) -> None:
        """
        Add, update, or remove multiple labels (key=value) on multiple devices

        Must provide either add_labels or remove_labels. If neither are
        provided, a BadRequest error will be raised.

        If a key provided with `add_labels` already exists for a
        device, the value will be updated accordingly.

        Parameters
        ----------
        project_id : str
            Unique ID of target project.
        device_ids : list[str]
            List of unique IDs for the target devices.
        add_labels : dict[str, str], optional
            Key and value of labels to be added / updated.
        remove_labels : list[str], optional
            Label keys to be removed.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        """

        # Construct list of devices.
        name = 'projects/{}/devices/{}'
        devices = [name.format(project_id, xid) for xid in device_ids]

        # Construct request body dictionary.
        body: dict = dict()
        body['devices'] = devices
        if set_labels is not None:
            body['addLabels'] = set_labels
        if remove_labels is not None:
            body['removeLabels'] = remove_labels

        # Construct URL.
        url = dt.api_url
        url += '/projects/{}/devices:batchUpdate'.format(project_id)

        # Sent POST request, but return nothing.
        dtrequests.generic_request(
            method='POST',
            url=url,
            body=body,
            **kwargs,
        )

    @staticmethod
    def set_label(project_id: str,
                  device_id: str,
                  key: str,
                  value: str,
                  **kwargs,
                  ) -> None:
        """
        Add a label (key=value) for a single device.
        If key already exists, the value is updated.

        Parameters
        ----------
        project_id : str
            Unique ID of the target project.
        device_id : str
            Unique ID of the target device.
        key : str
            Label key to be added.
        value : str
            Label value to be added.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        """

        # Use batch_update_labels for safer call.
        Device.batch_update_labels(
            project_id=project_id,
            device_ids=[device_id],
            set_labels={key: value},
            **kwargs,
        )

    @staticmethod
    def remove_label(project_id: str,
                     device_id: str,
                     key: str,
                     **kwargs,
                     ) -> None:
        """
        Remove a label (key=value) from a single device.

        Parameters
        ----------
        project_id : str
            Unique ID of the target project.
        device_id : str
            Unique ID of the target device.
        key : str
            Key of the label to be removed.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        """

        # Use batch_update_labels for safer call.
        Device.batch_update_labels(
            project_id=project_id,
            device_ids=[device_id],
            remove_labels=[key],
            **kwargs,
        )

    @staticmethod
    def transfer_device(source_project_id: str,
                        target_project_id: str,
                        device_ids: list[str],
                        **kwargs,
                        ) -> None:
        """
        Transfer devices from one project to another.

        Parameters
        ----------
        source_project_id : str
            Unique ID of the source project.
        target_project_id : str
            Unique ID of the target project.
        device_ids : list[str]
            List of unique IDs for the target devices.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        """

        # Construct list of devices.
        name = 'projects/{}/devices/{}'
        devices = [name.format(source_project_id, xid) for xid in device_ids]

        # Construct request body dictionary.
        body = {
            "devices": devices
        }

        # Sent POST request, but return nothing.
        dtrequests.generic_request(
            method='POST',
            url=dt.api_url + '/projects/{}/devices:transfer'.format(
                target_project_id
            ),
            body=body,
            **kwargs,
        )


class Reported(dtoutputs.OutputBase):
    """
    Represents the "reported" field for a device.

    Contains one attribute for each event type, initialized to None.
    For each event type represented in the reported field, the related
    attribute is updated with the appropriate EventData child.

    Attributes
    ----------
    raw : dict
        Unmodified dictionary of the "reported" field.
    touch : Touch, None
        Object representing reported touch event data.
    temperature : Temperature, None
        Object representing reported temperature event data.
    object_present : ObjectPresent, None
        Object representing reported objectPresent event data.
    humidity : Humidity, None
        Object representing reported humidity event data.
    object_present_count : ObjectPresentCount, None
        Object representing reported objectPresentCount event data.
    touch_count : TouchCount, None
        Object representing reported touchCount event data.
    water_present : WaterPresent, None
        Object representing reported waterPresent event data.
    network_status : NetworkStatus, None
        Object representing reported networkStatus event data.
    battery_status : BatteryStatus, None
        Object representing reported batteryStatus event data.
    connection_status : ConnectionStatus, None
        Object representing reported connectionStatus event data.
    ethernet_status : EthernetStatus, None
        Object representing reported ethernetStatus event data.
    cellular_status : CellularStatus, None
        Object representing reported cellularStatus event data.

    """

    def __init__(self, reported: dict) -> None:
        """
        Constructs the Reported object by unpacking each event in the field.

        Parameters
        ----------
        reported : dict
            Dictionary of the reported field for a device.

        """

        # Inherit parent Event class init.
        dtoutputs.OutputBase.__init__(self, reported)

        # Set default attribute values.
        for key in dtevents.EVENTS_MAP:
            # Skip labelsChanged as it does not exist in reported.
            if key == 'labelsChanged':
                continue

            # Set attribute to None.
            setattr(self, str(dtevents.EVENTS_MAP[key]['attr']), None)

        # Unpack the reported dictionary data.
        self.__unpack()

    def __unpack(self) -> None:
        """
        Iterates each field in the raw dictionary and set the
        related attribute to the appropriate EventData child object.
        If an event type is not found, the attribute is left as None.

        """

        # Iterate keys in reported dictionary.
        for key in self._raw.keys():
            # Fields can be None on emulated devices. Skip if that is the case.
            if self._raw[key] is None:
                continue

            # Also skip labelsChanged key as it does not exist in reported.
            if key == 'labelsChanged':
                continue

            # Repack the data field in expected format.
            repacked = {key: self._raw[key]}

            # Initialize appropriate data instance.
            data = dtevents.EventData.from_event_type(repacked, key)

            # Set attribute according to event type.
            if key in dtevents.EVENTS_MAP:
                setattr(self, str(dtevents.EVENTS_MAP[key]['attr']), data)
            else:
                raise dterrors.NotFound('Unknown event type {}.'.format(key))
