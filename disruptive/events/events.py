from __future__ import annotations

from typing import Optional, Union
from datetime import datetime

import disruptive
import disruptive.logging as dtlog
import disruptive.outputs as dtoutputs
import disruptive.transforms as dttrans

# Event-type constants.
TOUCH = 'touch'
TEMPERATURE = 'temperature'
OBJECT_PRESENT = 'objectPresent'
HUMIDITY = 'humidity'
OBJECT_PRESENT_COUNT = 'objectPresentCount'
TOUCH_COUNT = 'touchCount'
WATER_PRESENT = 'waterPresent'
NETWORK_STATUS = 'networkStatus'
BATTERY_STATUS = 'batteryStatus'
LABELS_CHANGED = 'labelsChanged'
CONNECTION_STATUS = 'connectionStatus'
ETHERNET_STATUS = 'ethernetStatus'
CELLULAR_STATUS = 'cellularStatus'


class _EventData(dtoutputs.OutputBase):
    """
    Parent class for all the different event data field types.

    Attributes are mainly inherited from OutputBase, and otherwise
    contains a few convenience methods for setting the correct child.

    Attributes
    ----------
    timestamp : datetime, str, optional
        Timestamp of when the event was received by a Cloud Connector.

    """

    def __init__(self, data: dict, event_type: str) -> None:
        """
        Constructs the _EventData object by inheriting parent.

        Parameters
        ----------
        data : dict
            Event data dictionary.
        event_type : str
            Name of the event type.

        """

        self.timestamp: Optional[datetime | str] = None

        # If timestamp is provided, verify type and set attribute.
        if 'updateTime' in data:
            # Raw should be iso8601 str format, while
            # attribute should be type datetime.
            ts_iso8601 = dttrans.to_iso8601(data['updateTime'])
            ts_datetime = dttrans.to_datetime(data['updateTime'])

            # If we can not verify iso8601 format, remove field.
            if ts_iso8601 is not None:
                data['updateTime'] = ts_iso8601
            else:
                del data['updateTime']

            # Set datetime return as timestamp attribute.
            self.timestamp = ts_datetime
        else:
            # None timestamp if not provided.
            self.timestamp = None

        # Set other attributes.
        self.event_type = event_type

        # Inherit parent class.
        dtoutputs.OutputBase.__init__(self, data)

    @classmethod
    def from_event_type(cls,
                        data: dict,
                        event_type: str,
                        ) -> Optional[_EventType]:
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
            child_instance = child._from_raw(data[event_type])
        else:
            # Special case for labelsChanged event.
            child_instance = child._from_raw(data)
        return child_instance

    @staticmethod
    def __child_map(event_type: str,
                    ) -> tuple[Optional[_EventType], Optional[bool]]:
        """
        Based on provided event type, returns the
        child class and supporting information.

        Parameters
        ----------
        event_type : str
            The event type of the source event.

        """

        # Initialize the correct object.
        if event_type in _EVENTS_MAP._api_names:
            out = (
                getattr(
                    disruptive.events,
                    _EVENTS_MAP._api_names[event_type].class_name
                ),
                _EVENTS_MAP._api_names[event_type].is_keyed,
            )
            return out

        dtlog.warning('Skipping unknown event type {}.'.format(event_type))
        return None, None


class Touch(_EventData):
    """
    Represents the data found in a touch event.

    Attributes
    ----------
    timestamp : datetime
        Timestamp of when the event was received by a Cloud Connector.

    """

    def __init__(self, timestamp: Optional[datetime | str] = None):
        """
        Constructs the Touch object.

        Parameters
        ----------
        timestamp : datetime, str, optional
            Timestamp in either datetime or string iso8601 format
            (i.e. yyyy-MM-ddTHH:mm:ssZ).

        """

        # Set parameter attributes.
        self.timestamp: Optional[datetime | str] = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'touch')

    def __repr__(self) -> str:
        string = '{}.{}('\
            'timestamp={}'\
            ')'
        return string.format(
            self.__class__.__module__,
            self.__class__.__name__,
            repr(dttrans.to_iso8601(self.timestamp)),
        )

    @classmethod
    def _from_raw(cls, data: dict) -> Touch:
        """
        Constructs a Touch object from API response data.

        Parameters
        ----------
        data : dict
            API response data dictionary.

        Returns
        -------
        obj : Touch
            Object constructed from the API response data.

        """

        # Construct the object with unpacked parameters.
        obj = cls(
            timestamp=data['updateTime'],
        )

        # Re-inherit from parent, but now providing response data.
        _EventData.__init__(obj, data, obj.event_type)

        return obj

    def __repack(self) -> dict:
        data: dict = dict()
        if self.timestamp is not None:
            data['updateTime'] = self.timestamp
        return data


