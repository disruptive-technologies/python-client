auth_token_fresh = {
    'expires_in': 3600,
    'access_token': ''
}

auth_token_expired = {
    'expires_in': 0,
    'access_token': ''
}

ccon = {
    "name": "projects/c0md8mm0c7bet3vic78g/devices/emuc909fk1qdqebrvv2jqv0",
    "type": "ccon",
    "productNumber": "100011",
    "labels": {
        "name": "ccon",
        "virtual-sensor": ""
    },
    "reported": {
        "connectionStatus": {
            "connection": "CELLULAR",
            "available": [
                "ETHERNET",
                "CELLULAR"
            ],
            "updateTime": "2021-03-13T16:05:21.692975Z"
        },
        "connectionLatency": None,
        "ethernetStatus": {
            "macAddress": "",
            "ipAddress": "",
            "errors": [],
            "updateTime": "2021-03-13T16:05:25.552018Z"
        },
        "cellularStatus": {
            "signalStrength": 100,
            "errors": [],
            "updateTime": "2021-03-13T16:05:23.230101Z"
        },
        "touch": {
            "updateTime": "2021-03-13T16:05:27.591228Z"
        }
    }
}

humidity_sensor = {
    "name": "projects/c0md38m0c7bet4vico8g/devices/emuc109fhppdqebrvv2jqug",
    "type": "humidity",
    "productNumber": "101895",
    "labels": {
        "name": "humidity",
        "new-label": "99",
        "virtual-sensor": ""
    },
    "reported": {
        "networkStatus": {
            "signalStrength": 99,
            "rssi": 0,
            "updateTime": "2021-03-13T16:05:35.392072Z",
            "cloudConnectors": [
                {
                    "id": "emulated-ccon",
                    "signalStrength": 99,
                    "rssi": 0
                }
            ],
            "transmissionMode": "LOW_POWER_STANDARD_MODE"
        },
        "batteryStatus": {
            "percentage": 100,
            "updateTime": "2021-03-13T16:05:31.745319Z"
        },
        "humidity": {
            "temperature": 0,
            "relativeHumidity": 0,
            "updateTime": "2021-03-13T16:05:30.185800Z"
        },
        "touch": {
            "updateTime": "2021-03-13T16:05:35.380533Z"
        }
    }
}

proximity_sensor = {
    "name": "projects/c0md3mm0c7pet3vico8g/devices/emuc0pc36pqdqebrvv29r8g",
    "type": "proximity",
    "productNumber": "102064",
    "labels": {
        "name": "proximity",
        "virtual-sensor": ""
    },
    "reported": {
        "networkStatus": {
            "signalStrength": 99,
            "rssi": 0,
            "updateTime": "2021-03-13T16:05:45.289219Z",
            "cloudConnectors": [
                {
                    "id": "emulated-ccon",
                    "signalStrength": 99,
                    "rssi": 0
                }
            ],
            "transmissionMode": "LOW_POWER_STANDARD_MODE"
        },
        "batteryStatus": {
            "percentage": 100,
            "updateTime": "2021-03-13T16:05:41.082485Z"
        },
        "objectPresent": {
            "state": "PRESENT",
            "updateTime": "2021-03-13T16:05:39.474908Z"
        },
        "touch": {
            "updateTime": "2021-03-13T16:05:45.281488Z"
        }
    }
}

temperature_sensor = {
    "name": "projects/c0md3mm0c7pet3vico8g/devices/c0pppd1qdqebrvv1iqp0",
    "type": "temperature",
    "productNumber": "102067",
    "labels": {
        "name": "temperature",
        "test": "2",
    },
    "reported": {
        "networkStatus": {
            "signalStrength": 99,
            "rssi": 0,
            "updateTime": "2021-03-13T16:05:53.021835Z",
            "cloudConnectors": [
                {
                    "id": "emulated-ccon",
                    "signalStrength": 99,
                    "rssi": 0
                }
            ],
            "transmissionMode": "LOW_POWER_STANDARD_MODE"
        },
        "batteryStatus": {
            "percentage": 100,
            "updateTime": "2021-03-13T16:05:49.380240Z"
        },
        "temperature": {
            "value": -27,
            "samples": [
                {
                    "value": -27,
                    "sampleTime": "2021-03-13T16:05:47.722334Z"
                }
            ],
            "updateTime": "2021-03-13T16:05:47.722334Z"
        },
        "touch": {
            "updateTime": "2021-03-13T16:05:53.015325Z"
        }
    }
}

