.. _eventhistory:

EventHistory
------------
The EventHistory resource can be used fetch historic event data for a device. This can be achieved by using the API Method included in the class.

- :ref:`list_events() <list_events>`

All the fetched historic events are returned to the user as an instance of the :ref:`EventHistory <eventhistory_class>` class.

API Methods
^^^^^^^^^^^
.. _list_events:
.. autofunction:: disruptive.EventHistory.list_events

.. _eventhistory_class:

Class
^^^^^
.. autoclass:: disruptive.EventHistory

   .. automethod:: disruptive.EventHistory.get_events
   .. automethod:: disruptive.EventHistory.get_data_axes
