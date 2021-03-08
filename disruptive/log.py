import disruptive

def log(msg: str):
    if disruptive.log == True:
        print('[Disruptive]: {}'.format(msg))
