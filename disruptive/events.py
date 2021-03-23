from __future__ import annotations

from typing import Type

# Project imports.
import disruptive.transforms as dttrans
import disruptive.outputs as dtoutputs
import disruptive.log as dtlog


class EventData(dtoutputs.OutputBase):
    """
    Parent class for all the different event data field types.

    Attributes are mainly inherited from OutputBase, and otherwise
    contains a few convenience methods for setting the correct child.

    """

    def __init__(self, data: dict) -> None:
        """
        Constructs the EventData object by inheriting parent.

        """

        # Inherit parent Event class init.
        dtoutputs.OutputBase.__init__(self, data)

    @classmethod
    def from_event_type(cls, data: dict, event_type: str):
        """
        Constructs the appropriate child class from the provided event type.

        Parameters
        ----------
        data : dict
            Dictionary of the data field found in the source event.
        event_type : str
            The event type of the source event.

        """

        # From the type, select the appropriate child class.
        child, key = cls.__child_map(event_type)

        # Return None at invalid event type.
        if child is None:
            return None

        # Return the initialized class instance.
        if key:
            return child(data[event_type])
        else:
            # Special case for labelsChanged event.
            return child(data)

    @staticmethod
    def __child_map(event_type: str):
        """
        Based on provided event type, returns the
        child class and supporting information.

        Parameters
        ----------
        event_type : str
            The event type of the source event.

        """

        # Initialize the correct object.
        if event_type in EVENTS_MAP:
            out = (
                EVENTS_MAP[event_type]['class'],
                EVENTS_MAP[event_type]['is_keyed'],
            )
            return out
        else:
            dtlog.log('Skipping unknown event type {}.'.format(event_type))
            return None, None


class Touch(EventData):
    """
    Represents the data found in a touch event.

    Attributes
    ----------
    raw : dict
        Unmodified touch event data dictionary.

    """

    def __init__(self, data: dict):
        # Inherit parent Event class init.
        EventData.__init__(self, data)


class Temperature(EventData):
    """
    Represents the data found in a temperature event.

    Attributes
    ----------
    raw : dict
        Unmodified temperature event data dictionary.
    temperature : float
        Temperature in degress Celsius.

    """

    def __init__(self, data: dict):
        # Inherit parent Event class init.
        EventData.__init__(self, data)

        # Unpack attributes from dictionary.
        self.temperature = self.raw['value']


class ObjectPresent(EventData):
    """
    Represents the data found in an objectPresent event.

    Attributes
    ----------
    raw : dict
        Unmodified objectPresent event data dictionary.
    state : str
        Whether the event reported PRESENT or NOT_PRESENT.

    """

    def __init__(self, data: dict):
        # Inherit parent Event class init.
        EventData.__init__(self, data)

        # Unpack attributes from dictionary.
        self.state = self.raw['state']


class Humidity(EventData):
    """
    Represents the data found in an humidity event.

    Attributes
    ----------
    raw : dict
        Unmodified humidity event data dictionary.
    temperature : float
        Temperature in degress Celsius.
    humidity : int
        Relative humidity percentage.

    """

    def __init__(self, data: dict):
        # Inherit parent Event class init.
        EventData.__init__(self, data)

        # Unpack attributes from dictionary.
        self.temperature = self.raw['temperature']
        self.humidity = self.raw['relativeHumidity']


class ObjectPresentCount(EventData):
    """
    Represents the data found in an objectPresentCount event.

    Attributes
    ----------
    raw : dict
        Unmodified objectPresentCount event data dictionary.
    total : int
        Total number of times the sensor has detected the appearance
        or disappearance of an object over its lifetime.

    """

    def __init__(self, data: dict):
        # Inherit parent Event class init.
        EventData.__init__(self, data)

        # Unpack attributes from dictionary.
        self.total = self.raw['total']


class TouchCount(EventData):
    """
    Represents the data found in an touchCount event.

    Attributes
    ----------
    raw : dict
        Unmodified touchCount event data dictionary.
    total : int
        The total number of times the sensor
        has been touched over its lifetime.

    """

    def __init__(self, data: dict):
        # Inherit parent Event class init.
        EventData.__init__(self, data)

        # Unpack attributes from dictionary.
        self.total = self.raw['total']


