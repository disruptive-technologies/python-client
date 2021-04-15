DataConnector
-------------
The DataConnector class can, among other things, be used to create, modified, and delete Data Connectors.

API Methods
^^^^^^^^^^^
.. autofunction:: disruptive.DataConnector.get_dataconnector
.. autofunction:: disruptive.DataConnector.list_dataconnectors
.. autofunction:: disruptive.DataConnector.create_dataconnector
.. autofunction:: disruptive.DataConnector.update_dataconnector
.. autofunction:: disruptive.DataConnector.delete_dataconnector
.. autofunction:: disruptive.DataConnector.sync_dataconnector
.. autofunction:: disruptive.DataConnector.get_metrics

Class
^^^^^
.. autoclass:: disruptive.DataConnector

Type-Specific Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: disruptive.dataconnector_configs.HttpPush
   
   .. automethod:: disruptive.dataconnector_configs.HttpPush.__init__

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Extras:

   metrics
