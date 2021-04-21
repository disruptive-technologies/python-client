Threaded Stream
===============
This examples shows how one can use the built-in `threading` package to stream events in a separate thread where a buffer list is appended as new events arrive independently of the main loop.

Full Example
------------

.. code-block:: python 

   # Standard library imports.
   import os
   import time
   import threading
   
   # Import disruptive package.
   import disruptive as dt
   
   # Fetch credentials and IDs from environment variables.
   key_id = os.environ.get('DT_SERVICE_ACCOUNT_KEY_ID', '')
   secret = os.environ.get('DT_SERVICE_ACCOUNT_SECRET', '')
   email = os.environ.get('DT_SERVICE_ACCOUNT_EMAIL', '')
   project_id = os.environ.get('DT_PROJECT_ID', '')
   
   # Authenticate the package using serviceaccount credentials.
   dt.default_auth = dt.Auth.serviceaccount(key_id, secret, email)
   
   
   # Function which will be the target for our thread.
   def stream_worker(project_id):
       # Create stream generator
       for new_event in dt.Stream.project(project_id):
           # When a new event arrives, lock buffer before writing.
           print('[Thread] New Event')
           with buffer_lock:
               print('\t- locked')
               # Append new event to our buffer.
               event_buffer.append(new_event)
           print('\t- unlocked')
   
   
   # Initialize the stream buffer list where we will store events.
   event_buffer = []
   
   # Use locking to avoid corrupting data by writing simultaneously.
   buffer_lock = threading.Lock()
   
   # Start the stream worker in a separate thread.
   t = threading.Thread(
       target=stream_worker,
       args=(project_id,),
   )
   t.start()
   
   # Do something else while stream is running in the background.
   # Here we print and trim the buffer length every 5 second.
   while True:
       # Print length of the buffer.
       n_events = len(event_buffer)
       print('[Main] Length: {}/15. Popping {} events.'.format(
           n_events,
           -1*(min(0, 15-n_events)),
       ))
   
       # Pop older events until buffer is no longer than 15.
       while len(event_buffer) > 15:
           print('\t- pop')
           event_buffer.pop(0)
   
       # Patiently wait for 5 seconds.
       time.sleep(5)

Step-By-Step
------------

Environment variables are used for both credentials and the project ID. Therefore, in addition to importing the disruptive package, we also import os. Additionally, `threading` is required to spawn new threads, whereas `time` provides the :code:`sleep` function.

.. code-block:: python 

   # Standard library imports.
   import os
   import time
   import threading
   
   # Import disruptive package.
   import disruptive as dt

Using Service Account credentials, all endpoints in the package can be authenticated at once by updating the :code:`dt.default_auth` variable with an Auth object.

.. code-block:: python

   # Authenticate the package using serviceaccount credentials.
   dt.default_auth = dt.Auth.serviceaccount(key_id, secret, email)

When using the `threading` package, the target code to be ran in the newly spawned thread must be wrapped in a function, here called :code:`stream_worker`. It's job is to start the stream generator, then append new events to buffer as they arrive.

.. code-block:: python

   # Function which will be the target for our thread.
   def stream_worker(project_id):
       # Create stream generator
       for new_event in dt.Stream.project(project_id):
           # When a new event arrives, lock buffer before writing.
           print('[Thread] New Event')
           with buffer_lock:
               print('\t- locked')
               # Append new event to our buffer.
               event_buffer.append(new_event)
           print('\t- unlocked')

Before the thread is spawned using the target :code:`stream_worker`, a locking object is created. This can be called inside the thread when writing or reading a variable to make sure that other jobs that want to use it, like our main code, has to wait until we finish.

.. code-block:: python

   # Use locking to avoid corrupting data by writing simultaneously.
   buffer_lock = threading.Lock()
   
   # Start the stream worker in a separate thread.
   t = threading.Thread(
       target=stream_worker,
       args=(project_id,),
   )
   t.start()

The rest is simply an infinite :code:`while` loop that trims the buffer to a certain length every 5 seconds. This is where your main code would go.

.. code-block:: python

   # Do something else while stream is running in the background.
   # Here we print and trim the buffer length every 5 second.
   while True:
       # Print length of the buffer.
       n_events = len(event_buffer)
       print('[Main] Length: {}/15. Popping {} events.'.format(
           n_events,
           -1*(min(0, 15-n_events)),
       ))
   
       # Pop older events until buffer is no longer than 15.
       while len(event_buffer) > 15:
           print('\t- pop')
           event_buffer.pop(0)
   
       # Patiently wait for 5 seconds.
       time.sleep(5)
