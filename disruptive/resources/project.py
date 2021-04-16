from __future__ import annotations

# Standard library imports.
from typing import Optional

# Project imports.
import disruptive.requests as dtrequests
from disruptive.outputs import OutputBase, Member


class Project(OutputBase):
    """
    Represents a project.

    When a project response is received, the content is
    unpacked and the related attributes are updated.

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
        self.id = project['name'].split('/')[-1]
        self.display_name = project['displayName']
        self.organization_id = project['organization'].split('/')[-1]
        self.organization_display_name = project['organizationDisplayName']
        self.sensor_count = project['sensorCount']
        self.cloud_connector_count = project['cloudConnectorCount']
        self.is_inventory = project['inventory']

    @classmethod
    def get_project(cls,
                    project_id: str,
                    **kwargs,
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
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        project : Project
            Object representing the specified project.

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
                      **kwargs,
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
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        projects : list[Project]
            List of objects each representing a project.

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
                       **kwargs,
                       ) -> Project:
        """
        Create a new project in the specified organization.

        Parameters
        ----------
        organization_id : str
            Unique organization ID.
        display_name : str
            Sets a display name for the project.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        project : Project
            Object representing the newly created project.

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
                       **kwargs,
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
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

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
                       **kwargs,
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
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Raises
        ------
        BadRequest
            If the specified project contains devices or Data Connectors.

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
                     **kwargs,
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
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        members : list[Member]
            List of objects each representing a member.

        """

        # Construct URL
        url = '/projects/{}/members'.format(project_id)

        # Return list of Member objects of paginated GET response.
        members = dtrequests.DTRequest.paginated_get(
            url=url,
            pagination_key='members',
            **kwargs,
        )
        return [Member(m) for m in members]

    @staticmethod
    def add_member(project_id: str,
                   email: str,
                   roles: list[str],
                   **kwargs,
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
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        member : Member
            Object representing the newly added member.

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
                   **kwargs,
                   ) -> Member:
        """
        Get a member from the specified project.

        Parameters
        ----------
        member_id : str
            Unique ID of the member to get.
            For Service Account members, this is the Service Account ID.
            For User members, this is the unique User ID.
        project_id : str
            Unique ID of the project to get a member from.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        member : Member
            Object representing the member.

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
                      roles: Optional[list[str]] = None,
                      **kwargs,
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
        roles : list[str], optional
            List of new roles for the specified member.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        member : Member
            Object representing the updated member.

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
                      **kwargs,
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
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

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
                              **kwargs,
                              ) -> None:
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
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Raises
        ------
        BadRequest
            If the invite has already been accepted.

        """

        # Construct URL
        url = '/projects/{}/members/{}'.format(
            project_id,
            member_id,
        ) + ':getInviteUrl'

        # Return url string in GET response.
        return dtrequests.DTRequest.get(
            url=url,
            **kwargs,
        )['inviteUrl']

    @staticmethod
    def list_permissions(project_id: str,
                         **kwargs,
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
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        permissions : list[str]
            List of available permissions.

        """

        # Construct URL
        url = '/projects/{}/permissions'.format(project_id)

        # Return list of permissions in GET response.
        return dtrequests.DTRequest.paginated_get(
            url=url,
            pagination_key='permissions',
            **kwargs,
        )
