# Third-part imports.
import pytest

# Project imports.
from tests.framework import RequestMock


@pytest.fixture()
def request_mock(mocker):
    return RequestMock(mocker)