class Temperature(_EventData):
    """
    Represents the data found in a temperature event.

    Attributes
    ----------
    celsius : float
        Temperature value in Celsius.
    fahrenheit : float
        Temperature value in Fahrenheit.
    samples : list[TemperatureSample]
        Temperature values sampled over a single heartbeat.
    timestamp : datetime
        Timestamp of when the event was received by a Cloud Connector.

    """

    def __init__(self,
                 celsius: float,
                 samples: Optional[list] = None,
                 timestamp: Optional[datetime | str] = None,
                 ) -> None:
        """
        Constructs the Temperature object. The `fahrenheit` attribute is
        calculated from the provided `celsius` parameter.

        Parameters
        ----------
        celsius : float
            Temperature value in Celsius.
        samples : list[TemperatureSample]
            Temperature values sampled over a single heartbeat.
        timestamp : datetime, str, optional
            Timestamp in either datetime or string iso8601 format
            (i.e. yyyy-MM-ddTHH:mm:ssZ).

        """

        # Set parameter attributes.
        self.celsius: float = celsius
        self.samples: Optional[list] = samples
        self.fahrenheit: float = dttrans._celsius_to_fahrenheit(celsius)
        self.timestamp: Optional[datetime | str] = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'temperature')

    def __repr__(self) -> str:
        string = '{}.{}('\
            'celsius={}, '\
            'samples={}, '\
            'timestamp={}'\
            ')'
        return string.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.celsius,
            self.samples,
            repr(dttrans.to_iso8601(self.timestamp)),
        )

    @classmethod
    def _from_raw(cls, data: dict) -> Temperature:
        """
        Constructs a Temperature object from API response data.

        Parameters
        ----------
        data : dict
            API response data dictionary.

        Returns
        -------
        obj : Temperature
            Object constructed from the API response data.

        """

        # Convert samples dictionaries to TemperatureSample objects.
        sample_objs = []
        for sample in data['samples']:
            sample_objs.append(TemperatureSample(
                celsius=sample['value'],
                timestamp=sample['sampleTime'],
            ))

        # Construct the object with unpacked parameters.
        obj = cls(
            celsius=data['value'],
            samples=sample_objs,
            timestamp=data['updateTime'],
        )

        # Re-inherit from parent, but now providing response data.
        _EventData.__init__(obj, data, obj.event_type)

        return obj

    def __repack(self) -> dict:
        data: dict = dict()
        if self.celsius is not None:
            data['value'] = self.celsius
        if self.samples is not None:
            data['samples'] = [s._raw for s in self.samples]
        if self.timestamp is not None:
            data['updateTime'] = self.timestamp
        return data


class TemperatureSample(dtoutputs.OutputBase):
    """
    Represents a single temperature event sample from a heartbeat period.

    Attributes
    ----------
    celsius : float
        Temperature value in Celsius.
    fahrenheit : float
        Temperature value in Fahrenheit.
    timestamp : datetime
        Interpolated inter-heartbeat timestamp.

    """

    def __init__(self,
                 celsius: float,
                 timestamp: datetime | str,
                 ) -> None:
        """
        Constructs the TemperatureSample object. The `fahrenheit` attribute is
        calculated from the provided `celsius` parameter.

        Parameters
        ----------
        celsius : float
            Temperature value in Celsius.
        timestamp : datetime, str, optional
            Timestamp in either datetime or string iso8601 format
            (i.e. yyyy-MM-ddTHH:mm:ssZ).

        """

        # Set parameter attributes.
        self.celsius: float = celsius
        self.fahrenheit: float = dttrans._celsius_to_fahrenheit(celsius)
        self.timestamp = dttrans.to_datetime(timestamp)

        # Inherit parent class.
        dtoutputs.OutputBase.__init__(self, self.__repack())

    def __repr__(self) -> str:
        string = '{}.{}('\
            'celsius={}, '\
            'timestamp={}'\
            ')'
        return string.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.celsius,
            repr(dttrans.to_iso8601(self.timestamp)),
        )

    @classmethod
    def _from_raw(cls, data: dict) -> TemperatureSample:
        # Construct the object with unpacked parameters.
        obj = cls(
            celsius=data['value'],
            timestamp=data['sampleTime'],
        )

        # Inherit parent class.
        dtoutputs.OutputBase.__init__(obj, data)

        return obj

    def __repack(self) -> dict:
        data: dict = dict()
        if self.celsius is not None:
            data['value'] = self.celsius
        if self.timestamp is not None:
            data['sampleTime'] = dttrans.to_iso8601(self.timestamp)
        return data


