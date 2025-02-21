from __future__ import annotations

from typing import Any

import disruptive.requests as dtrequests
from disruptive.outputs import OutputBase, Member


class Organization(OutputBase):
    """
    Represents an organization.

    When an organization response is received, the content
    is unpacked and the related attributes updated.

    Attributes
    ----------
    organization_id : str
        Unique organization ID.
    display_name : str
        The provided display name.
    raw : dict[str, str]
        Unmodified API response JSON.

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
        self.organization_id: str = organization["name"].split("/")[-1]
        self.display_name: str = organization["displayName"]

    @classmethod
    def get_organization(
        cls,
        organization_id: str,
        **kwargs: Any,
    ) -> Organization:
        """
        Get a single organization.

        Parameters
        ----------
        organization_id : str
            Unique organization ID.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        organization : Organization
            Object representing the specified organization.

        Examples
        --------
        >>> # Fetch information about a specific organization.
        >>> org = dt.Organization.get_organization('<ORGANIZATION_ID>')

        """

        # Construct URL
        url = "/organizations/{}".format(organization_id)

        # Return Organization object of GET request response.
        return cls(
            dtrequests.DTRequest.get(
                url=url,
                **kwargs,
            )
        )

    @classmethod
    def list_organizations(cls, **kwargs: Any) -> list[Organization]:
        """
        Gets a list of all available organizations.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        organizations : list[Organization]
            List of objects each representing an organization.

        Examples
        --------
        >>> # Fetch information about all available organizations.
        >>> orgs = dt.Organization.list_organizations()

        """

        # Return list of Organization objects of paginated GET response.
        orgs = dtrequests.DTRequest.paginated_get(
            url="/organizations",
            pagination_key="organizations",
            **kwargs,
        )
        return [cls(org) for org in orgs]

    @staticmethod
    def list_members(
        organization_id: str,
        **kwargs: Any,
    ) -> list[Member]:
        """
        Gets a list of all members in an organization.

        Parameters
        ----------
        organization_id : str
            Unique ID of the organization to get members from.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        members : list[Member]
            List of objects each representing a member.

        Examples
        --------
        >>> # Fetch information about all members in an organization.
        >>> members = dt.Organization.list_members('<ORGANIZATION_ID>')

        """

        # Construct URL
        url = "/organizations/{}/members".format(organization_id)

        # Return list of Member objects of paginated GET response.
        members = dtrequests.DTRequest.paginated_get(
            url=url,
            pagination_key="members",
            **kwargs,
        )
        return [Member(m) for m in members]

    @staticmethod
    def add_member(
        organization_id: str,
        email: str,
        roles: list[str],
        **kwargs: Any,
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
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        member : Member
            Object representing the newly added member.

        Examples
        --------
        >>> # Add a new member to an organization.
        >>> member = dt.Organization.add_member(
        ...     organization_id='<ORGANIZATION_ID>',
        ...     email='<EMAIL_ADDRESS>',
        ...     roles=[dt.Role.ORGANIZATION_ADMIN],
        ... )

        """

        # Construct URL
        url = "/organizations/{}/members".format(organization_id)

        # Construct request body.
        body: dict = dict()
        body["roles"] = ["roles/" + r for r in roles]
        body["email"] = email

        # Return Member object of POST request response.
        return Member(
            dtrequests.DTRequest.post(
                url=url,
                body=body,
                **kwargs,
            )
        )

    @staticmethod
    def get_member(
        member_id: str,
        organization_id: str,
        **kwargs: Any,
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
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        member : Member
            Object representing the member.

        Examples
        --------
        >>> # Fetch information about a specific member in an organization.
        >>> org = dt.Organization.get_organization(
        ...     member_id='<MEMBER_ID>',
        ...     organization_id='<ORGANIZATION_ID>',
        ... )

        """

        # Construct URL
        url = "/organizations/{}/members/{}".format(
            organization_id,
            member_id,
        )

        # Return Member object of GET request response.
        return Member(
            dtrequests.DTRequest.get(
                url=url,
                **kwargs,
            )
        )

    @staticmethod
    def remove_member(
        member_id: str,
        organization_id: str,
        **kwargs: Any,
    ) -> None:
        """
        Revoke a member's membership in the specified organization.
        This does not delete the underlying Service Account or User.

        Parameters
        ----------
        member_id : str
            Unique ID of the member to get.
            For Service Account members, this is the Service Account ID.
            For User members, this is the unique User ID.
        organization_id : str
            Unique ID of the organization to remove a member from.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Examples
        --------
        >>> # Revoke the membership of a member in an organization.
        >>> org = dt.Organization.remove_member(
        ...     member_id='<MEMBER_ID>',
        ...     organization_id='<ORGANIZATION_ID>',
        ... )

        """

        # Construct URL
        url = "/organizations/{}/members/{}".format(
            organization_id,
            member_id,
        )

        # Send DELETE request, but return nothing.
        dtrequests.DTRequest.delete(
            url=url,
            **kwargs,
        )

    @staticmethod
    def get_member_invite_url(
        member_id: str,
        organization_id: str,
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
        organization_id : str
            Unique ID of the organization of the member to get the URL from.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Raises
        ------
        BadRequest
            If the invite has already been accepted.

        Examples
        --------
        >>> # Fetch the pending invite URL for a member.
        >>> org = dt.Organization.get_member_invite_url(
        ...     member_id='<MEMBER_ID>',
        ...     organization_id='<ORGANIZATION_ID>',
        ... )

        """

        # Construct URL
        url = (
            "/organizations/{}/members/{}".format(
                organization_id,
                member_id,
            )
            + ":getInviteUrl"
        )

        # Return url string in GET response.
        invite_url: str = dtrequests.DTRequest.get(
            url=url,
            **kwargs,
        )["inviteUrl"]
        return invite_url

    @staticmethod
    def list_permissions(
        organization_id: str,
        **kwargs: Any,
    ) -> list[str]:
        """
        List permissions available in the specified organization.

        Parameters
        ----------
        organization_id : str
            Unique ID of the organization to list permissions in.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        permissions : list[str]
            List of available permissions.

        Examples
        --------
        >>> # List all available permissions in an organization.
        >>> org = dt.Organization.list_permissions(
        ...     organization_id='<ORGANIZATION_ID>',
        ... )

        """

        # Construct URL
        url = "/organizations/{}/permissions".format(organization_id)

        # Return list of permissions in GET response.
        permissions: list[str] = dtrequests.DTRequest.paginated_get(
            url=url,
            pagination_key="permissions",
            **kwargs,
        )
        return permissions
