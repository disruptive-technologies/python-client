from __future__ import annotations

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
        self.dataconnector_id = self.raw['name'].split('/')[-1]
        self.type = self.raw['type']
        self.status = self.raw['status']
        self.display_name = self.raw['displayName']

    @classmethod
    def get(cls,
            project_id: str,
            dataconnector_id: str,
            auth: BasicAuth | OAuth | None = None
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
    def listing(cls,
                project_id: str,
                auth: BasicAuth | OAuth | None = None
                ) -> list[DataConnector]:

        # Return list of DataConnector objects of paginated GET response.
        dataconnectors = dtrequests.auto_paginated_list(
            url=dt.base_url + '/projects/{}/dataconnectors'.format(project_id),
            pagination_key='dataConnectors',
            auth=auth,
        )
        return [cls(dcon) for dcon in dataconnectors]

    @classmethod
    def create(cls,
               project_id: str,
               url: str,
               display_name: str = '',
               status: str = 'ACTIVE',
               events: list[str] = [],
               http_type: str = 'HTTP_PUSH',
               signature_secret: str = '',
               headers: dict = {},
               labels: list[str] = [],
               auth: BasicAuth | OAuth | None = None,
               ) -> DataConnector:

        # Construct request body dictionary.
        body: dict = dict()
        body['type'] = http_type
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
    def update(cls,
               project_id: str,
               dataconnector_id: str,
               display_name: str = '',
               status: str = '',
               events: list[str] = [],
               labels: list[str] = [],
               url: str = '',
               signature_secret: str = '',
               headers: dict = {},
               auth: BasicAuth | OAuth | None = None,
               ) -> DataConnector:

        # Construct request body dictionary.
        body: dict = dict()
        body['httpConfig'] = {}
        if len(display_name) > 0:
            body['displayName'] = display_name
        if len(status) > 0:
            body['status'] = status
        if len(events) > 0:
            body['events'] = events
        if len(labels) > 0:
            body['labels'] = labels
        if len(url) > 0:
            body['httpConfig']['url'] = url
        if len(signature_secret) > 0:
            body['httpConfig']['signatureSecret'] = signature_secret
        if len(headers) > 0:
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
    def delete(cls,
               project_id: str,
               dataconnector_id: str,
               auth: BasicAuth | OAuth | None = None
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
    def metrics(cls,
                project_id: str,
                dataconnector_id: str,
                auth: BasicAuth | OAuth | None = None
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
    def sync(cls,
             project_id: str,
             dataconnector_id: str,
             auth: BasicAuth | OAuth | None = None
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
