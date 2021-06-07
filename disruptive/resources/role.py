from __future__ import annotations

from typing import Any

import disruptive.requests as dtrequests
from disruptive.outputs import OutputBase


class Role(OutputBase):
    """
    Represents a role.

    When a role response is received, the content is
    unpacked and the related attributes are updated.

    Attributes
    ----------
    role : str
        Name of the role.
    display_name : str
        Display name of the role.
    description : str
        Description of what the role entails.
    permissions : list[str]
        List of permissions provided with the role.

    """

    # Constants for the available roles.
    PROJECT_USER = 'project.user'
    PROJECT_DEVELOPER = 'project.developer'
    PROJECT_ADMIN = 'project.admin'
    ORGANIZATION_ADMIN = 'organization.admin'
    ROLES = [PROJECT_USER, PROJECT_DEVELOPER, PROJECT_ADMIN,
             ORGANIZATION_ADMIN]

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
        self.role: str = role['name'].split('/')[-1]
        self.display_name: str = role['displayName']
        self.description: str = role['description']
        self.permissions: list[str] = role['permissions']

    @classmethod
    def get_role(cls,
                 role: str,
                 **kwargs: Any,
                 ) -> Role:
        """
        Gets a role specified by its name.

        Parameters
        ----------
        role : str
            :ref:`Name <role_types>` of the role.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        role : Role
            Object representing the specified :ref:`role <role_types>`.

        Examples
        --------
        >>> # Fetch information about the project.developer role.
        >>> role = disruptive.Role.get_role(disruptive.Role.PROJECT_DEVELOPER)

        """

        # Return list of Role objects.
        return cls(dtrequests.DTRequest.get(
            url='/roles/' + role,
            **kwargs,
        ))

    @classmethod
    def list_roles(cls, **kwargs: Any) -> list[Role]:
        """
        List all available roles.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        roles : list[Role]
            List of objects each representing a :ref:`role <role_types>`.

        Examples
        --------
        >>> # Fetch information about all available roles.
        >>> roles = disruptive.Role.list_roles()

        """

        # Return list of Role objects.
        response = dtrequests.DTRequest.paginated_get(
            url='/roles',
            pagination_key='roles',
            **kwargs,
        )
        return [cls(r) for r in response]
