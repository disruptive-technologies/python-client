from __future__ import annotations

from typing import Optional

import disruptive
import disruptive.logging as dtlog
import disruptive.requests as dtrequests
import disruptive.outputs as dtoutputs


class DataConnector(dtoutputs.OutputBase):
    """
    Represents a Data Connector.

    When a Data Connector response is received, the content
    is unpacked and the related attributes are set.

    Attributes
    ----------
    dataconnector_id : str
        Unique Data Connector ID.
    project_id : str
        Unique ID of the project where the Data Connector resides.
    display_name : str
        The provided display name.
    dataconnector_type : str
        Data Connector type. Currently, only HTTP_PUSH is available.
    status : str
        Whether the Data Connector is
        "ACTIVE", "USER_DISABLED", or "SYSTEM_DISABLED".
    config : HttpPushConfig, None
        An object representing the type-specific configuration.
        If an unknown Data Connector type is receiver, this is None.
    event_Types : list[str]
        List of event types that should be forwarded.
        If empty, all event types are forwarded.
    labels : list[str]
        Device labels are not included by default and will only be forwarded
        with the event if the key is specified in this list.

    """

    # Constants for the various dataconnector configuration types.
    HTTP_PUSH = 'HTTP_PUSH'
    DATACONNECTOR_TYPES = [HTTP_PUSH]

    def __init__(self, dataconnector: dict) -> None:
        """
        Constructs the Data Connector object by unpacking
        the raw Data Connector response.

        Parameters
        ----------
        dataconnector : dict
            Unmodified Data Connector response dictionary.

        """

        # Inherit from OutputBase parent.
        dtoutputs.OutputBase.__init__(self, dataconnector)

        # Unpack attributes from dictionary.
        self.dataconnector_id = dataconnector['name'].split('/')[-1]
        self.project_id = dataconnector['name'].split('/')[1]
        self.status = dataconnector['status']
        self.display_name = dataconnector['displayName']
        self.event_types = dataconnector['events']
        self.labels = dataconnector['labels']
        self.dataconnector_type = dataconnector['type']
        self.config = self._from_dict(dataconnector)

    @classmethod
    def get_dataconnector(cls,
                          dataconnector_id: str,
                          project_id: str,
                          **kwargs,
                          ) -> DataConnector:
        """
        Gets the current state of a single Data Connector.

        Parameters
        ----------
        dataconnector_id : str
            Unique Data Connector ID.
        project_id : str
            Unique project ID.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_attempts: int, optional
            Number of times a request is attempted before giving up.

        Returns
        -------
        dataconnector : DataConnector
            Object representing the target Data Connector.

        Examples
        --------
        >>> # Fetch information about a specific Data Connector.
        >>> dcon = disruptive.DataConnector.get_dataconnector(
        ...     dataconnector_id='<DATACONNECTOR_ID>',
        ...     project_id='<PROJECT_ID>',
        ... )

        """

        # Construct URL
        url = '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)

        # Return DataConnector object of GET request response.
        return cls(dtrequests.DTRequest.get(
            url=url,
            **kwargs,
        ))

    @classmethod
    def list_dataconnectors(cls,
                            project_id: str,
                            **kwargs,
                            ) -> list[DataConnector]:
        """
        Gets a list of the current state of all Data Connectors in a project.

        Parameters
        ----------
        project_id : str
            Unique project ID.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_attempts: int, optional
            Number of times a request is attempted before giving up.

        Returns
        -------
        dataconnectors : list[DataConnector]
            List of objects each representing a Data Connector.

        Examples
        --------
        >>> # List information about all Data Connectors in a project.
        >>> dcons = disruptive.DataConnector.list_dataconnectors(
        ...     project_id='<PROJECT_ID>',
        ... )

        """

        # Return list of DataConnector objects of paginated GET response.
        dataconnectors = dtrequests.DTRequest.paginated_get(
            url='/projects/{}/dataconnectors'.format(project_id),
            pagination_key='dataConnectors',
            **kwargs,
        )
        return [cls(dcon) for dcon in dataconnectors]

    @classmethod
    def create_dataconnector(cls,
                             project_id: str,
                             config: disruptive.DataConnector.HttpPushConfig,
                             display_name: str = '',
                             status: str = 'ACTIVE',
                             event_types: list[str] = [],
                             labels: list[str] = [],
                             **kwargs,
                             ) -> DataConnector:
        """
        Creates a new Data Connector in the specified project.

        Parameters
        ----------
        project_id : str
            Unique project ID.
        config : HttpPushConfig
            An object representing the type-specific configuration.
        display_name : str, optional
            Sets a display name for the project.
        status : {"ACTIVE", "USER_DISABLED"} strm optional
            Status of the new Data Connector.
        event_types : list[str], optional
            List of event types the Data Connector should forward.
        labels : list[str], optional
            List of labels to forward with each event.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_attempts: int, optional
            Number of times a request is attempted before giving up.

        Returns
        -------
        dataconnector : DataConnector
            Object representing the newly created Data Connector.

        Examples
        --------
        >>> # Create a new Data Connector.
        >>> dcon = disruptive.DataConnector.create_dataconnector(
        ...     project_id='<PROJECT_ID>',
        ...     config=disruptive.DataConnector.HttpPushConfig(
        ...         url='<HTTPS_ENDPOINT_URL>',
        ...         signature_secret='some-good-secret',
        ...     ),
        ...     display_name='my-first-dcon',
        ... )

        """

        # Construct request body dictionary.
        body: dict = dict()
        body['status'] = status
        body['events'] = event_types
        body['labels'] = labels
        if len(display_name) > 0:
            body['displayName'] = display_name

        # Add the appropriate field depending on config.
        body['type'] = config.dataconnector_type
        key, value = config._to_dict()
        body[key] = value

        # Construct URL.
        url = '/projects/{}/dataconnectors'.format(project_id)

        # Return DataConnector object of POST request response.
        return cls(dtrequests.DTRequest.post(
            url=url,
            body=body,
            **kwargs,
        ))

    @classmethod
    def update_dataconnector(
        cls,
        dataconnector_id: str,
        project_id: str,
        config: Optional[disruptive.DataConnector.HttpPushConfig] = None,
        display_name: Optional[str] = None,
        status: Optional[str] = None,
        event_types: Optional[list[str]] = None,
        labels: Optional[list[str]] = None,
        **kwargs,
    ) -> DataConnector:
        """
        Updates the attributes of a Data Connector.
        All parameters that are provided will be updated.

        Parameters
        ----------
        dataconnector_id : str
            Unique ID of the Data Connector to update.
        project_id : str
            Unique ID of the project that contains the Data Connector.
        config : HttpPushConfig, optional
            An object representing the type-specific configuration.
        display_name : str, optional
            Sets a display name for the Data Connector.
        status : {"ACTIVE", "USER_DISABLED"} str, optional
            Status of the Data Connector.
        event_types : list[str], optional
            List of event types the Data Connector should forward.
        labels : list[str], optional
            List of labels to forward with each event.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_attempts: int, optional
            Number of times a request is attempted before giving up.

        Returns
        -------
        dataconnector : DataConnector
            Object representing the updated Data Connector.

        Examples
        --------
        >>> # Update only the display_name of a Data Connector.
        >>> dcon = disruptive.DataConnector.update_dataconnector(
        ...     dataconnector_id='<DATACONNECTOR_ID>',
        ...     project_id='<PROJECT_ID>',
        ...     display_name='new-name',
        ... )

        >>> # Update both the display_name, labels, and forwarded event types.
        >>> dcon = disruptive.DataConnector.update_dataconnector(
        ...     dataconnector_id='<DATACONNECTOR_ID>',
        ...     project_id='<PROJECT_ID>',
        ...     display_name='new-name',
        ...     labels=['room-number', 'customer-id'],
        ...     event_types=[
        ...         disruptive.events.TOUCH,
        ...         disruptive.events.TEMPERATURE,
        ...         ],
        ... )

        """

        # Construct request body dictionary.
        body: dict = dict()
        if display_name is not None:
            body['displayName'] = display_name
        if status is not None:
            body['status'] = status
        if event_types is not None:
            body['events'] = event_types
        if labels is not None:
            body['labels'] = labels

        # Add the appropriate field depending on config.
        if config is not None:
            key, value = config._to_dict()
            body[key] = value

        # Construct URL.
        url = '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)

        # Return DataConnector object of PATCH request response.
        return cls(dtrequests.DTRequest.patch(
            url=url,
            body=body,
            **kwargs,
        ))

    @classmethod
    def delete_dataconnector(cls,
                             dataconnector_id: str,
                             project_id: str,
                             **kwargs,
                             ) -> None:
        """
        Deletes the specified Data Connector.

        Parameters
        ----------
        dataconnector_id : str
            Unique ID of the Data Connector to delete.
        project_id : str
            Unique ID of the project that contains the Data Connector.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_attempts: int, optional
            Number of times a request is attempted before giving up.

        Examples
        --------
        >>> # Delete the specified Data Connector.
        >>> disruptive.DataConnector.delete_dataconnector(
        ...     dataconnector_id='<DATACONNECTOR_ID>',
        ...     project_id='<PROJECT_ID>',
        ... )

        """

        # Construct URL.
        url = '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)

        # Send DELETE request, but return nothing.
        dtrequests.DTRequest.delete(
            url=url,
            **kwargs,
        )

    @classmethod
    def get_metrics(cls,
                    dataconnector_id: str,
                    project_id: str,
                    **kwargs,
                    ) -> Metric:
        """
        Get the metrics of the last 3 hours for a Data Connector.

        Parameters
        ----------
        dataconnector_id : str
            Unique ID of the Data Connector to list metrics for.
        project_id : str
            Unique ID of the project that contains the Data Connector.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_attempts: int, optional
            Number of times a request is attempted before giving up.

        Returns
        -------
        metric : Metric
            Object representing the fetched metrics.

        Examples
        --------
        >>> # Get the 3h metrics of the specified Data Connector.
        >>> metrics = disruptive.DataConnector.get_metrics(
        ...     dataconnector_id='<DATACONNECTOR_ID>',
        ...     project_id='<PROJECT_ID>',
        ... )

        """

        # Construct URL.
        url = '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)
        url += ':metrics'

        # Return Metric object of GET request response.
        return Metric(dtrequests.DTRequest.get(
            url=url,
            **kwargs,
        ))

    @classmethod
    def sync_dataconnector(cls,
                           dataconnector_id: str,
                           project_id: str,
                           **kwargs,
                           ) -> None:
        """
        Synchronizes the current Data Connector state.

        This method let's you synchronize your cloud service with the current
        state of the devices in your project. This entails pushing the most
        recent event of each type for all devices in your project.

        Parameters
        ----------
        dataconnector_id : str
            Unique ID of the Data Connector to synchronize.
        project_id : str
            Unique ID of the project that contains the Data Connector.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_attempts: int, optional
            Number of times a request is attempted before giving up.

        Examples
        --------
        >>> # Synchronize the specified Data Connector.
        >>> disruptive.DataConnector.sync_dataconnector(
        ...     dataconnector_id='<DATACONNECTOR_ID>',
        ...     project_id='<PROJECT_ID>',
        ... )

        """

        # Construct URL.
        url = '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)
        url += ':sync'

        # Send POST request, but return nothing.
        dtrequests.DTRequest.post(
            url=url,
            **kwargs,
        )

    @classmethod
    def _from_dict(cls, dataconnector: dict):
        # Isolate the dataconnector type.
        dataconnector_type = dataconnector['type']

        # Select the appropriate config depending on type.
        if dataconnector_type == 'HTTP_PUSH':
            # Isolate config field.
            config = dataconnector['httpConfig']

            # Create and return an HttpPush object.
            return cls.HttpPushConfig(
                url=config['url'],
                signature_secret=config['signatureSecret'],
                headers=config['headers'],
            )
        else:
            # If this else statement runs, no config is available for type.
            dtlog.warning('No config available for {} dataconnectors.'.format(
                dataconnector_type
            ))
            return None

    class HttpPushConfig():
        """
        Type-specific configurations for the HTTP_PUSH Data Connector.

        Attributes
        ----------
        url : str
            Endpoint URL towards which events are forwarded. Must be HTTPS.
        signature_secret : str
            Secret with which each forwarded event is signed.
        headers : dict[str, str]
            Dictionary of headers to include with each forwarded event.

        """

        dataconnector_type = 'HTTP_PUSH'

        def __init__(self,
                     url: Optional[str] = None,
                     signature_secret: Optional[str] = None,
                     headers: Optional[dict] = None,
                     ) -> None:
            """
            Constructs the HttpPushConfig object.

            Parameters
            ----------
            url : str, optional
                Endpoint URL towards which events are forwarded. Must be HTTPS.
            signature_secret : str, optional
                Secret with which each forwarded event is signed.
            headers : dict[str, str], optional
                Dictionary of headers to include with each forwarded event.

            """

            # Set parameter attributes.
            self.url = url
            self.signature_secret = signature_secret
            self.headers = headers

        def _to_dict(self):
            config: dict = dict()
            if self.url is not None:
                config['url'] = self.url
            if self.signature_secret is not None:
                config['signatureSecret'] = self.signature_secret
            if self.headers is not None:
                config['headers'] = self.headers
            return 'httpConfig', config


class Metric(dtoutputs.OutputBase):
    """
    Represents the metrics for a dataconnector over the last 3 hours.

    Attributes
    ----------
    success_count : int
        Number of 2xx responses.
    error_count : int
        Number of non-2xx responses.
    latency : str
        Average latency.

    """

    def __init__(self, metric: dict) -> None:
        """
        Constructs the Metric object by unpacking the raw response.

        """

        # Inherit attributes from ResponseBase parent.
        dtoutputs.OutputBase.__init__(self, metric)

        # Unpack attributes from dictionary.
        self.success_count = metric['metrics']['successCount']
        self.error_count = metric['metrics']['errorCount']
        self.latency = metric['metrics']['latency99p']