class ObjectPresent(_EventData):
    """
    Represents the data found in an objectPresent event.

    Attributes
    ----------
    state : str
        Indicates whether an object is "PRESENT" or "NOT_PRESENT".
    timestamp : datetime
        Timestamp of when the event was received by a Cloud Connector.

    """

    def __init__(self,
                 state: str,
                 timestamp: Optional[datetime | str] = None,
                 ) -> None:
        """
        Constructs the ObjectPresent object, inheriting parent class
        and setting the type-specific attributes.

        Parameters
        ----------
        state : str
            Indicates whether an object is "PRESENT" or "NOT_PRESENT".
        timestamp : datetime, str, optional
            Timestamp in either datetime or string iso8601 format
            (i.e. yyyy-MM-ddTHH:mm:ssZ).

        """

        # Set parameter attributes.
        self.state: str = state
        self.timestamp: Optional[datetime | str] = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'objectPresent')

    def __repr__(self) -> str:
        string = '{}.{}('\
            'state={}, '\
            'timestamp={}'\
            ')'
        return string.format(
            self.__class__.__module__,
            self.__class__.__name__,
            repr(self.state),
            repr(dttrans.to_iso8601(self.timestamp)),
        )

    @classmethod
    def _from_raw(cls, data: dict) -> ObjectPresent:
        """
        Constructs an ObjectPresent object from API response data.

        Parameters
        ----------
        data : dict
            API response data dictionary.

        Returns
        -------
        obj : ObjectPresent
            Object constructed from the API response data.

        """

        # Construct the object with unpacked parameters.
        obj = cls(
            state=data['state'],
            timestamp=data['updateTime'],
        )

        # Re-inherit from parent, but now providing response data.
        _EventData.__init__(obj, data, obj.event_type)

        return obj

    def __repack(self) -> dict:
        data: dict = dict()
        if self.state is not None:
            data['state'] = self.state
        if self.timestamp is not None:
            data['updateTime'] = self.timestamp
        return data


class Humidity(_EventData):
    """
    Represents the data found in an humidity event.

    Attributes
    ----------
    temperature : float
        Temperature value in Celsius.
    relative_humidity : float
        Relative humidity in percent.
    timestamp : datetime
        Timestamp of when the event was received by a Cloud Connector.

    """

    def __init__(self,
                 celsius: float,
                 relative_humidity: float,
                 timestamp: Optional[datetime | str] = None,
                 ):
        """
        Constructs the Humidity object.

        Parameters
        ----------
        temperature : float
            Temperature value in Celsius.
        relative_humidity : float
            Relative humidity in percent.
        timestamp : datetime, str, optional
            Timestamp in either datetime or string iso8601 format
            (i.e. yyyy-MM-ddTHH:mm:ssZ).

        """

        # Set parameter attributes.
        self.celsius: float = celsius
        self.fahrenheit: float = dttrans._celsius_to_fahrenheit(celsius)
        self.relative_humidity: float = relative_humidity
        self.timestamp: Optional[datetime | str] = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'humidity')

    def __repr__(self) -> str:
        string = '{}.{}('\
            'celsius={}, '\
            'relative_humidity={}, '\
            'timestamp={}'\
            ')'
        return string.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.celsius,
            self.relative_humidity,
            repr(dttrans.to_iso8601(self.timestamp)),
        )

    @classmethod
    def _from_raw(cls, data: dict) -> Humidity:
        """
        Constructs a Humidity object from API response data.

        Parameters
        ----------
        data : dict
            API response data dictionary.

        Returns
        -------
        obj : Humidity
            Object constructed from the API response data.

        """

        # Construct the object with unpacked parameters.
        obj = cls(
            celsius=data['temperature'],
            relative_humidity=data['relativeHumidity'],
            timestamp=data['updateTime'],
        )

        # Re-inherit from parent, but now providing response data.
        _EventData.__init__(obj, data, obj.event_type)

        return obj

    def __repack(self) -> dict:
        data: dict = dict()
        if self.celsius is not None:
            data['temperature'] = self.celsius
        if self.relative_humidity is not None:
            data['relativeHumidity'] = self.relative_humidity
        if self.timestamp is not None:
            data['updateTime'] = self.timestamp
        return data


class ObjectPresentCount(_EventData):
    """
    Represents the data found in an objectPresentCount event.

    Attributes
    ----------
    total : int
        The total number of times the sensor has detected the appearance
        or disappearance of an object over its lifetime.
    timestamp : datetime
        Timestamp of when the event was received by a Cloud Connector.

    """

    def __init__(self,
                 total: int,
                 timestamp: Optional[datetime | str] = None,
                 ):
        """
        Constructs the ObjectPresentCount object.

        Parameters
        ----------
        total : int
            The total number of times the sensor has detected the appearance
            or disappearance of an object over its lifetime.
        timestamp : datetime, str, optional
            Timestamp in either datetime or string iso8601 format
            (i.e. yyyy-MM-ddTHH:mm:ssZ).

        """

        # Set parameter attributes.
        self.total: int = total
        self.timestamp: Optional[datetime | str] = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'objectPresentCount')

    def __repr__(self) -> str:
        string = '{}.{}('\
            'total={}, '\
            'timestamp={}'\
            ')'
        return string.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.total,
            repr(dttrans.to_iso8601(self.timestamp)),
        )

    @classmethod
    def _from_raw(cls, data: dict) -> ObjectPresentCount:
        """
        Constructs a ObjectPresentCount object from API response data.

        Parameters
        ----------
        data : dict
            API response data dictionary.

        Returns
        -------
        obj : ObjectPresentCount
            Object constructed from the API response data.

        """

        # Construct the object with unpacked parameters.
        obj = cls(
            total=data['total'],
            timestamp=data['updateTime'],
        )

        # Re-inherit from parent, but now providing response data.
        _EventData.__init__(obj, data, obj.event_type)

        return obj

    def __repack(self) -> dict:
        data: dict = dict()
        data['total'] = self.total
        if self.timestamp is not None:
            data['updateTime'] = self.timestamp
        return data


