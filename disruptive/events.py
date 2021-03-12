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
        self.data = self.raw['data']

        # Convert ISO-8601 string to datetime format.
        self.timestamp = trf.iso8601_to_datetime(
            self.raw['timestamp']
        )

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
        if event['eventType'] == 'touch':
            return TouchEvent
        elif event['eventType'] == 'temperature':
            return TemperatureEvent
        elif event['eventType'] == 'objectPresent':
            return ObjectPresentEvent
        elif event['eventType'] == 'humidity':
            return HumidityEvent
        elif event['eventType'] == 'objectPresentCount':
            return ObjectPresentCountEvent
        elif event['eventType'] == 'touchCount':
            return TouchCountEvent
        elif event['eventType'] == 'waterPresent':
            return WaterPresentEvent
        elif event['eventType'] == 'networkStatus':
            return NetworkStatusEvent
        elif event['eventType'] == 'batteryStatus':
            return BatteryStatusEvent
        elif event['eventType'] == 'labelsChanged':
            return LabelsChangedEvent
        elif event['eventType'] == 'connectionStatus':
            return ConnectionStatusEvent
        elif event['eventType'] == 'ethernetStatus':
            return EthernetStatusEvent
        elif event['eventType'] == 'cellularStatus':
            return CellularStatusEvent
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
        self.value = self.data[self.type]['value']


class ObjectPresentEvent(Event):

    def __init__(self, event_dict):
        # Inherit parent Event class init.
        Event.__init__(self, event_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.state = self.data[self.type]['state']


class HumidityEvent(Event):

    def __init__(self, event_dict):
        # Inherit parent Event class init.
        Event.__init__(self, event_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.temperature = self.data[self.type]['temperature']
        self.humidity = self.data[self.type]['relativeHumidity']


class ObjectPresentCountEvent(Event):

    def __init__(self, event_dict):
        # Inherit parent Event class init.
        Event.__init__(self, event_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.total = self.data[self.type]['total']


class TouchCountEvent(Event):

    def __init__(self, event_dict):
        # Inherit parent Event class init.
        Event.__init__(self, event_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.total = self.data[self.type]['total']


class WaterPresentEvent(Event):

    def __init__(self, event_dict):
        # Inherit parent Event class init.
        Event.__init__(self, event_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.state = self.data[self.type]['state']


class NetworkStatusEvent(Event):

    def __init__(self, event_dict):
        # Inherit parent Event class init.
        Event.__init__(self, event_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.signal_strength = self.data[self.type]['signalStrength']
        self.rssi = self.data[self.type]['rssi']
        self.transmission_mode = self.data[self.type]['transmissionMode']
        self.cloud_connectors = []
        for ccon in self.data[self.type]['cloudConnectors']:
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
        self.percentage = self.data[self.type]['percentage']


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
        self.connection = self.data[self.type]['connection']
        self.available = self.data[self.type]['available']


class EthernetStatusEvent(Event):

    def __init__(self, event_dict):
        # Inherit parent Event class init.
        Event.__init__(self, event_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.mac_address = self.data[self.type]['macAddress']
        self.ip_address = self.data[self.type]['ipAddress']


class CellularStatusEvent(Event):

    def __init__(self, event_dict):
        # Inherit parent Event class init.
        Event.__init__(self, event_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        # Set attributes.
        self.signal_strength = self.data[self.type]['signalStrength']
