from __future__ import annotations

# Standard library imports.
from typing import Optional

# Project imports.
import disruptive as dt
import disruptive.requests as dtrequests
from disruptive.outputs import OutputBase, Member
from disruptive.authentication import Auth


class Project(OutputBase):
    """
    Represents a project.

    When a project response is received, the content is
    unpacked and the related attributes are updated.

    Attributes
    ----------
    raw : dict
        Unmodified project response dictionary.
    id : str
        Unique project ID.
    display_name : str
        The provided display name.
    organization_id : str
        Unique ID of parent organization.
    organization_display_name : str
        The provided display name to parent organization.
    sensor_count : int
        Number of sensors in project.
    cloud_connector_count : int
        Number of Cloud Connectors in project.
    is_inventory : bool
        True if project is organization inventory, otherwise False.

    """

    def __init__(self, project: dict) -> None:
        """
        Constructs the Project object by unpacking the raw project response.

        Parameters
        ----------
        project : dict
            Unmodified project response dictionary.

        """

        # Inherit from OutputBase parent.
        OutputBase.__init__(self, project)

        # Unpack attributes from dictionary.
        self.id = self.raw['name'].split('/')[-1]
        self.display_name = self.raw['displayName']
        self.organization_id = self.raw['organization'].split('/')[-1]
        self.organization_display_name = self.raw['organizationDisplayName']
        self.sensor_count = self.raw['sensorCount']
        self.cloud_connector_count = self.raw['cloudConnectorCount']
        self.is_inventory = self.raw['inventory']

    @classmethod
    def get_project(cls,
                    project_id: str,
                    auth: Optional[Auth] = None
                    ) -> Project:
        """
        Gets a project specified by its ID.

        Parameters
        ----------
        project_id : str
            Unique project ID.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.

        Returns
        -------
        project : Project
            Object representing the specified project.

        """

        # Construct URL.
        url = dt.base_url
        url += '/projects/{}'.format(project_id)

        # Return Project object of GET request response.
        return cls(dtrequests.get(
            url=url,
            auth=auth
        ))

    @classmethod
    def list_projects(cls,
                      organization_id: Optional[str] = None,
                      query: Optional[str] = None,
                      auth: Optional[Auth] = None
                      ) -> list[Project]:
        """
        List all available projects in the specified organization.

        Parameters
        ----------
        organization_id : str
            Unique organization ID.
        query : str, optional
            Keyword based search for project- and organization display names.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.

        Returns
        -------
        projects : list[Project]
            List of objects each representing a project.

        """

        # Construct URL.
        url = dt.base_url + '/projects'

        # Construct parameters dictionary.
        params = {}
        if organization_id is not None:
            params['organization'] = 'organizations/' + organization_id
        if query is not None:
            params['query'] = query

        # Return list of Project objects of paginated GET response.
        responses = dtrequests.auto_paginated_list(
            url=url,
            pagination_key='projects',
            params=params,
            auth=auth,
        )
        return [cls(r) for r in responses]

    @classmethod
    def create_project(cls,
                       organization_id: str,
                       display_name: str = '',
                       auth: Optional[Auth] = None
                       ) -> Project:
        """
        Create a new project in the specified organization.

        Parameters
        ----------
        organization_id : str
            Unique organization ID.
        display_name : str, optional
            Sets a display name for the project.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.

        Returns
        -------
        project : Project
            Object representing the newly created project.

        """

        # Construct URL.
        url = dt.base_url + '/projects'

        # Construct request body.
        body: dict = dict()
        body['organization'] = 'organizations/' + organization_id
        body['displayName'] = display_name

        # Return Project object of POST request response.
        return cls(dtrequests.post(
            url=url,
            body=body,
            auth=auth,
        ))

    @staticmethod
    def update_project(project_id: str,
                       display_name: Optional[str] = None,
                       auth: Optional[Auth] = None
                       ) -> None:
        """
        Updates the display name a specified project.

        Parameters
        ----------
        project_id : str
            Unique ID of the project to update.
        display_name : str, optional
            If provided, updates the project display name.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.

        """

        # Construct URL.
        url = dt.base_url + '/projects/' + project_id

        # Construct request body.
        body = {}
        if display_name is not None:
            body['displayName'] = display_name

        # Send PATCH request, but return nothing.
        dtrequests.patch(
            url=url,
            body=body,
            auth=auth,
        )

    @staticmethod
    def delete_project(project_id: str,
                       auth: Optional[Auth] = None
                       ) -> None:
        """
        Deletes the specified project.

        Only empty projects can be deleted. If the specified project contains
        any devices or Data Connectors, an error is raised.

        Parameters
        ----------
        project_id : str
            Unique ID of the project to delete.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.

        Raises
        ------
        BadRequest
            If the specified project contains devices or Data Connectors.

        """

        # Construct URL.
        url = dt.base_url + '/projects/' + project_id

        # Send DELETE request, but return nothing.
        dtrequests.delete(
            url=url,
            auth=auth,
        )

    @staticmethod
    def list_members(project_id: str,
                     auth: Optional[Auth] = None,
                     ) -> list[Member]:
        """
        List all members in the specified project.

        Parameters
        ----------
        project_id : str
            Unique ID of the project to get members from.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.

        Returns
        -------
        members : list[Member]
            List of objects each representing a member.

        """

        # Construct URL
        url = dt.base_url
        url += '/projects/{}/members'.format(project_id)

        # Return list of Member objects of paginated GET response.
        members = dtrequests.auto_paginated_list(
            url=url,
            pagination_key='members',
            auth=auth,
        )
        return [Member(m) for m in members]

    @staticmethod
    def add_member(project_id: str,
                   email: str,
                   roles: list[str],
                   auth: Optional[Auth] = None,
                   ) -> Member:
        """
        Add a new member to the specified project.

        Parameters
        ----------
        project_id : str
            Unique ID of the project to add a member to.
        email : str
            Email of the user or Service Account to be added.
        roles : list[str]
            The role(s) to provide the new member in the project.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.

        Returns
        -------
        member : Member
            Object representing the newly added member.

        """

        # Construct URL
        url = dt.base_url
        url += '/projects/{}/members'.format(project_id)

        # Construct request body.
        body: dict = dict()
        body['roles'] = ['roles/' + r for r in roles]
        body['email'] = email

        # Return Member object of POST request response.
        return Member(dtrequests.post(
            url=url,
            body=body,
            auth=auth,
        ))

    @staticmethod
    def get_member(project_id: str,
                   member_id: str,
                   auth: Optional[Auth] = None,
                   ) -> Member:
        """
        Get a member from the specified project.

        Parameters
        ----------
        project_id : str
            Unique ID of the project to get a member from.
        member_id : str
            Unique ID of the member to get.
            For Service Account members, this is the Service Account ID.
            For User members, this is the unique User ID.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.

        Returns
        -------
        member : Member
            Object representing the member.

        """

        # Construct URL
        url = dt.base_url
        url += '/projects/{}/members/{}'.format(
            project_id,
            member_id,
        )

        # Return Member object of GET request response.
        return Member(dtrequests.get(
            url=url,
            auth=auth,
        ))

    @staticmethod
    def update_member(project_id: str,
                      member_id: str,
                      roles: Optional[list[str]] = None,
                      auth: Optional[Auth] = None,
                      ) -> Member:
        """
        Update the role(s) of the specified member.

        Parameters
        ----------
        project_id : str
            Unique ID of the project to update a member in.
        member_id : str
            Unique ID of the member to get.
            For Service Account members, this is the Service Account ID.
            For User members, this is the unique User ID.
        roles : list[str], optional
            List of new roles for the specified member.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.

        Returns
        -------
        member : Member
            Object representing the updated member.

        """

        # Construct URL
        url = dt.base_url
        url += '/projects/{}/members/{}'.format(
            project_id,
            member_id,
        )

        # Construct request body.
        body: dict = dict()
        if roles is not None:
            body['roles'] = ['roles/' + r for r in roles]

        # Return updated Member object of PATCH request response.
        return Member(dtrequests.patch(
            url=url,
            body=body,
            auth=auth,
        ))

    @staticmethod
    def remove_member(project_id: str,
                      member_id: str,
                      auth: Optional[Auth] = None,
                      ) -> None:
        """
        Revoke a member's membership in the specified project.

        Parameters
        ----------
        project_id : str
            Unique ID of the project to remove a member from.
        member_id : str
            Unique ID of the member to get.
            For Service Account members, this is the Service Account ID.
            For User members, this is the unique User ID.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.

        """

        # Construct URL
        url = dt.base_url
        url += '/projects/{}/members/{}'.format(
            project_id,
            member_id,
        )

        # Send DELETE request, but return nothing.
        dtrequests.delete(
            url=url,
            auth=auth,
        )

    @staticmethod
    def get_member_invite_url(project_id: str,
                              member_id: str,
                              auth: Optional[Auth] = None,
                              ) -> None:
        """
        Get the invite URL for a member with pending invite.

        This will only work if the invite is still pending. If the invite has
        already been accepted, an error is raised.

        Parameters
        ----------
        project_id : str
            Unique ID of the project of the member to get the URL from.
        member_id : str
            Unique ID of the member to get.
            For Service Account members, this is the Service Account ID.
            For User members, this is the unique User ID.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.

        Raises
        ------
        BadRequest
            If the invite has already been accepted.

        """

        # Construct URL
        url = dt.base_url
        url += '/projects/{}/members/{}'.format(
            project_id,
            member_id,
        ) + ':getInviteUrl'

        # Return url string in GET response.
        return dtrequests.get(
            url=url,
            auth=auth,
        )['inviteUrl']

    @staticmethod
    def list_permissions(project_id: str,
                         auth: Optional[Auth] = None,
                         ) -> list[str]:
        """
        List permissions available in the specified project.

        Parameters
        ----------
        project_id : str
            Unique ID of the project to list permissions in.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.

        Returns
        -------
        permissions : list[str]
            List of available permissions.

        """

        # Construct URL
        url = dt.base_url
        url += '/projects/{}/permissions'.format(project_id)

        # Return list of permissions in GET response.
        return dtrequests.auto_paginated_list(
            url=url,
            pagination_key='permissions',
            auth=auth,
        )
