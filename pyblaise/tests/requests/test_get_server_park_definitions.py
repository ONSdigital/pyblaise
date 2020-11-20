import pytest
import requests
import urllib

from collections import namedtuple

from pyblaise import get_server_park

from pyblaise.operations.definitions import operations

host_infos = [
    {
        "protocol": "http",
        "host": "my-host.com",
        "port": 8000,
        "token": "my-dummy-token",
    },
]

mock_response_one_server_park = [
    """
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <GetServerParkDefinition201906Response xmlns="http://www.blaise.com/deploy/2019/06">
      <GetServerParkDefinition201906Result xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
        <AuditTrailMode>Local</AuditTrailMode>
        <DeleteDataAfterUpload>false</DeleteDataAfterUpload>
        <DownloadSurveysOnlyIfCasesAreAvailable>false</DownloadSurveysOnlyIfCasesAreAvailable>
        <IsPublic>false</IsPublic>
        <LoadBalancer i:nil="true"/>
        <Location>D:\Blaise5\Surveys</Location>
        <MasterAddress>blaise-gusty-mgmt:8031</MasterAddress>
        <Name>gusty</Name>
        <RunMode>ThinClient</RunMode>
        <Servers>
          <ServerDefinition201906>
            <Binding>http</Binding>
            <BlaiseVersion i:nil="true" xmlns:a="http://www.blaise.com/common/2019/06"/>
            <ExternalName i:nil="true"/>
            <ExtraInfo i:nil="true" xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>
            <IPAddressV4>10.6.15.207</IPAddressV4>
            <IPAddressV6>fe80::3072:52f2:c72e:8d14%6</IPAddressV6>
            <Location>D:\Blaise5\Surveys</Location>
            <LogicalRoot>default</LogicalRoot>
            <MasterHostName i:nil="true"/>
            <Name>blaise-gusty-mgmt</Name>
            <Port>8031</Port>
            <Roles xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays">
              <a:string>ADMIN</a:string>
            </Roles>
            <Status i:nil="true"/>
            <WebsiteName>1</WebsiteName>
          </ServerDefinition201906>
          <ServerDefinition201906>
            <Binding>http</Binding>
            <BlaiseVersion i:nil="true" xmlns:a="http://www.blaise.com/common/2019/06"/>
            <ExternalName i:nil="true"/>
            <ExtraInfo i:nil="true" xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>
            <IPAddressV4>10.6.15.207</IPAddressV4>
            <IPAddressV6>fe80::3072:52f2:c72e:8d14%6</IPAddressV6>
            <Location>D:\Blaise5\Surveys</Location>
            <LogicalRoot>default</LogicalRoot>
            <MasterHostName i:nil="true"/>
            <Name>blaise-gusty-mgmt</Name>
            <Port>8033</Port>
            <Roles xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays">
              <a:string>RESOURCE</a:string>
              <a:string>SESSION</a:string>
            </Roles>
            <Status i:nil="true"/>
            <WebsiteName>1</WebsiteName>
          </ServerDefinition201906>
          <ServerDefinition201906>
            <Binding>http</Binding>
            <BlaiseVersion i:nil="true" xmlns:a="http://www.blaise.com/common/2019/06"/>
            <ExternalName i:nil="true"/>
            <ExtraInfo i:nil="true" xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>
            <IPAddressV4>10.6.15.207</IPAddressV4>
            <IPAddressV6>fe80::3072:52f2:c72e:8d14%6</IPAddressV6>
            <Location>D:\Blaise5\Surveys</Location>
            <LogicalRoot>default</LogicalRoot>
            <MasterHostName i:nil="true"/>
            <Name>blaise-gusty-mgmt</Name>
            <Port>0</Port>
            <Roles xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays">
              <a:string>DASHBOARD</a:string>
            </Roles>
            <Status i:nil="true"/>
            <WebsiteName>1</WebsiteName>
          </ServerDefinition201906>
        </Servers>
        <SessionMode>Local</SessionMode>
        <SyncDataWhenConnected>false</SyncDataWhenConnected>
        <SyncSurveysWhenConnected>false</SyncSurveysWhenConnected>
        <WebsiteName>1</WebsiteName>
      </GetServerParkDefinition201906Result>
    </GetServerParkDefinition201906Response>
  </s:Body>
</s:Envelope>
    """
]


@pytest.mark.parametrize("host_info", host_infos)
def test_get_server_park_definition_api_call(host_info, requests_mock):
    definition = operations["get-server-park-definition"]

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
        text=mock_response_one_server_park[0],
    )

    get_server_park(**host_info, server_park_name="gusty")

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
def test_get_server_park_definition_parse_definition_returns_name(
    host_info, requests_mock
):
    definition = operations["get-server-park-definition"]

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
        text=mock_response_one_server_park[0],
    )

    status_code, server_park = get_server_park(**host_info, server_park_name="gusty")

    assert status_code == 200
    assert isinstance(server_park, dict)

    assert "name" in server_park
    assert server_park["name"] == "gusty"


@pytest.mark.parametrize("host_info", host_infos)
def test_get_server_park_definition_parse_definition_returns_server_park_name(
    host_info, requests_mock
):
    definition = operations["get-server-park-definition"]

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
        text=mock_response_one_server_park[0],
    )

    status_code, server_park = get_server_park(**host_info, server_park_name="gusty")

    assert status_code == 200
    assert isinstance(server_park, dict)

    assert "name" in server_park


