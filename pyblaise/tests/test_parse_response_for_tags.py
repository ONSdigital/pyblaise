import pytest

from pyblaise.soap_utils import parse_response_for_tags


def test_parse_get_all_from_server_park_definition_response():
    d = """
  <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
    <s:Body>
      <GetAllServerParkDefinitions201906Response xmlns="http://www.blaise.com/deploy/2019/06">
        <GetAllServerParkDefinitions201906Result xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
          <ServerParkDefinition>
            <AuditTrailMode>Local</AuditTrailMode>
            <DeleteDataAfterUpload>false</DeleteDataAfterUpload>
            <DownloadSurveysOnlyIfCasesAreAvailable>false</DownloadSurveysOnlyIfCasesAreAvailable>
            <IsPublic>false</IsPublic>
            <LoadBalancer>http://ftf-83a75955:8033</LoadBalancer>
            <Location>D:\Blaise5Surveys\Surveys</Location>
            <MasterAddress>ftf-83a75955:8031</MasterAddress>
            <Name>ftf</Name>
            <RunMode>ThinClient</RunMode>
            <Servers>
              <ServerDefinition201906>
                <Binding>http</Binding>
                <BlaiseVersion i:nil="true" xmlns:a="http://www.blaise.com/common/2019/06"/>
                <ExternalName i:nil="true"/>
                <ExtraInfo i:nil="true" xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>
                <IPAddressV4>10.6.0.2</IPAddressV4>
                <IPAddressV6>fe80::ec30:b026:8934:283b%3</IPAddressV6>
                <Location>D:\Blaise5Surveys\Surveys</Location>
                <LogicalRoot>default</LogicalRoot>
                <MasterHostName i:nil="true"/>
                <Name>ftf-83a75955</Name>
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
                <IPAddressV4>10.6.0.2</IPAddressV4>
                <IPAddressV6>fe80::ec30:b026:8934:283b%3</IPAddressV6>
                <Location>D:\Blaise5Surveys\Surveys</Location>
                <LogicalRoot>default</LogicalRoot>
                <MasterHostName i:nil="true"/>
                <Name>ftf-83a75955</Name>
                <Port>0</Port>
                <Roles xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays">
                  <a:string>WEB</a:string>
                  <a:string>DASHBOARD</a:string>
                </Roles>
                <Status i:nil="true"/>
                <WebsiteName>1</WebsiteName>
              </ServerDefinition201906>
              <ServerDefinition201906>
                <Binding>http</Binding>
                <BlaiseVersion i:nil="true" xmlns:a="http://www.blaise.com/common/2019/06"/>
                <ExternalName i:nil="true"/>
                <ExtraInfo i:nil="true" xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>
                <IPAddressV4>10.6.0.2</IPAddressV4>
                <IPAddressV6>fe80::ec30:b026:8934:283b%3</IPAddressV6>
                <Location>D:\Blaise5Surveys\Surveys</Location>
                <LogicalRoot>default</LogicalRoot>
                <MasterHostName i:nil="true"/>
                <Name>ftf-83a75955</Name>
                <Port>8033</Port>
                <Roles xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays">
                  <a:string>DATAENTRY</a:string>
                  <a:string>DATA</a:string>
                  <a:string>RESOURCE</a:string>
                  <a:string>SESSION</a:string>
                  <a:string>AUDITTRAIL</a:string>
                  <a:string>CATI</a:string>
                </Roles>
                <Status i:nil="true"/>
                <WebsiteName>1</WebsiteName>
              </ServerDefinition201906>
            </Servers>
            <SessionMode>Local</SessionMode>
            <SyncDataWhenConnected>false</SyncDataWhenConnected>
            <SyncSurveysWhenConnected>false</SyncSurveysWhenConnected>
            <WebsiteName>1</WebsiteName>
          </ServerParkDefinition>
        </GetAllServerParkDefinitions201906Result>
      </GetAllServerParkDefinitions201906Response>
    </s:Body>
  </s:Envelope>
  """

    assert (
        parse_response_for_tags(d, ["ServerParkDefinition", "Roles", "SessionMode"])
        is True
    )
