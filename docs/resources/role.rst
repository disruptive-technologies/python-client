Role
====
The Role resource can be used to fetch `roles <https://developer.disruptive-technologies.com/docs/devices>`_ information. This can be done by using the API Methods included in the class.

- :ref:`get_role() <get_role>`
- :ref:`list_roles() <list_roles>`

Each role fetched by an API Method is represented by an instance of the :ref:`Role <role>` class that is returned to the user.

API Methods
-----------
.. _get_role:
.. autofunction:: disruptive.Role.get_role
.. _list_roles:
.. autofunction:: disruptive.Role.list_roles

.. _role:

Class
-----
.. autoclass:: disruptive.Role

.. _role_types:

Type Constants
--------------
The Role class contains a string constant for each available role.

.. autoattribute:: disruptive.Role.PROJECT_USER
.. autoattribute:: disruptive.Role.PROJECT_DEVELOPER
.. autoattribute:: disruptive.Role.PROJECT_ADMIN
.. autoattribute:: disruptive.Role.ORGANIZATION_ADMIN
.. autoattribute:: disruptive.Role.ROLES

This can be a useful alternative to writing the strings directly.

.. code-block:: python

   # Add a new developer member to the specified project.
   dt.Project.add_member(
       project_id='<PROJECT_ID>',
       email='<EMAIL_ADDRESS>',
       roles=[dt.Role.PROJECT_DEVELOPER],
   )
