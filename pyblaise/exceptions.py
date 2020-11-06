class ServerConnectionTimeout(Exception):
    """
    Wrapper for the requests.ConnectTimeout, requests.ReadTimeout and requests.Timeout exceptions
    https://requests.readthedocs.io/en/latest/api/#exceptions
    """

    pass


class ServerConnectionError(Exception):
    """
    Wrapper for the requets.ConnectionError exception
    https://requests.readthedocs.io/en/latest/api/#exceptions
    """

    pass


class CreateRoleFailed(Exception):
    pass
