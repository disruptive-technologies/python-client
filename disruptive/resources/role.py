from __future__ import annotations

# Standard library imports.
from typing import Optional

# Project imports.
import disruptive as dt
import disruptive.requests as dtrequests
from disruptive.outputs import OutputBase
from disruptive.authentication import BasicAuth, OAuth


class Role(OutputBase):
    """
    Represents a role.

    When a role response is received, the content is
    unpacked and the related attributes are updated.

    Attributes
    ----------
    raw : dict
        Unmodified role response dictionary.
    role : str
        Name of the role.
    display_name : str
        Display name of the role.
    description : str
        Description of what the role entails.
    permissions : list[str]
        List of permissions provided with the role.

    """

    def __init__(self, role: dict) -> None:
        """
        Constructs the Role object by unpacking the raw role response.

        Parameters
        ----------
        role : dict
            Unmodified role response dictionary.

        """

        # Inherit from Response parent.
        OutputBase.__init__(self, role)

        # Unpack attributes from dictionary.
        self.role = self.raw['name'].split('/')[-1]
        self.display_name = self.raw['displayName']
        self.description = self.raw['description']
        self.permissions = self.raw['permissions']

    @classmethod
    def get_role(cls,
                 role: str,
                 auth: Optional[BasicAuth | OAuth] = None,
                 ) -> Role:
        """
        Gets a role specified by its name.

        Parameters
        ----------
        role : str
            Name of the role.
        auth: BasicAuth, OAuth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.

        Returns
        -------
        role : Role
            Object representing the specified role.

        """

        # Return list of Role objects.
        return cls(dtrequests.get(
            url=dt.base_url + '/roles/' + role,
            auth=auth,
        ))

    @classmethod
    def list_roles(cls,
                   auth: Optional[BasicAuth | OAuth] = None,
                   ) -> list[Role]:
        """
        List all available roles.

        Returns
        -------
        roles : list[Role]
            List of objects each representing a role.

        """

        # Return list of Role objects.
        response = dtrequests.auto_paginated_list(
            url=dt.base_url + '/roles',
            pagination_key='roles',
            auth=auth,
        )
        return [cls(r) for r in response]
