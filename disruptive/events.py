from __future__ import annotations

# Standard library imports.
from typing import Optional
from datetime import datetime

# Project imports.
import disruptive
import disruptive.outputs as dtoutputs
import disruptive.transforms as dttrans
import disruptive.log as dtlog
from disruptive.types import EventTypes


class _EventData(dtoutputs.OutputBase):
    """
    Parent class for all the different event data field types.

    Attributes are mainly inherited from OutputBase, and otherwise
    contains a few convenience methods for setting the correct child.

    Attributes
    ----------
    timestamp : datetime
        Timestamp of when the event was received by a Cloud Connector.

    """

    def __init__(self, data: dict, event_type: str) -> None:
        """
        Constructs the _EventData object by inheriting parent.

        """

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
            return child._from_raw(data[event_type])
        else:
            # Special case for labelsChanged event.
            return child._from_raw(data)

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
        # if event_type in [t.value['api_name'] for t in EventTypes]:
        if event_type in EventTypes._api_names:
            out = (
                getattr(
                    disruptive.events,
                    EventTypes._api_names[event_type].class_name
                ),
                EventTypes._api_names[event_type].is_keyed,
            )
            return out

        dtlog.log('Skipping unknown event type {}.'.format(event_type))
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
        Constructs the Touch object, inheriting parent class
        and setting the type-specific attributes.

        Parameters
        ----------
        timestamp : datetime, str, optional
            Timestamp of when the event was received by a Cloud Connector.

        """

        # Set parameter attributes.
        self.timestamp = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'touch')

    @classmethod
    def _from_raw(cls, data: dict):
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

    def __repack(self):
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
    timestamp : datetime
        Timestamp of when the event was received by a Cloud Connector.

    """

    def __init__(self,
                 celsius: Optional[float] = None,
                 timestamp: Optional[datetime | str] = None,
                 ) -> None:
        """
        Constructs the Temperature object, inheriting parent class
        and setting the type-specific attributes.

        Parameters
        ----------
        celsius : float, optional
            Temperature value in Celsius.
        timestamp : datetime, str, optional
            Timestamp of when the event was received by a Cloud Connector.

        """

        # Set parameter attributes.
        self.celsius = celsius
        self.fahrenheit = self.__celsius_to_fahrenheit(celsius)
        self.timestamp = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'temperature')

    @classmethod
    def _from_raw(cls, data: dict):
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

        # Construct the object with unpacked parameters.
        obj = cls(
            celsius=data['value'],
            timestamp=data['updateTime'],
        )

        # Re-inherit from parent, but now providing response data.
        _EventData.__init__(obj, data, obj.event_type)

        return obj

    def __repack(self):
        data: dict = dict()
        if self.celsius is not None:
            data['value'] = self.celsius
        if self.timestamp is not None:
            data['updateTime'] = self.timestamp
        return data

    def __celsius_to_fahrenheit(self, celsius: Optional[float]):
        """
        Converts Celsius temperature value to Fahrenheit.

        Parameters
        ----------
        celsius : float, None
            Temperature value in Celsius.

        Returns
        -------
        fahrenheit : float, None
            Temperature value in Fahrenheit if Celsius is not None.

        """

        if celsius is None:
            return None
        else:
            return (celsius * (9/5)) + 32


