from __future__ import annotations

# Project imports.
import disruptive.requests as dtrequests
from disruptive.outputs import OutputBase, Member


class Organization(OutputBase):
    """
    Represents an organization.

    When an organization response is received, the content
    is unpacked and the related attributes updated.

    Attributes
    ----------
    id : str
        Unique organization ID.
    display_name : str
        The provided display name.

    """

    def __init__(self, organization: dict) -> None:
        """
        Constructs the Organization object by unpacking the raw response.

        Parameters
        ----------
        organization : dict
            Unmodified organization response dictionary.

        """

        # Inherit from OutputBase parent.
        OutputBase.__init__(self, organization)

        # Unpack attributes from dictionary.
        self.id = organization['name'].split('/')[-1]
        self.display_name = organization['displayName']

    @classmethod
    def get_organization(cls,
                         organization_id: str,
                         **kwargs,
                         ) -> Organization:
        """
        Gets an organization specified by its ID.

        Parameters
        ----------
        organization_id : str
            Unique organization ID.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        organization : Organization
            Object representing the specified organization.

        """

        # Construct URL
        url = '/organizations/{}'.format(organization_id)

        # Return Organization object of GET request response.
        return cls(dtrequests.DTRequest.get(
            url=url,
            **kwargs,
        ))

    @classmethod
    def list_organizations(cls,
                           **kwargs,
                           ) -> list[Organization]:
        """
        List all available organizations.

        Parameters
        ----------
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        organizations : list[Organization]
            List of objects each representing an organization.

        """

        # Return list of Organization objects of paginated GET response.
        orgs = dtrequests.DTRequest.paginated_get(
            url='/organizations',
            pagination_key='organizations',
            **kwargs,
        )
        return [cls(org) for org in orgs]

    @staticmethod
    def list_members(organization_id: str,
                     **kwargs,
                     ) -> list[Member]:
        """
        List all members in the specified organization.

        Parameters
        ----------
        organization_id : str
            Unique ID of the organization to get members from.
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
        url = '/organizations/{}/members'.format(organization_id)

        # Return list of Member objects of paginated GET response.
        members = dtrequests.DTRequest.paginated_get(
            url=url,
            pagination_key='members',
            **kwargs,
        )
        return [Member(m) for m in members]

    @staticmethod
    def add_member(organization_id: str,
                   email: str,
                   roles: list[str],
                   **kwargs,
                   ) -> Member:
        """
        Add a new member to the specified organization.

        Parameters
        ----------
        organization_id : str
            Unique ID of the organization to add a member to.
        email : str
            Email of the user or Service Account to be added.
        roles : {["organization.admin"]} list[str]
            The role(s) to provide the new member in the organization.
            Currently only supports organization.admin.
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
        url = '/organizations/{}/members'.format(organization_id)

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
                   organization_id: str,
                   **kwargs,
                   ) -> Member:
        """
        Get a member from the specified organization.

        Parameters
        ----------
        member_id : str
            Unique ID of the member to get.
            For Service Account members, this is the Service Account ID.
            For User members, this is the unique User ID.
        organization_id : str
            Unique ID of the organization to get a member from.
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
        url = '/organizations/{}/members/{}'.format(
            organization_id,
            member_id,
        )

        # Return Member object of GET request response.
        return Member(dtrequests.DTRequest.get(
            url=url,
            **kwargs,
        ))

    @staticmethod
    def remove_member(member_id: str,
                      organization_id: str,
                      **kwargs,
                      ) -> None:
        """
        Revoke a member's membership in the specified organization.

        Parameters
        ----------
        member_id : str
            Unique ID of the member to get.
            For Service Account members, this is the Service Account ID.
            For User members, this is the unique User ID.
        organization_id : str
            Unique ID of the organization to remove a member from.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        """

        # Construct URL
        url = '/organizations/{}/members/{}'.format(
            organization_id,
            member_id,
        )

        # Send DELETE request, but return nothing.
        dtrequests.DTRequest.delete(
            url=url,
            **kwargs,
        )

    @staticmethod
    def get_member_invite_url(member_id: str,
                              organization_id: str,
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
        organization_id : str
            Unique ID of the organization of the member to get the URL from.
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
        url = '/organizations/{}/members/{}'.format(
            organization_id,
            member_id,
        ) + ':getInviteUrl'

        # Return url string in GET response.
        return dtrequests.DTRequest.get(
            url=url,
            **kwargs,
        )['inviteUrl']

    @staticmethod
    def list_permissions(organization_id: str,
                         **kwargs,
                         ) -> list[str]:
        """
        List permissions available in the specified organization.

        Parameters
        ----------
        organization_id : str
            Unique ID of the organization to list permissions in.
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
        url = '/organizations/{}/permissions'.format(organization_id)

        # Return list of permissions in GET response.
        return dtrequests.DTRequest.paginated_get(
            url=url,
            pagination_key='permissions',
            **kwargs,
        )
