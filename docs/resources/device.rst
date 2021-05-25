Device
======
The Device resource can be used to interact with `Sensors and Cloud Connectors <https://developer.disruptive-technologies.com/docs/devices>`_, together referred to as devices. Various tasks can be performed by using the API Methods included in the class.

- :ref:`get_device() <get_device>`
- :ref:`list_devices() <list_devices>`
- :ref:`transfer_devices() <transfer_devices>`
- :ref:`set_label() <set_label>`
- :ref:`remove_label() <remove_label>`
- :ref:`batch_update_labels() <batch_update_labels>`

Each device fetched by an API Method is represented by an instance of the :ref:`Device <device>` class that is returned to the user.


API Methods
-----------
.. _get_device:
.. autofunction:: disruptive.Device.get_device
.. _list_devices:
.. autofunction:: disruptive.Device.list_devices
.. _transfer_devices:
.. autofunction:: disruptive.Device.transfer_devices
.. _set_label:
.. autofunction:: disruptive.Device.set_label
.. _remove_label:
.. autofunction:: disruptive.Device.remove_label
.. _batch_update_labels:
.. autofunction:: disruptive.Device.batch_update_labels

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Extras:

   device/reported

.. _device:

Class
-----
.. autoclass:: disruptive.Device

.. _device_type_constants:

Type Constants
--------------
The Device class contains a string constant for each available device type.

.. autoattribute:: disruptive.Device.TEMPERATURE
.. autoattribute:: disruptive.Device.PROXIMITY
.. autoattribute:: disruptive.Device.TOUCH
.. autoattribute:: disruptive.Device.HUMIDITY
.. autoattribute:: disruptive.Device.PROXIMITY_COUNTER
.. autoattribute:: disruptive.Device.TOUCH_COUNTER
.. autoattribute:: disruptive.Device.WATER_DETECTOR
.. autoattribute:: disruptive.Device.CLOUD_CONNECTOR
.. autoattribute:: disruptive.Device.DEVICE_TYPES

This can be a useful alternative to writing the strings directly.

.. code-block:: python

   # List all temperature- and touch sensors in a project.
   devices = dt.Device.list_devices(
       project_id='<PROJECT_ID>',
       device_types=[
           dt.Device.TEMPERATURE,
           dt.Device.TOUCH,
           dt.Device.WATER_DETECTOR,
       ],
   )
