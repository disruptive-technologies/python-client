# Standard library imports.
import re
import base64
from datetime import datetime

# Project imports.
import disruptive.errors as dterrors


def base64_encode(string: str):
    string_bytes = string.encode('ascii')
    base64_bytes = base64.b64encode(string_bytes)
    base64_string = base64_bytes.decode('ascii')
    return base64_string


def to_iso8601(ts):
    # Verify that we even got a string.
    if isinstance(ts, str):
        # As it is a string, verify iso8601 format.
        if validate_iso8601_format(ts):
            # Nothing to do, return as is.
            return ts
        else:
            # Invalid iso8601 format, raise error.
            raise dterrors.FormatError(
                'Timestamp format {} is invalid iso8601 format.\n'
                'E.g. 2020-01-01T00:00:00Z'.format(
                    ts
                )
            )

    # If not string, datetime is also fine as it can be converted.
    elif isinstance(ts, datetime):
        # Use built-in functions for converting to string.
        dt = ts.isoformat()

        # Add timezone information if lacking.
        if '+' not in dt:
            dt += 'Z'

        return dt

    # If ts is None, return None.
    elif ts is None:
        return None

    # If any other type, raise TypeError.
    else:
        raise TypeError(
            'Got timestamp of type {}, expected'
            ' iso8601 str or datetime.'.format(
                type(ts).__name__
            )
        )


def to_datetime(ts):
    # Check if input is already datetime format.
    if isinstance(ts, datetime):
        # Nothing to do, just return it.
        return ts

    # If input is string, we might be able to convert it.
    elif isinstance(ts, str):
        # First, verify if string is valid iso8601 format.
        if validate_iso8601_format(ts):
            # Use built-in functions for converting to datetime.
            return datetime.fromisoformat(ts.replace('Z', '+00:00'))
        else:
            # Invalid iso8601 format, raise error.
            raise dterrors.FormatError(
                'Timestamp format {} is invalid iso8601 format.\n'
                'E.g. 2020-01-01T00:00:00Z'
            )

    # If ts is None, return None.
    elif ts is None:
        return None

    # If any other type, raise TypeError.
    else:
        raise TypeError(
            'Got timestamp of type {}, expected'
            ' iso8601 str or datetime.'.format(
                type(ts).__name__
            )
        )


def validate_iso8601_format(dt_str):
    # Set up regex for matching iso8601 string.
    # This should probably be changed in the future as it is
    # a little forced. However, the reason for using this approach is
    # that the datetime built-in method for checking iso8601 format
    # allows missing timezone infromation (i.e. Z or +-00:00 suffix).
    # This must be included in our API, and is why this regex exists.
    iso8601_regex = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-' \
        '(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):' \
        '([0-5][0-9])?(.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])$'
    match_iso8601 = re.compile(iso8601_regex).match

    if match_iso8601(dt_str) is not None:
        return True
    else:
        return False
