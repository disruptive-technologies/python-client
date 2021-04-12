# This exampel shows how one can use the built-in multiprocessing
# package to initialize a stream in a separate thread where it
# can sit and listen for events while we do other things in the code.
# This is useful as we often don't want to have the main parts of our
# program inside the stream generator.

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


# Function that starts the stream generator we put in a separate thread.
def stream_worker(project_id):
    # Create stream generator
    for new_event in dt.Stream.project(project_id):
        # When a new event arrives, lock the event_buffer before writing.
        print('[Thread] New Event')
        with buffer_lock:
            print('\t- locked')
            # Append new event to our buffer.
            event_buffer.append(new_event)
        print('\t- unlocked')


# Initialize the stream buffer list where we will store events.
event_buffer = []

# Implement locking to avoid corrupting data by writing simultaneously.
buffer_lock = threading.Lock()

# Start the stream worker in a separate thread.
t = threading.Thread(
    target=stream_worker,
    args=(project_id,),
)
t.start()

# Do something else while stream is running in the background, here mocked as
# an infinite while loop that prints and trims the buffer every 5 second.
while True:
    # Print length of the buffer.
    n_events = len(event_buffer)
    print('[Main] Buffer length: {}/15. Popping {} oldest events.'.format(
        n_events,
        -1*(min(0, 15-n_events)),
    ))

    # If there are more than 15 events in the buffer, drop the oldest ones.
    while len(event_buffer) > 15:
        print('\t- pop')
        event_buffer.pop(0)

    # Patiently wait for 5 seconds.
    time.sleep(5)
