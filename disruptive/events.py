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
        else:
            print('Unknown event type {}.'.format(event['eventType']))
            return None


class TemperatureEvent(Event):

    def __init__(self, event_dict):
        # Inherit parent Event class init.
        Event.__init__(self, event_dict)

        # Unpack type-specific data in event dictionary.
        self.__unpack()

    def __unpack(self):
        self.value = self.data['value']


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


class TouchEvent(Event):

    def __init__(self, event_dict):
        # Inherit parent Event class init.
        Event.__init__(self, event_dict)
