from typing import Optional, Any
from dataclasses import dataclass

import disruptive
import disruptive.transforms as dttrans
import tests.api_responses as dtapiresponses


class TestOutputs():

    def test_str_dunder(self):
        # Fetch some events.
        history = dtapiresponses.event_history_each_type

        # Iterate events in history.
        for event in history['events']:
            # Construct event object.
            obj = disruptive.events.Event(event)

            # Print the event, calling __str__ dunder.
            str(obj)

    def test_repr_dunder_eval(self):
        # Fetch some events.
        history = dtapiresponses.event_history_each_type

        # Iterate events in history.
        for event in history['events']:
            # Construct event object.
            obj = disruptive.events.Event(event)

            # Print the event, calling __repr__ dunder.
            str(repr(obj))

            # Evaluate the repr aswell.
            eval(repr(obj))

    def test_member_class(self):
        @dataclass
        class TestCase:
            name: str
            give_raw: dict

        tests = [
            TestCase(
                name='success',
                give_raw=dtapiresponses.user_member,
            ),
        ]

        for test in tests:
            member = disruptive.outputs.Member(test.give_raw)

            raw = test.give_raw

            assert member.member_id == raw['name'].split('/')[-1]
            assert member.display_name == raw['displayName']
            assert member.email == raw['email']
            assert member.roles == [r.split('/')[-1] for r in raw['roles']]
            assert member.status == raw['status']
            assert member.email == raw['email']
            assert member.account_type == raw['accountType']
            assert member.create_time == dttrans.to_datetime(raw['createTime'])

    def test_raw_attribute(self, request_mock):
        @dataclass
        class TestCase:
            name: str
            give_method: Any
            give_params: dict
            give_req: dict
            want_err: Optional[Exception]

        tests = [
            TestCase(
                name='data connector raw',
                give_method=disruptive.DataConnector.get_data_connector,
                give_params={
                    'data_connector_id': '-',
                    'project_id': '-',
                },
                give_req=dtapiresponses.simple_data_connector,
                want_err=None,
            ),
            TestCase(
                name='device raw',
                give_method=disruptive.Device.get_device,
                give_params={'device_id': '-'},
                give_req=dtapiresponses.touch_sensor,
                want_err=None,
            ),
            TestCase(
                name='organization raw',
                give_method=disruptive.Organization.get_organization,
                give_params={'organization_id': '-'},
                give_req=dtapiresponses.organization,
                want_err=None,
            ),
            TestCase(
                name='member raw',
                give_method=disruptive.Organization.get_member,
                give_params={
                    'member_id': '-',
                    'organization_id': '-',
                },
                give_req=dtapiresponses.user_member,
                want_err=None,
            ),
            TestCase(
                name='project raw',
                give_method=disruptive.Project.get_project,
                give_params={'project_id': '-'},
                give_req=dtapiresponses.small_project,
                want_err=None,
            ),
            TestCase(
                name='role raw',
                give_method=disruptive.Role.get_role,
                give_params={'role': '-'},
                give_req=dtapiresponses.project_user_role,
                want_err=None,
            ),
            TestCase(
                name='service account raw',
                give_method=disruptive.ServiceAccount.get_service_account,
                give_params={
                    'service_account_id': '-',
                    'project_id': '-',
                },
                give_req=dtapiresponses.service_account1,
                want_err=None,
            ),
            TestCase(
                name='service account key raw',
                give_method=disruptive.ServiceAccount.get_key,
                give_params={
                    'key_id': '-',
                    'service_account_id': '-',
                    'project_id': '-',
                },
                give_req=dtapiresponses.key_without_secret,
                want_err=None,
            ),
        ]

        for test in tests:
            request_mock.json = test.give_req
            res = test.give_method(**test.give_params)
            assert res.raw == test.give_req
