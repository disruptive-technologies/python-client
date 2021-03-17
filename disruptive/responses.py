

class DTResponse():

    def __init__(self, data: dict, status_code: int, headers: dict) -> None:
        self.data = data
        self.status_code = status_code
        self.headers = headers
