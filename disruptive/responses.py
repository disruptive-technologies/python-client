

class DTResponse():
    """
    Represents the REST API responses.

    Attributes
    ----------
    data : dict
        Raw response data dictionary.
    status_code : int
        Response status code.
    headers : dict
        Headers in the response.

    """

    def __init__(self, data: dict, status_code: int, headers: dict) -> None:
        self.data = data
        self.status_code = status_code
        self.headers = headers
