Role
----
The Role class can fetch the various roles available.

API Methods
^^^^^^^^^^^
.. autofunction:: disruptive.Role.get_role
.. autofunction:: disruptive.Role.list_roles

Class
^^^^^
.. autoclass:: disruptive.Role

   .. rubric:: Available Roles Constants
   .. compound::
      The Role resources class contains one string constant for each available role, including a list of all types.

   .. code-block:: python

      # Add a new developer member to the specified project.
      dt.Project.add_member(
          project_id,
          email,
          roles=[dt.Role.PROJECT_DEVELOPER],
      )

   .. autoattribute:: disruptive.Role.PROJECT_USER
   .. autoattribute:: disruptive.Role.PROJECT_DEVELOPER
   .. autoattribute:: disruptive.Role.PROJECT_ADMIN
   .. autoattribute:: disruptive.Role.ORGANIZATION_ADMIN
