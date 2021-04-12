# Standard library imports
from datetime import datetime
from typing import Optional

# Project imports.
import disruptive as dt


def log(msg: str, override: Optional[bool] = None) -> None:
    """
    Prints message to stdout if global flag is True.

    Parameters
    ----------
    msg : str
        Message to be printed.

    """

    # Initialize flag.
    should_log = False

    # First set flag from package-wide configuration.
    if dt.log is True:
        should_log = True

    # Override if provided.
    if override is not None:
        should_log = override

    if should_log:
        print('[{}]: {}'.format(
            datetime.now(),
            msg,
        ))
