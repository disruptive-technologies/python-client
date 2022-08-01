from datetime import datetime, timezone, timedelta
from dataclasses import dataclass

import pytest

import disruptive.transforms as dttrans
import disruptive.errors as dterrors


class TestTransforms():

    def test_base64_encode(self):
        outp = 'ZXhhbXBsZV9zdHJpbmc='
        assert dttrans.base64_encode('example_string') == outp

    def test_to_iso8601_invalid_type(self):
        inp = {'timestamp': '1970-01-01T00:00:00Z'}
        with pytest.raises(TypeError):
            dttrans.to_iso8601(inp)

    def test_to_iso8601_none(self):
        inp = None
        outp = None
        assert dttrans.to_iso8601(inp) == outp

    def test_to_iso8601_string_utc(self):
        inp = '1970-01-01T00:00:00Z'
        outp = '1970-01-01T00:00:00Z'
        assert dttrans.to_iso8601(inp) == outp

    def test_to_iso8601_string_tz_offset(self):
        inp = '1970-01-01T00:00:00+02:00'
        outp = '1970-01-01T00:00:00+02:00'
        assert dttrans.to_iso8601(inp) == outp

    def test_to_iso8601_string_invalid_tz(self):
        inp = '1970-01-01T00:00:00+02:00Z'
        with pytest.raises(dterrors.FormatError):
            dttrans.to_iso8601(inp)

    def test_to_iso8601_datetime_with_tz_utc(self):
        inp = datetime(1970, 1, 1, tzinfo=timezone(timedelta(hours=0)))
        # A timezone of 00:00 should return 'Z' instead.
        outp = '1970-01-01T00:00:00Z'
        assert dttrans.to_iso8601(inp) == outp

    def test_to_iso8601_datetime_with_tz_offset(self):
        inp = datetime(1970, 1, 1, tzinfo=timezone(timedelta(hours=2)))
        outp = '1970-01-01T00:00:00+02:00'
        assert dttrans.to_iso8601(inp) == outp

    def test_to_iso8601_datetime_without_tz(self):
        inp = datetime(1970, 1, 1)
        outp = '1970-01-01T00:00:00Z'
        assert dttrans.to_iso8601(inp) == outp

    def test_to_datetime_invalid_type(self):
        inp = {'timestamp': datetime(1970, 1, 1)}
        with pytest.raises(TypeError):
            dttrans.to_datetime(inp)

    def test_to_datetime_none(self):
        inp = None
        outp = None
        assert dttrans.to_datetime(inp) == outp

    def test_to_datetime_missing_tz(self):
        inp = '1970-01-01T00:00:00'
        with pytest.raises(dterrors.FormatError):
            dttrans.to_datetime(inp)

    def test_to_datetime_tz_utc(self):
        inp = '1970-01-01T00:00:00Z'
        outp = datetime(1970, 1, 1, tzinfo=timezone(timedelta(hours=0)))
        assert dttrans.to_datetime(inp) == outp

    def test_to_datetime_tz_offset(self):
        inp = '1970-01-01T00:00:00+02:00'
        outp = datetime(1970, 1, 1, tzinfo=timezone(timedelta(hours=2)))
        assert dttrans.to_datetime(inp) == outp

    def test_to_datetime_already_datetime(self):
        inp = datetime(1970, 1, 1, tzinfo=timezone(timedelta(hours=2)))
        outp = datetime(1970, 1, 1, tzinfo=timezone(timedelta(hours=2)))
        assert dttrans.to_datetime(inp) == outp

    def test_validate_iso8601_format_valid(self):
        inp1 = '1970-01-01T00:00:00Z'
        assert dttrans.validate_iso8601_format(inp1) is True

        inp2 = '1970-01-01T00:00:00+00:00'
        assert dttrans.validate_iso8601_format(inp2) is True

    def test_validate_iso8601_format_missing_tz(self):
        inp = '1970-01-01T00:00:00'
        assert dttrans.validate_iso8601_format(inp) is False

    def test_validate_iso8601_format_date_only(self):
        inp = '1970-01-01'
        assert dttrans.validate_iso8601_format(inp) is False

    def test_camel_to_snake_case(self):
        @dataclass
        class TestCase:
            name: str
            give_str: str
            want_str: str

        tests = [
            TestCase(
                name='single case',
                give_str='camelCase',
                want_str='camel_case',
            ),
            TestCase(
                name='multiple cases',
                give_str='camelCaseDoesntBelongInPython',
                want_str='camel_case_doesnt_belong_in_python',
            ),
            TestCase(
                name='keep dots',
                give_str='name.camelCase',
                want_str='name.camel_case',
            ),
            TestCase(
                name='keep spaces',
                give_str='name and camelCase',
                want_str='name and camel_case',
            ),
        ]

        for test in tests:
            snake_case = dttrans.camel_to_snake_case(test.give_str)
            assert snake_case == test.want_str, test.name
