import pytest
import requests
import urllib

from collections import namedtuple

from pyblaise import get_all_users

from pyblaise.operations.definitions import operations

host_infos = [
    {
        "protocol": "http",
        "host": "my-host.com",
        "port": 8000,
        "token": "my-dummy-token",
    },
]

mock_users = [{"username": "test-user-0123", "serverpark": "my-server-park"}]

mock_response_no_users = [
    """
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <GetAllUsers201812Response xmlns="http://www.blaise.com/security/2018/12">
      <GetAllUsers201812Result xmlns:i="http://www.w3.org/2001/XMLSchema-instance"/>
    </GetAllUsers201812Response>
  </s:Body>
</s:Envelope>
"""
]

mock_response_one_user = [
    """
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <GetAllUsers201812Response xmlns="http://www.blaise.com/security/2018/12">
      <GetAllUsers201812Result xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
        <User201812>
          <AdIdentifier i:nil="true"/>
          <AdSyncEnabled>
            0
          </AdSyncEnabled>
          <Claims i:nil="true" xmlns:a="http://www.blaise.com/security/2016/03"/>
          <Description>
            hi this my description
          </Description>
          <LastActivity i:nil="true"/>
          <LastLogin i:nil="true"/>
          <LastLogout i:nil="true"/>
          <Name>
            {username}
          </Name>
          <Password i:nil="true"/>
          <Permissions xmlns:a="http://www.blaise.com/security/2016/06"/>
          <Preferences i:nil="true" xmlns:a="http://www.blaise.com/security/2016/06"/>
          <RoleId>
            1
          </RoleId>
          <Roles xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays">
            <a:string/>
          </Roles>
          <ServerParks xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays">
            <a:string>
              {serverpark}
            </a:string>
          </ServerParks>
          <UserSkills/>
        </User201812>
      </GetAllUsers201812Result>
    </GetAllUsers201812Response>
  </s:Body>
</s:Envelope>
""".format(
        **mock_users[0]
    )
]


@pytest.mark.parametrize("host_info", host_infos)
def test_get_all_users_api_call(host_info, requests_mock):
    definition = operations["get-all-users"]

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
        text=mock_response_no_users[0],
    )

    get_all_users(**host_info)

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
def test_get_all_users_parse_no_users(host_info, requests_mock):
    definition = operations["get-all-users"]

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
        text=mock_response_no_users[0],
    )

    x = get_all_users(**host_info)

    assert x is not None
    assert len(x) == 2
    assert x[0] == 200
    assert isinstance(x[1], list)
    assert len(x[1]) == 0


@pytest.mark.parametrize("host_info", host_infos)
def test_get_all_users_parse_one_user(host_info, requests_mock):
    definition = operations["get-all-users"]

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
        text=mock_response_one_user[0],
    )

    x = get_all_users(**host_info)

    assert x is not None
    assert len(x) == 2
    assert x[0] == 200
    assert isinstance(x[1], list)
    assert len(x[1]) == 1

    users = x[1]
    assert len(users) == 1
    assert users[0]["name"] == mock_users[0]["username"]
