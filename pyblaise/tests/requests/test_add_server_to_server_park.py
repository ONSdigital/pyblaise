import pytest
import requests
import urllib

from collections import namedtuple

from pyblaise import update_server_park

from pyblaise.operations.definitions import operations

host_infos = [
    {
        "protocol": "http",
        "host": "my-host.com",
        "port": 8000,
        "token": "my-dummy-token",
    },
]

server_park_definition = {
    "audit-trail-mode": "false",
    "delete-data-after-upload": "false",
    "download-surveys-only-if-cases-are-available": "false",
    "is-public": "false",
    "location": r"D:\Blaise5\Surveys",
    "master-address": "blaise-gusty-mgmt:8031",
    "name": "gusty",
    "run-mode": "ThinClient",
    "session-mode": "Local",
    "sync-data-when-connected": "false",
    "sync-surveys-when-connected": "false",
    "website-name": "1",
    "servers": [
        {
            "binding": "http",
            "ip-v4": "127.0.0.1",
            "ip-v6": "notip",
            "hostname": "host-01",
            "port": "8031",
            "roles": ["ADMIN"],
        },
        {
            "binding": "http",
            "ip-v4": "127.0.0.2",
            "ip-v6": "notip",
            "hostname": "host-02",
            "port": "8033",
            "roles": ["SESSION", "RESOURCE"],
        },
        {
            "binding": "http",
            "ip-v4": "127.0.0.3",
            "ip-v6": "notip",
            "hostname": "host-03",
            "port": "0",
            "roles": ["DASHBOARD"],
        },
    ],
}

new_server = {
    "binding": "http",
    "ip-v4": "127.0.0.4",
    "ip-v6": "notip",
    "hostname": "host-04",
    "port": "8031",
    "roles": ["DATA"],
}

mock_response_operation_success = [
    """
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <UpdateServerParkDefinition201906Response xmlns="http://www.blaise.com/deploy/2019/06">
      <UpdateServerParkDefinition201906Result xmlns:a="http://www.blaise.com/deploy/2013/03" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
        <a:Message>Operation success</a:Message>
        <a:Statuscode>0</a:Statuscode>
      </UpdateServerParkDefinition201906Result>
    </UpdateServerParkDefinition201906Response>
  </s:Body>
</s:Envelope>
    """
]


@pytest.mark.parametrize("host_info", host_infos)
def test_add_server_to_server_park_api_call(host_info, requests_mock):
    definition = operations["update-server-park-definition"]

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

    update_server_park(**host_info, server_park_definition=server_park_definition)

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
def test_add_server_to_server_park_definition_operation_success(host_info, requests_mock):
    definition = operations["update-server-park-definition"]

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

    status_code, message = update_server_park(
        **host_info,
        server_park_definition=server_park_definition
    )

    assert status_code == 200
    assert message is not None


@pytest.mark.parametrize("host_info", host_infos)
def test_add_server_to_server_park_definition_new_server_in_request_body(
    host_info, requests_mock
):
    definition = operations["update-server-park-definition"]

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

    # create a new def
    server_park_definition["servers"].append(new_server)

    # send the dict to the function
    status_code, message = update_server_park(
        **host_info,
        server_park_definition=server_park_definition
    )

    assert status_code == 200
    assert message is not None

    # check the new host is in the request body
    # FIXME: would be good to parse the request text here and check there are four servers in the update
    assert "host-04" in requests_mock.last_request.text
