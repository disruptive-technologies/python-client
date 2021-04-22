DataConnector
=============
The DataConnector resource can be used to interact with `Data Connectors <https://developer.disruptive-technologies.com/docs/data-connectors/introduction-to-data-connector>`_. Various tasks can be performed by using the API Methods included in the class.

- :ref:`get_dataconnector() <get_dataconnector>`
- :ref:`list_dataconnectors() <list_dataconnectors>`
- :ref:`create_dataconnector() <create_dataconnector>`
- :ref:`update_dataconnector() <update_dataconnector>`
- :ref:`delete_dataconnector() <delete_dataconnector>`
- :ref:`sync_dataconnector() <sync_dataconnector>`
- :ref:`get_metrics() <get_metrics>`

Each Data Connector fetched by an API Method is represented by an instance of the :ref:`DataConnector <dataconnector>` class that is returned to the user.

API Methods
-----------
.. _get_dataconnector:
.. autofunction:: disruptive.DataConnector.get_dataconnector
.. _list_dataconnectors:
.. autofunction:: disruptive.DataConnector.list_dataconnectors
.. _create_dataconnector:
.. autofunction:: disruptive.DataConnector.create_dataconnector
.. _update_dataconnector:
.. autofunction:: disruptive.DataConnector.update_dataconnector
.. _delete_dataconnector:
.. autofunction:: disruptive.DataConnector.delete_dataconnector
.. _sync_dataconnector:
.. autofunction:: disruptive.DataConnector.sync_dataconnector
.. _get_metrics:
.. autofunction:: disruptive.DataConnector.get_metrics

Class
-----
.. _dataconnector:
.. autoclass:: disruptive.DataConnector

   .. rubric:: Data Connector Type Constants
   .. compound::
      The DataConnector resources class contains one string constant for each configuration type available, including a list of all types.

   .. autoattribute:: disruptive.DataConnector.HTTP_PUSH
   .. autoattribute:: disruptive.DataConnector.DATACONNECTOR_TYPES

Configurations
--------------
When fetching a Data Connector, the `config` attribute holds its type-specific configuration. When creating or updating one, it must be specified with one of the following classes.

.. code-block:: python

   # Create an HTTP_PUSH Data Connector.
   disruptive.DataConnector.create_dataconnector(
       project_id='y14u8p094l37cdv1o0ug',
       display_name='new-dataconnector',
       config=dt.DataConnector.HttpPushConfig(
           url='https://some-endpoint-url.com',
           signature_secret='good-secret',
       ),
   )

.. autoclass:: disruptive.DataConnector.HttpPushConfig
   
   .. automethod:: disruptive.DataConnector.HttpPushConfig.__init__

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Extras:

   metrics
