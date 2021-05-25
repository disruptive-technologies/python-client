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

.. _data_connector_types:

Type Constants
--------------

The DataConnector class contains a string constant for each available Data Connector type.

.. autoattribute:: disruptive.DataConnector.HTTP_PUSH
.. autoattribute:: disruptive.DataConnector.DATA_CONNECTOR_TYPES

.. _data_connector_configs:

Configurations
--------------
The :code:`config` attribute of the :ref:`DataConnector <data_connector>` class holds one of the following type-specific configuration class objects. 

- :ref:`HttpPushConfig <http_push_config>`

When fetching a Data Connector, this attribute is set automatically, but when :ref:`creating <create_data_connector>` or :ref:`updating <update_data_connector>` one, it must be provided.

.. code-block:: python

   import disruptive as dt

   # Create an HTTP_PUSH Data Connector.
   dt.DataConnector.create_data_connector(
      project_id='<PROJECT_ID>',
      config=dt.DataConnector.<CONFIG>('parameters...'),
   )

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Extras:

   data_connector/http_push_config
   data_connector/metrics

.. _data_connector_status:

Status
------
A Data Connector can have on of the following statuses.

- :code:`ACTIVE`
- :code:`USER_DISABLED`
- :code:`SYSTEM_DISABLED.`

You can read more about what this entails in our `developer documentation <https://developer.disruptive-technologies.com/docs/data-connectors/advanced-configurations#enable-and-disable>`_.
