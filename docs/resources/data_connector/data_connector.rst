DataConnector
=============
The DataConnector resource can be used to interact with `Data Connectors <https://developer.disruptive-technologies.com/docs/data-connectors/introduction-to-data-connector>`_. Various tasks can be performed by using the API Methods included in the class.

- :ref:`get_data_connector() <get_data_connector>`
- :ref:`list_data_connectors() <list_data_connectors>`
- :ref:`create_data_connector() <create_data_connector>`
- :ref:`update_data_connector() <update_data_connector>`
- :ref:`delete_data_connector() <delete_data_connector>`
- :ref:`sync_data_connector() <sync_data_connector>`
- :ref:`get_metrics() <get_metrics>`

Each Data Connector fetched by an API Method is represented by an instance of the :ref:`DataConnector <data_connector>` class that is returned to the user.

API Methods
-----------
.. _get_data_connector:
.. autofunction:: disruptive.DataConnector.get_data_connector
.. _list_data_connectors:
.. autofunction:: disruptive.DataConnector.list_data_connectors
.. _create_data_connector:
.. autofunction:: disruptive.DataConnector.create_data_connector
.. _update_data_connector:
.. autofunction:: disruptive.DataConnector.update_data_connector
.. _delete_data_connector:
.. autofunction:: disruptive.DataConnector.delete_data_connector
.. _sync_data_connector:
.. autofunction:: disruptive.DataConnector.sync_data_connector
.. _get_metrics:
.. autofunction:: disruptive.DataConnector.get_metrics

.. _data_connector:

Class
-----
.. autoclass:: disruptive.DataConnector

   .. rubric:: Data Connector Type Constants
   .. compound::
      The DataConnector resources class contains one string constant for each configuration type available, including a list of all types.

   .. autoattribute:: disruptive.DataConnector.HTTP_PUSH
   .. autoattribute:: disruptive.DataConnector.DATA_CONNECTOR_TYPES

Configurations
--------------
The :ref:`DataConnector <data_connector>` `config` attribute holds an instance of a type-specific configuration class.

- :ref:`HttpPushConfig <httppush_config>`

When fetching a Data Connector, this attribute is set automatically, but when :ref:`creating <create_data_connector>` or :ref:`updating <update_data_connector>` one, it must be provided.

.. code-block:: python

   # Create an HTTP_PUSH Data Connector.
   disruptive.DataConnector.create_data_connector(
       project_id='y14u8p094l37cdv1o0ug',
       display_name='new-data-connector',
       config=dt.DataConnector.HttpPushConfig(
           url='https://some-endpoint-url.com',
           signature_secret='good-secret',
       ),
   )

.. _httppush_config:
.. autoclass:: disruptive.DataConnector.HttpPushConfig
   
   .. automethod:: disruptive.DataConnector.HttpPushConfig.__init__

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Extras:

   metrics
