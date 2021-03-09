devices = {
    'touch': {
        'name': 'projects/c0md3mm0c7bet3vico8g/devices/emuc0uc989qdqebrvv29so0',
        'type': 'touch',
        'labels': {
            'name': 'touch',
            'virtual-sensor': ''
        }, 'reported': {
            'networkStatus': {
                'signalStrength': 99,
                'rssi': 0,
                'updateTime': '2021-03-05T16:03:54.563449Z',
                'cloudConnectors': [
                    {
                        'id':
                        'emulated-ccon',
                        'signalStrength': 99,
                        'rssi': 0
                    }
                ],
                'transmissionMode': 'LOW_POWER_STANDARD_MODE'
            },
            'batteryStatus': None,
            'touch': {
                'updateTime': '2021-03-05T16:03:54.554749Z'
            }
        }
    }
}

dataconnectors = {
    'basic': {
        'name': 'projects/c0md3mm0c7bet3vico8g/dataconnectors/c0selfd3dsqvucf9l990',
        'displayName': 'ngrok',
        'type': 'HTTP_PUSH',
        'status': 'ACTIVE',
        'events': [],
        'labels': ['name'],
        'httpConfig': {
            'url': 'https://584087e0a1fa.eu.ngrok.io/api/endpoint',
            'signatureSecret': 'veryGoodSecret',
            'headers': {}
        }
    }
}
