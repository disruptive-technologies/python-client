# Project imports
import disruptive.log as dtlog

# Standard library imports.
from typing import Optional


def _from_dict(dataconnector: dict):
    # Isolate the dataconnector type.
    dataconnector_type = dataconnector['type']

    # Select the appropriate config depending on type.
    if dataconnector_type == 'HTTP_PUSH':
        # Create and return an HttpPush object.
        return HttpPush(
            url=dataconnector['httpConfig']['url'],
            signature_secret=dataconnector['httpConfig']['signatureSecret'],
            headers=dataconnector['httpConfig']['headers'],
        )
    else:
        # If this else statement runs, no config is (yet) available for type.
        dtlog.log('No config available for {} dataconnectors.'.format(
            dataconnector_type
        ))


class HttpPush():
    """
    Type-specific configurations for the HTTP_PUSH dataconnector.

    Attributes
    ----------
    url : str
        Endpoint URL towards which events are forwarded. Must be HTTPS.
    signature_secret : str
        Secret with which each forwarded event is signed.
    headers : dict[str, str]
        Dictionary of headers to include with each forwarded event.

    """

    dataconnector_type = 'HTTP_PUSH'

    def __init__(self,
                 url: Optional[str] = None,
                 signature_secret: Optional[str] = None,
                 headers: Optional[dict] = None,
                 ) -> None:
        """
        Constructs the HttpPush object.

        Parameters
        ----------
        url : str, optional
            Endpoint URL towards which events are forwarded. Must be HTTPS.
        signature_secret : str, optional
            Secret with which each forwarded event is signed.
        headers : dict[str, str], optional
            Dictionary of headers to include with each forwarded event.

        """

        # Set parameter attributes.
        self.url = url
        self.signature_secret = signature_secret
        self.headers = headers

    def _to_dict(self):
        config: dict = dict()
        if self.url is not None:
            config['url'] = self.url
        if self.signature_secret is not None:
            config['signatureSecret'] = self.signature_secret
        if self.headers is not None:
            config['headers'] = self.headers
        return 'httpConfig', config
