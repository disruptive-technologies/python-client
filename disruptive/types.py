

class _EventType():

    def __init__(self, api_name, attr_name, class_name, is_keyed):
        self.api_name = api_name
        self.attr_name = attr_name
        self.class_name = class_name
        self.is_keyed = is_keyed


class _EventTypes():

    _api_names = {
        'touch': _EventType(
            api_name='touch',
            attr_name='touch',
            class_name='Touch',
            is_keyed=True
        ),
        'temperature': _EventType(
            api_name='temperature',
            attr_name='temperature',
            class_name='Temperature',
            is_keyed=True
        ),
        'objectPresent': _EventType(
            api_name='objectPresent',
            attr_name='object_present',
            class_name='ObjectPresent',
            is_keyed=True
        ),
        'humidity': _EventType(
            api_name='humidity',
            attr_name='humidity',
            class_name='Humidity',
            is_keyed=True
        ),
        'objectPresentCount': _EventType(
            api_name='objectPresentCount',
            attr_name='object_present_count',
            class_name='ObjectPresentCount',
            is_keyed=True
        ),
        'touchCount': _EventType(
            api_name='touchCount',
            attr_name='touch_count',
            class_name='TouchCount',
            is_keyed=True
        ),
        'waterPresent': _EventType(
            api_name='waterPresent',
            attr_name='water_present',
            class_name='WaterPresent',
            is_keyed=True
        ),
        'networkStatus': _EventType(
            api_name='networkStatus',
            attr_name='network_status',
            class_name='NetworkStatus',
            is_keyed=True,
        ),
        'batteryStatus': _EventType(
            api_name='batteryStatus',
            attr_name='battery_status',
            class_name='BatteryStatus',
            is_keyed=True,
        ),
        'labelsChanged': _EventType(
            api_name='labelsChanged',
            attr_name='labels_changed',
            class_name='LabelsChanged',
            is_keyed=False,
        ),
        'connectionStatus': _EventType(
            api_name='connectionStatus',
            attr_name='connection_status',
            class_name='ConnectionStatus',
            is_keyed=True,
        ),
        'ethernetStatus': _EventType(
            api_name='ethernetStatus',
            attr_name='ethernet_status',
            class_name='EthernetStatus',
            is_keyed=True,
        ),
        'cellularStatus': _EventType(
            api_name='cellularStatus',
            attr_name='cellular_status',
            class_name='CellularStatus',
            is_keyed=True,
        )
    }

    # Using properties instead of variables to prevent changing the values.
    @property
    def touch(self):
        return self._api_names['touch'].api_name

    @property
    def temperature(self):
        return self._api_names['temperature'].api_name

    @property
    def objectPresent(self):
        return self._api_names['objectPresent'].api_name

    @property
    def humidity(self):
        return self._api_names['humidity'].api_name

    @property
    def objectPresentCount(self):
        return self._api_names['objectPresentCount'].api_name

    @property
    def touchCount(self):
        return self._api_names['touchCount'].api_name

    @property
    def waterPresent(self):
        return self._api_names['waterPresent'].api_name

    @property
    def networkStatus(self):
        return self._api_names['networkStatus'].api_name

    @property
    def batteryStatus(self):
        return self._api_names['batteryStatus'].api_name

    @property
    def labelsChanged(self):
        return self._api_names['labelsChanged'].api_name

    @property
    def connectionStatus(self):
        return self._api_names['connectionStatus'].api_name

    @property
    def ethernetStatus(self):
        return self._api_names['ethernetStatus'].api_name

    @property
    def cellularStatus(self):
        return self._api_names['cellularStatus'].api_name


EventTypes = _EventTypes()
