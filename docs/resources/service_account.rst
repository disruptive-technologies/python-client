ServiceAccount
--------------
The ServiceAccount resource can be used to interact with `Service Accounts <https://developer.disruptive-technologies.com/docs/service-accounts/introduction-to-service-accounts>`_. Various tasks can be performed by using the API Methods included in the class.

- :ref:`get_service_account() <get_service_account>`
- :ref:`list_service_accounts() <list_service_accounts>`
- :ref:`create_service_account() <create_service_account>`
- :ref:`update_service_account() <update_service_account>`
- :ref:`delete_service_account() <delete_service_account>`
- :ref:`list_keys() <list_keys>`
- :ref:`get_key() <get_key>`
- :ref:`create_key() <create_key>`
- :ref:`delete_key() <delete_key>`

Each Service Account fetched by an API Method is represented by an instance of the :ref:`ServiceAccount <service_account>` class that is returned to the user.

API Methods
^^^^^^^^^^^
.. _get_service_account:
.. autofunction:: disruptive.ServiceAccount.get_service_account
.. _list_service_accounts:
.. autofunction:: disruptive.ServiceAccount.list_service_accounts
.. _create_service_account:
.. autofunction:: disruptive.ServiceAccount.create_service_account
.. _update_service_account:
.. autofunction:: disruptive.ServiceAccount.update_service_account
.. _delete_service_account:
.. autofunction:: disruptive.ServiceAccount.delete_service_account
.. _list_keys:
.. autofunction:: disruptive.ServiceAccount.list_keys
.. _get_key:
.. autofunction:: disruptive.ServiceAccount.get_key
.. _create_key:
.. autofunction:: disruptive.ServiceAccount.create_key
.. _delete_key:
.. autofunction:: disruptive.ServiceAccount.delete_key

.. _service_account:

Class
^^^^^
.. autoclass:: disruptive.ServiceAccount

.. toctree::
   :hidden:
   :maxdepth: 4
   :caption: Extras:

   service_account/key
