from __future__ import annotations

import logging
from datetime import datetime

import disruptive
import disruptive.errors as dterrors

# Fetch the disruptive logger, but with disabled output.
logger = logging.getLogger('disruptive')
logger.setLevel(99)

levels = {'debug': 1, 'info': 2, 'warning': 3, 'error': 4, 'critical': 5}


def debug(msg: str | dict) -> None:
    if _log_flag_exceeds('debug'):
        _fmt_log(msg, 'DEBUG')
    logger.debug(msg)


def info(msg: str | dict) -> None:
    if _log_flag_exceeds('info'):
        _fmt_log(msg, 'INFO')
    logger.info(msg)


def warning(msg: str | dict) -> None:
    if _log_flag_exceeds('warning'):
        _fmt_log(msg, 'WARNING')
    logger.warning(msg)


def error(msg: str | dict) -> None:
    if _log_flag_exceeds('error'):
        _fmt_log(msg, 'ERROR')
    logger.error(msg)


def critical(msg: str | dict) -> None:
    if _log_flag_exceeds('critical'):
        _fmt_log(msg, 'CRITICAL')
    logger.critical(msg)


def _log_flag_exceeds(level: str | dict) -> bool:
    # If None, never True.
    if disruptive.log_level is None:
        return False

    # Verify set value is valid.
    if disruptive.log_level not in levels:
        raise dterrors.ConfigurationError(
            'Invalid logging level {}. '
            'Must be either None, "debug", "info", '
            '"warning", "error", or "critical".'.format(disruptive.log_level)
        )

    # Check if level is exceeded.
    if levels[level] >= levels[disruptive.log_level]:
        return True
    else:
        return False


def _fmt_log(msg: str | dict, level: str | dict) -> None:
    print('[{}] {:<8} - {}'.format(
        datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
        level,
        msg,
    ))
