from __future__ import annotations

# Project imports.
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
        self.role = role['name'].split('/')[-1]
        self.display_name = role['displayName']
        self.description = role['description']
        self.permissions = role['permissions']

    @classmethod
    def get_role(cls,
                 role: str,
                 **kwargs,
                 ) -> Role:
        """
        Gets a role specified by its name.

        Parameters
        ----------
        role : str
            Name of the role.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_attempts: int, optional
            Number of times a request is attempted before giving up.

        Returns
        -------
        role : Role
            Object representing the specified role.

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
    def list_roles(cls,
                   **kwargs,
                   ) -> list[Role]:
        """
        List all available roles.

        Parameters
        ----------
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_attempts: int, optional
            Number of times a request is attempted before giving up.

        Returns
        -------
        roles : list[Role]
            List of objects each representing a role.

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
