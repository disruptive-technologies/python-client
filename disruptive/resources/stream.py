from __future__ import annotations

from typing import Generator, Optional, Any

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
                     label_filters: Optional[dict] = None,
                     device_types: Optional[list[str]] = None,
                     event_types: Optional[list[str]] = None,
                     **kwargs: Any,
                     ) -> Generator:
        """
        Stream events for one, multiple, or all device(s) in a project.

        Implements a basic retry-routine. If connection is lost, the stream
        will attempt to reconnect with an exponential backoff. Events that
        are published during reconnection are not accounted for.

        If you want to forward your data in a server-to-server
        integration, consider using Data Connectors for a simpler
        and more reliable service with an added at-least-once guarantee.

        Parameters
        ----------
        project_id : str
            Unique ID of the target project.
        device_ids : list[str], optional
            Only includes events from the specified device(s).
        label_filters : dict[str, Optional[str]], optional
            Filter devices by their labels. Takes
            the form :code:`{"key": "value"}`, or :code:`{"key": None}` to
            allow any label value.
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
        >>> # Sream real-time events from all devices in a project.
        >>> for event in dt.Stream.event_stream('<PROJECT_ID>'):
        ...     print(event)

        >>> # Sream real-time temperature- and touch events
        >>> # only from temperature devices that have set
        >>> # the labels `room-number=99` or `group=red`.
        >>> stream = dt.Stream.event_stream(
        ...     project_id='<PROJECT_ID>',
        ...     label_filters={
        ...         'room-number': '99',
        ...         'group': 'red',
        ...     },
        ...     device_types=[
        ...         dt.Device.TEMPERATURE,
        ...     ],
        ...     event_types=[
        ...         dt.events.TOUCH,
        ...         dt.events.TEMPERATURE,
        ...     ],
        ... )
        >>>
        >>> for event in stream:
        ...     print(event)

        """

        # Construct parameters dictionary.
        params: dict = dict()
        if device_ids is not None:
            params['device_ids'] = device_ids
        if device_types is not None:
            params['device_types'] = device_types
        if label_filters is not None:
            params['label_filters'] = []
            for key in label_filters:
                if isinstance(label_filters[key], str):
                    string = key + '=' + label_filters[key]
                    params['label_filters'].append(string)
                else:
                    params['label_filters'].append(key)
        if event_types is not None:
            params['event_types'] = event_types

        # Relay generator output.
        url = '/projects/{}/devices:stream'.format(project_id)
        for event in dtrequests.DTRequest.stream(url, params=params, **kwargs):
            yield Event(event)
