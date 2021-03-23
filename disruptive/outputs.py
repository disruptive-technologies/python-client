# Standard-library imports.
import json

# Project imports.
import disruptive.transforms as dttrans


class OutputBase():
    """
    Represents common features for all returnable objects.

    Attributes
    ----------
    raw : dict
        Unmodified dictionary of data received from the REST API.

    """

    def __init__(self, raw: dict) -> None:
        """
        Constructs the OutputBase object by setting raw attribute.

        Parameters
        ----------
        raw : dict
            Unmodified dictionary of data received from the REST API.

        """

        # Set attribute from input argument.
        self.raw = raw

    def pprint(self, n: int = 4) -> None:
        """
        Print the raw attribute using json.dumps() for formatting.

        Parameters
        ----------
        n : int
            Number of spaces in indent.

        """

        print(json.dumps(self.raw, indent=n))


class Metric(OutputBase):
    """
    Represents the metrics for a dataconnector over the last 3 hours.

    Attributes
    ----------
    raw : dict
        Unmodified metric response dictionary.
    success_count : int
        Number of 2xx responses.
    error_count : int
        Number of non-2xx responses.
    latency : str
        Average latency.

    """

    def __init__(self, metric: dict) -> None:
        """
        Constructs the Metric object by unpacking the raw response.

        """

        # Inherit attributes from ResponseBase parent.
        OutputBase.__init__(self, metric)

        # Unpack attributes from dictionary.
        self.success_count = self.raw['metrics']['successCount']
        self.error_count = self.raw['metrics']['errorCount']
        self.latency = self.raw['metrics']['latency99p']


class Member(OutputBase):
    """
    Represents a member.

    Attributes
    ----------
    raw : dict
        Unmodified member response dictionary.
    display_name : str
        Provided member display name.
    roles : list[str]
        Roles provided to the member.
    status : str
        Whether the member invite is ACCEPTED or PENDING.
    email : str
        Member email address.
    account_type : str
        Whether the member is a USER or SERVICE_ACCOUNT.
    create_time : datetime
        Timestamp of when the member was created.

    """

    def __init__(self, member):
        """
        Constructs the Member object by unpacking the raw response.

        """

        # Inherit from Response parent.
        OutputBase.__init__(self, member)

        # Unpack attributes from dictionary.
        self.display_name = self.raw['displayName']
        self.roles = [r.split('/')[-1] for r in self.raw['roles']]
        self.status = self.raw['status']
        self.email = self.raw['email']
        self.account_type = self.raw['accountType']
        self.create_time = dttrans.iso8601_to_datetime(self.raw['createTime'])