@pytest.mark.parametrize("host_info", host_infos)
def test_get_server_park_definition_parse_definition_returns_data(
    host_info, requests_mock
):
    definition = operations["get-server-park-definition"]

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
        text=mock_response_one_server_park[0],
    )

    status_code, server_park = get_server_park(**host_info, server_park_name="gusty")

    assert status_code == 200
    assert isinstance(server_park, dict)

    assert "audit-trail-mode" in server_park
    assert "delete-data-after-upload" in server_park
    assert "download-surveys-only-if-cases-are-available" in server_park
    assert "is-public" in server_park
    assert "location" in server_park
    assert "master-address" in server_park
    assert "name" in server_park
    assert "run-mode" in server_park
    assert "session-mode" in server_park
    assert "sync-data-when-connected" in server_park
    assert "sync-surveys-when-connected" in server_park
    assert "website-name" in server_park

    assert server_park["audit-trail-mode"] == "Local"
    assert server_park["delete-data-after-upload"] == "false"
    assert server_park["download-surveys-only-if-cases-are-available"] == "false"
    assert server_park["is-public"] == "false"
    assert server_park["location"] == "D:\Blaise5\Surveys"
    assert server_park["master-address"] == "blaise-gusty-mgmt:8031"
    assert server_park["name"] == "gusty"
    assert server_park["run-mode"] == "ThinClient"
    assert server_park["session-mode"] == "Local"
    assert server_park["sync-data-when-connected"] == "false"
    assert server_park["sync-surveys-when-connected"] == "false"
    assert server_park["website-name"] == "1"


@pytest.mark.parametrize("host_info", host_infos)
def test_get_server_park_definition_parse_definition_returns_data_for_three_servers(
    host_info, requests_mock
):
    definition = operations["get-server-park-definition"]

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
        text=mock_response_one_server_park[0],
    )

    status_code, server_park = get_server_park(**host_info, server_park_name="gusty")

    assert status_code == 200
    assert isinstance(server_park, dict)

    assert "servers" in server_park
    assert len(server_park["servers"]) == 3


@pytest.mark.parametrize("host_info", host_infos)
def test_get_server_park_definition_parse_definition_returns_data_for_first_server(
    host_info, requests_mock
):
    definition = operations["get-server-park-definition"]

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
        text=mock_response_one_server_park[0],
    )

    status_code, server_park = get_server_park(**host_info, server_park_name="gusty")

    assert status_code == 200
    assert isinstance(server_park, dict)

    assert "servers" in server_park
    assert len(server_park["servers"]) == 3

    server = server_park["servers"][0]

    assert "binding" in server
    assert "ip-v4" in server
    assert "ip-v6" in server
    assert "hostname" in server
    assert "port" in server
    assert "roles" in server
    assert isinstance(server["roles"], list)

    assert server["binding"] == "http"
    assert server["ip-v4"] == "10.6.15.207"
    assert server["ip-v6"] == "fe80::3072:52f2:c72e:8d14%6"
    assert server["hostname"] == "blaise-gusty-mgmt"
    assert server["port"] == "8031"
    assert "ADMIN" in server["roles"]


@pytest.mark.parametrize("host_info", host_infos)
def test_get_server_park_definition_parse_definition_returns_data_for_second_server(
    host_info, requests_mock
):
    definition = operations["get-server-park-definition"]

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
        text=mock_response_one_server_park[0],
    )

    status_code, server_park = get_server_park(**host_info, server_park_name="gusty")

    assert status_code == 200
    assert isinstance(server_park, dict)

    assert "servers" in server_park
    assert len(server_park["servers"]) == 3

    server = server_park["servers"][1]

    assert "binding" in server
    assert "ip-v4" in server
    assert "ip-v6" in server
    assert "hostname" in server
    assert "port" in server
    assert "roles" in server
    assert isinstance(server["roles"], list)

    assert server["binding"] == "http"
    assert server["ip-v4"] == "10.6.15.207"
    assert server["ip-v6"] == "fe80::3072:52f2:c72e:8d14%6"
    assert server["hostname"] == "blaise-gusty-mgmt"
    assert server["port"] == "8033"
    assert "RESOURCE" in server["roles"]
    assert "SESSION" in server["roles"]


@pytest.mark.parametrize("host_info", host_infos)
def test_get_server_park_definition_parse_definition_returns_data_for_third_server(
    host_info, requests_mock
):
    definition = operations["get-server-park-definition"]

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
        text=mock_response_one_server_park[0],
    )

    status_code, server_park = get_server_park(**host_info, server_park_name="gusty")

    assert status_code == 200
    assert isinstance(server_park, dict)

    assert "servers" in server_park
    assert len(server_park["servers"]) == 3

    server = server_park["servers"][2]

    assert "binding" in server
    assert "ip-v4" in server
    assert "ip-v6" in server
    assert "hostname" in server
    assert "port" in server
    assert "roles" in server
    assert isinstance(server["roles"], list)

    assert server["binding"] == "http"
    assert server["ip-v4"] == "10.6.15.207"
    assert server["ip-v6"] == "fe80::3072:52f2:c72e:8d14%6"
    assert server["hostname"] == "blaise-gusty-mgmt"
    assert server["port"] == "0"
    assert "DASHBOARD" in server["roles"]
