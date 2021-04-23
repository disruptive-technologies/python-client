ServiceAccount
--------------
The ServiceAccount resource can be used to interact with `Service Accounts <https://developer.disruptive-technologies.com/docs/service-accounts/introduction-to-service-accounts>`_. Various tasks can be performed by using the API Methods included in the class.

- :ref:`get_serviceaccount() <get_serviceaccount>`
- :ref:`list_serviceaccounts() <list_serviceaccounts>`
- :ref:`create_serviceaccount() <create_serviceaccount>`
- :ref:`update_serviceaccount() <update_serviceaccount>`
- :ref:`delete_serviceaccount() <delete_serviceaccount>`
- :ref:`list_keys() <list_keys>`
- :ref:`get_key() <get_key>`
- :ref:`create_key() <create_key>`
- :ref:`delete_key() <delete_key>`

Each Service Account fetched by an API Method is represented by an instance of the :ref:`ServiceAccount <serviceaccount>` class that is returned to the user.

API Methods
^^^^^^^^^^^
.. _get_serviceaccount:
.. autofunction:: disruptive.ServiceAccount.get_serviceaccount
.. _list_serviceaccounts:
.. autofunction:: disruptive.ServiceAccount.list_serviceaccounts
.. _create_serviceaccount:
.. autofunction:: disruptive.ServiceAccount.create_serviceaccount
.. _update_serviceaccount:
.. autofunction:: disruptive.ServiceAccount.update_serviceaccount
.. _delete_serviceaccount:
.. autofunction:: disruptive.ServiceAccount.delete_serviceaccount
.. _list_keys:
.. autofunction:: disruptive.ServiceAccount.list_keys
.. _get_key:
.. autofunction:: disruptive.ServiceAccount.get_key
.. _create_key:
.. autofunction:: disruptive.ServiceAccount.create_key
.. _delete_key:
.. autofunction:: disruptive.ServiceAccount.delete_key

.. _serviceaccount:

Class
^^^^^
.. autoclass:: disruptive.ServiceAccount

.. toctree::
   :hidden:
   :maxdepth: 4
   :caption: Extras:

   key