class TouchCount(_EventData):
    """
    Represents the data found in an touchCount event.

    Attributes
    ----------
    total : int
        The total number of times the sensor has been
        touched over its lifetime.
    timestamp : datetime
        Timestamp of when the event was received by a Cloud Connector.

    """

    def __init__(self,
                 total: int,
                 timestamp: Optional[datetime | str] = None,
                 ):
        """
        Constructs the TouchCount object.

        Parameters
        ----------
        total : int
            The total number of times the sensor has been
            touched over its lifetime.
        timestamp : datetime, str, optional
            Timestamp in either datetime or string iso8601 format
            (i.e. yyyy-MM-ddTHH:mm:ssZ).

        """

        # Set parameter attributes.
        self.total: int = total
        self.timestamp: Optional[datetime | str] = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'touchCount')

    def __repr__(self) -> str:
        string = '{}.{}('\
            'total={}, '\
            'timestamp={}'\
            ')'
        return string.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.total,
            repr(dttrans.to_iso8601(self.timestamp)),
        )

    @classmethod
    def _from_raw(cls, data: dict) -> TouchCount:
        """
        Constructs a TouchCount object from API response data.

        Parameters
        ----------
        data : dict
            API response data dictionary.

        Returns
        -------
        obj : TouchCount
            Object constructed from the API response data.

        """

        # Construct the object with unpacked parameters.
        obj = cls(
            total=data['total'],
            timestamp=data['updateTime'],
        )

        # Re-inherit from parent, but now providing response data.
        _EventData.__init__(obj, data, obj.event_type)

        return obj

    def __repack(self) -> dict:
        data: dict = dict()
        data['total'] = self.total
        if self.timestamp is not None:
            data['updateTime'] = self.timestamp
        return data


class WaterPresent(_EventData):
    """
    Represents the data found in an waterPresent event.

    Attributes
    ----------
    state : str
        Indicates whether water is PRESENT or NOT_PRESENT.
    timestamp : datetime
        Timestamp of when the event was received by a Cloud Connector.

    """

    def __init__(self,
                 state: str,
                 timestamp: Optional[datetime | str] = None,
                 ):
        """
        Constructs the WaterPresent object.

        Parameters
        ----------
        state : str
            Indicates whether water is "PRESENT" or "NOT_PRESENT".
        timestamp : datetime, str, optional
            Timestamp in either datetime or string iso8601 format
            (i.e. yyyy-MM-ddTHH:mm:ssZ).

        """

        # Set parameter attributes.
        self.state: str = state
        self.timestamp: Optional[datetime | str] = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'waterPresent')

    def __repr__(self) -> str:
        string = '{}.{}('\
            'state={}, '\
            'timestamp={}'\
            ')'
        return string.format(
            self.__class__.__module__,
            self.__class__.__name__,
            repr(self.state),
            repr(dttrans.to_iso8601(self.timestamp)),
        )

    @classmethod
    def _from_raw(cls, data: dict) -> WaterPresent:
        """
        Constructs a WaterPresent object from API response data.

        Parameters
        ----------
        data : dict
            API response data dictionary.

        Returns
        -------
        obj : WaterPresent
            Object constructed from the API response data.

        """

        # Construct the object with unpacked parameters.
        obj = cls(
            state=data['state'],
            timestamp=data['updateTime'],
        )

        # Re-inherit from parent, but now providing response data.
        _EventData.__init__(obj, data, obj.event_type)

        return obj

    def __repack(self) -> dict:
        data: dict = dict()
        data['state'] = self.state
        if self.timestamp is not None:
            data['updateTime'] = self.timestamp
        return data


class NetworkStatusCloudConnector(dtoutputs.OutputBase):
    """
    Represents a Cloud Connector found in the networkStatus event data.

    Attributes
    ----------
    device_id : str
        Device ID of the Cloud Connector.
    signal_strength : int
        The percentage signal strength (0% to 100%) between
        the sensor and Cloud Connector.
    rssi : int
        Raw Received Signal Strength Indication (RSSI) between
        the sensor and Cloud Connector.

    """

    def __init__(self,
                 device_id: str,
                 signal_strength: int,
                 rssi: int,
                 ):
        """
        Constructs the NetworkStatusCloudConnector object.

        Parameters
        ----------
        device_id : str
            Device ID of the Cloud Connector.
        signal_strength : int
            The percentage signal strength (0% to 100%) between
            the sensor and Cloud Connector.
        rssi : int
            Raw Received Signal Strength Indication (RSSI) between
            the sensor and Cloud Connector.

        """

        # Inherit parent OutputBase class init.
        dtoutputs.OutputBase.__init__(self, {})

        # Unpack attributes.
        self.device_id: str = device_id
        self.signal_strength: int = signal_strength
        self.rssi: int = rssi

    def __repr__(self) -> str:
        string = '{}.{}('\
            'device_id={}, '\
            'signal_strength={}, '\
            'rssi={}'\
            ')'
        return string.format(
            self.__class__.__module__,
            self.__class__.__name__,
            repr(self.device_id),
            self.signal_strength,
            self.rssi,
        )

    @classmethod
    def _from_raw(cls, data: dict) -> NetworkStatusCloudConnector:
        """
        Constructs a NetworkStatusCloudConnector object from API response data.

        Parameters
        ----------
        data : dict
            API response data dictionary.

        Returns
        -------
        obj : NetworkStatusCloudConnector
            Object constructed from the API response data.

        """

        # Construct the object with unpacked parameters.
        obj = cls(
            device_id=data['id'],
            signal_strength=data['signalStrength'],
            rssi=data['rssi'],
        )

        # Re-inherit from parent, but now providing response data.
        dtoutputs.OutputBase.__init__(obj, data)

        return obj


