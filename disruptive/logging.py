from __future__ import annotations

import logging
from datetime import datetime

import disruptive
import disruptive.errors as dterrors

DEBUG = 'DEBUG'
INFO = 'INFO'
WARNING = 'WARNING'
ERROR = 'ERROR'
CRITICAL = 'CRITICAL'
LOG_LEVELS = [DEBUG, INFO, WARNING, ERROR, CRITICAL]

# Fetch the disruptive logger, but with disabled output.
logger = logging.getLogger('disruptive')
logger.setLevel(99)


def debug(msg: str | dict) -> None:
    if _log_flag_exceeds(DEBUG):
        _fmt_log(msg, DEBUG)
    logger.debug(msg)


def info(msg: str | dict) -> None:
    if _log_flag_exceeds(INFO):
        _fmt_log(msg, INFO)
    logger.info(msg)


def warning(msg: str | dict) -> None:
    if _log_flag_exceeds(WARNING):
        _fmt_log(msg, WARNING)
    logger.warning(msg)


def error(msg: str | dict) -> None:
    if _log_flag_exceeds(ERROR):
        _fmt_log(msg, ERROR)
    logger.error(msg)


def critical(msg: str | dict) -> None:
    if _log_flag_exceeds(CRITICAL):
        _fmt_log(msg, CRITICAL)
    logger.critical(msg)


def _log_flag_exceeds(level: str) -> bool:
    # If not string, never True.
    if not isinstance(disruptive.log_level, str):
        return False

    set_level = disruptive.log_level.upper()

    # Verify set value is valid.
    if set_level not in LOG_LEVELS:
        # As an invalid log_level has been provided, reset it
        # to default before raising the exception.
        disruptive.log_level = INFO

        msg = f'Invalid log_level {set_level}.\n' \
              f'Must be either of {LOG_LEVELS}.'
        raise dterrors.ConfigurationError(msg)

    # Check if level is exceeded.
    if LOG_LEVELS.index(level) >= LOG_LEVELS.index(set_level):
        return True
    else:
        return False


def _fmt_log(msg: str | dict, level: str) -> None:
    print(f'[{datetime.now().isoformat()}] {level:<8} - {msg}')
