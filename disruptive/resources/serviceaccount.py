import disruptive as dt
import disruptive.requests as dtrequests
import disruptive.outputs as dtoutputs


class ServiceAccount(dtoutputs.OutputBase):

    def __init__(self, org_dict):
        # Inherit from Response parent.
        dtoutputs.OutputBase.__init__(self, org_dict)

        # Unpack organization json.
        self.__unpack()

    def __unpack(self):
        pass

    @classmethod
    def list(cls, project_id: str = None, auth=None):
        # Construct URL
        url = dt.base_url
        url += '/projects/{}/serviceaccounts'.format(project_id)

        # Return list of ServiceAccount objects.
        service_accounts = dtrequests.auto_paginated_list(
            url=url,
            pagination_key='serviceAccounts',
            auth=auth,
        )
        return [cls(sa) for sa in service_accounts]