touch_sensor = {
    "name": "projects/c0md3mm0c7pet3vico8g/devices/emucpuc989qdqebrvv29so0",
    "type": "touch",
    "productNumber": "100110",
    "labels": {
        "name": "touch",
        "new-label": "99",
        "virtual-sensor": ""
    },
    "reported": {
        "networkStatus": {
            "signalStrength": 99,
            "rssi": -50,
            "updateTime": "2021-03-13T16:05:58.421952Z",
            "cloudConnectors": [
                {
                    "id": "emulated-ccon",
                    "signalStrength": 99,
                    "rssi": -50
                }
            ],
            "transmissionMode": "LOW_POWER_STANDARD_MODE"
        },
        "batteryStatus": {
            "percentage": 100,
            "updateTime": "2021-03-13T16:05:56.684645Z"
        },
        "touch": {
            "updateTime": "2021-03-13T16:05:55.084433Z"
        }
    }
}

water_present_sensor = {
    "name": "projects/c0md3mmpc7bet3vico8g/devices/emucpppobpqdqebrvv1iqog",
    "type": "waterDetector",
    "productNumber": "101714",
    "labels": {
        "name": "water",
        "virtual-sensor": ""
    },
    "reported": {
        "networkStatus": {
            "signalStrength": 99,
            "rssi": 0,
            "updateTime": "2021-03-13T16:06:05.532940Z",
            "cloudConnectors": [
                {
                    "id": "emulated-ccon",
                    "signalStrength": 99,
                    "rssi": 0
                }
            ],
            "transmissionMode": "LOW_POWER_STANDARD_MODE"
        },
        "batteryStatus": {
            "percentage": 100,
            "updateTime": "2021-03-13T16:06:03.571156Z"
        },
        "waterPresent": {
            "state": "NOT_PRESENT",
            "updateTime": "2021-03-13T16:06:00.157924Z"
        },
        "touch": {
            "updateTime": "2021-03-13T16:06:05.526762Z"
        }
    }
}

proximity_counter_sensor = {
    "name": "projects/c0md3mmpc7bet3vico8g/devices/emucp6e7qvlq0bgk44sg46g",
    "type": "proximityCounter",
    "productNumber": "101730",
    "labels": {
        "name": "proximity counter",
        "virtual-sensor": ""
    },
    "reported": {
        "networkStatus": {
            "signalStrength": 99,
            "rssi": 0,
            "updateTime": "2021-03-13T16:10:32.198962Z",
            "cloudConnectors": [
                {
                    "id": "emulated-ccon",
                    "signalStrength": 99,
                    "rssi": 0
                }
            ],
            "transmissionMode": "LOW_POWER_STANDARD_MODE"
        },
        "batteryStatus": {
            "percentage": 100,
            "updateTime": "2021-03-13T16:10:27.026545Z"
        },
        "objectPresentCount": {
            "total": 55,
            "updateTime": "2021-03-13T16:10:25.184478Z"
        },
        "touch": {
            "updateTime": "2021-03-13T16:10:32.184589Z"
        }
    }
}

touch_count_sensor = {
    "name": "projects/c0md3mmpc7bet3vico8g/devices/emucp6e8dnlq0bgk44sg4c0",
    "type": "touchCounter",
    "productNumber": "101675",
    "labels": {
        "name": "touch counter",
        "virtual-sensor": ""
    },
    "reported": {
        "networkStatus": {
            "signalStrength": 99,
            "rssi": 0,
            "updateTime": "2021-03-13T16:11:43.908965Z",
            "cloudConnectors": [
                {
                    "id": "emulated-ccon",
                    "signalStrength": 99,
                    "rssi": 0
                }
            ],
            "transmissionMode": "LOW_POWER_STANDARD_MODE"
        },
        "batteryStatus": {
            "percentage": 100,
            "updateTime": "2021-03-13T16:11:40.092811Z"
        },
        "touchCount": {
            "total": 33,
            "updateTime": "2021-03-13T16:11:37.365770Z"
        },
        "touch": {
            "updateTime": "2021-03-13T16:11:43.902157Z"
        }
    }
}