class ObjectPresent(_EventData):
    """
    Represents the data found in an objectPresent event.

    Attributes
    ----------
    state : str
        Indicates whether an object is PRESENT or NOT_PRESENT.
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
            Indicates whether an object is PRESENT or NOT_PRESENT.
        timestamp : datetime, str, optional
            Timestamp of when the event was received by a Cloud Connector.

        """

        # Set parameter attributes.
        self.state = state
        self.timestamp = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'objectPresent')

    @classmethod
    def _from_raw(cls, data: dict):
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

    def __repack(self):
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
    humidity : int
        Relative humidity in percent.
    timestamp : datetime
        Timestamp of when the event was received by a Cloud Connector.

    """

    def __init__(self,
                 temperature: Optional[float] = None,
                 humidity: Optional[float] = None,
                 timestamp: Optional[datetime | str] = None,
                 ):
        """
        Constructs the Humidity object, inheriting parent class
        and setting the type-specific attributes.

        Parameters
        ----------
        temperature : float, optional
            Temperature value in Celsius.
        humidity : float, optional
            Relative humidity in percent.
        timestamp : datetime, str, optional
            Timestamp of when the event was received by a Cloud Connector.

        """

        # Set parameter attributes.
        self.temperature = temperature
        self.humidity = humidity
        self.timestamp = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'humidity')

    @classmethod
    def _from_raw(cls, data: dict):
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
            temperature=data['temperature'],
            humidity=data['relativeHumidity'],
            timestamp=data['updateTime'],
        )

        # Re-inherit from parent, but now providing response data.
        _EventData.__init__(obj, data, obj.event_type)

        return obj

    def __repack(self):
        data: dict = dict()
        if self.temperature is not None:
            data['temperature'] = self.temperature
        if self.humidity is not None:
            data['relativeHumidity'] = self.humidity
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
        Constructs the ObjectPresentCount object, inheriting parent class
        and setting the type-specific attributes.

        Parameters
        ----------
        total : int
            The total number of times the sensor has detected the appearance
            or disappearance of an object over its lifetime.
        timestamp : datetime, str, optional
            Timestamp of when the event was received by a Cloud Connector.

        """

        # Set parameter attributes.
        self.total = total
        self.timestamp = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'objectPresentCount')

    @classmethod
    def _from_raw(cls, data: dict):
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

    def __repack(self):
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
        Constructs the TouchCount object, inheriting parent class
        and setting the type-specific attributes.

        Parameters
        ----------
        total : int
            The total number of times the sensor has been
            touched over its lifetime.
        timestamp : datetime, str, optional
            Timestamp of when the event was received by a Cloud Connector.

        """

        # Set parameter attributes.
        self.total = total
        self.timestamp = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'touchCount')

    @classmethod
    def _from_raw(cls, data: dict):
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

    def __repack(self):
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
        Constructs the WaterPresent object, inheriting parent class
        and setting the type-specific attributes.

        Parameters
        ----------
        state : str
            Indicates whether water is PRESENT or NOT_PRESENT.
        timestamp : datetime, str, optional
            Timestamp of when the event was received by a Cloud Connector.

        """

        # Set parameter attributes.
        self.state = state
        self.timestamp = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'waterPresent')

    @classmethod
    def _from_raw(cls, data: dict):
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

    def __repack(self):
        data: dict = dict()
        data['state'] = self.state
        if self.timestamp is not None:
            data['updateTime'] = self.timestamp
        return data


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
        signal_strength: Optional[int] = None,
        rssi: Optional[int] = None,
        transmission_mode: Optional[str] = None,
        cloud_connectors: Optional[list[NetworkStatusCloudConnector]] = None,
        timestamp: Optional[datetime | str] = None
    ) -> None:
        """
        Constructs the NetworkStatus object, inheriting parent class
        and setting the type-specific attributes.

        Parameters
        ----------
        signal_strength : int, optional
            The percentage signal strength (0% to 100%) of the strongest
            Cloud Connector, derived directly from the RSSI value.
        rssi : float, optional
            Raw Received Signal Strength Indication (RSSI) as measured
            by the strongest Cloud Connector.
        transmission_mode : str, optional
            Indicated whether the sensor is in
            LOW_POWER_STANDARD_MODE or HIGH_POWER_BOOST_MODE.
        cloud_connectors : list[NetworkStatusCloudConnector], optional
            List of the Cloud Connector that forwarded the event.
        timestamp : datetime, str, optional
            Timestamp of when the event was received by a Cloud Connector.

        """

        # Set attributes.
        self.signal_strength = signal_strength
        self.rssi = rssi
        self.transmission_mode = transmission_mode
        self.cloud_connectors = cloud_connectors
        self.timestamp = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'networkStatus')

    @classmethod
    def _from_raw(cls, data: dict):
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

    def __repack(self):
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
                if ccon.cloudconnector_id is not None:
                    ccon_data['id'] = ccon.cloudconnector_id
                if ccon.signal_strength is not None:
                    ccon_data['signalStrength'] = ccon.signal_strength
                if len(ccon_data) > 0:
                    data['cloud_connectors'].append(ccon_data)
        return data


