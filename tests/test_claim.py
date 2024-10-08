from dataclasses import dataclass
from typing import Any

import pytest

import disruptive
import disruptive.errors as dterrors
import tests.api_responses as dtapiresponses


class TestClaim():

    def test_claim(self, request_mock):
        @dataclass
        class TestCase:
            name: str
            give_project_id: str
            give_device_ids: list[str]
            give_kit_ids: list[str]
            give_dry_run: bool
            give_res: dict
            want_device_ids: list[str]
            want_error: Any

        tests = [
            TestCase(
                name='claim devices',
                give_project_id='p1',
                give_device_ids=['a', 'b'],
                give_kit_ids=[],
                give_dry_run=False,
                give_res=dtapiresponses.claimed_devices,
                want_device_ids=['a', 'b'],
                want_error=None,
            ),
            TestCase(
                name='claim kits',
                give_project_id='p1',
                give_device_ids=[],
                give_kit_ids=['k1'],
                give_dry_run=False,
                give_res=dtapiresponses.claimed_devices,
                want_device_ids=['a', 'b'],
                want_error=None,
            ),
            TestCase(
                name='device already claimed',
                give_project_id='p1',
                give_device_ids=['a'],
                give_kit_ids=[],
                give_dry_run=False,
                give_res=dtapiresponses.claimed_device_already_claimed,
                want_device_ids=['a'],
                want_error=dterrors.ClaimErrorDeviceAlreadyClaimed,
            ),
            TestCase(
                name='device not found',
                give_project_id='p1',
                give_device_ids=['a'],
                give_kit_ids=[],
                give_dry_run=False,
                give_res=dtapiresponses.claimed_device_not_found,
                want_device_ids=['a'],
                want_error=dterrors.ClaimErrorDeviceNotFound,
            ),
            TestCase(
                name='kit not found',
                give_project_id='p1',
                give_device_ids=[],
                give_kit_ids=['a'],
                give_dry_run=False,
                give_res=dtapiresponses.claimed_kit_not_found,
                want_device_ids=['a'],
                want_error=dterrors.ClaimErrorKitNotFound,
            ),
        ]

        for test in tests:
            request_mock.json = test.give_res
            devices, errors = disruptive.Claim.claim(
                target_project_id=test.give_project_id,
                kid_ids=test.give_kit_ids,
                device_ids=test.give_device_ids,
                dry_run=test.give_dry_run,
            )

            for i in range(len(devices)):
                assert devices[i].device_id == test.want_device_ids[i], \
                    test.name

                for error in errors:
                    if test.want_error is not None:
                        assert isinstance(error, test.want_error), test.name
                        with pytest.raises(test.want_error):
                            raise error
                    else:
                        assert len(errors) == 0, test.name

    def test_claim_info(self, request_mock):
        @dataclass
        class TestCase:
            name: str
            give_identifier: str
            give_res: dict
            want_err: Any

        tests = [
            TestCase(
                name='test 1',
                give_identifier='id1',
                give_res=dtapiresponses.claim_info_kit,
                want_err=None,
            ),
            TestCase(
                name='identifier type conflict',
                give_identifier=99,
                give_res={},
                want_err=TypeError,
            ),
        ]

        for test in tests:
            request_mock.json = test.give_res

            if test.want_err is None:
                claim = disruptive.Claim.claim_info(test.give_identifier)
                assert isinstance(claim, disruptive.Claim), test.name
            else:
                with pytest.raises(test.want_err):
                    disruptive.Claim.claim_info(test.give_identifier)

    def test_claim_errors(self):
        @dataclass
        class TestCase:
            name: str
            give_res: dict
            want_err: Any

        tests = [
            TestCase(
                name='unknown code ClaimError',
                give_res={
                    'devices': [{'code': 'UNKNOWN_CODE'}],
                    'kits': [{'code': 'UNKNOWN_CODE'}],
                },
                want_err=dterrors.ClaimError,
            ),
            TestCase(
                name='device already claimed',
                give_res={
                    'devices': [
                        dtapiresponses.claim_error_device_already_claimed,
                    ],
                    'kits': [],
                },
                want_err=dterrors.ClaimErrorDeviceAlreadyClaimed,
            ),
            TestCase(
                name='device not found',
                give_res={
                    'devices': [
                        dtapiresponses.claim_error_device_not_found,
                    ],
                    'kits': [],
                },
                want_err=dterrors.ClaimErrorDeviceNotFound,
            ),
            TestCase(
                name='kit not found',
                give_res={
                    'devices': [],
                    'kits': [
                        dtapiresponses.claim_error_kit_not_found,
                    ],
                },
                want_err=dterrors.ClaimErrorKitNotFound,
            ),
        ]

        for test in tests:
            errors = disruptive.Claim._parse_claim_errors(test.give_res)
            for error in errors:
                assert isinstance(error, dterrors.ClaimError), test.name
                assert isinstance(error, test.want_err), test.name
                with pytest.raises(test.want_err):
                    raise error