null_reported_sensor = {
    "name": "projects/c0md3mmpc7bet3vico8g/devices/emuc1pe9nvlq0bgk44sg4o0",
    "type": "temperature",
    "labels": {
        "name": "Emulated temperature: emuc16e9nvlq0bgk44sg4o0",
        "virtual-sensor": ""
    },
    "reported": {
        "networkStatus": None,  # The REST API will return "null" for
        "batteryStatus": None,  # these values if they are yet to be set.
        "temperature": None,    # This is converted to None in python, which
        "touch": None           # is why we set that here.
    }
}

unknown_reported_sensor = {
    "name": "projects/c0md3mmpc7bet3vico8g/devices/emuc1pe9nvlq0bgk44sg4o0",
    "type": "temperature",
    "productNumber": "",
    "labels": {
        "name": "Emulated temperature: emuc16e9nvlq0bgk44sg4o0",
        "virtual-sensor": ""
    },
    "reported": {
        "networkStatus": None,  # The REST API will return "null" for
        "batteryStatus": None,  # these values if they are yet to be set.
        "temperature": None,    # This is converted to None in python, which
        "touch": None,          # is why we set that here.
        "does_not_exist": {'key1': 'value1', 'key2': 'value2'},
    }
}

all_devices_list = [
    ccon,
    humidity_sensor,
    proximity_sensor,
    temperature_sensor,
    touch_sensor,
    water_present_sensor,
    proximity_counter_sensor,
    touch_count_sensor,
    null_reported_sensor,
]

paginated_device_response = {
    'nextPageToken': '',
    'devices': all_devices_list,
}

simple_data_connector = {
    "name": "projects/c0md3mm0c7pet3vico8g/"
            + "dataconnectors/c16eegpdidie7lltpefg",
    "displayName": "my-new-dcon",
    "type": "HTTP_PUSH",
    "status": "ACTIVE",
    "events": [],
    "labels": [
        "name"
    ],
    "httpConfig": {
        "url": "https://584087e0a1fa.eu.ngrok.io/api/endpoint",
        "signatureSecret": "",
        "headers": {}
    }
}

unknown_data_connector = {
    "name": "projects/c0md3mm0c7pet3vico8g/"
            + "dataconnectors/c16eegpdidie7lltpefg",
    "displayName": "my-new-dcon",
    "type": "unknown",
    "status": "ACTIVE",
    "events": [],
    "labels": [
        "name"
    ],
    "httpConfig": {
        "url": "https://584087e0a1fa.eu.ngrok.io/api/endpoint",
        "signatureSecret": "",
        "headers": {}
    }
}

configured_data_connector = {
    "name": "projects/c0md3pm0p7bet3vico8g/"
            + "dataconnectors/c16pegipidie7lltrefg",
    "displayName": "my-new-dcon",
    "type": "HTTP_PUSH",
    "status": "ACTIVE",
    "events": [
        "touch",
        "temperature",
        "objectPresent"
    ],
    "labels": [
        "name",
        "custom-label-01",
        "custom-label-02"
    ],
    "httpConfig": {
        "url": "https://584087e0a1fa.eu.ngrok.io/api/endpoint",
        "signatureSecret": "some-very-good-secret",
        "headers": {
            "another-header": "header-contents",
            "some-header": "abc123"
        }
    }
}

paginated_data_connectors_response = {
    'nextPageToken': '',
    'dataConnectors': [
        simple_data_connector,
        configured_data_connector,
    ]
}

small_project = {
    "name": "projects/c15j9p094l47cdv0o3pg",
    "displayName": "my-project",
    "organization": "organizations/c11humqoss9000pgu53g",
    "organizationDisplayName": "some-display-name",
    "sensorCount": 7,
    "cloudConnectorCount": 1,
    "inventory": False
}

empty_project = {
    "name": "projects/c10humqoss90036gu876",
    "displayName": "no-sensors-here",
    "organization": "organizations/c10hamsoss90036gu53g",
    "organizationDisplayName": "some-display-name",
    "sensorCount": 0,
    "cloudConnectorCount": 0,
    "inventory": True
}

projects = {
    'nextPageToken': '',
    'projects': [
        small_project,
        empty_project
    ]
}

project_permissions = {
    'nextPageToken': '',
    'permissions': [
        'sensor.update',
        'serviceaccount.read',
        'dataconnector.read',
        'serviceaccount.key.read',
        'project.read',
        'emulator.create',
        'sensor.read',
        'serviceaccount.key.create',
    ]
}

