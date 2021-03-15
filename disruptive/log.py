import disruptive


def log(msg: str):
    if disruptive.log is True:
        print('[Disruptive]: {}'.format(msg))
