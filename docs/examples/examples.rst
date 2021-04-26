.. _Examples:

********
Examples
********
The following examples are meant to help you get started using our Python API.

Preliminaries
-------------
A Service Account with sufficient permissions is required to make requests to the API. If you're unfamiliar with this concept, read the `Introduction to Service Accounts <https://developer.disruptive-technologies.com/docs/service-accounts/introduction-to-service-accounts>`_.

Additionally, to prevent hardcoding strings in the code, all examples use environment variables to fetch credentials and IDs. When necessary, these can be set by:

.. code-block:: bash

   export ENV_VARIABLE_NAME=VALUE

Index
-----

.. toctree::
   :maxdepth: 1
   
   get_device
   plot_sensor_data
   threaded_stream
