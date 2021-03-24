import disruptive as dt


def log(msg: str) -> None:
    """
    Prints message to stdout if global flag is True.

    Parameters
    ----------
    msg : str
        Message to be printed.

    """

    if dt.log is True:
        print('[Disruptive]: {}'.format(msg))
