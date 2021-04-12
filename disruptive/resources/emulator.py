from __future__ import annotations

# Standard library imports.
from typing import Optional

# Project imports.
import disruptive
import disruptive.requests as dtrequests
from disruptive.resources.device import Device


class Emulator():
    """
    Contains staticmethods for the emulator resource.
    Used for namespacing only and thus does not have a constructor

    """

    @staticmethod
    def get_device(project_id: str,
                   device_id: str,
                   **kwargs,
                   ) -> Device:
        """
        Gets an emulated device specified by its project and ID.

        Parameters
        ----------
        project_id : str
            Unique ID of the target project.
        device_id : str
            Unique ID of the target device.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        device : Device
            Object representing the specified emulated device.

        """

        # Construct URL
        url = disruptive.emulator_url
        url += '/projects/{}/devices/{}'.format(project_id, device_id)

        # Return Device object of GET request response.
        return Device(dtrequests.generic_request(
            method='GET',
            url=url,
            **kwargs,
        ), emulated=True)

    @staticmethod
    def list_devices(project_id: str,
                     **kwargs,
                     ) -> list[Device]:
        """
        List all available emulated devices in the specified project.

        Parameters
        ----------
        project_id : str
            Unique ID of the target project.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        page_size: int, optional
            Number of devices [1, 100] to get per request. Defaults to 100.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        devices : list[Device]
            List of objects each representing an emulated device.

        """

        # Return list of Device objects of paginated GET response.
        devices = dtrequests.auto_paginated_list(
            url=disruptive.emulator_url + '/projects/{}/devices'.format(
                project_id
            ),
            pagination_key='devices',
            params={},
            **kwargs,
        )
        return [Device(device, emulated=True) for device in devices]

    @staticmethod
    def create_device(project_id: str,
                      device_type: str,
                      display_name: Optional[str] = None,
                      labels: Optional[dict[str, str]] = {},
                      **kwargs,
                      ) -> Device:
        """
        Create a new emulated device with specified type and project.

        Parameters
        ----------
        project_id : str
            Unique ID of the target project.
        device_type : str
            Specifies which device type to create.
        display_name : str, optional
            Provides a display name to the device.
        labels : dict[str, str], optional
            Set labels for the new device.
            Format: {'key': 'value'}.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        device : Device
            Object representing the created emulated device.

        """

        # Construct URL
        url = disruptive.emulator_url
        url += '/projects/{}/devices'.format(project_id)

        # Construct body dictionary.
        body: dict = dict()
        body['type'] = device_type
        body['labels'] = labels

        # Add display_name to labels dictionary in body.
        if display_name is not None:
            body['labels']['name'] = display_name

        # Return Device object of GET request response.
        return Device(dtrequests.generic_request(
            method='POST',
            url=url,
            body=body,
            **kwargs,
        ), emulated=True)

    @staticmethod
    def delete_device(project_id: str,
                      device_id: str,
                      **kwargs,
                      ) -> None:
        """
        Deletes the specified emulated device.

        Parameters
        ----------
        project_id : str
            Unique ID of the target project.
        device_id : str
            Specifies which device type to delete.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        """

        # Construct URL
        url = disruptive.emulator_url
        url += '/projects/{}/devices/{}'.format(project_id, device_id)

        # Send DELETE request, but return nothing.
        dtrequests.generic_request(
            method='DELETE',
            url=url,
            **kwargs,
        )

    @staticmethod
    def publish_event(project_id: str,
                      device_id: str,
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
                      **kwargs,
                      ) -> None:
        """
        From the specified device, publish an event of the given type.

        Parameters
        ----------
        project_id : str
            Unique ID of the target project.
        device_id : str
            Unique ID of the target device.
        data : :ref:`Event Data`
            An object representing the event data to be published.
            Can be any of the listed :ref:`Event Data` classes.
            labelsChanged is not supported when publishing emulated events.
            The chosen :ref:`Event Data` must be supported by the device.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        """

        # Construct URL
        url = disruptive.emulator_url
        url += '/projects/{}/devices/{}:publish'.format(project_id, device_id)

        # Send POST request, but return nothing.
        dtrequests.generic_request(
            method='POST',
            url=url,
            body={data.event_type: data._raw},
            **kwargs,
        )
