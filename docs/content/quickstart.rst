.. _quickstart:

**********
Quickstart
**********

Installation
============
To install the package using pip, run:

.. code-block:: bash

   pip install --upgrade disruptive

Python 3.7+ is currently supported.

Authentication
==============
Most of the provided functionality requires authentication to the API. Using Service Account credentials, the entire package can be authenticated at once.

.. code-block:: python

   # Import the disruptive package.
   import disruptive as dt

   # Authenticate all API methods in package at once.
   dt.default_auth = dt.Auth.serviceaccount(key_id, secret, email)

See the :ref:`Authentication` section for more details.

Usage
=====
Assuming you've already authenticated, here is a few example of how to call various methods.

.. code-block:: python

   # Fetch devices from endpoint.
   devices = dt.Device.list_devices(project_id)

See the :ref:`Examples` section for more in-depth usage.
