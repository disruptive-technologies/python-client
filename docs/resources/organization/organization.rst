Organization
------------
The Organization resource can be used to interact with `organizations <https://developer.disruptive-technologies.com/docs/overview#organizations>`_. Various tasks can be performed by using the API Methods included in the class.

- :ref:`get_organization() <get_organization>`
- :ref:`list_organizations() <list_organizations>`
- :ref:`list_members() <list_members>`
- :ref:`add_member() <org_add_member>`
- :ref:`get_member() <get_member>`
- :ref:`remove_member() <remove_member>`
- :ref:`get_member_invite_url() <get_member_invite_url>`
- :ref:`list_permissions() <list_permissions>`

Each organization fetched by an API Method is represented by an instance of the :ref:`Organization <organization>` class that is returned to the user.

API Methods
^^^^^^^^^^^
.. _get_organization:
.. autofunction:: disruptive.Organization.get_organization
.. _list_organizations:
.. autofunction:: disruptive.Organization.list_organizations
.. _list_members:
.. autofunction:: disruptive.Organization.list_members
.. _org_add_member:
.. autofunction:: disruptive.Organization.add_member
.. _get_member:
.. autofunction:: disruptive.Organization.get_member
.. _remove_member:
.. autofunction:: disruptive.Organization.remove_member
.. _get_member_invite_url:
.. autofunction:: disruptive.Organization.get_member_invite_url
.. _list_permissions:
.. autofunction:: disruptive.Organization.list_permissions

.. _organization:

Class
^^^^^
.. autoclass:: disruptive.Organization
