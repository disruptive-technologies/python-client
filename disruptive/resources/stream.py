from __future__ import annotations

# Standard library imports
from typing import Generator, Optional

# Project Imports.
import disruptive.requests as dtrequests
from disruptive.events.events import Event


class Stream():
    """
    Contains staticmethods for streaming events.
    Used for namespacing only and thus does not have a constructor

    """

    @staticmethod
    def event_stream(project_id: str,
                     device_ids: Optional[list[str]] = None,
                     label_filters: Optional[list[str]] = None,
                     device_types: Optional[list[str]] = None,
                     event_types: Optional[list[str]] = None,
                     **kwargs,
                     ) -> Generator:
        """
        Streams events for one, several, or all devices in a project.

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
            Only includes events from devices with specified
            :ref:`type(s) <device_type_constants>`.
        event_types : list[str], optional
            Only includes events of the specified :ref:`type(s) <event_types>`.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        stream : Generator
            A python Generator type that yields each new event in the stream.

        Examples
        --------
        >>> # Stream real-time events from all devices in a project.
        >>> for event in dt.Stream.event_stream('<PROJECT_ID>'):
        ...     print(event)

        >>> # Stream real-time events from one device in a project.
        >>> for event in dt.Stream.event_stream(project_id='<PROJECT_ID>',
        ...                                     device_ids=['<DEVICE_ID>'],
        ...                                     ):
        ...     print(event)

        >>> # Stream real-time touch events from a select list of
        >>> # humidity- and touch sensors, but only those with a 'v1' label.
        >>> for e in dt.Stream.event_stream(project_id='<PROJECT_ID>',
        ...                                 device_ids=[
        ...                                     '<DEVICE_ID_1>',
        ...                                     '<DEVICE_ID_2>',
        ...                                     '<DEVICE_ID_3>',
        ...                                 ]
        ...                                 event_types=['touch'],
        ...                                 device_types=['humidity', 'touch'],
        ...                                 label_filters=['v1'],
        ...                                 ):
        ...     print(e.data)

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
        for event in dtrequests.DTRequest.stream(url, params=params, **kwargs):
            yield Event(event)
