import base64
import datetime


def base64_encode(string: str):
    string_bytes = string.encode('ascii')
    base64_bytes = base64.b64encode(string_bytes)
    base64_string = base64_bytes.decode('ascii')
    return base64_string


def iso8601_to_datetime(ts: str):
    # Remove trailing Z as it is not expected by datetime
    return datetime.datetime.fromisoformat(ts[:-1])