organization = {
    "name": "organizations/c10hussoss90036gu54g",
    "displayName": "some-display-name"
}

organizations = {
    'nextPageToken': '',
    'organizations': [
        organization,
        organization,
        organization,
    ]
}

organization_permissions = {
    'nextPageToken': '',
    'permissions': [
        'project.create',
        'membership.create',
        'membership.read',
        'membership.update',
        'organization.update',
        'organization.read',
        'membership.delete',
    ]
}

service_account1 = {
    "name": "projects/c14u9q095l47ccv1o3pg/"
            + "serviceaccounts/c14uar7915fg90c8lfp0",
    "email": "c15uar7915fg13c8lfp0@c15u9p094l47cdv1o3qg."
            + "serviceaccount.d21s.com",
    "displayName": "service-account-1",
    "enableBasicAuth": False,
    "createTime": "2021-03-11T09:39:56.015971Z",
    "updateTime": "2021-03-11T09:39:56.103249Z"
}

service_account2 = {
    "name": "projects/c14u88094l47cdv1o3pg/"
            + "serviceaccounts/c17m9hm914gg00c8levg",
    "email": "c17m8hn915gg00c8levg@c24u9p094l47cdv1o2pg."
            + "serviceaccount.d21s.com",
    "displayName": "service-account-2",
    "enableBasicAuth": True,
    "createTime": "2021-03-15T13:44:38.974097Z",
    "updateTime": "2021-03-15T13:44:39.039375Z"
}

service_accounts = {
    'nextPageToken': '',
    'serviceAccounts': [
        service_account1,
        service_account2,
    ]
}

key_without_secret = {
    "name": "projects/c14u0p894l47cdd1o3pg/serviceaccounts/"
            + "c18jpqmolv9076epsv1g/keys/c18rs36olv9021epsv2g",
    "id": "c18rs36olv9021epsv2g",
    "createTime": "2021-03-17T08:25:48.953067Z"
}

key_with_secret = {
    "key": {
        "name": "projects/c14u9p095l47ccv1o3pg/serviceaccounts/"
                + "c18ppqmoiv9008epsv1g/keys/c19tg0eoiv9008epsv50",
        "id": "c19tg0eoiv9008epsv50",
        "createTime": "2021-03-17T10:20:49.231251Z",
    },
    "secret": "239dcd912b8041a58054f843a2a633a4"
}

keys = {
    'nextPageToken': '',
    'keys': [
        key_without_secret,
        key_without_secret,
    ]
}

user_member = {
    "name": "organizations/c11humq0ss9o036gu53g/members/9201",
    "displayName": "my-org-member",
    "roles": [
        "roles/organization.admin"
    ],
    "status": "ACCEPTED",
    "email": "my_user_account@disruptive-technologies.com",
    "accountType": "USER",
    "createTime": "1970-01-01T00:00:00.000000Z"
}

service_account_member = {
    "name": "organizations/c10humqoss90032gu54g/members/c17n9hn915gg00c8ievg",
    "displayName": "localdev",
    "roles": [
        "roles/project.developer"
    ],
    "status": "ACCEPTED",
    "email": "c17m9hn815gg00c8levu@c14u9p094l47cdv1o3pg."
    + "serviceaccount.d21s.com",
    "accountType": "SERVICE_ACCOUNT",
    "createTime": "2021-03-15T13:45:53.964040Z"
}

members = {
    'nextPageToken': '',
    'members': [
        user_member,
        service_account_member,
    ]
}

project_user_role = {
    "name": "roles/project.user",
    "displayName": "Project user",
    "description": "Users cannot change anything, just view "
    + "the data in the Project",
    "permissions": [
        "project.read",
        "membership.read",
        "sensor.read",
        "device.read",
        "dataconnector.read",
        "serviceaccount.read",
        "serviceaccount.key.read",
        "emulator.read"
    ]
}

project_developer_role = {
    "name": "roles/project.developer",
    "displayName": "Project developer",
    "description": "Allows editing devices and Project settings",
    "permissions": [
        "project.read",
        "membership.read",
        "sensor.read",
        "sensor.update",
        "device.read",
        "device.update",
        "dataconnector.create",
        "dataconnector.read",
        "dataconnector.update",
        "dataconnector.delete",
        "serviceaccount.read",
        "serviceaccount.key.read",
        "emulator.read",
        "emulator.update",
        "emulator.create",
        "emulator.delete"
    ]
}

