import disruptive as dt
import disruptive.requests as dtrequests
import disruptive.outputs as dtoutputs
import disruptive.transforms as dttransforms


class ServiceAccount(dtoutputs.OutputBase):

    def __init__(self, org_dict):
        # Inherit from Response parent.
        dtoutputs.OutputBase.__init__(self, org_dict)

        # Unpack organization json.
        self.__unpack()

    def __unpack(self):
        self.email = self.raw['email']
        self.display_name = self.raw['displayName']
        self.basic_auth = self.raw['enableBasicAuth']
        self.created = dttransforms.iso8601_to_datetime(self.raw['createTime'])
        self.updated = dttransforms.iso8601_to_datetime(self.raw['updateTime'])

    @classmethod
    def get(cls, project_id: str, serviceaccount_id: str, auth=None):
        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/serviceaccounts/{}'.format(
            project_id,
            serviceaccount_id,
        )

        # Return ServiceAccount object of GET request response.
        return cls(dtrequests.get(
            url=url,
            auth=auth
        ))

    @classmethod
    def list(cls, project_id: str, auth=None):
        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/serviceaccounts'.format(project_id)

        # Return list of ServiceAccount objects of paginated GET response.
        service_accounts = dtrequests.auto_paginated_list(
            url=url,
            pagination_key='serviceAccounts',
            auth=auth,
        )
        return [cls(sa) for sa in service_accounts]

    @classmethod
    def create(cls,
               project_id: str,
               display_name: str = None,
               basic_auth: bool = None,
               auth=None
               ):
        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/serviceaccounts'.format(project_id)

        # Construct body.
        body = {}
        if display_name is not None:
            body['displayName'] = display_name
        if basic_auth is not None:
            body['enableBasicAuth'] = basic_auth

        # Return ServiceAccount object of GET request response.
        return (cls(dtrequests.post(
            url=url,
            body=body,
            auth=auth,
        )))
