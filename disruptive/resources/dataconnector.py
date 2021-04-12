from __future__ import annotations

# Standard library imports.
from typing import Optional

# Project imports.
import disruptive as dt
import disruptive.requests as dtrequests
import disruptive.outputs as dtoutputs
from disruptive.outputs import Metric


class DataConnector(dtoutputs.OutputBase):
    """
    Represents a dataconnector.

    When a dataconnector response is received, the content
    is unpacked and the related attributes are updated.

    Attributes
    ----------
    dataconnector_id : str
        Unique dataconnector ID.
    display_name : str
        The provided display name.
    dataconnector_type : str
        Dataconnector type. Currently only HTTP_PUSH is available.
    status : str
        Whether the dataconnector is ACTIVE, USER_DISABLED, or SYSTEM_DISABLED.

    """

    def __init__(self, dataconnector: dict) -> None:
        """
        Constructs the DataConnector object by unpacking
        the raw dataconnector response.

        Parameters
        ----------
        dataconnector : dict
            Unmodified dataconnector response dictionary.

        """

        # Inherit from OutputBase parent.
        dtoutputs.OutputBase.__init__(self, dataconnector)

        # Unpack attributes from dictionary.
        self.dataconnector_id = dataconnector['name'].split('/')[-1]
        self.dataconnector_type = dataconnector['type']
        self.status = dataconnector['status']
        self.display_name = dataconnector['displayName']

    @classmethod
    def get_dataconnector(cls,
                          project_id: str,
                          dataconnector_id: str,
                          **kwargs,
                          ) -> DataConnector:
        """
        Gets a dataconnector specified by its ID.

        Parameters
        ----------
        project_id : str
            Unique project ID.
        dataconnector_id : str
            Unique dataconnector ID.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        dataconnector : DataConnector
            Object representing the specified dataconnector.

        """

        # Construct URL
        url = dt.api_url
        url += '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)

        # Return DataConnector object of GET request response.
        return cls(dtrequests.generic_request(
            method='GET',
            url=url,
            **kwargs,
        ))

    @classmethod
    def list_dataconnectors(cls,
                            project_id: str,
                            **kwargs,
                            ) -> list[DataConnector]:
        """
        List all available dataconnectors in the specified project.

        Parameters
        ----------
        project_id : str
            Unique project ID.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        dataconnectors : list[DataConnector]
            List of objects each representing a dataconnector.

        """

        # Return list of DataConnector objects of paginated GET response.
        dataconnectors = dtrequests.auto_paginated_list(
            url=dt.api_url + '/projects/{}/dataconnectors'.format(project_id),
            pagination_key='dataConnectors',
            **kwargs,
        )
        return [cls(dcon) for dcon in dataconnectors]

    @classmethod
    def create_dataconnector(cls,
                             project_id: str,
                             url: str,
                             dataconnector_type: str,
                             display_name: str = '',
                             status: str = 'ACTIVE',
                             events: list[str] = [],
                             signature_secret: str = '',
                             headers: dict[str, str] = {},
                             labels: list[str] = [],
                             **kwargs,
                             ) -> DataConnector:
        """
        Create a new dataconnector in the specified project.

        Parameters
        ----------
        project_id : str
            Unique project ID.
        url : str
            Endpoint URL towards which events are forwarded. Must be HTTPS.
        dataconnector_type : {"HTTP_PUSH"} str, optional
            Type of dataconnector to create. Currently only supports HTTP_PUSH.
        display_name : str, optional
            Sets a display name for the project.
        status : {"ACTIVE", "USER_DISABLED"} strm optional
            Status of the new dataconnector.
        events : list[str], optional
            List of event types the dataconnectors should forward.
        signature_secret : str, optional
            Secret with which each forwarded event is signed.
        headers : dict[str, str], optional
            Dictionary of headers to include with each forwarded event.
        labels : list[str], optional
            List of labels to forward with each event.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        dataconnector : DataConnector
            Object representing the newly created dataconnector.

        """

        # Construct request body dictionary.
        body: dict = dict()
        body['type'] = dataconnector_type
        body['status'] = status
        body['events'] = events
        body['labels'] = labels
        body['httpConfig'] = dict()
        body['httpConfig']['url'] = url
        body['httpConfig']['headers'] = headers
        body['httpConfig']['signatureSecret'] = signature_secret
        if len(display_name) > 0:
            body['displayName'] = display_name

        # Construct URL.
        url = dt.api_url
        url += '/projects/{}/dataconnectors'.format(project_id)

        # Return DataConnector object of POST request response.
        return cls(dtrequests.generic_request(
            method='POST',
            url=url,
            body=body,
            **kwargs,
        ))

    @classmethod
    def update_dataconnector(cls,
                             project_id: str,
                             dataconnector_id: str,
                             display_name: Optional[str] = None,
                             status: Optional[str] = None,
                             events: Optional[list[str]] = None,
                             labels: Optional[list[str]] = None,
                             url: Optional[str] = None,
                             signature_secret: Optional[str] = None,
                             headers: Optional[dict[str, str]] = None,
                             **kwargs,
                             ) -> DataConnector:
        """
        Updates the attributes of a dataconnector.

        Parameters
        ----------
        project_id : str
            Unique ID of the project that contains the dataconnector.
        dataconnector_id : str
            Unique ID of the dataconnector to update.
        url : str, optional
            Endpoint URL towards which events are forwarded. Must be HTTPS.
        display_name : str, optional
            Sets a display name for the dataconnector.
        status : {"ACTIVE", "USER_DISABLED"} str, optional
            Status of the dataconnector.
        events : list[str], optional
            List of event types the dataconnectors should forward.
        signature_secret : str, optional
            Secret with which each forwarded event is signed.
        headers : dict[str, str], optional
            Dictionary of headers to include with each forwarded event.
        labels : list[str], optional
            List of labels to forward with each event.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        """

        # Construct request body dictionary.
        body: dict = dict()
        body['httpConfig'] = {}
        if display_name is not None:
            body['displayName'] = display_name
        if status is not None:
            body['status'] = status
        if events is not None:
            body['events'] = events
        if labels is not None:
            body['labels'] = labels
        if url is not None:
            body['httpConfig']['url'] = url
        if signature_secret is not None:
            body['httpConfig']['signatureSecret'] = signature_secret
        if headers is not None:
            body['headers'] = headers

        # Construct URL.
        url = dt.api_url
        url += '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)

        # Return DataConnector object of PATCH request response.
        return cls(dtrequests.generic_request(
            method='PATCH',
            url=url,
            body=body,
            **kwargs,
        ))

    @classmethod
    def delete_dataconnector(cls,
                             project_id: str,
                             dataconnector_id: str,
                             **kwargs,
                             ) -> None:
        """
        Deletes the specified dataconnector.

        Parameters
        ----------
        project_id : str
            Unique ID of the project that contains the dataconnector.
        dataconnector_id : str
            Unique ID of the dataconnector to delete.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        """

        # Construct URL.
        url = dt.api_url
        url += '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)

        # Send DELETE request, but return nothing.
        dtrequests.generic_request(
            method='DELETE',
            url=url,
            **kwargs,
        )

    @classmethod
    def get_metrics(cls,
                    project_id: str,
                    dataconnector_id: str,
                    **kwargs,
                    ) -> Metric:
        """
        Get the metrics of the last 3 hours for a dataconnector.

        Parameters
        ----------
        project_id : str
            Unique ID of the project that contains the dataconnector.
        dataconnector_id : str
            Unique ID of the dataconnector to list metrics for.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        metric : Metric
            Object representing the fetched metrics.

        """

        # Construct URL.
        url = dt.api_url
        url += '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)
        url += ':metrics'

        # Return Metric object of GET request response.
        return Metric(dtrequests.generic_request(
            method='GET',
            url=url,
            **kwargs,
        ))

    @classmethod
    def sync_dataconnector(cls,
                           project_id: str,
                           dataconnector_id: str,
                           **kwargs,
                           ) -> None:
        """
        Synchronizes the current dataconnector state.

        This method let's you synchronize your cloud service with the current
        state of the devices in your project. This entails pushing the most
        recent event of each type for all devices in your project.

        Parameters
        ----------
        project_id : str
            Unique ID of the project that contains the dataconnector.
        dataconnector_id : str
            Unique ID of the dataconnector to synchronize.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        """

        # Construct URL.
        url = dt.api_url
        url += '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)
        url += ':sync'

        # Send POST request, but return nothing.
        dtrequests.generic_request(
            method='POST',
            url=url,
            **kwargs,
        )
