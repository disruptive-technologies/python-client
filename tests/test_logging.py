# Standard library imports.
from unittest.mock import patch

# Project imports.
import disruptive
import disruptive.logging as dtlog


class TestLogging():

    @patch('disruptive.log', True)
    def test_default_enabled(self):
        # Verify default flag fisabled.
        assert disruptive.log is True

        # Do some logging.
        with patch('builtins.print') as print_mock:
            dtlog.log('This is a message.')

        # Verify print called only once.
        assert print_mock.call_count == 1

    @patch('disruptive.log', False)
    def test_default_disabled(self):
        # Verify default flag fisabled.
        assert disruptive.log is False

        # Do some logging.
        with patch('builtins.print') as print_mock:
            dtlog.log('This is a message.')

        # Verify print never called.
        assert print_mock.call_count == 0

    @patch('disruptive.log', False)
    def test_override_enabled(self):
        # Verify default flag fisabled.
        assert disruptive.log is False

        # Do some logging.
        with patch('builtins.print') as print_mock:
            dtlog.log('This is a message.', override=True)

        # Verify print called once.
        assert print_mock.call_count == 1

    @patch('disruptive.log', True)
    def test_override_disabled(self):
        # Verify default flag enabled.
        assert disruptive.log is True

        # Do some logging.
        with patch('builtins.print') as print_mock:
            dtlog.log('This is a message.', override=False)

        # Verify print never called.
        assert print_mock.call_count == 0
