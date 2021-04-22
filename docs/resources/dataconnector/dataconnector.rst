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

   .. rubric:: Data Connector Type Constants
   .. compound::
      The DataConnector resources class contains one string constant for each configuration type available, including a list of all types.

   .. autoattribute:: disruptive.DataConnector.HTTP_PUSH
   .. autoattribute:: disruptive.DataConnector.DATACONNECTOR_TYPES

Configurations
^^^^^^^^^^^^^^
.. autoclass:: disruptive.DataConnector.HttpPushConfig
   
   .. automethod:: disruptive.DataConnector.HttpPushConfig.__init__

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Extras:

   metrics
