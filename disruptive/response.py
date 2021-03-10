

class DTResponse():

    def __init__(self, data, status_code, headers):
        self.data = data
        self.status_code = status_code
        self.headers = headers
