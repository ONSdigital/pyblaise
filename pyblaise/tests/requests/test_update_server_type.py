import pytest
import requests
import urllib

from collections import namedtuple

from pyblaise import update_server_type

from pyblaise.operations.definitions import operations

host_infos = [
    {
        "protocol": "http",
        "host": "my-host.com",
        "port": 8000,
        "token": "my-dummy-token",
    },
]

mock_response_operation_success = [
    r"""
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <UpdateServerTypeResponse xmlns="http://www.blaise.com/deploy/2013/03">
      <UpdateServerTypeResult xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
        <Message>Operation success</Message>
        <Statuscode>0</Statuscode>
      </UpdateServerTypeResult>
    </UpdateServerTypeResponse>
  </s:Body>
</s:Envelope>
    """
]


@pytest.mark.parametrize("host_info", host_infos)
def test_update_server_type_api_call(host_info, requests_mock):
    definition = operations["update-server-type"]

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
        text=mock_response_operation_success[0],
    )

    update_server_type(**host_info, new_server_type="slave", master_hostname="newhost")

    assert requests_mock.last_request.scheme == host_info["protocol"]
    assert requests_mock.last_request.netloc == "%s:%i" % (
        host_info["host"],
        host_info["port"],
    )
    assert requests_mock.last_request.port == host_info["port"]
    assert requests_mock.called is True
    assert requests_mock.call_count == 1
    assert "my-dummy-token" in requests_mock.last_request.text


@pytest.mark.parametrize("host_info", host_infos)
def test_update_server_type_parse_response_returns_message(
    host_info, requests_mock
):
    definition = operations["update-server-type"]

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
        text=mock_response_operation_success[0],
    )

    status_code, message = update_server_type(**host_info, new_server_type="slave", master_hostname="newhost")

    assert status_code == 200
    assert isinstance(message, str)

    assert "Operation success" == message
