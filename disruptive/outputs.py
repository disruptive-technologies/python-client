# Project imports.
import disruptive.transforms as dttrans


class OutputBase():
    """
    Represents common features for all returnable objects.

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
        self._raw = raw

    def __str__(self):
        out = self.__dump([], self, level=0)
        return '\n'.join(out)

    def __dump(self, out, obj, level):
        # Set the two formatting indent levels.
        n_spaces = 4
        ls = level*' '*n_spaces

        # Print name of the current object if level is 0.
        if level == 0:
            out.append(ls + str(self.__class__.__name__) + ' object:')
            # out.insert(-1, ls + '_'*len(out[-1]))
            out.insert(-1, '')
            out.append(ls + '-'*len(out[-1]))

        # Append the various public attributes recursively.
        for a in vars(obj):
            # Skip private attributes.
            if a.startswith('_'):
                continue

            # Fetch and evaluate the attribute value / type.
            val = getattr(obj, a)
            if hasattr(val, '__dict__'):
                # Class objects should be dumped recursively.
                out.append('{}[{}] {}:'.format(ls, type(val).__name__, a))
                self.__dump(out, val, level=level+1)

            elif isinstance(val, list):
                # Lists content should be iterated through.
                out.append('{}[{}] {}:'.format(ls, type(val).__name__, a))
                self.__dump_list(out, val, level+1)

            else:
                # Other types can be printed directly.
                out.append('{}[{}] {}: {}'.format(
                    ls, type(val).__name__, a, str(val)
                ))

        return out

    def __dump_list(self, out, lst, level):
        n_spaces = 4
        ls = (level+1)*' '*n_spaces
        for val in lst:
            if hasattr(val, '__dict__'):
                out.append('{}[{}]:'.format(ls, type(val).__name__))
                self.__dump(out, val, level=level+2)
            else:
                out.append('{}[{}] {}'.format(
                    ls, type(val).__name__, val
                ))
        return out


class Metric(OutputBase):
    """
    Represents the metrics for a dataconnector over the last 3 hours.

    Attributes
    ----------
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
        self.success_count = metric['metrics']['successCount']
        self.error_count = metric['metrics']['errorCount']
        self.latency = metric['metrics']['latency99p']


class Member(OutputBase):
    """
    Represents a member.

    Attributes
    ----------
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
        self.display_name = member['displayName']
        self.roles = [r.split('/')[-1] for r in member['roles']]
        self.status = member['status']
        self.email = member['email']
        self.account_type = member['accountType']
        self.create_time = dttrans.to_datetime(member['createTime'])
