Project
-------
The Project resource can be used to interact with `projects <https://developer.disruptive-technologies.com/docs/overview#projects>`_. Various tasks can be performed by using the API Methods included in the class.

- :ref:`get_project() <get_project>`
- :ref:`list_projects() <list_projects>`
- :ref:`create_project() <create_project>`
- :ref:`update_project() <update_project>`
- :ref:`delete_project() <delete_project>`
- :ref:`list_members() <list_members>`
- :ref:`add_member() <project_add_member>`
- :ref:`update_member() <update_member>`
- :ref:`remove_member() <remove_member>`
- :ref:`get_member_invite_url() <get_member_invite_url>`
- :ref:`list_permissions() <list_permissions>`

Each project fetched by an API Method is represented by an instance of the :ref:`Project <project>` class that is returned to the user.

API Methods
^^^^^^^^^^^
.. _get_project:
.. autofunction:: disruptive.Project.get_project
.. _list_projects:
.. autofunction:: disruptive.Project.list_projects
.. _create_project:
.. autofunction:: disruptive.Project.create_project
.. _update_project:
.. autofunction:: disruptive.Project.update_project
.. _delete_project:
.. autofunction:: disruptive.Project.delete_project
.. _list_members:
.. autofunction:: disruptive.Project.list_members
.. _project_add_member:
.. autofunction:: disruptive.Project.add_member
.. _update_member:
.. autofunction:: disruptive.Project.update_member
.. _remove_member:
.. autofunction:: disruptive.Project.remove_member
.. _get_member_invite_url:
.. autofunction:: disruptive.Project.get_member_invite_url
.. _list_permissions:
.. autofunction:: disruptive.Project.list_permissions

.. _project:

Class
^^^^^
.. autoclass:: disruptive.Project