class WaterPresent(EventData):
    """
    Represents the data found in an waterPresent event.

    Attributes
    ----------
    raw : dict
        Unmodified waterPresent event data dictionary.
    state : str
        Indicates whether water is PRESENT or NOT_PRESENT.

    """

    def __init__(self, data: dict):
        # Inherit parent Event class init.
        EventData.__init__(self, data)

        # Unpack attributes from dictionary.
        self.state = self.raw['state']


class NetworkStatus(EventData):
    """
    Represents the data found in a networkStatus event.

    Attributes
    ----------
    raw : dict
        Unmodified networkStatus event data dictionary.
    signal_strength : int
        Percentage signal strength of the strongest Cloud Connector.
    rssi : float
        RSSI of the strongest Cloud Connector.
    transmission_mode : str
        Indicates whether the sensor is in
        LOW_POWER_STANDARD_MODE or HIGH_POWER_BOOST_MODE.
    cloud_connectors : list[str]
        Lists the ID of the Cloud Connector that relayed the event.

    """

    def __init__(self, data: dict):
        """
        Constructs the NetworkStatus object by unpacking the raw response.

        """

        # Inherit parent Event class init.
        EventData.__init__(self, data)

        # Unpack attributes from dictionary.
        self.signal_strength = self.raw['signalStrength']
        self.rssi = self.raw['rssi']
        self.transmission_mode = self.raw['transmissionMode']
        self.cloud_connectors = []
        for ccon in self.raw['cloudConnectors']:
            self.cloud_connectors.append({
                'id': ccon['id'],
                'signalStrength': ccon['signalStrength'],
                'rssi': ccon['rssi'],
            })


class BatteryStatus(EventData):
    """
    Represents the data found in a batteryStatus event.

    Attributes
    ----------
    raw : dict
        Unmodified networkStatus event data dictionary.
    percentage : int
        Percentage estimate of remaining battery.

    """

    def __init__(self, data: dict):
        """
        Constructs the BatteryStatus object by unpacking the raw response.

        """

        # Inherit parent Event class init.
        EventData.__init__(self, data)

        # Unpack attributes from dictionary.
        self.percentage = self.raw['percentage']


class LabelsChanged(EventData):
    """
    Represents the data found in an labelsChanged event.

    Attributes
    ----------
    raw : dict
        Unmodified waterPresent event data dictionary.
    added : dict[str, str]
        Keys and values of new labels added.
    modified : dict[str, str]
        New keys and values of modified labels.
    removed : list[str]
        List of keys of removed labels.

    """

    def __init__(self, data: dict):
        # Inherit parent Event class init.
        EventData.__init__(self, data)

        # Unpack attributes from dictionary.
        self.added = self.raw['added']
        self.modified = self.raw['modified']
        self.removed = self.raw['removed']


class ConnectionStatus(EventData):
    """
    Represents the data found in a connectionStatus event.

    Attributes
    ----------
    raw : dict
        Unmodified connectionStatus event data dictionary.
    connection : str
        Whether the Cloud Connector is on ETHERNET, CELLULAR, or OFFLINE.
    available : str
        Lists available connections. Can contain ETHERNET, CELLULAR, or both.

    """

    def __init__(self, data: dict):
        # Inherit parent Event class init.
        EventData.__init__(self, data)

        # Unpack attributes from dictionary.
        self.connection = self.raw['connection']
        self.available = self.raw['available']


class EthernetStatus(EventData):
    """
    Represents the data found in a ethernetStatus event.

    Attributes
    ----------
    raw : dict
        Unmodified connectionStatus event data dictionary.
    mac_address : str
        MAC address of the local network interface.
    ip_address : str
        IP address of the Cloud Connector on the local network.

    """

    def __init__(self, data: dict):
        # Inherit parent Event class init.
        EventData.__init__(self, data)

        # Unpack attributes from dictionary.
        self.mac_address = self.raw['macAddress']
        self.ip_address = self.raw['ipAddress']