class NetworkStatusCloudConnector(dtoutputs.OutputBase):
    """
    Represents a Cloud Connector found in the networkStatus event data.

    Attributes
    ----------
    cloudconnector_id : str
        Cloud Connector identifier.
    signal_strength : int
        The percentage signal strength (0% to 100%) between
        the sensor and Cloud Connector.
    rssi : int
        Raw Received Signal Strength Indication (RSSI) between
        the sensor and Cloud Connector.

    """

    def __init__(self,
                 cloudconnector_id: Optional[str] = None,
                 signal_strength: Optional[int] = None,
                 rssi: Optional[int] = None,
                 ):
        """
        Constructs the NetworkStatusCloudConnector object, inheriting
        parent class and setting the type-specific attributes.

        Parameters
        ----------
        id : str
            Cloud Connector identifier.
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
        self.cloudconnector_id = cloudconnector_id
        self.signal_strength = signal_strength
        self.rssi = rssi

    @classmethod
    def _from_raw(cls, data: dict):
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
            cloudconnector_id=data['id'],
            signal_strength=data['signalStrength'],
            rssi=data['rssi'],
        )

        # Re-inherit from parent, but now providing response data.
        dtoutputs.OutputBase.__init__(obj, data)

        return obj


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
                 percentage: Optional[int] = None,
                 timestamp: Optional[datetime | str] = None,
                 ) -> None:
        """
        Constructs the Temperature object, inheriting parent class
        and setting the type-specific attributes.

        Parameters
        ----------
        percentage : int, optional
            A coarse percentage estimate (0% to 100%) of the remaining battery.
        timestamp : datetime, str, optional
            Timestamp of when the event was received by a Cloud Connector.

        """

        # Inherit parent _EventData class init with repacked data dictionary.
        self.percentage = percentage
        self.timestamp = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'batteryStatus')

    @classmethod
    def _from_raw(cls, data: dict):
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

    def __repack(self):
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
        Constructs the LabelsChanged object, inheriting parent class
        and setting the type-specific attributes.

        Parameters
        ----------
        added : dict[str, str]
            Keys and values of new labels added.
        modified : dict[str, str]
            New keys and values of modified labels.
        removed : list[str]
            List of keys of removed labels.
        timestamp : datetime, str, optional
            Timestamp of when the event was received by a Cloud Connector.

        """

        # Set parameter attributes.
        self.added = added
        self.modified = modified
        self.removed = removed
        self.timestamp = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'labelsChanged')

    @classmethod
    def _from_raw(cls, data: dict):
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

    def __repack(self):
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
        Whether the Cloud Connector is on ETHERNET, CELLULAR, or OFFLINE.
    available : str
        Lists available connections. Can contain ETHERNET, CELLULAR, or both.
    timestamp : datetime
        Timestamp of when the event was received by a Cloud Connector.

    """

    def __init__(self,
                 connection: Optional[str] = None,
                 available: Optional[str] = None,
                 timestamp: Optional[datetime | str] = None,
                 ):
        """
        Constructs the ConnectionStatus object, inheriting parent class
        and setting the type-specific attributes.

        Parameters
        ----------
        connection : str, optional
            Whether the Cloud Connector is on ETHERNET, CELLULAR, or OFFLINE.
        available : str, optional
            Lists available connections.
            Can contain ETHERNET, CELLULAR, or both.
        timestamp : datetime, str, optional
            Timestamp of when the event was received by a Cloud Connector.

        """

        # Set parameter attributes.
        self.connection = connection
        self.available = available
        self.timestamp = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'connectionStatus')

    @classmethod
    def _from_raw(cls, data: dict):
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

    def __repack(self):
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
                 mac_address: Optional[str] = None,
                 ip_address: Optional[str] = None,
                 timestamp: Optional[datetime | str] = None,
                 ):
        """
        Constructs the EthernetStatus object, inheriting parent class
        and setting the type-specific attributes.

        Parameters
        ----------
        mac_address : str, optional
            MAC address of the local network interface.
        ip_address : str, optional
            IP address of the Cloud Connector on the local network.
        timestamp : datetime, str, optional
            Timestamp of when the event was received by a Cloud Connector.

        """

        # Set parameter attributes.
        self.mac_address = mac_address
        self.ip_address = ip_address
        self.timestamp = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'ethernetStatus')

    @classmethod
    def _from_raw(cls, data: dict):
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

    def __repack(self):
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
                 signal_strength: Optional[int] = None,
                 timestamp: Optional[datetime | str] = None,
                 ):
        """
        Constructs the Temperature object, inheriting parent class
        and setting the type-specific attributes.

        Parameters
        ----------
        signal_strength : int, optional
            Cloud Connector cellular reception percentage.
        timestamp : datetime, str, optional
            Timestamp of when the event was received by a Cloud Connector.

        """

        # Set parameter attributes.
        self.signal_strength = signal_strength
        self.timestamp = timestamp

        # Inherit parent _EventData class init with repacked data dictionary.
        _EventData.__init__(self, self.__repack(), 'cellularStatus')

    @classmethod
    def _from_raw(cls, data: dict):
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

    def __repack(self):
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
    data : :ref:`Event Data`
        An object representing type-specific event data.

    """

    def __init__(self, event: dict):
        # Inherit attributes from ResponseBase parent.
        dtoutputs.OutputBase.__init__(self, event)

        # Unpack attributes from dictionary.
        self.event_id = event['eventId']
        self.event_type = event['eventType']
        self.device_id = event['targetName'].split('/')[-1]
        self.project_id = event['targetName'].split('/')[1]

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