class NetworkStatus(_EventData):
    """
    Represents the data found in a networkStatus event.

    Attributes
    ----------
    signal_strength : int
        The percentage signal strength (0% to 100%) of the strongest
        Cloud Connector, derived directly from the RSSI value.
    rssi : float
        Raw Received Signal Strength Indication (RSSI) as measured
        by the strongest Cloud Connector.
    transmission_mode : str
        Indicated whether the sensor is in
        LOW_POWER_STANDARD_MODE or HIGH_POWER_BOOST_MODE.
    cloud_connectors : list[NetworkStatusCloudConnector]
        List of the Cloud Connector that forwarded the event.
    timestamp : datetime
        Timestamp of when the event was received by a Cloud Connector.

    """

    def __init__(
        self,
        signal_strength: int,
        rssi: int,
        transmission_mode: str,
        cloud_connectors: list[NetworkStatusCloudConnector],
        timestamp: Optional[datetime | str] = None
    ) -> None:
        """
        Constructs the NetworkStatus object.

        Parameters
        ----------
        signal_strength : int
            The percentage signal strength (0% to 100%) of the strongest
            Cloud Connector, derived directly from the RSSI value.
        rssi : float
            Raw Received Signal Strength Indication (RSSI) as measured
            by the strongest Cloud Connector.
        transmission_mode : str
            Indicated whether the sensor is in
            LOW_POWER_STANDARD_MODE or HIGH_POWER_BOOST_MODE.
        cloud_connectors : list[NetworkStatusCloudConnector]
            List of the Cloud Connector that forwarded the event.
        timestamp : datetime, str, optional
            Timestamp in either datetime or string iso8601 format
            (i.e. yyyy-MM-ddTHH:mm:ssZ).

        """

        # Set attributes.
        self.signal_strength: int = signal_strength
        self.rssi: int = rssi
        self.transmission_mode: str = transmission_mode
        self.cloud_connectors: list[NetworkStatusCloudConnector] = \
            cloud_connectors
        self.timestamp: Optional[datetime | str] = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'networkStatus')

    def __repr__(self) -> str:
        string = '{}.{}('\
            'signal_strength={}, '\
            'rssi={}, '\
            'transmission_mode={}, '\
            'cloud_connectors={}, '\
            'timestamp={}'\
            ')'
        return string.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.signal_strength,
            self.rssi,
            repr(self.transmission_mode),
            self.cloud_connectors,
            repr(dttrans.to_iso8601(self.timestamp)),
        )

    @classmethod
    def _from_raw(cls, data: dict) -> NetworkStatus:
        """
        Constructs a NetworkStatus object from API response data.

        Parameters
        ----------
        data : dict
            API response data dictionary.

        Returns
        -------
        obj : NetworkStatus
            Object constructed from the API response data.

        """

        # Isolate list of NetworkStatusCloudConnector objects.
        cloud_connectors = []
        for ccon in data['cloudConnectors']:
            cloud_connectors.append(
                NetworkStatusCloudConnector._from_raw(ccon)
            )

        # Construct the object with unpacked parameters.
        obj = cls(
            signal_strength=data['signalStrength'],
            rssi=data['rssi'],
            transmission_mode=data['transmissionMode'],
            cloud_connectors=cloud_connectors,
            timestamp=data['updateTime'],
        )

        # Re-inherit from parent, but now providing response data.
        _EventData.__init__(obj, data, obj.event_type)

        return obj

    def __repack(self) -> dict:
        data: dict = dict()
        if self.signal_strength is not None:
            data['signalStrength'] = self.signal_strength
        if self.rssi is not None:
            data['rssi'] = self.rssi
        if self.transmission_mode is not None:
            data['transmissionMode'] = self.transmission_mode
        if self.timestamp is not None:
            data['updateTime'] = self.timestamp
        if self.cloud_connectors is not None:
            data['cloud_connectors'] = []
            for ccon in self.cloud_connectors:
                ccon_data: dict = dict()
                if ccon.device_id is not None:
                    ccon_data['id'] = ccon.device_id
                if ccon.signal_strength is not None:
                    ccon_data['signalStrength'] = ccon.signal_strength
                if len(ccon_data) > 0:
                    data['cloud_connectors'].append(ccon_data)
        return data


