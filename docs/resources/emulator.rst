Emulator
========
The Emulator resource can be used to interact with `emulated devices <https://developer.disruptive-technologies.com/docs/sensor-emulator>`_. Various tasks can be performed by using the API Methods included in the class.

- :ref:`create_device() <create_device>`
- :ref:`delete_device() <delete_device>`
- :ref:`publish_event() <publish_event>`

Each device fetched by an API Method is represented by an instance of the :ref:`Device <device>` class that is returned to the user.

API Methods
-----------
.. _create_device:
.. autofunction:: disruptive.Emulator.create_device
.. _delete_device:
.. autofunction:: disruptive.Emulator.delete_device
.. _publish_event:
.. autofunction:: disruptive.Emulator.publish_event
