import pytest
import requests
import urllib

from collections import namedtuple

from pyblaise import get_auth_token

from pyblaise.definitions import operations

host_infos = [
    {
        "protocol": "http",
        "host": "my-host.com",
        "port": 8000,
        "username": "admin",
        "password": "admin",
    },
]

mock_tokens = [
    {
        "access-token": "hi-this-is-my-access-token",
        "refresh-token": "hi-this-is-my-refresh-token",
    }
]

mock_response = [
    """
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <RequestTokenResponse xmlns="http://www.blaise.com/security/2016/06">
      <RequestTokenResult xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
        <AccessToken>{access-token}</AccessToken>
        <RefreshToken>{refresh-token}</RefreshToken>
      </RequestTokenResult>
    </RequestTokenResponse>
  </s:Body>
</s:Envelope>
""".format(
        **mock_tokens[0]
    )
]


@pytest.mark.parametrize("host_info", host_infos)
def test_get_auth_token_api_call(host_info, requests_mock):
    definition = operations["request-token"]

    requests_mock.register_uri(
        "POST",
        urllib.parse.urlunsplit(
            (
                host_info["protocol"],
                "%s:%i" % (host_info["host"], host_info["port"]),
                definition["path"],
                "",
                "",
            )
        ),
        headers=definition["headers"],
        text=mock_response[0],
    )

    get_auth_token(**host_info)

    assert requests_mock.last_request.scheme == host_info["protocol"]
    assert requests_mock.last_request.netloc == "%s:%i" % (
        host_info["host"],
        host_info["port"],
    )
    assert requests_mock.last_request.port == host_info["port"]
    assert requests_mock.called is True
    assert requests_mock.call_count == 1


@pytest.mark.parametrize("host_info", host_infos)
def test_get_auth_token_returns_token(host_info, requests_mock):
    definition = operations["request-token"]

    requests_mock.register_uri(
        "POST",
        urllib.parse.urlunsplit(
            (
                host_info["protocol"],
                "%s:%i" % (host_info["host"], host_info["port"]),
                definition["path"],
                "",
                "",
            )
        ),
        headers=definition["headers"],
        text=mock_response[0],
        status_code=200,
        reason="OK",
    )

    x = get_auth_token(**host_info)

    assert x is not None
    assert len(x) == 2
    assert x[0] == 200
    assert x[1] == mock_tokens[0]["access-token"]