class BatteryStatus(_EventData):
    """
    Represents the data found in a batteryStatus event.

    Attributes
    ----------
    percentage : int
        A coarse percentage estimate (0% to 100%) of the remaining battery.
    timestamp : datetime
        Timestamp of when the event was received by a Cloud Connector.

    """

    def __init__(self,
                 percentage: int,
                 timestamp: Optional[datetime | str] = None,
                 ) -> None:
        """
        Constructs the Temperature object.

        Parameters
        ----------
        percentage : int
            A coarse percentage estimate (0% to 100%) of the remaining battery.
        timestamp : datetime, str, optional
            Timestamp in either datetime or string iso8601 format
            (i.e. yyyy-MM-ddTHH:mm:ssZ).

        """

        # Inherit parent _EventData class init with repacked data dictionary.
        self.percentage: int = percentage
        self.timestamp: Optional[datetime | str] = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'batteryStatus')

    def __repr__(self) -> str:
        string = '{}.{}('\
            'percentage={}, '\
            'timestamp={}'\
            ')'
        return string.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.percentage,
            repr(dttrans.to_iso8601(self.timestamp)),
        )

    @classmethod
    def _from_raw(cls, data: dict) -> BatteryStatus:
        """
        Constructs a BatteryStatus object from API response data.

        Parameters
        ----------
        data : dict
            API response data dictionary.

        Returns
        -------
        obj : BatteryStatus
            Object constructed from the API response data.

        """

        # Construct the object with unpacked parameters.
        obj = cls(
            percentage=data['percentage'],
            timestamp=data['updateTime'],
        )

        # Re-inherit from parent, but now providing response data.
        _EventData.__init__(obj, data, obj.event_type)

        return obj

    def __repack(self) -> dict:
        data: dict = dict()
        if self.percentage is not None:
            data['percentage'] = self.percentage
        if self.timestamp is not None:
            data['updateTime'] = self.timestamp
        return data


class LabelsChanged(_EventData):
    """
    Represents the data found in an labelsChanged event.

    Attributes
    ----------
    added : dict[str, str]
        Keys and values of new labels added.
    modified : dict[str, str]
        New keys and values of modified labels.
    removed : list[str]
        List of keys of removed labels.
    timestamp : datetime
        Timestamp of when the event was received by a Cloud Connector.

    """

    def __init__(self,
                 added: dict[str, str],
                 modified: dict[str, str],
                 removed: list[str],
                 timestamp: Optional[datetime | str] = None,
                 ):
        """
        Constructs the LabelsChanged object.

        Parameters
        ----------
        added : dict[str, str]
            Keys and values of new labels added.
        modified : dict[str, str]
            New keys and values of modified labels.
        removed : list[str]
            List of keys of removed labels.
        timestamp : datetime, str, optional
            Timestamp in either datetime or string iso8601 format
            (i.e. yyyy-MM-ddTHH:mm:ssZ).

        """

        # Set parameter attributes.
        self.added: dict = added
        self.modified: dict = modified
        self.removed: list[str] = removed
        self.timestamp: Optional[datetime | str] = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'labelsChanged')

    def __repr__(self) -> str:
        string = '{}.{}('\
            'added={}, '\
            'modified={}, '\
            'removed={}, '\
            'timestamp={}'\
            ')'
        return string.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.added,
            self.modified,
            self.removed,
            repr(dttrans.to_iso8601(self.timestamp)),
        )

    @classmethod
    def _from_raw(cls, data: dict) -> LabelsChanged:
        """
        Constructs a LabelsChanged object from API response data.

        Parameters
        ----------
        data : dict
            API response data dictionary.

        Returns
        -------
        obj : LabelsChanged
            Object constructed from the API response data.

        """

        # Construct the object with unpacked parameters.
        obj = cls(
            added=data['added'],
            modified=data['modified'],
            removed=data['removed'],
            timestamp=data['updateTime'],
        )

        # Re-inherit from parent, but now providing response data.
        _EventData.__init__(obj, data, obj.event_type)

        return obj

    def __repack(self) -> dict:
        data: dict = dict()
        if self.added is not None:
            data['added'] = self.added
        if self.modified is not None:
            data['modified'] = self.modified
        if self.removed is not None:
            data['removed'] = self.removed
        if self.timestamp is not None:
            data['updateTime'] = self.timestamp
        return data


