from __future__ import annotations

# Standard library imports.
from typing import Optional

# Project imports.
import disruptive.requests as dtrequests
import disruptive.outputs as dtoutputs
import disruptive.transforms as dttrans


class ServiceAccount(dtoutputs.OutputBase):
    """
    Represents a serviceaccount.

    When a serviceaccount response is received, the content is
    unpacked and the related attributes are updated.

    Attributes
    ----------
    serviceaccount_id : str
        Unique serviceaccount ID.
    email : str
        Unique serviceaccount email.
    display_name : str
        The provided display name.
    basic_auth : bool
        True if Basic Auth is enabled, otherwise False.
    create_time : datetime
        Timestamp of when the serviceaccount was created.
    update_time : datetime
        Timestamp of when the serviceaccount was last updated.

    """

    def __init__(self, serviceaccount: dict) -> None:
        """
        Constructs the ServiceAccount object by unpacking the raw response.

        Parameters
        ----------
        serviceaccount : dict
            Unmodified serviceaccount response dictionary.

        """

        # Inherit from Response parent.
        dtoutputs.OutputBase.__init__(self, serviceaccount)

        # Unpack attributes from dictionary.
        self.serviceaccount_id = serviceaccount['name'].split('/')[-1]
        self.email = serviceaccount['email']
        self.display_name = serviceaccount['displayName']
        self.basic_auth = serviceaccount['enableBasicAuth']
        self.create_time = dttrans.to_datetime(serviceaccount['createTime'])
        self.update_time = dttrans.to_datetime(serviceaccount['updateTime'])

    @classmethod
    def get_serviceaccount(cls,
                           serviceaccount_id: str,
                           project_id: str,
                           **kwargs,
                           ) -> ServiceAccount:
        """
        Gets a serviceaccount specified by its ID.

        Parameters
        ----------
        serviceaccount_id : str
            Unique ID of the target serviceaccount.
        project_id : str
            Unique ID of the target project.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        serviceaccount : ServiceAccount
            Object representing the target serviceaccount.

        """

        # Construct URL.
        url = '/projects/{}/serviceaccounts/{}'.format(
            project_id,
            serviceaccount_id,
        )

        # Return ServiceAccount object of GET request response.
        return cls(dtrequests.DTRequest.get(
            url=url,
            **kwargs,
        ))

    @classmethod
    def list_serviceaccounts(cls,
                             project_id: str,
                             **kwargs,
                             ) -> list[ServiceAccount]:
        """
        List all available serviceaccounts in the specified project.

        Parameters
        ----------
        project_id : str
            Unique ID of the target project.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        serviceaccounts : list[ServiceAccount]
            List of objects each representing a serviceaccount.

        """

        # Construct URL.
        url = '/projects/{}/serviceaccounts'.format(project_id)

        # Return list of ServiceAccount objects of paginated GET response.
        service_accounts = dtrequests.DTRequest.paginated_get(
            url=url,
            pagination_key='serviceAccounts',
            **kwargs,
        )
        return [cls(sa) for sa in service_accounts]

    @classmethod
    def create_serviceaccount(cls,
                              project_id: str,
                              display_name: str = '',
                              basic_auth: bool = False,
                              **kwargs,
                              ) -> ServiceAccount:
        """
        Create a new serviceaccount in the specified project.

        Parameters
        ----------
        project_id : str
            Unique ID of the target project.
        display_name : str, optional
            Sets a display name for the serviceaccount.
        basic_auth : bool, optional
            Enables Basic Auth for the serviceaccount if True.
            Defaults to False.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        serviceaccount : ServiceAccount
            Object representing the newly created serviceaccount.

        """

        # Construct URL.
        url = '/projects/{}/serviceaccounts'.format(project_id)

        # Construct body.
        body: dict = dict()
        body['enableBasicAuth'] = basic_auth
        if len(display_name) > 0:
            body['displayName'] = display_name

        # Return ServiceAccount object of GET request response.
        return cls(dtrequests.DTRequest.post(
            url=url,
            body=body,
            **kwargs,
        ))

    @classmethod
    def update_serviceaccount(cls,
                              serviceaccount_id: str,
                              project_id: str,
                              display_name: Optional[str] = None,
                              basic_auth: Optional[bool] = None,
                              **kwargs,
                              ) -> ServiceAccount:
        """
        Updates the attributes of a specified serviceaccount.

        Parameters
        ----------
        serviceaccount_id : str
            Unique ID of the target serviceaccount.
        project_id : str
            Unique ID of the target project.
        display_name : str, optional
            Updates the serviceaccount display name.
        basic_auth : bool, optional
            If True, enables Basic Auth while False disables it.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        """

        # Construct URL.
        url = '/projects/{}/serviceaccounts/{}'.format(
            project_id,
            serviceaccount_id,
        )

        # Construct body.
        body: dict = dict()
        if display_name is not None:
            body['displayName'] = display_name
        if basic_auth is not None:
            body['enableBasicAuth'] = basic_auth

        # Return ServiceAccount object of GET request response.
        return cls(dtrequests.DTRequest.patch(
            url=url,
            body=body,
            **kwargs,
        ))

    @classmethod
    def delete_serviceaccount(cls,
                              serviceaccount_id: str,
                              project_id: str,
                              **kwargs,
                              ) -> None:
        """
        Deletes the specified serviceaccount.

        Parameters
        ----------
        serviceaccount_id : str
            Unique ID of the serviceaccount to delete.
        project_id : str
            Unique ID of the target project.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        """

        # Construct URL.
        url = '/projects/{}/serviceaccounts/{}'.format(
            project_id,
            serviceaccount_id,
        )

        # Send DELETE request, but return nothing.
        dtrequests.DTRequest.delete(
            url=url,
            **kwargs,
        )

    @staticmethod
    def get_key(serviceaccount_id: str,
                project_id: str,
                key_id: str,
                **kwargs,
                ) -> Key:
        """
        Get the key of a serviceaccount.

        Parameters
        ----------
        serviceaccount_id : str
            Unique ID of the target serviceaccount.
        project_id : str
            Unique ID of the target project.
        key_id : str
            Unique ID of the target key.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        key : Key
            Object representing the target key.

        """

        # Construct URL.
        url = '/projects/{}/serviceaccounts/{}/keys/{}'.format(
            project_id,
            serviceaccount_id,
            key_id,
        )

        # Return Key object of GET request response.
        return Key(dtrequests.DTRequest.get(
            url=url,
            **kwargs,
        ))

    @staticmethod
    def list_keys(serviceaccount_id: str,
                  project_id: str,
                  **kwargs,
                  ) -> list[Key]:
        """
        Get a list of all keys for a serviceaccount.

        Parameters
        ----------
        serviceaccount_id : str
            Unique ID of the target serviceaccount.
        project_id : str
            Unique ID of the target project.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        keys : list[Key]
            List of objects each representing a key.

        """

        # Construct URL.
        url = '/projects/{}/serviceaccounts/{}/keys'.format(
            project_id,
            serviceaccount_id,
        )

        # Return list of Key objects of paginated GET response.
        keys = dtrequests.DTRequest.paginated_get(
            url=url,
            pagination_key='keys',
            **kwargs,
        )
        return [Key(key) for key in keys]

    @staticmethod
    def create_key(serviceaccount_id: str,
                   project_id: str,
                   **kwargs,
                   ) -> Key:
        """
        Create a new key for the specified serviceaccount.

        Parameters
        ----------
        serviceaccount_id : str
            Unique ID of the target serviceaccount.
        project_id : str
            Unique ID of the target project.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        key : Key
            Object representing the newly created key.

        """

        # Construct URL.
        url = '/projects/{}/serviceaccounts/{}/keys'.format(
            project_id,
            serviceaccount_id,
        )

        # Return Key object of POST request response.
        response = dtrequests.DTRequest.post(
            url=url,
            **kwargs,
        )
        return Key._with_secret(response)

    @staticmethod
    def delete_key(serviceaccount_id: str,
                   key_id: str,
                   project_id: str,
                   **kwargs,
                   ) -> None:
        """
        Deletes a key in the specified serviceaccount.

        Parameters
        ----------
        serviceaccount_id : str
            Unique ID of the target serviceaccount.
        key_id : str
            Unique ID of the key to delete.
        project_id : str
            Unique ID of the target project.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        """

        # Construct URL.
        url = '/projects/{}/serviceaccounts/{}/keys/{}'.format(
            project_id,
            serviceaccount_id,
            key_id,
        )

        # Send DELETE request, but return nothing.
        dtrequests.DTRequest.delete(
            url=url,
            **kwargs,
        )


