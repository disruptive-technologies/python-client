import pytest
from unittest.mock import patch

import disruptive
import disruptive.logging as dtlog
import disruptive.errors as dterrors


class TestLogging():

    def _check_level_called(self, msg, debug=True, info=True,
                            warning=True, error=True, critical=True):

        with patch('disruptive.logging._fmt_log') as log_mock:
            dtlog.debug(msg)
            if debug:
                log_mock.assert_called_with(msg, 'DEBUG')
            else:
                assert log_mock.call_count == 0

        with patch('disruptive.logging._fmt_log') as log_mock:
            dtlog.info(msg)
            if info:
                log_mock.assert_called_with(msg, 'INFO')
            else:
                assert log_mock.call_count == 0

        with patch('disruptive.logging._fmt_log') as log_mock:
            dtlog.warning(msg)
            if warning:
                log_mock.assert_called_with(msg, 'WARNING')
            else:
                assert log_mock.call_count == 0

        with patch('disruptive.logging._fmt_log') as log_mock:
            dtlog.error(msg)
            if error:
                log_mock.assert_called_with(msg, 'ERROR')
            else:
                assert log_mock.call_count == 0

        with patch('disruptive.logging._fmt_log') as log_mock:
            dtlog.critical(msg)
            if critical:
                log_mock.assert_called_with(msg, 'CRITICAL')
            else:
                assert log_mock.call_count == 0

    def test_flag_debug(self):
        disruptive.log_level = 'debug'
        self._check_level_called('Test message.')
        disruptive.log_level = None

    def test_flag_info(self):
        disruptive.log_level = 'info'
        self._check_level_called('Test message.', debug=False)
        disruptive.log_level = None

    def test_flag_warning(self):
        disruptive.log_level = 'warning'
        self._check_level_called(
            msg='Test message.',
            debug=False,
            info=False,
        )
        disruptive.log_level = None

    def test_flag_error(self):
        disruptive.log_level = 'error'
        self._check_level_called(
            msg='Test message.',
            debug=False,
            info=False,
            warning=False,
        )
        disruptive.log_level = None

    def test_flag_critical(self):
        disruptive.log_level = 'critical'
        self._check_level_called(
            msg='Test message.',
            debug=False,
            info=False,
            warning=False,
            error=False,
        )
        disruptive.log_level = None

    def test_case_insensitive(self):
        disruptive.log_level = "CRITICAL"
        self._check_level_called(
            msg='Test message.',
            debug=False,
            info=False,
            warning=False,
            error=False,
        )
        disruptive.log_level = None

    def test_invalid_level_reset(self):
        disruptive.log_level = "SOME_INVALID_STRING"
        with pytest.raises(dterrors.ConfigurationError):
            self._check_level_called(
                msg='Test message.',
                debug=False,
                info=False,
                warning=False,
                error=False,
                critical=False,
            )

            # Log level should be reset to default.
            assert disruptive.log_level == 'info'

        disruptive.log_level = None
