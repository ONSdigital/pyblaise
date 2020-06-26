# pyblaise
Python interface to the blaise SOAP API
=======
# Blaise SOAP Interface

Simple wrapper for the [Blaise](https://blaise.com/products/blaise-5) SOAP interface.

*NB: This is mostly hacked together with direct HTTP requests.*

SOAP requests are an XML payload POSTed to an endpoint.

The `SOAPAction` header in the HTTP Request headers needs to match the payload. You will get a 500 error on mismatch.


## Blaise Server Manager Initial Connection

+ `SOAPAction: "http://www.blaise.com/security/2016/06/ISecurityTokenService/RequestToken"` request an OAuth token
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <RequestTokenResponse xmlns="http://www.blaise.com/security/2016/06">
      <RequestTokenResult xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
        <AccessToken>xxx</AccessToken>
        <RefreshToken>xxx</RefreshToken>
      </RequestTokenResult>
    </RequestTokenResponse>
  </s:Body>
</s:Envelope>
```

+ `SOAPAction: "http://www.blaise.com/deploy/2013/03/IDeployService/IsInteractiveConnectionAllowed"` ?
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <IsInteractiveConnectionAllowedResponse xmlns="http://www.blaise.com/deploy/2013/03">
      <IsInteractiveConnectionAllowedResult>true</IsInteractiveConnectionAllowedResult>
    </IsInteractiveConnectionAllowedResponse>
  </s:Body>
</s:Envelope>
```

+ `SOAPAction: "http://www.blaise.com/deploy/2014/09/IDeployService/GetVersionResponse"` ?
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <GetVersionResponseResponse xmlns="http://www.blaise.com/security/2017/11">
      <GetVersionResponseResult xmlns:a="http://www.blaise.com/dataentry/2013/09"
                                xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
        <a:CurrentVersion>
          <a:Month>6</a:Month>
          <a:Year>2019</a:Year>
        </a:CurrentVersion>
        <a:MinimumVersion>
          <a:Month>3</a:Month>
          <a:Year>2013</a:Year>
        </a:MinimumVersion>
      </GetVersionResponseResult>
    </GetVersionResponseResponse>
  </s:Body>
</s:Envelope>
```

+ `SOAPAction: "http://www.blaise.com/security/2018/12/ISecurityManagementService/GetSkills"` ?
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <GetSkillsResponse xmlns="http://www.blaise.com/security/2018/12">
      <GetSkillsResult xmlns:i="http://www.w3.org/2001/XMLSchema-instance"/>
    </GetSkillsResponse>
  </s:Body>
</s:Envelope>
```

+ `SOAPAction: "http://www.blaise.com/security/2018/12/ISecurityManagementService/GetAllUsers201812"` registered users
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <GetAllUsers201812Response xmlns="http://www.blaise.com/security/2018/12">
      <GetAllUsers201812Result xmlns:i="http://www.w3.org/2001/XMLSchema-instance"/>
    </GetAllUsers201812Response>
  </s:Body>
</s:Envelope>
```

+ `SOAPAction: "http://www.blaise.com/security/2016/06/ISecurityManagementService/GetRoles"` server-park roles
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <GetRolesResponse xmlns="http://www.blaise.com/security/2016/06">
      <GetRolesResult xmlns:i="http://www.w3.org/2001/XMLSchema-instance"/>
    </GetRolesResponse>
  </s:Body>
</s:Envelope>
```

+ `SOAPAction: "http://www.blaise.com/deploy/2019/06/IDeployService/GetAllServerParkDefinitions201906"` detailed server-park information
```
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
```

+ `SOAPAction: "http://www.blaise.com/deploy/2019/06/IDeployService/GetServerVersion"` server runtime version
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <GetServerVersionResponse xmlns="http://www.blaise.com/deploy/2019/06">
      <GetServerVersionResult xmlns:a="http://www.blaise.com/common/2019/06" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
        <a:Build>2082</a:Build>
        <a:Major>5</a:Major>
        <a:Minor>6</a:Minor>
        <a:Release>9</a:Release>
      </GetServerVersionResult>
    </GetServerVersionResponse>
  </s:Body>
</s:Envelope>
```
+ `SOAPAction: "http://www.blaise.com/deploy/2013/09/IDeployService/VerifyPorts"` ? (not implemented)
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <VerifyPortsResponse xmlns="http://www.blaise.com/deploy/2013/09">
      <VerifyPortsResult/>
    </VerifyPortsResponse>
  </s:Body>
</s:Envelope>
```

+ `SOAPAction: "http://www.blaise.com/deploy/2013/03/IDeployService/GetListOfInstruments"` ? (not implemented)
    + each `InstrumentMeta` block relates to an instrument on the ServerPark
    + empty example:
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <GetListOfInstrumentsResponse xmlns="http://www.blaise.com/deploy/2013/03">
      <GetListOfInstrumentsResult xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
      </GetListOfInstrumentsResult>
    </GetListOfInstrumentsResponse>
  </s:Body>
</s:Envelope>
```
    + populated example:
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <GetListOfInstrumentsResponse xmlns="http://www.blaise.com/deploy/2013/03">
      <GetListOfInstrumentsResult xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
        <InstrumentMeta>
          <DownloadType i:nil="true"/>
          <InstallDate>2020-06-05T19:55:14.1737216+01:00</InstallDate>
          <InstrumentId>8a2d121e-6dba-4bf5-a6bf-d1b0e6c36160</InstrumentId>
          <InstrumentName>OPN2004A</InstrumentName>
          <ServerPark>ftf</ServerPark>
          <Status>Failed</Status>
        </InstrumentMeta>
        <InstrumentMeta>
          <DownloadType i:nil="true"/>
          <InstallDate>2020-06-08T12:19:54.0317922+01:00</InstallDate>
          <InstrumentId>8a2d121e-6dba-4bf5-a6bf-d1b0e6c36161</InstrumentId>
          <InstrumentName>OPN2004A-test-upload</InstrumentName>
          <ServerPark>ftf</ServerPark>
          <Status>Active</Status>
        </InstrumentMeta>
        <InstrumentMeta>
          <DownloadType i:nil="true"/>
          <InstallDate>2020-06-08T12:54:09.422547+01:00</InstallDate>
          <InstrumentId>8a2d121e-6dba-4bf5-a6bf-d1b0e6c36162</InstrumentId>
          <InstrumentName>OPN2004A-test-upload-2</InstrumentName>
          <ServerPark>ftf</ServerPark>
          <Status>Active</Status>
        </InstrumentMeta>
        <InstrumentMeta>
          <DownloadType i:nil="true"/>
          <InstallDate>2020-06-08T12:58:01.4846821+01:00</InstallDate>
          <InstrumentId>12345678-1234-5678-1234-567812345678</InstrumentId>
          <InstrumentName>OPN2004A-test-upload-3</InstrumentName>
          <ServerPark>ftf</ServerPark>
          <Status>Active</Status>
        </InstrumentMeta>
      </GetListOfInstrumentsResult>
    </GetListOfInstrumentsResponse>
  </s:Body>
</s:Envelope>
```

+ `SOAPAction: "http://www.blaise.com/deploy/2013/12/IDeployService/GetLogicalRoots"` ? (not implemented)
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <GetLogicalRootsResponse xmlns="http://www.blaise.com/deploy/2013/12">
      <GetLogicalRootsResult xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
        <Root>
          <Binding>http</Binding>
          <Location>D:\Blaise5Surveys\Surveys</Location>
          <Name>default</Name>
          <Port>80</Port>
          <WebsiteId>1</WebsiteId>
          <WebsiteName>Default Web Site</WebsiteName>
        </Root>
      </GetLogicalRootsResult>
    </GetLogicalRootsResponse>
  </s:Body>
</s:Envelope>
```

+ `SOAPAction: "http://www.blaise.com/deploy/2017/11/IDeployService/GetRemoteLogicalRoots201711"` ? (not implemented)
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <GetRemoteLogicalRoots201711Response xmlns="http://www.blaise.com/deploy/2017/11">
      <GetRemoteLogicalRoots201711Result xmlns:a="http://www.blaise.com/deploy/2013/12" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
        <a:Root>
          <a:Binding>http</a:Binding>
          <a:Location>D:\Blaise5Surveys\Surveys</a:Location>
          <a:Name>default</a:Name>
          <a:Port>80</a:Port>
          <a:WebsiteId>1</a:WebsiteId>
          <a:WebsiteName>Default Web Site</a:WebsiteName>
        </a:Root>
      </GetRemoteLogicalRoots201711Result>
    </GetRemoteLogicalRoots201711Response>
  </s:Body>
</s:Envelope>
```
+ `SOAPAction: "http://www.blaise.com/configuration/2019/06/IConfigurationService/GetServerParkConfigurations201906"` get info for particular server park
```

<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><GetServerParkConfigurations201906Response xmlns="http://www.blaise.com/configuration/2019/06"><GetServerParkConfigurations201906Result xmlns:i="http://www.w3.org/2001/XMLSchema-instance"/></GetServerParkConfigurations201906Response></s:Body></s:Envelope>
```
+ `SOAPAction: "http://www.blaise.com/configuration/2019/06/IConfigurationService/GetAllConfigurations201906"` ?
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <GetAllConfigurations201906Response xmlns="http://www.blaise.com/configuration/2019/06">
      <GetAllConfigurations201906Result xmlns:i="http://www.w3.org/2001/XMLSchema-instance"/>
    </GetAllConfigurations201906Response>
  </s:Body>
</s:Envelope>
```

## OAuth Token Invalidation

Sometimes will appear as a `500 Internal Server Error` with the content:
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <s:Fault>
      <faultcode>s:access_token_invalid</faultcode>
      <faultstring xml:lang="en-US">The provided access token is invalid.</faultstring>
    </s:Fault>
  </s:Body>
</s:Envelope>
```

## OAuth Token Refresh

+ `SOAPAction: "http://www.blaise.com/security/2016/06/ISecurityTokenService/RefreshToken"` post the refresh token to obtain new access token
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <RefreshTokenResponse xmlns="http://www.blaise.com/security/2016/06">
      <RefreshTokenResult xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
        <AccessToken>xxx</AccessToken>
        <RefreshToken>xxx</RefreshToken>
      </RefreshTokenResult>
    </RefreshTokenResponse>
  </s:Body>
</s:Envelope>
```


## Blaise Server Manager Survey Upload

Survey upload requires that the archive (`.bpkg` or `.zip`) contiains a `.manifest` file.
This file should list the files in the archive, ID of the survey and title of the survey.
The ID field should be a UUID which matches an expected pattern (FIXME: fill in this pattern, sorry reader...).
Valid UUID strings can be created with the python library UUID as:
```python
from uuid import uuid4

id = str(uuid4())
print(id)
```

NB: the survey file contents must be the body of the POST request, do not use a multipart file encoding.

+ `SOAPAction: "http://www.blaise.com/configuration/2013/03/IConfigurationService/GetInstrumentConfiguration"` (no idea where this `id` comes from)
    + request:
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Header>
    <Authorization xmlns="http://schemas.blaise.com/2016/06/authheader">Bearer xxx</Authorization>
  </s:Header>
  <s:Body>
    <GetInstrumentConfiguration xmlns="http://www.blaise.com/configuration/2013/03">
      <id>8a2d121e-6dba-4bf5-a6bf-d1b0e6c36160</id>
    </GetInstrumentConfiguration>
  </s:Body>
</s:Envelope>
```
    + response:
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <GetInstrumentConfigurationResponse xmlns="http://www.blaise.com/configuration/2013/03">
      <GetInstrumentConfigurationResult i:nil="true" xmlns:a="http://www.blaise.com/configuration/2013/06" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"/>
    </GetInstrumentConfigurationResponse>
  </s:Body>
</s:Envelope>
```

+ `SOAPAction: "http://www.blaise.com/configuration/2017/11/IConfigurationService/GetAllConfigurations201711"`
    + request:
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Header>
    <Authorization xmlns="http://schemas.blaise.com/2016/06/authheader">Bearer xxx</Authorization>
  </s:Header>
  <s:Body>
    <GetAllConfigurations201711 xmlns="http://www.blaise.com/configuration/2017/11"/>
  </s:Body>
</s:Envelope>
```
    + response:
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <GetAllConfigurations201711Response xmlns="http://www.blaise.com/configuration/2017/11">
      <GetAllConfigurations201711Result xmlns:i="http://www.w3.org/2001/XMLSchema-instance"/>
    </GetAllConfigurations201711Response>
  </s:Body>
</s:Envelope>
```

+ `POST /Blaise/Administer/Services/REST/ftf/OPN2004A/8a2d121e-6dba-4bf5-a6bf-d1b0e6c36160/uploadpackage`
    + request: `Content-Type: application\r\nContent-Length: 7664\r\nAuthorization: Bearer xxx\r\n`
    + response: `<int xmlns="http://schemas.microsoft.com/2003/10/Serialization/">0</int>`

+ `SOAPAction: "http://www.blaise.com/configuration/2019/06/IConfigurationService/GetInstrumentConfiguration201906"`
    + request:
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Header>
    <Authorization xmlns="http://schemas.blaise.com/2016/06/authheader">Bearer xxx</Authorization>
  </s:Header>
  <s:Body>
    <GetInstrumentConfiguration201906 xmlns="http://www.blaise.com/configuration/2019/06">
      <id>8a2d121e-6dba-4bf5-a6bf-d1b0e6c36160</id>
    </GetInstrumentConfiguration201906>
  </s:Body>
</s:Envelope>
```

    + response:
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <GetInstrumentConfiguration201906Response xmlns="http://www.blaise.com/configuration/2019/06">
      <GetInstrumentConfiguration201906Result xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
        <ActionsSetupFileName i:nil="true"/>
        <AllowDownloadOverMeteredConnection>false</AllowDownloadOverMeteredConnection>
        <AuditTrailFileName i:nil="true"/>
        <BlaiseVersion i:nil="true"/>
        <CatiRole i:nil="true"/>
        <CatiSpecificationFileName i:nil="true"/>
        <DataChecksum i:nil="true"/>
        <DataFileName>INSTALLATION IN PROGRESS</DataFileName>
        <Dependencies xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>
        <DownloadInterceptorSetupFileName i:nil="true"/>
        <InitialAppCariSetting i:nil="true"/>
        <InitialDataEntrySettingsName>INSTALLATION IN PROGRESS</InitialDataEntrySettingsName>
        <InitialLayoutSetGroupName>INSTALLATION IN PROGRESS</InitialLayoutSetGroupName>
        <InitialLayoutSetName i:nil="true"/>
        <InstallDate>2020-06-05T15:34:09.2039904+01:00</InstallDate>
        <InstrumentId>8a2d121e-6dba-4bf5-a6bf-d1b0e6c36160</InstrumentId>
        <InstrumentName>OPN2004A</InstrumentName>
        <LauncherId i:nil="true"/>
        <MainInstrumentId i:nil="true"/>
        <MetaFileName>INSTALLATION IN PROGRESS</MetaFileName>
        <Modes xmlns:a="http://www.blaise.com/configuration/2015/11"/>
        <PackageFileName i:nil="true"/>
        <ResourceFileName>INSTALLATION IN PROGRESS</ResourceFileName>
        <ServerParkName>ftf</ServerParkName>
        <SessionFileName i:nil="true"/>
        <SetupFileName i:nil="true"/>
        <SilverlightApplicationFileName>INSTALLATION IN PROGRESS</SilverlightApplicationFileName>
        <StartCondition i:nil="true"/>
        <StartPageFileName>INSTALLATION IN PROGRESS</StartPageFileName>
        <Status>Installing</Status>
        <StatusInfo i:nil="true"/>
        <SurveyRole i:nil="true"/>
        <SurveyRoot>opn2004a</SurveyRoot>
        <ToWhomField i:nil="true"/><Version>1</Version>
        <WaveName i:nil="true"/>
        <WebDataEntryClient i:nil="true"/>
        <WriteInterceptorSetupFileName i:nil="true"/>
      </GetInstrumentConfiguration201906Result>
    </GetInstrumentConfiguration201906Response>
  </s:Body>
</s:Envelope>
```

+ `SOAPAction: "http://www.blaise.com/configuration/2019/06/IConfigurationService/GetInstrumentConfiguration201906"` (repeated)
    + request: `<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Header><Authorization xmlns="http://schemas.blaise.com/2016/06/authheader">Bearer xxx</Authorization></s:Header><s:Body><GetInstrumentConfiguration201906 xmlns="http://www.blaise.com/configuration/2019/06"><id>8a2d121e-6dba-4bf5-a6bf-d1b0e6c36160</id></GetInstrumentConfiguration201906></s:Body></s:Envelope>`
    + response: `<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><GetInstrumentConfiguration201906Response xmlns="http://www.blaise.com/configuration/2019/06"><GetInstrumentConfiguration201906Result xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><ActionsSetupFileName/><AllowDownloadOverMeteredConnection>false</AllowDownloadOverMeteredConnection><AuditTrailFileName i:nil="true"/><BlaiseVersion>5.6.5.2055</BlaiseVersion><CatiRole>Main</CatiRole><CatiSpecificationFileName>D:\Blaise5Surveys\Surveys\opn2004a\OPN2004A.btrx</CatiSpecificationFileName><DataChecksum/><DataFileName>D:\Blaise5Surveys\Surveys\opn2004a\OPN2004A.bdix</DataFileName><Dependencies xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"><a:string>8a2d121e-6dba-4bf5-a6bf-d1b0e6c36160</a:string><a:string>57ec5f87-42f4-4763-b433-9c5241057fa3</a:string></Dependencies><DownloadInterceptorSetupFileName/><InitialAppCariSetting/><InitialDataEntrySettingsName>StrictInterviewing</InitialDataEntrySettingsName><InitialLayoutSetGroupName>CATI</InitialLayoutSetGroupName><InitialLayoutSetName/><InstallDate>2020-06-05T15:34:09.2039904+01:00</InstallDate><InstrumentId>8a2d121e-6dba-4bf5-a6bf-d1b0e6c36160</InstrumentId><InstrumentName>OPN2004A</InstrumentName><LauncherId i:nil="true"/><MainInstrumentId i:nil="true"/><MetaFileName>D:\Blaise5Surveys\Surveys\opn2004a\OPN2004A.bmix</MetaFileName><Modes xmlns:a="http://www.blaise.com/configuration/2015/11"><a:Mode><a:DataChecksum>749292572.1575518578.2643763670</a:DataChecksum><a:Name>CAWI</a:Name></a:Mode><a:Mode><a:DataChecksum>3249934867.1478189997.440957705</a:DataChecksum><a:Name>CATI</a:Name></a:Mode></Modes><PackageFileName i:nil="true"/><ResourceFileName>D:\Blaise5Surveys\Surveys\opn2004a\SocialSurveyTemplates.blrd</ResourceFileName><ServerParkName>ftf</ServerParkName><SessionFileName i:nil="true"/><SetupFileName/><SilverlightApplicationFileName i:nil="true"/><StartCondition i:nil="true"/><StartPageFileName>D:\Blaise5Surveys\Surveys\opn2004a\default.aspx</StartPageFileName><Status>Active</Status><StatusInfo/><SurveyRole>Survey</SurveyRole><SurveyRoot>opn2004a</SurveyRoot><ToWhomField i:nil="true"/><Version>1</Version><WaveName i:nil="true"/><WebDataEntryClient>MvcDebug</WebDataEntryClient><WriteInterceptorSetupFileName/></GetInstrumentConfiguration201906Result></GetInstrumentConfiguration201906Response></s:Body></s:Envelope>`

## Blaise Server Manager Survey Remove

+ `SOAPAction: "http://www.blaise.com/deploy/2013/03/IDeployService/RemoveInstrument"`
    + request: `<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Header><Authorization xmlns="http://schemas.blaise.com/2016/06/authheader">Bearer xxx</Authorization></s:Header><s:Body><RemoveInstrument xmlns="http://www.blaise.com/deploy/2013/03"><instrument xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><DownloadType i:nil="true"/><InstallDate>0001-01-01T00:00:00</InstallDate><InstrumentId>8a2d121e-6dba-4bf5-a6bf-d1b0e6c36160</InstrumentId><InstrumentName>OPN2004A</InstrumentName><ServerPark>ftf</ServerPark><Status i:nil="true"/></instrument></RemoveInstrument></s:Body></s:Envelope>`
    + response: `<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><RemoveInstrumentResponse xmlns="http://www.blaise.com/deploy/2013/03"><RemoveInstrumentResult xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><Message>Operation success</Message><Statuscode>0</Statuscode></RemoveInstrumentResult></RemoveInstrumentResponse></s:Body></s:Envelope>`

+ `SOAPAction: "http://www.blaise.com/deploy/2013/03/IDeployService/GetListOfInstruments"`
    + request: `<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Header><Authorization xmlns="http://schemas.blaise.com/2016/06/authheader">Bearer xxx</Authorization></s:Header><s:Body><GetListOfInstruments xmlns="http://www.blaise.com/deploy/2013/03"/></s:Body></s:Envelope>`
    + response: `<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><GetListOfInstrumentsResponse xmlns="http://www.blaise.com/deploy/2013/03"><GetListOfInstrumentsResult xmlns:i="http://www.w3.org/2001/XMLSchema-instance"/></GetListOfInstrumentsResponse></s:Body></s:Envelope>`

## Blaise Server Manager Update Serverpark Definition

+ `SOAPAction: "http://www.blaise.com/deploy/2019/06/IDeployService/UpdateServerParkDefinition201906"`
    + request: `<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Header><Authorization xmlns="http://schemas.blaise.com/2016/06/authheader">Bearer xxx</Authorization></s:Header><s:Body><UpdateServerParkDefinition201906 xmlns="http://www.blaise.com/deploy/2019/06"><definitionToUpdate xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><AuditTrailMode>Local</AuditTrailMode><DeleteDataAfterUpload>false</DeleteDataAfterUpload><DownloadSurveysOnlyIfCasesAreAvailable>false</DownloadSurveysOnlyIfCasesAreAvailable><IsPublic>false</IsPublic><LoadBalancer>http://ftf-83a75955:8033</LoadBalancer><Location>D:\Blaise5Surveys\Surveys</Location><MasterAddress>ftf-83a75955:8031</MasterAddress><Name>ftf</Name><RunMode>ThinClient</RunMode><Servers><ServerDefinition201906><Binding>http</Binding><BlaiseVersion i:nil="true" xmlns:a="http://www.blaise.com/common/2019/06"/><ExternalName i:nil="true"/><ExtraInfo i:nil="true" xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><IPAddressV4>10.6.0.2</IPAddressV4><IPAddressV6>fe80::ec30:b026:8934:283b%3</IPAddressV6><Location>D:\Blaise5Surveys\Surveys</Location><LogicalRoot>default</LogicalRoot><MasterHostName i:nil="true"/><Name>ftf-83a75955</Name><Port>8031</Port><Roles xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"><a:string>ADMIN</a:string></Roles><Status>Unreachable</Status><WebsiteName>1</WebsiteName></ServerDefinition201906><ServerDefinition201906><Binding>http</Binding><BlaiseVersion i:nil="true" xmlns:a="http://www.blaise.com/common/2019/06"/><ExternalName i:nil="true"/><ExtraInfo i:nil="true" xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><IPAddressV4>10.6.0.2</IPAddressV4><IPAddressV6>fe80::ec30:b026:8934:283b%3</IPAddressV6><Location>D:\Blaise5Surveys\Surveys</Location><LogicalRoot>default</LogicalRoot><MasterHostName i:nil="true"/><Name>ftf-83a75955</Name><Port>0</Port><Roles xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"><a:string>WEB</a:string><a:string>DASHBOARD</a:string></Roles><Status>Unreachable</Status><WebsiteName>1</WebsiteName></ServerDefinition201906><ServerDefinition201906><Binding>http</Binding><BlaiseVersion i:nil="true" xmlns:a="http://www.blaise.com/common/2019/06"/><ExternalName i:nil="true"/><ExtraInfo i:nil="true" xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><IPAddressV4>10.6.0.2</IPAddressV4><IPAddressV6>fe80::ec30:b026:8934:283b%3</IPAddressV6><Location>D:\Blaise5Surveys\Surveys</Location><LogicalRoot>default</LogicalRoot><MasterHostName i:nil="true"/><Name>ftf-83a75955</Name><Port>8033</Port><Roles xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"><a:string>DATAENTRY</a:string><a:string>DATA</a:string><a:string>RESOURCE</a:string><a:string>SESSION</a:string><a:string>AUDITTRAIL</a:string><a:string>CATI</a:string></Roles><Status>Unreachable</Status><WebsiteName>1</WebsiteName></ServerDefinition201906></Servers><SessionMode>Server</SessionMode><SyncDataWhenConnected>false</SyncDataWhenConnected><SyncSurveysWhenConnected>false</SyncSurveysWhenConnected><WebsiteName>1</WebsiteName></definitionToUpdate></UpdateServerParkDefinition201906></s:Body></s:Envelope>`
    + response: `<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><UpdateServerParkDefinition201906Response xmlns="http://www.blaise.com/deploy/2019/06"><UpdateServerParkDefinition201906Result xmlns:a="http://www.blaise.com/deploy/2013/03" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><a:Message>Operation success</a:Message><a:Statuscode>0</a:Statuscode></UpdateServerParkDefinition201906Result></UpdateServerParkDefinition201906Response></s:Body></s:Envelope>`


## Blaise Role Setup

Create a new role with a set of permissions.
The server will respond with the `CreateRoleResult` token containing the `ID` of the new role.

+ `SOAPAction: "http://www.blaise.com/security/2016/06/ISecurityManagementService/GetRoles"`
    + request:
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Header>
    <Authorization xmlns="http://schemas.blaise.com/2016/06/authheader">Bearer xxx</Authorization>
  </s:Header>
  <s:Body>
    <GetRoles xmlns="http://www.blaise.com/security/2016/06"/>
  </s:Body>
</s:Envelope>
```
    + response:
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <GetRolesResponse xmlns="http://www.blaise.com/security/2016/06">
      <GetRolesResult xmlns:i="http://www.w3.org/2001/XMLSchema-instance"/>
    </GetRolesResponse>
  </s:Body>
</s:Envelope>
```

+ `SOAPAction: "http://www.blaise.com/security/2016/06/ISecurityManagementService/CreateRole"`
    + request:
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Header>
    <Authorization xmlns="http://schemas.blaise.com/2016/06/authheader">Bearer xxx</Authorization>
  </s:Header>
  <s:Body>
    <CreateRole xmlns="http://www.blaise.com/security/2016/06">
      <role xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
        <Description>This is my funky new role</Description>
        <Id>0</Id>
        <Name>ROle Funky</Name>
        <Permissions>
          <ActionPermission><Action>user.createuser</Action><Permission>1</Permission></ActionPermission>
          <ActionPermission><Action>user.updateuser</Action><Permission>1</Permission></ActionPermission>
          <ActionPermission><Action>user.removeuser</Action><Permission>1</Permission></ActionPermission>
          <ActionPermission><Action>CATI</Action><Permission>1</Permission></ActionPermission>
          <ActionPermission><Action>CATI.setcatispecification</Action><Permission>1</Permission></ActionPermission>
          <ActionPermission><Action>CATI.setgeneralparameters</Action><Permission>1</Permission></ActionPermission>
          <ActionPermission><Action>CATI.setgeneralparameters.setsurveydescription</Action><Permission>1</Permission></ActionPermission>
          <ActionPermission><Action>CATI.setappointmentparameters</Action><Permission>1</Permission></ActionPermission>
          <ActionPermission><Action>CATI.setappointmentparameters.setappointmentbuffer</Action><Permission>1</Permission></ActionPermission>
          <ActionPermission><Action>CATI.setappointmentparameters.setkeeptimeofexpiredappointment</Action><Permission>1</Permission></ActionPermission>
          <ActionPermission><Action>CATI.setappointmentparameters.settreatexpiredappointmentasmedium</Action><Permission>1</Permission></ActionPermission>
          <ActionPermission><Action>CATI.setdaybatchparameters</Action><Permission>1</Permission></ActionPermission>
          <ActionPermission><Action>CATI.setdaybatchparameters.setdaybatchsize</Action><Permission>1</Permission></ActionPermission>
          <ActionPermission><Action>CATI.setdaybatchparameters.setmaxnumberofcalls</Action><Permission>1</Permission></ActionPermission>
        </Permissions>
      </role>
    </CreateRole>
  </s:Body>
</s:Envelope>
```
    + response:
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <CreateRoleResponse xmlns="http://www.blaise.com/security/2016/06">
      <CreateRoleResult>ID-of-new-role</CreateRoleResult>
    </CreateRoleResponse>
  </s:Body>
</s:Envelope>
```

  + response to `get-roles` (not following the above request):
```xml
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <GetRolesResponse xmlns="http://www.blaise.com/security/2016/06">
      <GetRolesResult xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
        <Role>
          <Description>none</Description>
          <Id>2</Id>
          <Name>test-role-001</Name>
          <Permissions>
            <ActionPermission>
              <Action>user.createuser</Action>
              <Permission>1</Permission>
            </ActionPermission>
            <ActionPermission>
              <Action>user.updateuser</Action>
              <Permission>1</Permission>
            </ActionPermission>
            <ActionPermission>
              <Action>user.removeuser</Action>
              <Permission>1</Permission>
            </ActionPermission>
            <ActionPermission>
              <Action>CATI</Action>
              <Permission>1</Permission>
            </ActionPermission>
            <ActionPermission>
              <Action>CATI.setcatispecification</Action>
              <Permission>1</Permission>
            </ActionPermission>
            <ActionPermission>
              <Action>CATI.setgeneralparameters</Action>
              <Permission>1</Permission>
            </ActionPermission>
            <ActionPermission>
              <Action>CATI.setgeneralparameters.setsurveydescription</Action>
              <Permission>1</Permission>
            </ActionPermission>
          </Permissions>
        </Role>
      </GetRolesResult>
    </GetRolesResponse>
  </s:Body>
</s:Envelope>
```

  + response when the `name` field contains the name of an existing role:
```
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <s:Fault>
      <faultcode xmlns:a="http://schemas.microsoft.com/net/2005/12/windowscommunicationfoundation/dispatcher">a:InternalServiceFault</faultcode>
      <faultstring xml:lang="en-US">The server was unable to process the request due to an internal error.  For more information about the error, either turn on IncludeExceptionDetailInFaults (either from ServiceBehaviorAttribute or from the &lt;serviceDebug&gt; configuration behavior) on the server in order to send the exception information back to the client, or turn on tracing as per the Microsoft .NET Framework SDK documentation and inspect the server trace logs.</faultstring>
    </s:Fault>
  </s:Body>
</s:Envelope>
```


# Protocol Sniffing Process

+ Setup a Blaise VM on a HTTP connection __NOT__ HTTPS.
+ Note the IP of the Blaise VM or LoadBalancer
+ Start [Wireshark](https://www.wireshark.org/download.html)
  + Filter the traffic by VM/LoadBalancer IP
  + Wireshark/Edit/Preferences/Protocols/HTTP add ports 8031 and 8033
+ Start Blaise Server Manager
  + Connect to IP/LoadBalancer
+ Observe traffic between your machine and the server
