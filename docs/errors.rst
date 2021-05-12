Errors
======
The Python API is designed to raise exceptions for any problems that occur during usage, where the exceptions are grouped by four major categories depending on the cause.

- :ref:`ServerError <server_error_group>`
- :ref:`UsageError <usage_error_group>`
- :ref:`ConnectionError <connection_error_group>`
- :ref:`BatchError <batch_error_group>`

Users are encouraged to handle exceptions as they see fit, but the major groups should at least be considered. They can be accessed as shown in the following snippet.

.. code-block:: python

   try:
       dt.Project.list_members('<PROJECT_ID>')
   except dt.errors.ServerError as e:
       server_error_handler(e)
   except dt.errors.UsageError as e:
       usage_error_handler(e)
   except dt.errors.ConnectionError as e:
       connection_error_handler(e)
   except dt.errors.UnknownError as e:
       generic_error_handler(e)

.. _server_error_group:

ServerError
-----------
Covers API responses with a status code in the 500 range.

.. _internal_server_error:
.. autoexception:: disruptive.errors.InternalServerError

.. _usage_error_group:

UsageError
----------
Covers API responses with a status code in the 400 range in addition to problems caused by invalid parameter inputs.

.. _bad_request_error:
.. autoexception:: disruptive.errors.BadRequest
.. _unauthorized_error:
.. autoexception:: disruptive.errors.Unauthorized
.. _forbidden_error:
.. autoexception:: disruptive.errors.Forbidden
.. _not_found_error:
.. autoexception:: disruptive.errors.NotFound
.. _conflict_error:
.. autoexception:: disruptive.errors.Conflict
.. _too_many_requests_error:
.. autoexception:: disruptive.errors.TooManyRequests
.. _format_error:
.. autoexception:: disruptive.errors.FormatError
.. _configuration_error:
.. autoexception:: disruptive.errors.ConfigurationError

.. _connection_error_group:

ConnectionError
---------------
Covers errors caused by unsuccessful connections from the client.

.. _connection_error:
.. autoexception:: disruptive.errors.ConnectionError
.. _read_timeout_error:
.. autoexception:: disruptive.errors.ReadTimeout

.. _batch_error_group:

BatchError
----------
Unlike the other exceptions, a BatchError is not raised, but returned to the user as a class object with information for them to deal with as they see fit. They are used in batch-style functions like :ref:`transfer_devices() <transfer_devices>` and :ref:`batch_update_labels() <batch_update_labels>` that may fail one- or several action in an otherwise successful request.

.. _transfer_device_error:
.. autoclass:: disruptive.errors.TransferDeviceError
.. _label_update_error:
.. autoclass:: disruptive.errors.LabelUpdateError

.. _unknown_error_group:

UnknownError
------------
.. _unknown_error:
.. autoexception:: disruptive.errors.UnknownError
