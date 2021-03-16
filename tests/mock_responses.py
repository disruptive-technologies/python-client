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
    "name": "projects/c0md3mm0c7pet3vico8g/devices/emuc0pppd1qdqebrvv1iqp0",
    "type": "temperature",
    "labels": {
        "name": "temperature",
        "test": "2",
        "virtual-sensor": ""
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

touch_counter_sensor = {
    "name": "projects/c0md3mmpc7bet3vico8g/devices/emucp6e8dnlq0bgk44sg4c0",
    "type": "touchCounter",
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

all_devices_list = [
    ccon,
    humidity_sensor,
    proximity_sensor,
    temperature_sensor,
    touch_sensor,
    water_present_sensor,
    proximity_counter_sensor,
    touch_counter_sensor,
    null_reported_sensor,
]

paginated_device_response = {
    'nextPageToken': '',
    'devices': all_devices_list,
}

simple_dataconnector = {
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

configured_dataconnector = {
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

paginated_dataconnectors_response = {
    'nextPageToken': '',
    'dataConnectors': [
        simple_dataconnector,
        configured_dataconnector,
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

serviceaccount1 = {
    "name": "projects/c14u9q095l47ccv1o3pg/serviceaccounts/c14uar7915fg90c8lfp0",
    "email": "c15uar7915fg13c8lfp0@c15u9p094l47cdv1o3qg.serviceaccount.d21s.com",
    "displayName": "service-account-1",
    "enableBasicAuth": False,
    "createTime": "2021-03-11T09:39:56.015971Z",
    "updateTime": "2021-03-11T09:39:56.103249Z"
}

serviceaccount2 = {
    "name": "projects/c14u88094l47cdv1o3pg/serviceaccounts/c17m9hm914gg00c8levg",
    "email": "c17m8hn915gg00c8levg@c24u9p094l47cdv1o2pg.serviceaccount.d21s.com",
    "displayName": "service-account-2",
    "enableBasicAuth": True,
    "createTime": "2021-03-15T13:44:38.974097Z",
    "updateTime": "2021-03-15T13:44:39.039375Z"
}

serviceaccounts = {
    'nextPageToken': '',
    'serviceAccounts': [
        serviceaccount1,
        serviceaccount2,
    ]
}
