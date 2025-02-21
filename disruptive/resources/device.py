from __future__ import annotations

import warnings
from typing import Any, Optional

import disruptive.logging as dtlog
import disruptive.outputs as dtoutputs
import disruptive.requests as dtrequests
from disruptive.errors import LabelUpdateError, TransferDeviceError
from disruptive.events import events


class Device(dtoutputs.OutputBase):
    """
    Represents Sensors and Cloud Connectors, together referred to as devices.

    When a device response is received, the content is
    unpacked and the related attributes are set.

    Attributes
    ----------
    device_id : str
        Unique device ID.
    project_id : str
        Project in which the device resides.
    display_name : str, None
        Given device name if set through a label with key `name`.
        Otherwise None.
    device_type : str
        :ref:`Device type <device_type_constants>`.
    product_number : str
        The product number of the device.
    labels : dict
        Label keys and values.
    is_emulated : bool
        True if the device is emulated, otherwise False.
    reported : Reported
        Object containing the data from the most recent events.
    raw : dict[str, str]
        Unmodified API response JSON.

    """

    # Constants for the various device types.
    TEMPERATURE: str = "temperature"
    PROXIMITY: str = "proximity"
    TOUCH: str = "touch"
    HUMIDITY: str = "humidity"
    PROXIMITY_COUNTER: str = "proximityCounter"
    TOUCH_COUNTER: str = "touchCounter"
    WATER_DETECTOR: str = "waterDetector"
    CLOUD_CONNECTOR: str = "ccon"
    CO2: str = "co2"
    MOTION: str = "motion"
    DESK_OCCUPANCY: str = "deskOccupancy"
    CONTACT: str = "contact"
    DEVICE_TYPES = [
        TEMPERATURE,
        PROXIMITY,
        TOUCH,
        HUMIDITY,
        PROXIMITY_COUNTER,
        TOUCH_COUNTER,
        WATER_DETECTOR,
        CLOUD_CONNECTOR,
        CO2,
        MOTION,
        DESK_OCCUPANCY,
        CONTACT,
    ]

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
        self.device_id: str = device["name"].split("/")[-1]
        self.project_id: str = device["name"].split("/")[1]
        self.device_type: str = device["type"]
        self.labels: dict = device["labels"]

        # Set display_name if `name` label key exists.
        self.display_name: str | None = None
        if "name" in self.labels:
            self.display_name = self.labels["name"]

        # Determine if the device is an emulator by checking id prefix.
        self.is_emulated: bool = False
        if self.device_id.startswith("emu") and len(self.device_id) == 23:
            self.is_emulated = True

        # If it exists, set the product number.
        # This is not present for emulated devices.
        self.product_number: str = ""
        if "productNumber" in device:
            self.product_number = device["productNumber"]

        # If it exists, set the reported object.
        self.reported: Reported | None = None
        if "reported" in device:
            self.reported = Reported(device["reported"])

    @classmethod
    def get_device(
        cls,
        device_id: str,
        project_id: Optional[str] = None,
        **kwargs: Any,
    ) -> Device:
        """
        Gets the current state of a single device.

        Parameters
        ----------
        device_id : str
            Unique ID of the target device.
        project_id : str, optional
            Unique ID of the target project.
            If not provided, a wildcard project will be used, resulting
            in a search for the device through all available projects.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        device : Device
            Object representing the target device.

        Examples
        --------
        >>> # Fetch a single device.
        >>> device = dt.Device.get_device('<DEVICE_ID>')

        """

        # If project_id is not given, use wildcard "-".
        if project_id is None:
            project_id = "-"

        # Construct URL
        url = "/projects/{}/devices/{}".format(project_id, device_id)

        # Return Device object of GET request response.
        return cls(dtrequests.DTRequest.get(url, **kwargs))

    @classmethod
    def list_devices(
        cls,
        project_id: str,
        query: Optional[str] = None,
        device_ids: Optional[list[str]] = None,
        device_types: Optional[list[str]] = None,
        label_filters: Optional[dict[str, str]] = None,
        order_by: Optional[str] = None,
        organization_id: Optional[str] = None,
        project_ids: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> list[Device]:
        """
        Gets a list of devices from either a project or
        projects in an organization.

        Parameters
        ----------
        project_id : str
            Either a unique ID of the target project, or
            wildcard `"-"` to list devices from all projects
            in an organization. If `"-"` is provided, the
            parameter `organization_id` must be set.
        query : str, optional
            Keyword-based device search device type, labels, and identifiers.
            Does not provide additional capabilities over setting explicit
            parameters available in this method.
        device_ids : list[str], optional
            Specify devices by their unique IDs.
        device_types : list[str], optional
            Filter by :ref:`device types <device_type_constants>`.
        label_filters : dict[str, str], optional
            Specify devices by label keys and values (i.e. {"key": "value"}).
            If only a key is provided (i.e. {"key": ""}), all
            device with that key is fetched.
        order_by : str, optional
            The field name you want to order the response by.
            Referred to using dot notation (i.e. "reported.temperature.value").
            Default order is ascending, but can be flipped by prefixing "-".
        organization_id : str, optional
            Unique ID of the target organization.
            Required if `project_id` is wildcard `"-"`.
            Ignored if `project_id` is unique project ID.
        project_ids : list[str], optional
            Filter by a list of project IDs.
            Optional if `project_id` is wildcard `"-"`.
            Ignored if `project_id` is unique project ID.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        devices : list[Device]
            List of objects each representing a device.

        Examples
        --------
        >>> # List all devices in a project.
        >>> devices = dt.Device.list_devices(
        ...     project_id='<PROJECT_ID>',
        ... )

        >>> # List all devices in an organization.
        >>> devices = dt.Device.list_devices(
        ...     project_id='-',
        ...     organization_id='<ORGANIZATION_ID>',
        ... )

        >>> # List all touch, temperature, and proximity sensors
        >>> # in a project that has both the labels "room-number"
        >>> # and "external-id" set to spesific values, then
        >>> # sort by their most recent touch event time.
        >>> devices = dt.Device.list_devices(
        ...     project_id=PROJECT_ID,
        ...     device_types=[
        ...         dt.Device.TOUCH,
        ...         dt.Device.TEMPERATURE,
        ...         dt.Device.PROXIMITY,
        ...     ],
        ...     label_filters={
        ...         'room-number': '99',
        ...         'external-id': '55E21B',
        ...     },
        ...     order_by='reported.touch.updateTime',
        ... )

        """

        # Enforce organization_id if project_id is wildcard.
        if project_id == "-" and organization_id is None:
            raise ValueError(
                "Parameter `organization_id` is required when "
                '`project_id` is wildcard `"-"`.'
            )

        # Warn about unsupported combination of parameters.
        if project_id != "-" and organization_id is not None:
            warnings.warn(
                "Parameter `organization_id` is ignored when "
                '`project_id` is not wildcard "-".',
                UserWarning,
            )
        if project_id != "-" and project_ids is not None:
            warnings.warn(
                "Parameter `project_ids` is ignored when "
                '`project_id` is not wildcard "-".',
                UserWarning,
            )

        params: dict = dict()
        if query is not None:
            params["query"] = query
        if device_ids is not None:
            params["device_ids"] = device_ids
        if device_types is not None:
            params["device_types"] = device_types
        if order_by is not None:
            params["order_by"] = order_by
        if organization_id is not None:
            params["organization"] = "organizations/" + organization_id
        if project_ids is not None:
            params["projects"] = ["projects/" + xid for xid in project_ids]

        # Convert label_filters dictionary to list of strings.
        if label_filters is not None:
            labels_list = []
            for key in label_filters:
                labels_list.append(key + "=" + label_filters[key])
            params["label_filters"] = labels_list

        # Return list of Device objects of paginated GET response.
        devices = dtrequests.DTRequest.paginated_get(
            url=f"/projects/{project_id}/devices",
            pagination_key="devices",
            params=params,
            **kwargs,
        )
        return [cls(device) for device in devices]

    @staticmethod
    def transfer_devices(
        device_ids: list[str],
        source_project_id: str,
        target_project_id: str,
        **kwargs: Any,
    ) -> list[TransferDeviceError]:
        """
        Transfers all specified devices to the target project.

        The caller must have the permissions of either `project.admin` or
        `organization.admin` in both the source- and target project.

        Parameters
        ----------
        device_ids : list[str]
            Unique IDs for the devices to transfer.
        source_project_id : str
            Unique ID of the source project.
        target_project_id : str
            Unique ID of the target project.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        errors : list[TransferDeviceError]
            A list that contains one error object for each device that
            could not be successfully transferred.

        Examples
        --------
        >>> # Transfer a device from one project to another.
        >>> err = dt.Device.transfer_devices(
        ...     device_ids=[
        ...         '<DEVICE_ID_1>',
        ...         '<DEVICE_ID_2>',
        ...     ],
        ...     source_project_id='<SOURCE_PROJECT_ID>',
        ...     target_project_id='<TARGET_PROJECT_ID>',
        ... )

        """

        # Construct list of devices.
        name = "projects/{}/devices/{}"
        devices = [name.format(source_project_id, xid) for xid in device_ids]

        # Construct request body dictionary.
        body = {"devices": devices}

        # Sent POST request.
        response = dtrequests.DTRequest.post(
            url="/projects/{}/devices:transfer".format(target_project_id),
            body=body,
            **kwargs,
        )

        # Return any transferErrors found in response.
        return [TransferDeviceError(err) for err in response["transferErrors"]]

    @staticmethod
    def set_label(
        device_id: str,
        project_id: str,
        key: str,
        value: str,
        **kwargs: Any,
    ) -> list[LabelUpdateError]:
        """
        Set a label key and value for a single device.

        If a label key already exists, the value is updated.

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
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        errors : list[LabelUpdateError]
            A list that contains one error object for each label that
            could not be successfully updated.

        Examples
        --------
        >>> # Add a new `room-number` label to a device.
        >>> err = dt.Device.set_label(
        ...     device_id='<DEVICE_ID>',
        ...     project_id='<PROJECT_ID>',
        ...     key='room-number',
        ...     value='99',
        ... )

        """

        # Construct URL.
        url = "/projects/{}/devices:batchUpdate".format(project_id)

        # Construct request body dictionary.
        body: dict = dict()
        body["devices"] = ["projects/" + project_id + "/devices/" + device_id]
        body["addLabels"] = {key: value}

        # Sent POST request.
        response = dtrequests.DTRequest.post(url, body=body, **kwargs)

        # Return any batchErrors found in response.
        return [LabelUpdateError(err) for err in response["batchErrors"]]

    @staticmethod
    def remove_label(
        device_id: str,
        project_id: str,
        key: str,
        **kwargs: Any,
    ) -> list[LabelUpdateError]:
        """
        Remove a label (key and value) from a single device.

        Parameters
        ----------
        device_id : str
            Unique ID of the target device.
        project_id : str
            Unique ID of the target project.
        key : str
            Key of the label to be removed.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        errors : list[LabelUpdateError]
            A list that contains one error object for each label that
            could not be successfully updated.

        Examples
        --------
        >>> # Remove the `room-number` label from a device.
        >>> dt.Device.remove_label(
        ...     device_id='<DEVICE_ID>',
        ...     project_id='<PROJECT_ID>',
        ...     key='room-number',
        ... )

        """

        # Construct URL.
        url = "/projects/{}/devices:batchUpdate".format(project_id)

        # Construct request body dictionary.
        body: dict = dict()
        body["devices"] = ["projects/" + project_id + "/devices/" + device_id]
        body["removeLabels"] = [key]

        # Sent POST request.
        response = dtrequests.DTRequest.post(url, body=body, **kwargs)

        # Return any batchErrors found in response.
        return [LabelUpdateError(err) for err in response["batchErrors"]]

    @staticmethod
    def batch_update_labels(
        device_ids: list[str],
        project_id: str,
        set_labels: Optional[dict[str, str]] = None,
        remove_labels: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> list[LabelUpdateError]:
        """
        Add, update, or remove multiple labels (key and value)
        on multiple devices

        Must provide either `set_labels` or `remove_labels`. If neither are
        provided, a :ref:`BadRequest <bad_request_error>` error will be raised.

        Parameters
        ----------
        device_ids : list[str]
            List of unique IDs for the target devices.
        project_id : str
            Unique ID of target project.
        set_labels : dict[str, str], optional
            Key and value of labels to be added. If a label key
            already exists, the value is updated.
        remove_labels : list[str], optional
            Label keys to be removed.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        errors : list[LabelUpdateError]
            A list that contains one error object for each label that
            could not be successfully updated.

        Raises
        ------
        BadRequest
            If neither `set_labels` nor `remove_labels` is provided.

        Examples
        --------
        >>> # Add 3 new and remove 2 old labels for a few devices.
        >>> err = dt.Device.batch_update_labels(
        ...     device_ids=[
        ...         '<DEVICE_1>',
        ...         '<DEVICE_2>',
        ...         '<DEVICE_3>',
        ...     ],
        ...     project_id='<PROJECT_ID>',
        ...     set_labels={
        ...         'room-number': '99',
        ...         'group': 'favorite',
        ...         'alias': 'cookies',
        ...     },
        ...     remove_labels=[
        ...         'external-id',
        ...         'old-tag',
        ...     ],
        ... )

        """

        # Construct list of devices.
        name = "projects/{}/devices/{}"
        devices = [name.format(project_id, xid) for xid in device_ids]

        # Construct request body dictionary.
        body: dict = dict()
        body["devices"] = devices
        if set_labels is not None:
            body["addLabels"] = set_labels
        if remove_labels is not None:
            body["removeLabels"] = remove_labels

        # Construct URL.
        url = "/projects/{}/devices:batchUpdate".format(project_id)

        # Sent POST request.
        response = dtrequests.DTRequest.post(url, body=body, **kwargs)

        # Return any batchErrors found in response.
        return [LabelUpdateError(err) for err in response["batchErrors"]]


class Reported(dtoutputs.OutputBase):
    """
    Represents the most recent :ref:`Event Data <eventdata>` of
    each type for a single :ref:`Device <device>`.
    If an event type has never been emitted or is not available to
    the device type, the related attribute is `None`.

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
    co2 : Co2, None
        Object representing reported co2 event data.
    pressure : Pressure, None
        Object representing reported pressure event data.
    motion : Motion, None
        Object representing reported motion event data.
    desk_occupancy : DeskOccupancy, None
        Object representing reported deskOccupancy event data.
    contact : Contact, None
        Object representing reported contact event data.
    probe_wire_status : ProbeWireStatus, None
        Object representing reported probeWireStatus event data.

    """

    touch: events.Touch | None = None
    temperature: events.Temperature | None = None
    object_present: events.ObjectPresent | None = None
    humidity: events.Humidity | None = None
    object_present_count: events.ObjectPresentCount | None = None
    touch_count: events.TouchCount | None = None
    water_present: events.WaterPresent | None = None
    network_status: events.NetworkStatus | None = None
    battery_status: events.BatteryStatus | None = None
    connection_status: events.ConnectionStatus | None = None
    ethernet_status: events.EthernetStatus | None = None
    cellular_status: events.CellularStatus | None = None
    co2: events.Co2 | None = None
    pressure: events.Pressure | None = None
    motion: events.Motion | None = None
    desk_occupancy: events.DeskOccupancy | None = None
    contact: events.Contact | None = None
    probe_wire_status: events.ProbeWireStatus | None = None

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

            # Repack the data field in expected format.
            repacked = {key: self._raw[key]}

            # Check if key exists in map of known events.
            if key in events._EVENTS_MAP._api_names:
                # Initialize appropriate data instance.
                data = events._EventData.from_event_type(repacked, key)

                # Set attribute according to event type.
                setattr(
                    self,
                    events._EVENTS_MAP._api_names[key].attr_name,
                    data,
                )
            else:
                dtlog.warning("Skipping unknown reported type {}.".format(key))
