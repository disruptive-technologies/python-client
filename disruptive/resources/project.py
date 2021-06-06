from __future__ import annotations

from typing import Optional, Any

import disruptive.requests as dtrequests
from disruptive.outputs import OutputBase, Member


class Project(OutputBase):
    """
    Represents a project.

    When a project response is received, the content is
    unpacked and the related attributes are set.

    Attributes
    ----------
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
        self.id: str = project['name'].split('/')[-1]
        self.display_name: str = project['displayName']
        self.organization_id: str = project['organization'].split('/')[-1]
        self.organization_display_name: str = \
            project['organizationDisplayName']
        self.sensor_count: int = project['sensorCount']
        self.cloud_connector_count: int = project['cloudConnectorCount']
        self.is_inventory: bool = project['inventory']

    @classmethod
    def get_project(cls,
                    project_id: str,
                    **kwargs: Any,
                    ) -> Project:
        """
        Gets the current state of a single project.

        Parameters
        ----------
        project_id : str
            Unique project ID.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        project : Project
            Object representing the specified project.

        Examples
        --------
        >>> # Fetch information about a specific project.
        >>> project = disruptive.Project.get_project(
        ...     project_id='<PROJECT_ID>',
        ... )

        """

        # Construct URL.
        url = '/projects/{}'.format(project_id)

        # Return Project object of GET request response.
        return cls(dtrequests.DTRequest.get(
            url=url,
            **kwargs,
        ))

    @classmethod
    def list_projects(cls,
                      organization_id: Optional[str] = None,
                      query: Optional[str] = None,
                      **kwargs: Any,
                      ) -> list[Project]:
        """
        Gets a list of the current state of all available projects.

        Parameters
        ----------
        organization_id : str
            Unique organization ID.
        query : str, optional
            Keyword based search for project- and organization display names.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        projects : list[Project]
            List of objects each representing a project.

        Examples
        --------
        >>> # Fetch information about all projects in an organization.
        >>> projects = disruptive.Project.list_projects(
        ...     organization_id='<ORGANIZATION_ID>',
        ... )

        """

        # Construct URL.
        url = '/projects'

        # Construct parameters dictionary.
        params = {}
        if organization_id is not None:
            params['organization'] = 'organizations/' + organization_id
        if query is not None:
            params['query'] = query

        # Return list of Project objects of paginated GET response.
        responses = dtrequests.DTRequest.paginated_get(
            url=url,
            pagination_key='projects',
            params=params,
            **kwargs,
        )
        return [cls(r) for r in responses]

    @classmethod
    def create_project(cls,
                       organization_id: str,
                       display_name: str,
                       **kwargs: Any,
                       ) -> Project:
        """
        Create a new project in the specified organization.

        Parameters
        ----------
        organization_id : str
            Unique organization ID.
        display_name : str
            Sets a display name for the project.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        project : Project
            Object representing the newly created project.

        Examples
        --------
        >>> # Create a new project.
        >>> project = disruptive.Project.create_project(
        ...     organization_id='<ORGANIZATION_ID>',
        ...     display_name='my-new-project',
        ... )

        """

        # Construct URL.
        url = '/projects'

        # Construct request body.
        body: dict = dict()
        body['organization'] = 'organizations/' + organization_id
        body['displayName'] = display_name

        # Return Project object of POST request response.
        return cls(dtrequests.DTRequest.post(
            url=url,
            body=body,
            **kwargs,
        ))

    @staticmethod
    def update_project(project_id: str,
                       display_name: Optional[str] = None,
                       **kwargs: Any,
                       ) -> None:
        """
        Updates the display name a specified project.

        Parameters
        ----------
        project_id : str
            Unique ID of the project to update.
        display_name : str, optional
            If provided, updates the project display name.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Examples
        --------
        >>> # Update the display_name of a project.
        >>> disruptive.Project.update_project(
        ...     project_id='<PROJECT_ID>',
        ...     display_name='new-name',
        ... )

        """

        # Construct URL.
        url = '/projects/' + project_id

        # Construct request body.
        body = {}
        if display_name is not None:
            body['displayName'] = display_name

        # Send PATCH request, but return nothing.
        dtrequests.DTRequest.patch(
            url=url,
            body=body,
            **kwargs,
        )

    @staticmethod
    def delete_project(project_id: str,
                       **kwargs: Any,
                       ) -> None:
        """
        Deletes the specified project.

        Only empty projects can be deleted. If the specified project contains
        any devices or Data Connectors, an error is raised.

        Parameters
        ----------
        project_id : str
            Unique ID of the project to delete.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Raises
        ------
        BadRequest
            If the specified project contains devices or Data Connectors.

        Examples
        --------
        >>> # Delete the specified project.
        >>> disruptive.Project.delete_project(
        ...     project_id='<PROJECT_ID>',
        ... )

        """

        # Construct URL.
        url = '/projects/' + project_id

        # Send DELETE request, but return nothing.
        dtrequests.DTRequest.delete(
            url=url,
            **kwargs,
        )

    @staticmethod
    def list_members(project_id: str,
                     **kwargs: Any,
                     ) -> list[Member]:
        """
        Gets a list of the current state of all members in a project.

        Parameters
        ----------
        project_id : str
            Unique ID of the project to get members from.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        members : list[Member]
            List of objects each representing a member.

        Examples
        --------
        >>> # List all members in a project.
        >>> members = disruptive.Project.list_members(
        ...     project_id='<PROJECT_ID>',
        ... )

        """

        # Construct URL
        url = '/projects/{}/members'.format(project_id)

        # Return list of Member objects of paginated GET response.
        members = dtrequests.DTRequest.paginated_get(
            url=url,
            pagination_key='members',
            **kwargs,
        )
        members_list: list[Member] = [Member(m) for m in members]
        return members_list

    @staticmethod
    def add_member(project_id: str,
                   email: str,
                   roles: list[str],
                   **kwargs: Any,
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
            The :ref:`role(s) <role_types>` to provide the
            new member in the project.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        member : Member
            Object representing the newly added member.

        Examples
        --------
        >>> # Add a new project.developer member to a project.
        >>> member = disruptive.Project.add_member(
        ...     project_id='<PROJECT_ID>',
        ...     email='<MEMBER_EMAIL_ADDRESS>',
        ...     roles=[disruptive.Role.PROJECT_DEVELOPER],
        ... )

        """

        # Construct URL
        url = '/projects/{}/members'.format(project_id)

        # Construct request body.
        body: dict = dict()
        body['roles'] = ['roles/' + r for r in roles]
        body['email'] = email

        # Return Member object of POST request response.
        return Member(dtrequests.DTRequest.post(
            url=url,
            body=body,
            **kwargs,
        ))

    @staticmethod
    def get_member(member_id: str,
                   project_id: str,
                   **kwargs: Any,
                   ) -> Member:
        """
        Get the state of a member in the specified project.

        Parameters
        ----------
        member_id : str
            Unique ID of the member to get.
            For Service Account members, this is the Service Account ID.
            For User members, this is the unique User ID.
        project_id : str
            Unique ID of the project to get a member from.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        member : Member
            Object representing the member.

        Examples
        --------
        >>> # Fetch information about the specified member.
        >>> member = disruptive.Project.get_member(
        ...     member_id='<MEMBER_ID>',
        ...     project_id='<PROJECT_ID>',
        ... )

        """

        # Construct URL
        url = '/projects/{}/members/{}'.format(
            project_id,
            member_id,
        )

        # Return Member object of GET request response.
        return Member(dtrequests.DTRequest.get(
            url=url,
            **kwargs,
        ))

    @staticmethod
    def update_member(member_id: str,
                      project_id: str,
                      roles: list[str],
                      **kwargs: Any,
                      ) -> Member:
        """
        Update the role(s) of the specified member.

        Parameters
        ----------
        member_id : str
            Unique ID of the member to get.
            For Service Account members, this is the Service Account ID.
            For User members, this is the unique User ID.
        project_id : str
            Unique ID of the project to update a member in.
        roles : list[str]
            List of new :ref:`roles <role_types>` for the specified member.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        member : Member
            Object representing the updated member.

        Examples
        --------
        >>> # Update the role of a member.
        >>> member = disruptive.Project.update_member(
        ...     member_id='<MEMBER_ID>',
        ...     project_id='<PROJECT_ID>',
        ...     roles=[disruptive.Role.PROJECT_USER],
        ... )

        """

        # Construct URL
        url = '/projects/{}/members/{}'.format(
            project_id,
            member_id,
        )

        # Construct request body.
        body: dict = dict()
        if roles is not None:
            body['roles'] = ['roles/' + r for r in roles]

        # Return updated Member object of PATCH request response.
        return Member(dtrequests.DTRequest.patch(
            url=url,
            body=body,
            **kwargs,
        ))

    @staticmethod
    def remove_member(member_id: str,
                      project_id: str,
                      **kwargs: Any,
                      ) -> None:
        """
        Revoke a member's membership in the specified project.

        Parameters
        ----------
        member_id : str
            Unique ID of the member to get.
            For Service Account members, this is the Service Account ID.
            For User members, this is the unique User ID.
        project_id : str
            Unique ID of the project to remove a member from.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Examples
        --------
        >>> # Remove the specified member from a project.
        >>> disruptive.Project.remove_member(
        ...     member_id='<MEMBER_ID>',
        ...     project_id='<PROJECT_ID>',
        ... )

        """

        # Construct URL
        url = '/projects/{}/members/{}'.format(
            project_id,
            member_id,
        )

        # Send DELETE request, but return nothing.
        dtrequests.DTRequest.delete(
            url=url,
            **kwargs,
        )

    @staticmethod
    def get_member_invite_url(member_id: str,
                              project_id: str,
                              **kwargs: Any,
                              ) -> str:
        """
        Get the invite URL for a member with pending invite.

        This will only work if the invite is still pending. If the invite has
        already been accepted, an error is raised.

        Parameters
        ----------
        member_id : str
            Unique ID of the member to get.
            For Service Account members, this is the Service Account ID.
            For User members, this is the unique User ID.
        project_id : str
            Unique ID of the project of the member to get the URL from.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        invite_url : str
            The invite url for the specified member.

        Raises
        ------
        BadRequest
            If the invite has already been accepted.

        Examples
        --------
        >>> # Fetch the pending invite URL of a member.
        >>> url = disruptive.Project.get_member_invite_url(
        ...     member_id='<MEMBER_ID>',
        ...     project_id='<PROJECT_ID>',
        ... )

        """

        # Construct URL
        url = '/projects/{}/members/{}'.format(
            project_id,
            member_id,
        ) + ':getInviteUrl'

        # Return url string in GET response.
        invite_url: str = dtrequests.DTRequest.get(
            url=url,
            **kwargs,
        )['inviteUrl']
        return invite_url

    @staticmethod
    def list_permissions(project_id: str,
                         **kwargs: Any,
                         ) -> list[str]:
        """
        List permissions available to the caller in the specified project.

        Parameters
        ----------
        project_id : str
            Unique ID of the project to list permissions in.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        permissions : list[str]
            List of permissions available to the caller.

        Examples
        --------
        >>> # List the available permissions in a project.
        >>> permissions = disruptive.Project.list_permissions('<PROJECT_ID>')

        """

        # Construct URL
        url = '/projects/{}/permissions'.format(project_id)

        # Return list of permissions in GET response.
        permissions: list[str] = dtrequests.DTRequest.paginated_get(
            url=url,
            pagination_key='permissions',
            **kwargs,
        )
        return permissions