class ConnectionStatus(_EventData):
    """
    Represents the data found in a connectionStatus event.

    Attributes
    ----------
    connection : str
        Whether the Cloud Connector is on "ETHERNET", "CELLULAR", or "OFFLINE".
    available : list[str]
        Lists available connections. Can contain
        "ETHERNET", "CELLULAR", or both.
    timestamp : datetime
        Timestamp of when the event was received by a Cloud Connector.

    """

    def __init__(self,
                 connection: str,
                 available: list[str],
                 timestamp: Optional[datetime | str] = None,
                 ):
        """
        Constructs the ConnectionStatus object.

        Parameters
        ----------
        connection : str
            Whether the Cloud Connector is on
            "ETHERNET", "CELLULAR", or "OFFLINE".
        available : list[str]
            Lists available connections.
            Can contain "ETHERNET", "CELLULAR", or both.
        timestamp : datetime, str, optional
            Timestamp in either datetime or string iso8601 format
            (i.e. yyyy-MM-ddTHH:mm:ssZ).

        """

        # Set parameter attributes.
        self.connection: str = connection
        self.available: list[str] = available
        self.timestamp: Optional[datetime | str] = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'connectionStatus')

    def __repr__(self) -> str:
        string = '{}.{}('\
            'connection={}, '\
            'available={}, '\
            'timestamp={}'\
            ')'
        return string.format(
            self.__class__.__module__,
            self.__class__.__name__,
            repr(self.connection),
            repr(self.available),
            repr(dttrans.to_iso8601(self.timestamp)),
        )

    @classmethod
    def _from_raw(cls, data: dict) -> ConnectionStatus:
        """
        Constructs a ConnectionStatus object from API response data.

        Parameters
        ----------
        data : dict
            API response data dictionary.

        Returns
        -------
        obj : ConnectionStatus
            Object constructed from the API response data.

        """

        # Construct the object with unpacked parameters.
        obj = cls(
            connection=data['connection'],
            available=data['available'],
            timestamp=data['updateTime'],
        )

        # Re-inherit from parent, but now providing response data.
        _EventData.__init__(obj, data, obj.event_type)

        return obj

    def __repack(self) -> dict:
        data: dict = dict()
        if self.connection is not None:
            data['connection'] = self.connection
        if self.available is not None:
            data['available'] = self.available
        if self.timestamp is not None:
            data['updateTime'] = self.timestamp
        return data


class EthernetStatus(_EventData):
    """
    Represents the data found in a ethernetStatus event.

    Attributes
    ----------
    mac_address : str
        MAC address of the local network interface.
    ip_address : str
        IP address of the Cloud Connector on the local network.
    timestamp : datetime
        Timestamp of when the event was received by a Cloud Connector.

    """

    def __init__(self,
                 mac_address: str,
                 ip_address: str,
                 timestamp: Optional[datetime | str] = None,
                 ):
        """
        Constructs the EthernetStatus object, inheriting parent class
        and setting the type-specific attributes.

        Parameters
        ----------
        mac_address : str
            MAC address of the local network interface.
        ip_address : str
            IP address of the Cloud Connector on the local network.
        timestamp : datetime, str, optional
            Timestamp in either datetime or string iso8601 format
            (i.e. yyyy-MM-ddTHH:mm:ssZ).

        """

        # Set parameter attributes.
        self.mac_address: str = mac_address
        self.ip_address: str = ip_address
        self.timestamp: Optional[datetime | str] = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'ethernetStatus')

    def __repr__(self) -> str:
        string = '{}.{}('\
            'mac_address={}, '\
            'ip_address={}, '\
            'timestamp={}'\
            ')'
        return string.format(
            self.__class__.__module__,
            self.__class__.__name__,
            repr(self.mac_address),
            repr(self.ip_address),
            repr(dttrans.to_iso8601(self.timestamp)),
        )

    @classmethod
    def _from_raw(cls, data: dict) -> EthernetStatus:
        """
        Constructs a EthernetStatus object from API response data.

        Parameters
        ----------
        data : dict
            API response data dictionary.

        Returns
        -------
        obj : EthernetStatus
            Object constructed from the API response data.

        """

        # Construct the object with unpacked parameters.
        obj = cls(
            mac_address=data['macAddress'],
            ip_address=data['ipAddress'],
            timestamp=data['updateTime'],
        )

        # Re-inherit from parent, but now providing response data.
        _EventData.__init__(obj, data, obj.event_type)

        return obj

    def __repack(self) -> dict:
        data: dict = dict()
        if self.mac_address is not None:
            data['macAddress'] = self.mac_address
        if self.ip_address is not None:
            data['ipAddress'] = self.ip_address
        if self.timestamp is not None:
            data['updateTime'] = self.timestamp
        return data


