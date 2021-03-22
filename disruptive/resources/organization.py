from __future__ import annotations

# Standard library imports
from typing import Optional

# Project imports.
import disruptive as dt
import disruptive.requests as dtrequests
from disruptive.outputs import OutputBase, Member
from disruptive.authentication import BasicAuth, OAuth


class Organization(OutputBase):
    """
    Represents an organization.

    When an organization response is received, the content
    is unpacked and the related attributes updated.

    Attributes
    ----------
    raw : dict
        Unmodified organization response dictionary.
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

        # Unpack organization json.
        self.__unpack()

    def __unpack(self) -> None:
        self.id = self.raw['name'].split('/')[-1]
        self.display_name = self.raw['displayName']

    @classmethod
    def get_organization(cls,
                         organization_id: str,
                         auth: Optional[BasicAuth | OAuth] = None,
                         ) -> Organization:
        """
        Gets an organization specified by its ID.

        Parameters
        ----------
        organization_id : str
            Unique organization ID.
        auth: BasicAuth, OAuth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.

        Returns
        -------
        organization : Organization
            Object representing the specified organization.

        """

        # Construct URL
        url = dt.base_url
        url += '/organizations/{}'.format(organization_id)

        # Return Organization object of GET request response.
        return cls(dtrequests.get(
            url=url,
            auth=auth
        ))

    @classmethod
    def list_organizations(cls,
                           auth: Optional[BasicAuth | OAuth] = None,
                           ) -> list[Organization]:
        """
        List all available organizations.

        Parameters
        ----------
        auth: BasicAuth, OAuth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.

        Returns
        -------
        organizations : list[Organization]
            List of objects each representing an organization.

        """

        # Return list of Organization objects of paginated GET response.
        orgs = dtrequests.auto_paginated_list(
            url=dt.base_url + '/organizations',
            pagination_key='organizations',
            auth=auth,
        )
        return [cls(org) for org in orgs]

    @staticmethod
    def list_members(organization_id: str,
                     auth: Optional[BasicAuth | OAuth] = None,
                     ) -> list[Member]:
        """
        List all members in the specified organization.

        Parameters
        ----------
        organization_id : str
            Unique ID of the organization to get members from.
        auth: BasicAuth, OAuth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.

        Returns
        -------
        members : list[Member]
            List of objects each representing a member.

        """

        # Construct URL
        url = dt.base_url
        url += '/organizations/{}/members'.format(organization_id)

        # Return list of Member objects of paginated GET response.
        members = dtrequests.auto_paginated_list(
            url=url,
            pagination_key='members',
            auth=auth,
        )
        return [Member(m) for m in members]

    @staticmethod
    def add_member(organization_id: str,
                   email: str,
                   roles: list[str],
                   auth: Optional[BasicAuth | OAuth] = None,
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
        auth: BasicAuth, OAuth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.

        Returns
        -------
        member : Member
            Object representing the newly added member.

        """

        # Construct URL
        url = dt.base_url
        url += '/organizations/{}/members'.format(organization_id)

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
    def get_member(organization_id: str,
                   member_id: str,
                   auth: Optional[BasicAuth | OAuth] = None,
                   ) -> Member:
        """
        Get a member from the specified organization.

        Parameters
        ----------
        organization_id : str
            Unique ID of the organization to get a member from.
        member_id : str
            Unique ID of the member to get.
            For Service Account members, this is the Service Account ID.
            For User members, this is the unique User ID.
        auth: BasicAuth, OAuth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.

        Returns
        -------
        member : Member
            Object representing the member.

        """

        # Construct URL
        url = dt.base_url
        url += '/organizations/{}/members/{}'.format(
            organization_id,
            member_id,
        )

        # Return Member object of GET request response.
        return Member(dtrequests.get(
            url=url,
            auth=auth,
        ))

    @staticmethod
    def remove_member(organization_id: str,
                      member_id: str,
                      auth: Optional[BasicAuth | OAuth] = None,
                      ) -> None:
        """
        Revoke a member's membership in the specified organization.

        Parameters
        ----------
        organization_id : str
            Unique ID of the organization to remove a member from.
        member_id : str
            Unique ID of the member to get.
            For Service Account members, this is the Service Account ID.
            For User members, this is the unique User ID.
        auth: BasicAuth, OAuth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.

        """

        # Construct URL
        url = dt.base_url
        url += '/organizations/{}/members/{}'.format(
            organization_id,
            member_id,
        )

        # Send DELETE request, but return nothing.
        dtrequests.delete(
            url=url,
            auth=auth,
        )

    @staticmethod
    def get_member_invite_url(organization_id: str,
                              member_id: str,
                              auth: Optional[BasicAuth | OAuth] = None,
                              ) -> None:
        """
        Get the invite URL for a member with pending invite.

        This will only work if the invite is still pending. If the invite has
        already been accepted, an error is raised.

        Parameters
        ----------
        organization_id : str
            Unique ID of the organization of the member to get the URL from.
        member_id : str
            Unique ID of the member to get.
            For Service Account members, this is the Service Account ID.
            For User members, this is the unique User ID.
        auth: BasicAuth, OAuth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.

        Raises
        ------
        BadRequest
            If the invite has already been accepted.

        """

        # Construct URL
        url = dt.base_url
        url += '/organizations/{}/members/{}'.format(
            organization_id,
            member_id,
        ) + ':getInviteUrl'

        # Return url string in GET response.
        return dtrequests.get(
            url=url,
            auth=auth,
        )['inviteUrl']

    @staticmethod
    def list_permissions(organization_id: str,
                         auth: Optional[BasicAuth | OAuth] = None,
                         ) -> list[str]:
        """
        List permissions available in the specified organization.

        Parameters
        ----------
        organization_id : str
            Unique ID of the organization to list permissions in.
        auth: BasicAuth, OAuth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.

        Returns
        -------
        permissions : list[str]
            List of available permissions.

        """

        # Construct URL
        url = dt.base_url
        url += '/organizations/{}/permissions'.format(organization_id)

        # Return list of permissions in GET response.
        return dtrequests.auto_paginated_list(
            url=url,
            pagination_key='permissions',
            auth=auth,
        )
