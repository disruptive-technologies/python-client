Device
======
The Device resource can be used to interact with `Sensors and Cloud Connectors <https://developer.disruptive-technologies.com/docs/devices>`_, together referred to as devices. Various actions can be performed by using the included API Methods.

- :ref:`get_device() <get_device>`
- :ref:`list_device() <list_devices>`
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

   reported

Class
-----
.. _device:
.. autoclass:: disruptive.Device

   .. rubric:: Device Type Constants
   .. compound::
      The Device resources class contains one string constant for each device type available, including a list of all types.

   .. code-block:: python

      # List all temperature- and touch sensors in a project.
      devices = dt.Device.list_devices(
          project_id,
          device_types=[
              dt.Device.TEMPERATURE,
              dt.Device.TOUCH,
          ],
      )

   .. autoattribute:: disruptive.Device.TEMPERATURE
   .. autoattribute:: disruptive.Device.PROXIMITY
   .. autoattribute:: disruptive.Device.TOUCH
   .. autoattribute:: disruptive.Device.HUMIDITY
   .. autoattribute:: disruptive.Device.PROXIMITY_COUNTER
   .. autoattribute:: disruptive.Device.TOUCH_COUNTER
   .. autoattribute:: disruptive.Device.WATER_DETECTOR
   .. autoattribute:: disruptive.Device.DEVICE_TYPES