class CellularStatus(EventData):
    """
    Represents the data found in a cellularStatus event.

    Attributes
    ----------
    raw : dict
        Unmodified connectionStatus event data dictionary.
    signal_strength : int
        Cloud Connector cellular reception percentage.

    """

    def __init__(self, data: dict):
        # Inherit parent Event class init.
        EventData.__init__(self, data)

        # Unpack attributes from dictionary.
        self.signal_strength = self.raw['signalStrength']


# This dictionary is created to bridge the three different naming conventions
# used for every single event. The REST API returns events with camel case,
# whereas in python we prefer snake casing, and classes fully cased. It also
# prevent recreating long if-statements when choosing an event by type as it
# lists all event-types currently known.
EVENTS_MAP = {
    'touch': {
        'attr': 'touch',
        'class': Touch,
        'is_keyed': True,
    },
    'temperature': {
        'attr': 'temperature',
        'class': Temperature,
        'is_keyed': True,
    },
    'objectPresent': {
        'attr': 'object_present',
        'class': ObjectPresent,
        'is_keyed': True,
    },
    'humidity': {
        'attr': 'humidity',
        'class': Humidity,
        'is_keyed': True,
    },
    'objectPresentCount': {
        'attr': 'object_present_count',
        'class': ObjectPresentCount,
        'is_keyed': True,
    },
    'touchCount': {
        'attr': 'touch_count',
        'class': TouchCount,
        'is_keyed': True,
    },
    'waterPresent': {
        'attr': 'water_present',
        'class': WaterPresent,
        'is_keyed': True,
    },
    'networkStatus': {
        'attr': 'network_status',
        'class': NetworkStatus,
        'is_keyed': True,
    },
    'batteryStatus': {
        'attr': 'battery_status',
        'class': BatteryStatus,
        'is_keyed': True,
    },
    'labelsChanged': {
        'attr': 'labels_changed',
        'class': LabelsChanged,
        'is_keyed': False,
    },
    'connectionStatus': {
        'attr': 'connection_status',
        'class': ConnectionStatus,
        'is_keyed': True,
    },
    'ethernetStatus': {
        'attr': 'ethernet_status',
        'class': EthernetStatus,
        'is_keyed': True,
    },
    'cellularStatus': {
        'attr': 'cellular_status',
        'class': CellularStatus,
        'is_keyed': True,
    },
}


class Event(dtoutputs.OutputBase):
    """
    Represents device events.

    Attributes
    ----------
    raw : dict
        Unmodified event response dictionary.
    id : str
        Unique event ID.
    type : str
        Event type.
    device_id : str
        Unique ID of the source device.
    project_id : str
        Unique ID of the source project.
    data : :ref:`Event Data`
        An object representing type-specific event data.
    timestamp : datetime
        Timestamp of when the event was received by a Cloud Connector.

    """

    def __init__(self, event: dict):
        # Inherit attributes from ResponseBase parent.
        dtoutputs.OutputBase.__init__(self, event)

        # Unpack parts of event that is common for all types.
        self.__unpack()

    def __unpack(self) -> None:
        self.id = self.raw['eventId']
        self.type = self.raw['eventType']
        self.device_id = self.raw['targetName'].split('/')[-1]
        self.project_id = self.raw['targetName'].split('/')[1]

        # Initialize the appropriate data class.
        self.data = EventData.from_event_type(
            self.raw['data'],
            self.type
        )

        # Convert ISO-8601 string to datetime format.
        self.timestamp = dttrans.iso8601_to_datetime(
            self.raw['timestamp']
        )

    @classmethod
    def from_mixed_list(cls, events: list[dict]):
        """
        Construct Event objects for each event in list.

        Parameters
        ----------
        events : list[dict]
            List of raw event response dictionaries.

        Returns
        -------
        events : list[Event]
            List of constructed event objects.

        """

        # Initialise output list.
        object_list = []

        # Iterate events in list.
        for event in events:
            # Initialize instance and append to output.
            object_list.append(cls(event))

        return object_list
