from __future__ import annotations

# Standard library imports.
from typing import Optional

# Project imports.
import disruptive as dt
import disruptive.requests as dtrequests
from disruptive.outputs import Metric
from disruptive.authentication import BasicAuth, OAuth


class DataConnector():

    def __init__(self, dataconnector: dict) -> None:
        # Inherit everything from Response parent.
        self.raw = dataconnector

        # Unpack device json.
        self.__unpack()

    def __unpack(self) -> None:
        self.id = self.raw['name'].split('/')[-1]
        self.type = self.raw['type']
        self.status = self.raw['status']
        self.display_name = self.raw['displayName']

    @classmethod
    def get_dataconnector(cls,
                          project_id: str,
                          dataconnector_id: str,
                          auth: Optional[BasicAuth | OAuth] = None
                          ) -> DataConnector:

        # Construct URL
        url = dt.base_url
        url += '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)

        # Return DataConnector object of GET request response.
        return cls(dtrequests.get(
            url=url,
            auth=auth
        ))

    @classmethod
    def list_dataconnectors(cls,
                            project_id: str,
                            auth: Optional[BasicAuth | OAuth] = None
                            ) -> list[DataConnector]:

        # Return list of DataConnector objects of paginated GET response.
        dataconnectors = dtrequests.auto_paginated_list(
            url=dt.base_url + '/projects/{}/dataconnectors'.format(project_id),
            pagination_key='dataConnectors',
            auth=auth,
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
                             auth: Optional[BasicAuth | OAuth] = None,
                             ) -> DataConnector:

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
        url = dt.base_url
        url += '/projects/{}/dataconnectors'.format(project_id)

        # Return DataConnector object of POST request response.
        return cls(dtrequests.post(
            url=url,
            body=body,
            auth=auth,
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
                             auth: Optional[BasicAuth | OAuth] = None,
                             ) -> DataConnector:

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
        url = dt.base_url
        url += '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)

        # Return DataConnector object of PATCH request response.
        return cls(dtrequests.patch(
            url=url,
            body=body,
            auth=auth,
        ))

    @classmethod
    def delete_dataconnector(cls,
                             project_id: str,
                             dataconnector_id: str,
                             auth: Optional[BasicAuth | OAuth] = None
                             ) -> None:

        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)

        # Send DELETE request, but return nothing.
        dtrequests.delete(
            url=url,
            auth=auth,
        )

    @classmethod
    def dataconnector_metrics(cls,
                              project_id: str,
                              dataconnector_id: str,
                              auth: Optional[BasicAuth | OAuth] = None
                              ) -> Metric:

        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)
        url += ':metrics'

        # Return Metric object of GET request response.
        return Metric(dtrequests.get(
            url=url,
            auth=auth,
        ))

    @classmethod
    def sync_dataconnector(cls,
                           project_id: str,
                           dataconnector_id: str,
                           auth: Optional[BasicAuth | OAuth] = None
                           ) -> None:

        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)
        url += ':sync'

        # Send POST request, but return nothing.
        dtrequests.post(
            url=url,
            auth=auth,
        )
