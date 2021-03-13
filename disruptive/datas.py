import disruptive.outputs as dtoutputs
import disruptive.events as dtevents
import disruptive.log as dtlog


class DataClass(dtoutputs.OutputBase):

    def __init__(self, data_dict):
        # Inherit parent Event class init.
        dtoutputs.OutputBase.__init__(self, data_dict)

    @classmethod
    def from_event_type(cls, data_dict, event_type):
        # From the type, select the appropriate child class.
        child, key = cls.__child_map(event_type)

        # Return None at invalid event type.
        if child is None:
            return None

        # Return the initialized class instance.
        if key:
            return child(data_dict[event_type])
        else:
            # Special case for labelsChanged event.
            return child(data_dict)

    def __child_map(event_type):
        # Initialize the correct object.
        if event_type in dtevents.EVENTS_MAP:
            out = (
                dtevents.EVENTS_MAP[event_type]['class'],
                dtevents.EVENTS_MAP[event_type]['is_keyed'],
            )
            return out
        else:
            dtlog.log('Unknown event type {}. Skipping.'.format(event_type))
            return None, None


class Touch(DataClass):

    def __init__(self, data_dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data_dict)


class Temperature(DataClass):

    def __init__(self, data_dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        self.value = self.raw['value']


class ObjectPresent(DataClass):

    def __init__(self, data_dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.state = self.raw['state']


class Humidity(DataClass):

    def __init__(self, data_dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.temperature = self.raw['temperature']
        self.humidity = self.raw['relativeHumidity']


class ObjectPresentCount(DataClass):

    def __init__(self, data_dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.total = self.raw['total']


class TouchCount(DataClass):

    def __init__(self, data_dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.total = self.raw['total']


class WaterPresent(DataClass):

    def __init__(self, data_dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.state = self.raw['state']


class NetworkStatus(DataClass):

    def __init__(self, data_dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
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

    def __init__(self, event_dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, event_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.percentage = self.raw['percentage']


class LabelsChanged(DataClass):

    def __init__(self, data_dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.added = self.raw['added']
        self.modified = self.raw['modified']
        self.removed = self.raw['removed']


class ConnectionStatus(DataClass):

    def __init__(self, data_dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.connection = self.raw['connection']
        self.available = self.raw['available']


class EthernetStatus(DataClass):

    def __init__(self, data_dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.mac_address = self.raw['macAddress']
        self.ip_address = self.raw['ipAddress']


class CellularStatus(DataClass):

    def __init__(self, data_dict):
        # Inherit parent Event class init.
        DataClass.__init__(self, data_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.signal_strength = self.raw['signalStrength']