class Key(dtoutputs.OutputBase):
    """
    Represents a key in a serviceaccount.

    When a key response is received, the content is
    unpacked and the related attributes are updated.

    Attributes
    ----------
    key_id : str
        Unique key ID.
    secret : str, None
        If the Key object was constructed from a newly created key, i.e. from
        calling the create_key() method, this attributes contains the
        key secret. This only displays once, and is otherwise None.
    create_time : datetime
        Timestamp of when the key was created.

    """

    def __init__(self, key: dict) -> None:
        """
        Constructs the Key object by unpacking the raw key response.

        Parameters
        ----------
        key : dict
            Key response dictionary.

        """
        # Inherit from Response parent.
        dtoutputs.OutputBase.__init__(self, key)

        # Initialize secret, which is only not-None when created.
        self.secret = None

        # Unpack attributes from dictionary.
        self.key_id = key['id']
        self.create_time = dttrans.to_datetime(key['createTime'])
        if 'secret' in key:
            self.secret = key['secret']

    @classmethod
    def _with_secret(cls, key: dict) -> Key:
        """
        Moves the secret field in the response dictionary.

        This is done for convenience and consistency. For some reason, when
        the secret is included, the raw response dictionary is changed, adding
        another layer outside the key field. This just flattens the structure.

        Parameters
        ----------
        key : dict
            Unmodified key response dictionary.

        Returns
        -------
        flattened : dict
            Modified key response dictionary.

        """

        flattened = key['key']
        flattened['secret'] = key['secret']
        return cls(flattened)