class CellularStatus(_EventData):
    """
    Represents the data found in a cellularStatus event.

    Attributes
    ----------
    signal_strength : int
        Cloud Connector cellular reception percentage.
    timestamp : datetime
        Timestamp of when the event was received by a Cloud Connector.

    """

    def __init__(self,
                 signal_strength: int,
                 timestamp: Optional[datetime | str] = None,
                 ):
        """
        Constructs the Temperature object.

        Parameters
        ----------
        signal_strength : int
            Cloud Connector cellular reception percentage.
        timestamp : datetime, str, optional
            Timestamp in either datetime or string iso8601 format
            (i.e. yyyy-MM-ddTHH:mm:ssZ).

        """

        # Set parameter attributes.
        self.signal_strength: int = signal_strength
        self.timestamp: Optional[datetime | str] = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'cellularStatus')

    def __repr__(self) -> str:
        string = '{}.{}('\
            'signal_strength={}, '\
            'timestamp={}'\
            ')'
        return string.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.signal_strength,
            repr(dttrans.to_iso8601(self.timestamp)),
        )

    @classmethod
    def _from_raw(cls, data: dict) -> CellularStatus:
        """
        Constructs a CellularStatus object from API response data.

        Parameters
        ----------
        data : dict
            API response data dictionary.

        Returns
        -------
        obj : CellularStatus
            Object constructed from the API response data.

        """

        # Construct the object with unpacked parameters.
        obj = cls(
            signal_strength=data['signalStrength'],
            timestamp=data['updateTime'],
        )

        # Re-inherit from parent using a full raw dictionary.
        _EventData.__init__(obj, data, obj.event_type)

        return obj

    def __repack(self) -> dict:
        data: dict = dict()
        if self.signal_strength is not None:
            data['signalStrength'] = self.signal_strength
        if self.timestamp is not None:
            data['updateTime'] = self.timestamp
        return data


class Event(dtoutputs.OutputBase):
    """
    Represents device events.

    Attributes
    ----------
    event_id : str
        Unique event ID.
    event_type : str
        Event type.
    device_id : str
        Unique ID of the source device.
    project_id : str
        Unique ID of the source project.
    data : :ref:`Event Data <eventdata>`
        An object representing type-specific event data.

    """

    def __init__(self, event: dict):
        # Inherit attributes from ResponseBase parent.
        dtoutputs.OutputBase.__init__(self, event)

        # Unpack attributes from dictionary.
        self.event_id: str = event['eventId']
        self.event_type: str = event['eventType']
        self.device_id: str = event['targetName'].split('/')[-1]
        self.project_id: str = event['targetName'].split('/')[1]

        # Since labelsChanged is the only event that does not
        # contain an updateTime field in data, we provide the
        # field as it is a massive convenience boost.
        if self.event_type == 'labelsChanged':
            event['data']['updateTime'] = event['timestamp']

        # Initialize the appropriate data class.
        self.data = _EventData.from_event_type(
            event['data'],
            self.event_type,
        )

    @classmethod
    def from_mixed_list(cls, events: list[dict]) -> list[Event]:
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


class __EventsMap():

    class __TypeNames():

        def __init__(self,
                     api_name: str,
                     attr_name: str,
                     class_name: str,
                     is_keyed: bool
                     ) -> None:
            self.api_name = api_name
            self.attr_name = attr_name
            self.class_name = class_name
            self.is_keyed = is_keyed

    _api_names = {
        'touch': __TypeNames(
            api_name='touch',
            attr_name='touch',
            class_name='Touch',
            is_keyed=True
        ),
        'temperature': __TypeNames(
            api_name='temperature',
            attr_name='temperature',
            class_name='Temperature',
            is_keyed=True
        ),
        'objectPresent': __TypeNames(
            api_name='objectPresent',
            attr_name='object_present',
            class_name='ObjectPresent',
            is_keyed=True
        ),
        'humidity': __TypeNames(
            api_name='humidity',
            attr_name='humidity',
            class_name='Humidity',
            is_keyed=True
        ),
        'objectPresentCount': __TypeNames(
            api_name='objectPresentCount',
            attr_name='object_present_count',
            class_name='ObjectPresentCount',
            is_keyed=True
        ),
        'touchCount': __TypeNames(
            api_name='touchCount',
            attr_name='touch_count',
            class_name='TouchCount',
            is_keyed=True
        ),
        'waterPresent': __TypeNames(
            api_name='waterPresent',
            attr_name='water_present',
            class_name='WaterPresent',
            is_keyed=True
        ),
        'networkStatus': __TypeNames(
            api_name='networkStatus',
            attr_name='network_status',
            class_name='NetworkStatus',
            is_keyed=True,
        ),
        'batteryStatus': __TypeNames(
            api_name='batteryStatus',
            attr_name='battery_status',
            class_name='BatteryStatus',
            is_keyed=True,
        ),
        'labelsChanged': __TypeNames(
            api_name='labelsChanged',
            attr_name='labels_changed',
            class_name='LabelsChanged',
            is_keyed=False,
        ),
        'connectionStatus': __TypeNames(
            api_name='connectionStatus',
            attr_name='connection_status',
            class_name='ConnectionStatus',
            is_keyed=True,
        ),
        'ethernetStatus': __TypeNames(
            api_name='ethernetStatus',
            attr_name='ethernet_status',
            class_name='EthernetStatus',
            is_keyed=True,
        ),
        'cellularStatus': __TypeNames(
            api_name='cellularStatus',
            attr_name='cellular_status',
            class_name='CellularStatus',
            is_keyed=True,
        )
    }


_EVENTS_MAP = __EventsMap()

_EventType = Union[
    Touch, Temperature, ObjectPresent, Humidity, ObjectPresentCount,
    TouchCount, WaterPresent, NetworkStatus, NetworkStatusCloudConnector,
    BatteryStatus, LabelsChanged, ConnectionStatus, EthernetStatus,
    CellularStatus,
]