roles = {
    'nextPageToken': '',
    'roles': [
        project_user_role,
        project_developer_role,
    ]
}

metrics = {
    'metrics': {
        'successCount': 9,
        'errorCount': 0,
        'latency99p': '0.411s',
    }
}

created_temperature_emulator = {
    'name': 'projects/c14u9p094l47cdv1o3pg/devices/emuc1so7tgttn8sjobqvvug',
    'type': 'temperature',
    'productNumber': '102058',
    'labels': {
        'key': 'value',
        'name': 'new-device',
        'virtual-sensor': '',
    }
}

touch_event = {
    "eventId": "01",
    "targetName": "/projets/project_id/devices/device_id ",
    "eventType": "touch",
    "data": {
        "touch": {
            "updateTime": "2019-05-16T08:13:15.361624Z"
        }
    },
    "timestamp": "1970-01-01T00:00:00Z"
}

temperature_event = {
    "eventId": "02",
    "targetName": "/projets/project_id/devices/device_id ",
    "eventType": "temperature",
    "data": {
        "temperature": {
            "value": 24.9,
            "samples": [
                {
                    "value": 24.9,
                    "sampleTime": "2019-05-16T08:15:18.318751Z"
                }
            ],
            "updateTime": "2019-05-16T08:15:18.318751Z"
        }
    },
    "timestamp": "1970-01-01T00:00:00Z"
}

object_present_event = {
    "eventId": "03",
    "targetName": "/projets/project_id/devices/device_id ",
    "eventType": "objectPresent",
    "data": {
        "objectPresent": {
            "state": "NOT_PRESENT",
            "updateTime": "2019-05-16T08:37:10.711412Z"
        }
    },
    "timestamp": "1970-01-01T00:00:00Z"
}

humidity_event = {
    "eventId": "04",
    "targetName": "/projets/project_id/devices/device_id ",
    "eventType": "humidity",
    "data": {
        "humidity": {
            "temperature": 22.45,
            "relativeHumidity": 17,
            "updateTime": "2019-05-16T06:13:46.369000Z"
        }
    },
    "timestamp": "1970-01-01T00:00:00Z"
}

object_present_count_event = {
    "eventId": "05",
    "targetName": "/projets/project_id/devices/device_id ",
    "eventType": "objectPresentCount",
    "data": {
        "objectPresentCount": {
            "total": 4176,
            "updateTime": "2019-05-16T08:23:43.209000Z"
        }
    },
    "timestamp": "1970-01-01T00:00:00Z"
}

touch_count_event = {
    "eventId": "06",
    "targetName": "/projets/project_id/devices/device_id ",
    "eventType": "touchCount",
    "data": {
        "touchCount": {
            "total": 469,
            "updateTime": "2019-05-16T08:25:21.604000Z"
        }
    },
    "timestamp": "1970-01-01T00:00:00Z"
}

water_present_event = {
    "eventId": "07",
    "targetName": "/projets/project_id/devices/device_id ",
    "eventType": "waterPresent",
    "data": {
        "waterPresent": {
            "state": "PRESENT",
            "updateTime": "2019-05-16T08:43:16.266000Z"
        }
    },
    "timestamp": "1970-01-01T00:00:00Z"
}

network_status_event = {
    "eventId": "08",
    "targetName": "/projets/project_id/devices/device_id ",
    "eventType": "networkStatus",
    "data": {
        "networkStatus": {
            "signalStrength": 45,
            "rssi": -83,
            "updateTime": "2019-05-16T08:21:21.076013Z",
            "cloudConnectors": [
                {
                    "id": "bdkjbo2v0000uk377c4g",
                    "signalStrength": 45,
                    "rssi": -83
                }
            ],
            "transmissionMode": "LOW_POWER_STANDARD_MODE"
        }
    },
    "timestamp": "1970-01-01T00:00:00Z"
}

battery_status_event = {
    "eventId": "09",
    "targetName": "/projets/project_id/devices/device_id ",
    "eventType": "batteryStatus",
    "data": {
        "batteryStatus": {
            "percentage": 100,
            "updateTime": "2019-05-16T08:21:21.076013Z"
        }
    },
    "timestamp": "1970-01-01T00:00:00Z"
}

