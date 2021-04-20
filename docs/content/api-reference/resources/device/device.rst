Device
======
The Device class can be used to fetch and manipulate your devices, from listing the ones in a project to setting labels.

API Methods
-----------
.. autofunction:: disruptive.Device.get_device
.. autofunction:: disruptive.Device.list_devices
.. autofunction:: disruptive.Device.batch_update_labels
.. autofunction:: disruptive.Device.set_label
.. autofunction:: disruptive.Device.remove_label
.. autofunction:: disruptive.Device.transfer_devices

Class
-----
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

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Extras:

   reported
