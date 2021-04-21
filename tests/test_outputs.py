# Project imports.
import disruptive
import tests.api_responses as dtapiresponses


class TestOutputs():

    def test_str_dunder(self):
        # Fetch some events.
        history = dtapiresponses.event_history_each_type

        # Iterate events in history.
        for event in history['events']:
            # Construct event object.
            obj = disruptive.events.Event(event)

            # Print the event, calling __str__ dunder.
            print(obj)

    def test_repr_dunder_eval(self):
        # Fetch some events.
        history = dtapiresponses.event_history_each_type

        # Iterate events in history.
        for event in history['events']:
            # Construct event object.
            obj = disruptive.events.Event(event)

            # Print the event, calling __repr__ dunder.
            print(repr(obj))

            # Evaluate the repr aswell.
            eval(repr(obj))
