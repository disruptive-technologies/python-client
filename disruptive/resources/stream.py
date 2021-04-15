from __future__ import annotations

# Standard library imports
from typing import Generator, Optional

# Project Imports.
import disruptive.requests as dtrequests
from disruptive.events.events import Event
from disruptive.authentication import Auth


class Stream():
    """
    Contains staticmethods for streaming events.
    Used for namespacing only and thus does not have a constructor

    """

    @staticmethod
    def device(device_id: str,
               project_id: str,
               event_types: Optional[list[str]] = None,
               **kwargs,
               ) -> Generator:
        """
        Streams events for a single device.

        Implements a basic retry-routine. If connection is lost, the stream
        will attempt to reconnect with an exponential backoff. Potential
        lost events while reconnecting are, however, not acocunted for.

        Parameters
        ----------
        device_id : str
            Unique ID of the target device.
        project_id : str
            Unique ID of the target project.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.

        Returns
        -------
        stream : Generator
            A python Generator type that yields each new event in the stream.

        Examples
        --------
        >>> for event in dt.Stream.device(project_id, device_id):
        ...     print(event)

        """

        # Construct URL.
        url = '/projects/{}/devices/{}:stream'.format(
            project_id,
            device_id
        )

        # Construct parameters dictionary.
        params: dict = dict()
        if event_types is not None:
            params['event_types'] = event_types

        # Relay generator output.
        for event in dtrequests.DTRequest.stream(url, params=params, **kwargs):
            yield Event(event)

    @staticmethod
    def project(project_id: str,
                device_ids: Optional[list[str]] = None,
                label_filters: Optional[list[str]] = None,
                device_types: Optional[list[str]] = None,
                event_types: Optional[list[str]] = None,
                auth: Optional[Auth] = None,
                ) -> Generator:
        """
        Streams events for a multiple devices in a project.

        Implements a basic retry-routine. If connection is lost, the stream
        will attempt to reconnect with an exponential backoff. Potential
        lost events while reconnecting are, however, not acocunted for.

        Parameters
        ----------
        project_id : str
            Unique ID of the target project.
        device_ids : list[str], optional
            Only includes events from the specified device(s).
        label_filters : list[str], optional
            Only includes events from devices with specified label(s).
        device_types : list[str], optional
            Only includes events from devices with specified type(s).
        event_types : list[str], optional
            Only includes events of the specified type(s).
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.

        Returns
        -------
        stream : Generator
            A python Generator type that yields each new event in the stream.

        Examples
        --------
        >>> for event in dt.Stream.project(project_id):
        ...     print(event)

        """

        # Construct parameters dictionary.
        params: dict = dict()
        if device_ids is not None:
            params['device_ids'] = device_ids
        if device_types is not None:
            params['device_types'] = device_types
        if label_filters is not None:
            params['label_filters'] = label_filters
        if event_types is not None:
            params['event_types'] = event_types

        # Relay generator output.
        url = '/projects/{}/devices:stream'.format(project_id)
        for event in dtrequests.DTRequest.stream(url, params=params):
            yield Event(event)
