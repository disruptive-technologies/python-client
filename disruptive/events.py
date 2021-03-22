from __future__ import annotations

# Project imports.
import disruptive.transforms as dttrans
import disruptive.outputs as dtoutputs
import disruptive.log as dtlog


class DataClass(dtoutputs.OutputBase):

    def __init__(self, data: dict) -> None:
        # Inherit parent Event class init.
        dtoutputs.OutputBase.__init__(self, data)

    @classmethod
    def from_event_type(cls, data: dict, event_type: str):
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
        # Initialize the correct object.
        if event_type in EVENTS_MAP:
            out = (
                EVENTS_MAP[event_type]['class'],
                EVENTS_MAP[event_type]['is_keyed'],
            )
            return out
        else:
            dtlog.log('Unknown event type {}. Skipping.'.format(event_type))
            return None, None


class Touch(DataClass):

    def __init__(self, data: dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data)


class Temperature(DataClass):

    def __init__(self, data: dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self) -> None:
        self.value = self.raw['value']


class ObjectPresent(DataClass):

    def __init__(self, data: dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self) -> None:
        # Set attributes.
        self.state = self.raw['state']


class Humidity(DataClass):

    def __init__(self, data: dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self) -> None:
        # Set attributes.
        self.temperature = self.raw['temperature']
        self.humidity = self.raw['relativeHumidity']


class ObjectPresentCount(DataClass):

    def __init__(self, data: dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self) -> None:
        # Set attributes.
        self.total = self.raw['total']


class TouchCount(DataClass):

    def __init__(self, data: dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self) -> None:
        # Set attributes.
        self.total = self.raw['total']


class WaterPresent(DataClass):

    def __init__(self, data: dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self) -> None:
        # Set attributes.
        self.state = self.raw['state']


class NetworkStatus(DataClass):

    def __init__(self, data: dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self) -> None:
        # Set attributes.
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


class BatteryStatus(DataClass):

    def __init__(self, data: dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self) -> None:
        # Set attributes.
        self.percentage = self.raw['percentage']


class LabelsChanged(DataClass):

    def __init__(self, data: dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self) -> None:
        # Set attributes.
        self.added = self.raw['added']
        self.modified = self.raw['modified']
        self.removed = self.raw['removed']


class ConnectionStatus(DataClass):

    def __init__(self, data: dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self) -> None:
        # Set attributes.
        self.connection = self.raw['connection']
        self.available = self.raw['available']


class EthernetStatus(DataClass):

    def __init__(self, data: dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self) -> None:
        # Set attributes.
        self.mac_address = self.raw['macAddress']
        self.ip_address = self.raw['ipAddress']


class CellularStatus(DataClass):

    def __init__(self, data: dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self) -> None:
        # Set attributes.
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
        self.data = DataClass.from_event_type(
            self.raw['data'],
            self.type
        )

        # Convert ISO-8601 string to datetime format.
        self.timestamp = dttrans.iso8601_to_datetime(
            self.raw['timestamp']
        )

    @classmethod
    def from_mixed_list(cls, events: list[dict]):
        # Initialise output list.
        object_list = []

        # Iterate events in list.
        for event in events:
            # Initialize instance and append to output.
            object_list.append(cls(event))

        return object_list
