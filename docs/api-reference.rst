*************
API-Reference
*************

The examples provided with methods in the following modules assume that the disruptive package has been imported and authenticated globally.

.. code-block:: python

   # Import disruptive package.
   import disruptive as dt

   # Authenticate globally using either OAuth (recommended) ...
   dt.auth = dt.OAuth(key_id, secret, email)

   # ... or BasicAuth
   dt.auth = dt.BasicAuth(key_id, secret)

Resources
=========

Device
------
..
.. automodule:: disruptive.resources.device
   :members:
.. autoclass:: disruptive.Device
   :members:

EventHistory
------------
.. automodule:: disruptive.resources.event_history
   :members:

Project
-------
.. automodule:: disruptive.resources.project
   :members:

Organization
------------
.. automodule:: disruptive.resources.organization
   :members:

DataConnector
--------------
.. automodule:: disruptive.resources.dataconnector
   :members:

Role
----
.. automodule:: disruptive.resources.role
   :members:

ServiceAccount
--------------
.. automodule:: disruptive.resources.serviceaccount
   :members:

Stream
------
.. automodule:: disruptive.resources.stream
   :members:


Authentication
==============

BasicAuth
----------
.. autoclass:: disruptive.authentication.BasicAuth
.. autofunction:: disruptive.authentication.BasicAuth.__init__

OAuth
-----
.. autoclass:: disruptive.authentication.OAuth
.. autofunction:: disruptive.authentication.OAuth.__init__