labels_changed_event = {
    "eventId": "10",
    "targetName": "/projets/project_id/devices/device_id ",
    "eventType": "labelsChanged",
    "data": {
        "added": {
            "label-key": "label-value"
        },
        "modified": {
            "label-key": "new-label-value"
        },
        "removed": [
            "remove-key1",
            "remove-key2"
        ]
    },
    "timestamp": "1970-01-01T00:00:00Z"
}

connection_status_event = {
    "eventId": "11",
    "targetName": "/projets/project_id/devices/device_id ",
    "eventType": "connectionStatus",
    "data": {
        "connectionStatus": {
            "connection": "ETHERNET",
            "available": [
                "CELLULAR",
                "ETHERNET"
            ],
            "updateTime": "2019-05-16T08:21:21.076013Z"
        }
    },
    "timestamp": "1970-01-01T00:00:00Z"
}

ethernet_status_event = {
    "eventId": "12",
    "targetName": "/projets/project_id/devices/device_id ",
    "eventType": "ethernetStatus",
    "data": {
        "ethernetStatus": {
            "macAddress": "f0:b5:b7:00:0a:08",
            "ipAddress": "10.0.0.1",
            "errors": [],
            "updateTime": "2019-05-16T08:21:21.076013Z"
        }
    },
    "timestamp": "1970-01-01T00:00:00Z"
}

cellular_status_event = {
    "eventId": "13",
    "targetName": "/projets/project_id/devices/device_id ",
    "eventType": "cellularStatus",
    "data": {
        "cellularStatus": {
            "signalStrength": 80,
            "errors": [],
            "updateTime": "2019-05-16T08:21:21.076013Z"
        }
    },
    "timestamp": "1970-01-01T00:00:00Z"
}

co2_event = {
    "eventId": "u7pbuijjnlactnn1p510",
    "targetName": "projects/i75ivl3go7df88ctp0uu/devices/b6sfppl7rihg1dm4ud8g",
    "eventType": "co2",
    "data": {
        "co2": {
            "ppm": 526,
            "updateTime": "2022-01-27T15:50:34.471000Z"
        }
    },
    "timestamp": "2022-01-27T15:50:34.471000Z"
}

pressure_event = {
    "eventId": "c0pbuiurq6u6ltshi151",
    "targetName": "projects/c75ivl3go7df88ctp0ug/devices/u6sfppl7rihg0dm4ud7s",
    "eventType": "pressure",
    "data": {
        "pressure": {
            "pascal": 99301,
            "updateTime": "2022-01-27T15:50:34.471000Z"
        }
    },
    "timestamp": "2022-01-27T15:50:34.471000Z"
}

event_history_each_type = {
    'nextPageToken': '',
    'events': [
        touch_event,
        temperature_event,
        object_present_event,
        humidity_event,
        object_present_count_event,
        touch_count_event,
        water_present_event,
        network_status_event,
        battery_status_event,
        labels_changed_event,
        connection_status_event,
        ethernet_status_event,
        cellular_status_event,
        co2_event,
        pressure_event,
    ]
}

stream_ping = b'{"result":{"event":{"eventId":"c18tihhh9sn7fi2hur50",'\
    b'"targetName":"projects/c14u9p094l47ccv1o3p9","eventType":'\
    b'"ping","data":null,"timestamp":"2021-04-21T07:50:30.604786Z"}}}'

stream_temperature_event = b'{"result":{"event":{"eventId":'\
    b'"d1vtobtd83ut9sd2bj9g","targetName":"projects/914u9p094l47cdv1o3pg'\
    b'/devices/emui17m69nlq0bgk44smcng","eventType":"temperature","data"'\
    b':{"temperature":{"value":5,"updateTime":"2021-04-21T08:'\
    b'15:43.512330Z","samples":[{"value":5,"sampleTime":"2021-04-21T08:'\
    b'15:43.512330Z"}]}},"timestamp":"2021-04-21T08:15:43.512330Z"}}}'

stream_networkstatus_event = b'{"result":{"event":{"eventId":"c1vtubtd83it'\
    b'9ud2bja0","targetName":"projects/c14u9p094l47cdb1oipg/devices/'\
    b'emuc17m69nlq0bgk4osmcug","eventType":"networkStatus","data"'\
    b':{"networkStatus":{"signalStrength":99,"rssi":0,"updateTime"'\
    b':"2021-04-21T08:15:43.520167Z","cloudConnectors":[{"id":'\
    b'"emulated-ccon","signalStrength":99,"rssi":0}],'\
    b'"transmissionMode":"LOW_POWER_STANDARD_MODE"}},"timestamp":'\
    b'"2021-04-21T08:15:43.520167Z"}}}'

