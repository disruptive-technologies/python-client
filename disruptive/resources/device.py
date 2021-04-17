from __future__ import annotations

# Standard library imports.
from typing import Optional

# Project imports.
import disruptive.log as dtlog
import disruptive.requests as dtrequests
import disruptive.events.events as dtevents
import disruptive.outputs as dtoutputs


class Device(dtoutputs.OutputBase):
    """
    Represents sensors and cloud connectors.

    When a device response is received, the content is
    unpacked and the related attributes are updated.

    Attributes
    ----------
    device_id : str
        Unique device ID.
    project_id : str
        Project in which the device resides.
    display_name : str, None
        Given device name if set through a label with key `name`.
        Otherwise None.
    type : str
        Device type.
    labels : dict
        Label keys and values.
    is_emulator : bool
        True if the device is an emulator, otherwise False.
    reported : Reported, None
        Object containing the data from the most recent events.

    """

    def __init__(self, device: dict) -> None:
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
        self.device_id = device['name'].split('/')[-1]
        self.project_id = device['name'].split('/')[1]
        self.type = device['type']
        self.labels = device['labels']

        # Set display_name if `name` label key exists.
        self.display_name = None
        if 'name' in self.labels:
            self.display_name = self.labels['name']

        # Determine if the device is an emulator by checking id prefix.
        if self.device_id.startswith('emu'):
            self.is_emulator = True
        else:
            self.is_emulator = False

        # If it exists, set the reported object.
        self.reported = None
        if 'reported' in device:
            self.reported = Reported(device['reported'])

    @classmethod
    def get_device(cls,
                   device_id: str,
                   project_id: Optional[str] = None,
                   **kwargs,
                   ) -> Device:
        """
        Gets a device specified by its project and ID.

        Parameters
        ----------
        device_id : str
            Unique ID of the target device.
        project_id : str, optional
            Unique ID of the target project.
            If this is not provided, a wildcard project will be used, resulting
            in a search for the device through all available projects.
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
        >>> device = dt.Device.get_device(project_id, device_id)

        """

        if project_id is None:
            project_id = '-'

        # Construct URL
        url = '/projects/{}/devices/{}'.format(project_id, device_id)

        # Return Device object of GET request response.
        return cls(dtrequests.DTRequest.get(url, **kwargs))

    @classmethod
    def list_devices(cls,
                     project_id: str,
                     query: Optional[str] = None,
                     device_ids: Optional[list[str]] = None,
                     device_types: Optional[list[str]] = None,
                     label_filters: Optional[dict[str, str]] = None,
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
        label_filters : dict[str, str], optional
            Specify devices by label keys and values (i.e. {"key": "value"}).
            If a key is provided and value is set as an empty
            string (i.e. {"key": ""}), all device with that key is fetched.
        order_by : str, optional
            The field name you want to order the response by.
            Referred to using dot notation, e.g. reported.temperature.value.
            Default order is ascending, but can be flipped by prefixing a "~".
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
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
        if order_by is not None:
            params['order_by'] = order_by

        # Convert label_filters dictionary to list of strings.
        if label_filters is not None:
            labels_list = []
            for key in label_filters:
                labels_list.append(key + '=' + label_filters[key])
            params['label_filters'] = labels_list

        # Return list of Device objects of paginated GET response.
        devices = dtrequests.DTRequest.paginated_get(
            url='/projects/{}/devices'.format(project_id),
            pagination_key='devices',
            params=params,
            **kwargs,
        )
        return [cls(device) for device in devices]

    @staticmethod
    def batch_update_labels(device_ids: list[str],
                            project_id: str,
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
        device_ids : list[str]
            List of unique IDs for the target devices.
        project_id : str
            Unique ID of target project.
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
        url = '/projects/{}/devices:batchUpdate'.format(project_id)

        # Sent POST request, but return nothing.
        dtrequests.DTRequest.post(url, body=body, **kwargs)

    @staticmethod
    def set_label(device_id: str,
                  project_id: str,
                  key: str,
                  value: str,
                  **kwargs,
                  ) -> None:
        """
        Add a label (key=value) for a single device.
        If key already exists, the value is updated.

        Parameters
        ----------
        device_id : str
            Unique ID of the target device.
        project_id : str
            Unique ID of the target project.
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

        # Construct URL.
        url = '/projects/{}/devices:batchUpdate'.format(project_id)

        # Construct request body dictionary.
        body: dict = dict()
        body['devices'] = ['projects/' + project_id + '/devices/' + device_id]
        body['addLabels'] = {key: value}

        # Sent POST request, but return nothing.
        dtrequests.DTRequest.post(url, body=body, **kwargs)

    @staticmethod
    def remove_label(device_id: str,
                     project_id: str,
                     key: str,
                     **kwargs,
                     ) -> None:
        """
        Remove a label (key=value) from a single device.

        Parameters
        ----------
        device_id : str
            Unique ID of the target device.
        project_id : str
            Unique ID of the target project.
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

        # Construct URL.
        url = '/projects/{}/devices:batchUpdate'.format(project_id)

        # Construct request body dictionary.
        body: dict = dict()
        body['devices'] = ['projects/' + project_id + '/devices/' + device_id]
        body['removeLabels'] = [key]

        # Sent POST request, but return nothing.
        dtrequests.DTRequest.post(url, body=body, **kwargs)

    @staticmethod
    def transfer_devices(device_ids: list[str],
                         source_project_id: str,
                         target_project_id: str,
                         **kwargs,
                         ) -> None:
        """
        Transfer devices from one project to another.

        Parameters
        ----------
        device_ids : list[str]
            List of unique IDs for the target devices.
        source_project_id : str
            Unique ID of the source project.
        target_project_id : str
            Unique ID of the target project.
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
        dtrequests.DTRequest.post(
            url='/projects/{}/devices:transfer'.format(
                target_project_id
            ),
            body=body,
            **kwargs,
        )


class Reported(dtoutputs.OutputBase):
    """
    Represents the "reported" field for a device.

    Contains one attribute for each event type, initialized to None.
    For each event type represented in the reported field,
    the related attribute is updated with the
    appropriate :ref:`Event Data <Event Data>` class.

    Attributes
    ----------
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
        for key in dtevents._EVENTS_MAP._api_names:
            # Skip labelsChanged as it does not exist in reported.
            if key == 'labelsChanged':
                continue

            # Set attribute to None.
            setattr(self, dtevents._EVENTS_MAP._api_names[key].attr_name, None)

        # Unpack the reported dictionary data.
        self.__unpack()

    def __unpack(self) -> None:
        """
        Iterates each field in the raw dictionary and set the
        related attribute to the appropriate _EventData child object.
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
            data = dtevents._EventData.from_event_type(repacked, key)

            # Set attribute according to event type.
            if key in dtevents._EVENTS_MAP._api_names:
                setattr(
                    self,
                    dtevents._EVENTS_MAP._api_names[key].attr_name,
                    data,
                )
            else:
                dtlog.log('Skipping unknown event type {}.'.format(key))
