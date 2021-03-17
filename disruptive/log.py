import disruptive as dt


def log(msg: str) -> None:
    if dt.log is True:
        print('[Disruptive]: {}'.format(msg))
