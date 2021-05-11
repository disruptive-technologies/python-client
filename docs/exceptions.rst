Exceptions
==========
If the API returns a non-200 status code, or something unexpected occurs, and exception is raised.

.. _badrequest:
.. autoexception:: disruptive.errors.BadRequest
.. autoexception:: disruptive.errors.Unauthorized
.. autoexception:: disruptive.errors.Forbidden
.. autoexception:: disruptive.errors.NotFound
.. autoexception:: disruptive.errors.Conflict
.. autoexception:: disruptive.errors.TooManyRequests
.. autoexception:: disruptive.errors.InternalServerError
.. autoexception:: disruptive.errors.ReadTimeout
.. autoexception:: disruptive.errors.ConnectionError
.. autoexception:: disruptive.errors.FormatError
.. autoexception:: disruptive.errors.ConfigurationError
.. autoexception:: disruptive.errors.UnknownError

Errors
------
Unlike exceptions, errors and not raised, but a class object returned to the user with information for them to deal with as they see fit. Errors are only returned by batch-style functions like :ref:`transfer_devices() <transfer_devices>` and :ref:`batch_update_labels() <batch_update_labels>`.

.. autoclass:: disruptive.errors.BatchError
