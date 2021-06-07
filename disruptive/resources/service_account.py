from __future__ import annotations

from datetime import datetime
from typing import Optional, Any

import disruptive.requests as dtrequests
import disruptive.outputs as dtoutputs
import disruptive.transforms as dttrans


class ServiceAccount(dtoutputs.OutputBase):
    """
    Represents a Service Account.

    When a Service Account response is received, the content is
    unpacked and the related attributes are updated.

    Attributes
    ----------
    service_account_id : str
        Unique Service Account ID.
    email : str
        Unique Service Account email.
    display_name : str
        The provided display name.
    basic_auth_enabled : bool
        True if Basic Auth is enabled, otherwise False.
    create_time : datetime
        Timestamp of when the Service Account was created.
    update_time : datetime
        Timestamp of when the Service Account was last updated.

    """

    def __init__(self, service_account: dict) -> None:
        """
        Constructs the ServiceAccount object by unpacking the raw response.

        Parameters
        ----------
        service_account : dict
            Unmodified Service Account response dictionary.

        """

        # Inherit from Response parent.
        dtoutputs.OutputBase.__init__(self, service_account)

        # Unpack attributes from dictionary.
        self.service_account_id: str = service_account['name'].split('/')[-1]
        self.email: str = service_account['email']
        self.display_name: str = service_account['displayName']
        self.basic_auth_enabled: bool = service_account['enableBasicAuth']
        self.create_time: Optional[datetime] = \
            dttrans.to_datetime(service_account['createTime'])
        self.update_time: Optional[datetime] = \
            dttrans.to_datetime(service_account['updateTime'])

    @classmethod
    def get_service_account(cls,
                            service_account_id: str,
                            project_id: str,
                            **kwargs: Any,
                            ) -> ServiceAccount:
        """
        Gets the current state of a single Service Account.

        Parameters
        ----------
        service_account_id : str
            Unique ID of the target Service Account.
        project_id : str
            Unique ID of the target project.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        service_account : ServiceAccount
            Object representing the target Service Account.

        Examples
        --------
        >>> # Fetch information about a specific Service Account.
        >>> sa = disruptive.ServiceAccount.get_service_account(
        ...     service_account_id='<SERVICE_ACCOUNT_ID>',
        ...     project_id='<PROJECT_ID>',
        ... )

        """

        # Construct URL.
        url = '/projects/{}/serviceaccounts/{}'.format(
            project_id,
            service_account_id,
        )

        # Return ServiceAccount object of GET request response.
        return cls(dtrequests.DTRequest.get(
            url=url,
            **kwargs,
        ))

    @classmethod
    def list_service_accounts(cls,
                              project_id: str,
                              **kwargs: Any,
                              ) -> list[ServiceAccount]:
        """
        Gets a list of the current state of all Service Accounts in a project.

        Parameters
        ----------
        project_id : str
            Unique ID of the target project.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        service_accounts : list[ServiceAccount]
            List of objects each representing a Service Account.

        Examples
        --------
        >>> # Fetch a list of all Service Accounts in a project.
        >>> sas = disruptive.ServiceAccount.list_service_accounts(
        ...     project_id='<PROJECT_ID>',
        ... )

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
    def create_service_account(cls,
                               project_id: str,
                               display_name: str = '',
                               basic_auth_enabled: bool = False,
                               **kwargs: Any,
                               ) -> ServiceAccount:
        """
        Create a new Service Account in the specified project.

        Parameters
        ----------
        project_id : str
            Unique ID of the target project.
        display_name : str, optional
            Sets a display name for the Service Account.
        basic_auth_enabled : bool, optional
            Enables Basic Auth for the Service Account if True.
            Defaults to False.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        service_account : ServiceAccount
            Object representing the newly created Service Account.

        Examples
        --------
        >>> # Create a new Service Account with basic auth enabled.
        >>> sa = disruptive.ServiceAccount.create_service_account(
        ...     project_id='<PROJECT_ID>',
        ...     display_name='new-service-account',
        ...     basic_auth_enabled=True,
        ... )

        """

        # Construct URL.
        url = '/projects/{}/serviceaccounts'.format(project_id)

        # Construct body.
        body: dict = dict()
        body['enableBasicAuth'] = basic_auth_enabled
        if len(display_name) > 0:
            body['displayName'] = display_name

        # Return ServiceAccount object of GET request response.
        return cls(dtrequests.DTRequest.post(
            url=url,
            body=body,
            **kwargs,
        ))

    @classmethod
    def update_service_account(cls,
                               service_account_id: str,
                               project_id: str,
                               display_name: Optional[str] = None,
                               basic_auth_enabled: Optional[bool] = None,
                               **kwargs: Any,
                               ) -> ServiceAccount:
        """
        Updates the attributes of a specified Service Account.

        Parameters
        ----------
        service_account_id : str
            Unique ID of the target Service Account.
        project_id : str
            Unique ID of the target project.
        display_name : str, optional
            Updates the Service Account display name.
        basic_auth_enabled : bool, optional
            If True, enables Basic Auth while False disables it.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        service_account : ServiceAccount
            Object representing the updated Service Account.

        Examples
        --------
        >>> # Update only the `display_name` of a Service Account.
        >>> sa = disruptive.ServiceAccount.update_service_account(
        ...     service_account_id='<SERVICE_ACCOUNT_ID>',
        ...     project_id='<PROJECT_ID>',
        ...     display_name='new-name',
        ... )

        >>> # Update both `display_name` and `basic_auth_enabled`.
        >>> sa = disruptive.ServiceAccount.update_service_account(
        ...     service_account_id='<SERVICE_ACCOUNT_ID>',
        ...     project_id='<PROJECT_ID>',
        ...     display_name='new-name',
        ...     basic_auth_enabled=False,
        ... )

        """

        # Construct URL.
        url = '/projects/{}/serviceaccounts/{}'.format(
            project_id,
            service_account_id,
        )

        # Construct body.
        body: dict = dict()
        if display_name is not None:
            body['displayName'] = display_name
        if basic_auth_enabled is not None:
            body['enableBasicAuth'] = basic_auth_enabled

        # Return ServiceAccount object of GET request response.
        return cls(dtrequests.DTRequest.patch(
            url=url,
            body=body,
            **kwargs,
        ))

    @classmethod
    def delete_service_account(cls,
                               service_account_id: str,
                               project_id: str,
                               **kwargs: Any,
                               ) -> None:
        """
        Deletes the specified Service Account.

        Parameters
        ----------
        service_account_id : str
            Unique ID of the Service Account to delete.
        project_id : str
            Unique ID of the target project.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Examples
        --------
        >>> # Delete a single Service Account.
        >>> disruptive.ServiceAccount.delete_service_account(
        ...     service_account_id='<SERVICE_ACCOUNT_ID>',
        ...     project_id='<PROJECT_ID>',
        ... )

        """

        # Construct URL.
        url = '/projects/{}/serviceaccounts/{}'.format(
            project_id,
            service_account_id,
        )

        # Send DELETE request, but return nothing.
        dtrequests.DTRequest.delete(
            url=url,
            **kwargs,
        )

    @staticmethod
    def get_key(key_id: str,
                service_account_id: str,
                project_id: str,
                **kwargs: Any,
                ) -> Key:
        """
        Get the key of a Service Account.

        Parameters
        ----------
        key_id : str
            Unique ID of the target key.
        service_account_id : str
            Unique ID of the target Service Account.
        project_id : str
            Unique ID of the target project.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        key : Key
            Object representing the target key.

        Examples
        --------
        >>> # Get information about a specific key.
        >>> key = disruptive.ServiceAccount.get_key(
        ...     key_id='<KEY_ID>',
        ...     service_account_id='<SERVICE_ACCOUNT_ID>',
        ...     project_id='<PROJECT_ID>',
        ... )

        """

        # Construct URL.
        url = '/projects/{}/serviceaccounts/{}/keys/{}'.format(
            project_id,
            service_account_id,
            key_id,
        )

        # Return Key object of GET request response.
        return Key(dtrequests.DTRequest.get(
            url=url,
            **kwargs,
        ))

    @staticmethod
    def list_keys(service_account_id: str,
                  project_id: str,
                  **kwargs: Any,
                  ) -> list[Key]:
        """
        Get a list of all keys for a Service Account.

        Parameters
        ----------
        service_account_id : str
            Unique ID of the target Service Account.
        project_id : str
            Unique ID of the target project.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        keys : list[Key]
            List of objects each representing a key.

        Examples
        --------
        >>> # List all keys for a specific Service Account.
        >>> keys = disruptive.ServiceAccount.list_keys(
        ...     service_account_id='<SERVICE_ACCOUNT_ID>',
        ...     project_id='<PROJECT_ID>',
        ... )

        """

        # Construct URL.
        url = '/projects/{}/serviceaccounts/{}/keys'.format(
            project_id,
            service_account_id,
        )

        # Return list of Key objects of paginated GET response.
        keys = dtrequests.DTRequest.paginated_get(
            url=url,
            pagination_key='keys',
            **kwargs,
        )
        return [Key(key) for key in keys]

    @staticmethod
    def create_key(service_account_id: str,
                   project_id: str,
                   **kwargs: Any,
                   ) -> Key:
        """
        Create a new key for the specified Service Account.

        Parameters
        ----------
        service_account_id : str
            Unique ID of the target Service Account.
        project_id : str
            Unique ID of the target project.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        key : Key
            Object representing the newly created key.

        Examples
        --------
        >>> # Create a new key for a specific Service Account.
        >>> key = disruptive.ServiceAccount.create_key(
        ...     service_account_id='<SERVICE_ACCOUNT_ID>',
        ...     project_id='<PROJECT_ID>',
        ... )

        """

        # Construct URL.
        url = '/projects/{}/serviceaccounts/{}/keys'.format(
            project_id,
            service_account_id,
        )

        # Return Key object of POST request response.
        response = dtrequests.DTRequest.post(
            url=url,
            **kwargs,
        )
        return Key._with_secret(response)

    @staticmethod
    def delete_key(key_id: str,
                   service_account_id: str,
                   project_id: str,
                   **kwargs: Any,
                   ) -> None:
        """
        Deletes a key in the specified Service Account.

        Parameters
        ----------
        key_id : str
            Unique ID of the key to delete.
        service_account_id : str
            Unique ID of the target Service Account.
        project_id : str
            Unique ID of the target project.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Examples
        --------
        >>> # Delete a specific key on a Service Account.
        >>> disruptive.ServiceAccount.delete_key(
        ...     key_id='<KEY_ID',
        ...     service_account_id='<SERVICE_ACCOUNT_ID>',
        ...     project_id='<PROJECT_ID>',
        ... )

        """

        # Construct URL.
        url = '/projects/{}/serviceaccounts/{}/keys/{}'.format(
            project_id,
            service_account_id,
            key_id,
        )

        # Send DELETE request, but return nothing.
        dtrequests.DTRequest.delete(
            url=url,
            **kwargs,
        )


class Key(dtoutputs.OutputBase):
    """
    Represents a key in a Service Account.

    When a key response is received, the content is
    unpacked and the related attributes are updated.

    Attributes
    ----------
    key_id : str
        Unique key ID.
    secret : str, None
        If the Key object was constructed from a newly created key, i.e. from
        calling the :ref:`create_key() <create_key>` method, this attributes
        contains the key secret. This is displayed once, and is otherwise None.
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
        self.secret: Optional[str] = None

        # Unpack attributes from dictionary.
        self.key_id: str = key['id']
        self.create_time: Optional[datetime] = \
            dttrans.to_datetime(key['createTime'])
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
