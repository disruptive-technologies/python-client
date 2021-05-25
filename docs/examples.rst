.. _Examples:

********
Examples
********
The following examples are meant to help you get started using our Python API.

Environment Variables
---------------------
If you do not wish to edit the example code, certain environment variables must be set.

All examples authenticate using :ref:`Service Account credentials <service_account_auth>`. Therefore, the following environment variables are expected throughout.

.. code-block:: bash

   export DT_SERVICE_ACCOUNT_KEY_ID="<YOUR_CREDENTIAL_KEY_ID>"
   export DT_SERVICE_ACCOUNT_SECRET="<YOUR_CREDENTIAL_KEY_ID>"
   export DT_SERVICE_ACCOUNT_EMAIL="<YOUR_CREDENTIAL_KEY_ID>"

Depending on the example, additional environment variables like :code:`DEVICE_ID` and :code:`PROJECT_ID` may be required. These are listed early in the code for visibility.

List of Examples
----------------

- :ref:`Get Device <get_device_example>`
- :ref:`Plot Sensor Data <plot_sensor_data_example>`
- :ref:`Threaded Stream <threaded_stream_example>`

.. toctree::
   :maxdepth: 1
   :hidden:
   
   examples/get_device
   examples/fetch_event_history
   examples/plot_sensor_data
   examples/threaded_stream