transfer_device_no_errors = {
    'transferredDevices': [
        'projects/source_project/devices/device_id1',
        'projects/source_project/devices/device_id2',
    ],
    'transferErrors': [],
}

transfer_device_errors = {
    'transferredDevices': [
        'projects/source_project/devices/device_id1',
        'projects/source_project/devices/device_id2',
    ],
    'transferErrors': [
        {
            'device': 'projects/source_project/devices/123',
            'status': {
                'code': 'NOT_FOUND',
                'message': 'resource not found',
            }
        },
        {
            'device': 'projects/source_project/devices/abc',
            'status': {
                'code': 'NOT_FOUND',
                'message': 'resource not found',
            }
        },
    ],
}

batch_label_response = {
    "batchErrors": [
        {
            "device": "/projects/<source_project_id>/devices/<device_id_1>",
            "status": {
                "code": "INVALID_ARGUMENT",
                "message": "Max labels reached for device."
            }
        },
        {
            "device": "/projects/<source_project_id>/devices/<device_id_2>",
            "status": {
                "code": "INTERNAL_ERROR",
                "message": "Operation timed out. Retry again in a few seconds."
            }
        }
    ]
}

claim_error_device_already_claimed = {
    'deviceId': 'b',
    'code': 'ALREADY_CLAIMED',
    'message': 'The device was previously claimed',
}

claim_error_device_not_found = {
    'deviceId': 'c',
    'code': 'NOT_FOUND',
    'message': 'The device was not found',
}

claim_error_kit_not_found = {
    'kitId': 'd',
    'code': 'NOT_FOUND',
    'message': 'The kit was not found',
}

claimed_devices = {
    'claimedDevices': [
        {
            'deviceId': 'a',
            'deviceType': 'temperature',
            'productNumber': 'a',
            'isClaimed': True,
        },
        {
            'deviceId': 'b',
            'deviceType': 'temperature',
            'productNumber': 'b',
            'isClaimed': True,
        },
    ],
    'claimErrors': {
        'devices': [],
        'kits': [],
    }
}

claimed_device_already_claimed = {
    'claimedDevices': [
        {
            'deviceId': 'a',
            'deviceType': 'temperature',
            'productNumber': 'a',
            'isClaimed': True,
        },
    ],
    'claimErrors': {
        'devices': [
            claim_error_device_already_claimed,
        ],
        'kits': [],
    }
}

claimed_device_not_found = {
    'claimedDevices': [
        {
            'deviceId': 'a',
            'deviceType': 'temperature',
            'productNumber': 'a',
            'isClaimed': True,
        },
    ],
    'claimErrors': {
        'devices': [
            claim_error_device_not_found,
        ],
        'kits': [],
    }
}

claimed_kit_not_found = {
    'claimedDevices': [
        {
            'deviceId': 'a',
            'deviceType': 'temperature',
            'productNumber': 'a',
            'isClaimed': True,
        },
    ],
    'claimErrors': {
        'devices': [],
        'kits': [claim_error_kit_not_found],
    }
}

claim_info_kit = {
    'type': 'KIT',
    'kit': {
        'kitId': 'fff000',
        'displayName': 'Starter Kit EU, 5 sensors',
        'sensors': {
            'totalCount': 5,
            'claimedCount': 0,
        },
        'cloudConnectors': {
            'totalCount': 1,
            'claimedCount': 0,
        },
        'devices': [
            {
                'deviceId': 'a',
                'deviceType': 'touch',
                'productNumber': '',
                'isClaimed': True,
            },
            {
                'deviceId': 'b',
                'deviceType': 'proximity',
                'productNumber': '',
                'isClaimed': True,
             },
            {
                'deviceId': 'c',
                'deviceType': 'temperature',
                'productNumber': '',
                'isClaimed': True,
            },
            {
                'deviceId': 'd',
                'deviceType': 'proximity',
                'productNumber': '',
                'isClaimed': True,
            },
            {
                'deviceId': 'e',
                'deviceType': 'temperature',
                'productNumber': '',
                'isClaimed': True,
            },
        ],
    },
}
