.. _http_push_config:

HttpPushConfig
==============
Configuration class for the :code:`HTTP_PUSH` :ref:`Data Connector type <data_connector_types>`.

Usage
-----

.. code-block:: python

   import disruptive as dt

   # Create an HTTP_PUSH Data Connector.
   dt.DataConnector.create_data_connector(
       project_id='<PROJECT_ID>',
       display_name='new-data-connector',
       config=dt.DataConnector.HttpPushConfig(
           url='https://some-endpoint-url.com',
           signature_secret='good-secret',
           headers={
              'name1': 'value1',
              'name2': 'value2',
           },
       ),
   )

Class
-----
.. autoclass:: disruptive.DataConnector.HttpPushConfig
   
   .. automethod:: disruptive.DataConnector.HttpPushConfig.__init__
