from disruptive import transforms as trf
from disruptive.outputs import OutputBase


class Event(OutputBase):

    def __init__(self, event_dict):
        # Inherit attributes from ResponseBase parent.
        OutputBase.__init__(self, event_dict)

        # Unpack parts of event that is common for all types.
        self.__unpack()

    def __unpack(self):
        self.type = self.raw['eventType']
        self.device_id = self.raw['targetName'].split('/')[-1]
        self.project_id = self.raw['targetName'].split('/')[1]

        # Set isolated data field as attribute.
        self.data = self.raw['data'][self.type]

        # Convert ISO-8601 string to datetime format.
        self.timestamp = trf.iso8601_to_datetime(self.data['updateTime'])

    @classmethod
    def from_single(cls, event):
        child = cls.__classify_event_by_type(event)
        return child(event)

    @classmethod
    def from_mixed_list(cls, event_list):
        # Initialise output list.
        object_list = []

        # Iterate events in list.
        for event in event_list:
            # Identify correct child class.
            child = cls.__classify_event_by_type(event)

            # Initialize child object.
            object_list.append(child(event))

        return object_list

    def __classify_event_by_type(event):
        # Initialize the correct object.
        if event['eventType'] == 'temperature':
            return TemperatureEvent
        elif event['eventType'] == 'networkStatus':
            return NetworkStatusEvent
        elif event['eventType'] == 'touch':
            return TouchEvent
        elif event['eventType'] == 'objectPresent':
            return ObjectPresentEvent
        else:
            print('Unknown event type {}.'.format(event['eventType']))
            return None


class TouchEvent(Event):

    def __init__(self, event_dict):
        # Inherit parent Event class init.
        Event.__init__(self, event_dict)


class TemperatureEvent(Event):

    def __init__(self, event_dict):
        # Inherit parent Event class init.
        Event.__init__(self, event_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        self.value = self.data['value']


class ObjectPresentEvent(Event):

    def __init__(self, event_dict):
        # Inherit parent Event class init.
        Event.__init__(self, event_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.state = self.data['state']


class HumidityEvent(Event):

    def __init__(self, event_dict):
        # Inherit parent Event class init.
        Event.__init__(self, event_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.temperature = self.data['temperature']
        self.humidity = self.data['relativeHumidity']


class ObjectPresentCountEvent(Event):

    def __init__(self, event_dict):
        # Inherit parent Event class init.
        Event.__init__(self, event_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.total = self.data['total']


class TouchCountEvent(Event):

    def __init__(self, event_dict):
        # Inherit parent Event class init.
        Event.__init__(self, event_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.total = self.data['total']


class WaterPresentEvent(Event):

    def __init__(self, event_dict):
        # Inherit parent Event class init.
        Event.__init__(self, event_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.state = self.data['state']


class NetworkStatusEvent(Event):

    def __init__(self, event_dict):
        # Inherit parent Event class init.
        Event.__init__(self, event_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.signal_strength = self.data['signalStrength']
        self.rssi = self.data['rssi']
        self.transmission_mode = self.data['transmissionMode']
        self.cloud_connectors = []
        for ccon in self.data['cloudConnectors']:
            self.cloud_connectors.append({
                'id': ccon['id'],
                'signalStrength': ccon['signalStrength'],
                'rssi': ccon['rssi'],
            })


class BatteryStatusEvent(Event):

    def __init__(self, event_dict):
        # Inherit parent Event class init.
        Event.__init__(self, event_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.percentage = self.data['percentage']


class LabelsChangedEvent(Event):

    def __init__(self, event_dict):
        # Inherit parent Event class init.
        Event.__init__(self, event_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.added = self.data['added']
        self.modified = self.data['modified']
        self.removed = self.data['removed']


class ConnectionStatusEvent(Event):

    def __init__(self, event_dict):
        # Inherit parent Event class init.
        Event.__init__(self, event_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.connection = self.data['connection']
        self.available = self.data['available']


class EthernetStatusEvent(Event):

    def __init__(self, event_dict):
        # Inherit parent Event class init.
        Event.__init__(self, event_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.mac_address = self.data['macAddress']
        self.ip_address = self.data['ipAddress']


class CellularStatusEvent(Event):

    def __init__(self, event_dict):
        # Inherit parent Event class init.
        Event.__init__(self, event_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.signal_strength = self.data['signalStrength']
