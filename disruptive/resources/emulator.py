from __future__ import annotations

from typing import Optional, Any

import disruptive
import disruptive.requests as dtrequests
from disruptive.resources.device import Device


class Emulator():
    """
    Contains staticmethods for the emulator resource.
    Used for namespacing only and thus does not have a constructor

    """

    @staticmethod
    def create_device(project_id: str,
                      device_type: str,
                      display_name: Optional[str] = None,
                      labels: Optional[dict[str, str]] = {},
                      **kwargs: Any,
                      ) -> Device:
        """
        Create a new emulated device with specified type and project.

        Parameters
        ----------
        project_id : str
            Unique ID of the target project.
        device_type : str
            Specifies which device
            :ref:`type <device_type_constants>` to create.
        display_name : str, optional
            Provides a display name to the device.
        labels : dict[str, str], optional
            Set labels for the new device.
            Format: {'key': 'value'}.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        device : Device
            Object representing the created emulated device.

        Examples
        --------
        >>> # Create a new emulated humidity sensor.
        >>> disruptive.Emulator.create_device(
        ...     project_id='<PROJECT_ID>',
        ...     device_type=disruptive.Device.HUMIDITY,
        ...     display_name='new-humidity-sensor',
        ...     labels={
        ...         'room-number': '99',
        ...         'customer': 'x7',
        ...     },
        ... )

        """

        # Construct URL
        url = '/projects/{}/devices'.format(project_id)

        # Construct body dictionary.
        body: dict = dict()
        body['type'] = device_type
        body['labels'] = labels

        # Add display_name to labels dictionary in body.
        if display_name is not None:
            body['labels']['name'] = display_name

        # Return Device object of GET request response.
        return Device(dtrequests.DTRequest.post(
            url=url,
            base_url=disruptive.emulator_base_url,
            body=body,
            **kwargs,
        ))

    @staticmethod
    def delete_device(device_id: str,
                      project_id: str,
                      **kwargs: Any,
                      ) -> None:
        """
        Deletes the specified emulated device.

        Parameters
        ----------
        device_id : str
            Specifies which device type to delete.
        project_id : str
            Unique ID of the target project.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Examples
        --------
        >>> # Delete an emulated device.
        >>> disruptive.Emulator.delete_device('<DEVICE_ID>', '<PROJECT_ID>')

        """

        # Construct URL
        url = '/projects/{}/devices/{}'.format(project_id, device_id)

        # Send DELETE request, but return nothing.
        dtrequests.DTRequest.delete(
            url=url,
            base_url=disruptive.emulator_base_url,
            **kwargs,
        )

    @staticmethod
    def publish_event(device_id: str,
                      project_id: str,
                      data: disruptive.events.Touch |
                      disruptive.events.Temperature |
                      disruptive.events.ObjectPresent |
                      disruptive.events.Humidity |
                      disruptive.events.ObjectPresentCount |
                      disruptive.events.TouchCount |
                      disruptive.events.WaterPresent |
                      disruptive.events.NetworkStatus |
                      disruptive.events.BatteryStatus |
                      disruptive.events.ConnectionStatus |
                      disruptive.events.EthernetStatus |
                      disruptive.events.CellularStatus,
                      **kwargs: Any,
                      ) -> None:
        """
        From the specified device, publish an event of the given type.

        Parameters
        ----------
        device_id : str
            Unique ID of the target device.
        project_id : str
            Unique ID of the target project.
        data : :ref:`Event Data <eventdata>`
            An object representing the event data to be published.
            Can be any of the listed Event Data classes.
            :code:`labelsChanged` is not supported
            when publishing emulated events.
            The chosen Event Data must be supported by the device.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Examples
        --------
        >>> # Publish a Humidity event from an emulated device.
        >>> disruptive.Emulator.publish_event(
        ...     device_id='<DEVICE_ID>',
        ...     project_id='<PROJECT_ID>',
        ...     data=disruptive.events.Humidity(
        ...         celsius=23,
        ...         humidity=76,
        ...     ),
        ... )

        """

        # Construct URL
        url = '/projects/{}/devices/{}:publish'.format(project_id, device_id)

        # Send POST request, but return nothing.
        dtrequests.DTRequest.post(
            url=url,
            base_url=disruptive.emulator_base_url,
            body={data.event_type: data._raw},
            **kwargs,
        )
