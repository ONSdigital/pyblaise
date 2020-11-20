import pytest
import requests
import urllib

from collections import namedtuple

from pyblaise import get_remote_defined_roles

from pyblaise.operations.definitions import operations

host_infos = [
    {
        "protocol": "http",
        "host": "my-host.com",
        "port": 8000,
        "token": "my-dummy-token",
    },
]

mock_response_no_roles = [
    """
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <GetRemoteDefinedRoles201711Response xmlns="http://www.blaise.com/deploy/2017/11">
      <GetRemoteDefinedRoles201711Result xmlns:a="http://www.blaise.com/deploy/2014/12" xmlns:i="http://www.w3.org/2001/XMLSchema-instance" />
    </GetRemoteDefinedRoles201711Response>
  </s:Body>
</s:Envelope>
"""
]

mock_response_two_roles = [
    """
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <GetRemoteDefinedRoles201711Response xmlns="http://www.blaise.com/deploy/2017/11">
      <GetRemoteDefinedRoles201711Result xmlns:a="http://www.blaise.com/deploy/2014/12" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
        <a:RoleInfo2>
          <a:Binding>http</a:Binding>
          <a:Name>CATI</a:Name>
          <a:Port>8033</a:Port>
        </a:RoleInfo2>
        <a:RoleInfo2>
          <a:Binding>http</a:Binding>
          <a:Name>DASHBOARD</a:Name>
          <a:Port>80</a:Port>
        </a:RoleInfo2>
      </GetRemoteDefinedRoles201711Result>
    </GetRemoteDefinedRoles201711Response>
  </s:Body>
</s:Envelope>
"""
]


@pytest.mark.parametrize("host_info", host_infos)
def test_get_remote_defined_roles_api_call(host_info, requests_mock):
    definition = operations["get-remote-defined-roles"]

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
        text=mock_response_two_roles[0],
    )

    get_remote_defined_roles(
        **host_info, binding="http", remote_host="remote", remote_port="port"
    )

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
def test_get_remote_defined_roles_parse_no_roles(host_info, requests_mock):
    definition = operations["get-remote-defined-roles"]

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
        text=mock_response_no_roles[0],
    )

    status_code, roles = get_remote_defined_roles(
        **host_info, binding="http", remote_host="remote", remote_port="port"
    )

    assert status_code == 200
    assert isinstance(roles, list)
    assert len(roles) == 0


@pytest.mark.parametrize("host_info", host_infos)
def test_get_remote_defined_roles_parse_two_roles(host_info, requests_mock):
    definition = operations["get-remote-defined-roles"]

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
        text=mock_response_two_roles[0],
    )

    status_code, roles = get_remote_defined_roles(
        **host_info, binding="http", remote_host="remote", remote_port="port"
    )

    assert status_code == 200
    assert isinstance(roles, list)
    assert len(roles) == 2


@pytest.mark.parametrize("host_info", host_infos)
def test_get_remote_defined_roles_parse_two_roles_returns_correct_values(
    host_info, requests_mock
):
    definition = operations["get-remote-defined-roles"]

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
        text=mock_response_two_roles[0],
    )

    status_code, roles = get_remote_defined_roles(
        **host_info, binding="http", remote_host="remote", remote_port="port"
    )

    assert status_code == 200
    assert isinstance(roles, list)
    assert len(roles) == 2

    # check the role keys
    assert "name" in roles[0]
    assert "binding" in roles[0]
    assert "port" in roles[0]

    assert "name" in roles[1]
    assert "binding" in roles[1]
    assert "port" in roles[1]

    # check the role values
    assert roles[0]["name"] == "CATI"
    assert roles[0]["binding"] == "http"
    assert roles[0]["port"] == "8033"

    assert roles[1]["name"] == "DASHBOARD"
    assert roles[1]["binding"] == "http"
    assert roles[1]["port"] == "80"
