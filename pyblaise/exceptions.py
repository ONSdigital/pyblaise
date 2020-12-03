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


class ServerResponse500(Exception):
    """
    raised when the SOAP response has a 500 status code
    """
    def __init__(self, response_object = None):
        self.response_object = response_object

    def get_response_object(self):
        return self.response_object
