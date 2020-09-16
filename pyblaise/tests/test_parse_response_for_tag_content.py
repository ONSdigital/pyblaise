import pytest

from pyblaise.soap_utils import (
    parse_response_for_tags_contents,
    parse_response_for_tag_contents,
)


def test_parse_get_auth_token_response():
    d = """
  <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
    <s:Body>
      <RequestTokenResponse xmlns="http://www.blaise.com/security/2016/06">
        <RequestTokenResult xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
          <AccessToken>eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJSb290Iiwicm9sZSI6Ik1hc3RlciIsImlzcyI6IkJsYWlzZSBTVFMiLCJhdWQiOiJCbGFpc2UgNSBTZXJ2aWNlcyIsImV4cCI6MTU5MTM0OTc3OCwibmJmIjoxNTkxMzQ4NTc4fQ.Bo6RqvyYWGRDmoeEPiGhFGHYJlujPbzi1gxou1Z1CEM</AccessToken>
          <RefreshToken>eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJSb290Iiwicm9sZSI6Ik1hc3RlciIsImlzcyI6IkJsYWlzZSBTVFMiLCJhdWQiOiJodHRwOi8vezB9OnsxfS9CbGFpc2UvU2VjdXJpdHkvU2VydmljZXMvU2VjdXJpdHlUb2tlblNlcnZpY2UiLCJleHAiOjE1OTE0MzQ5NzgsIm5iZiI6MTU5MTM0ODU3OH0.YxJODlG6fHLy3-x97saaEWi5UjY8kpHW5a4dA7diag8</RefreshToken>
        </RequestTokenResult>
      </RequestTokenResponse>
    </s:Body>
  </s:Envelope>
  """

    x = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJSb290Iiwicm9sZSI6Ik1hc3RlciIsImlzcyI6IkJsYWlzZSBTVFMiLCJhdWQiOiJCbGFpc2UgNSBTZXJ2aWNlcyIsImV4cCI6MTU5MTM0OTc3OCwibmJmIjoxNTkxMzQ4NTc4fQ.Bo6RqvyYWGRDmoeEPiGhFGHYJlujPbzi1gxou1Z1CEM"

    v = parse_response_for_tag_contents(d, "AccessToken")

    assert v == x


@pytest.mark.skip(reason="cannot parse tags with attributes")
def test_parse_get_version_response():
    d = """
  <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
    <s:Body>
      <GetVersionResponseResponse xmlns="http://www.blaise.com/configuration/2015/11">
        <GetVersionResponseResult xmlns:a="http://www.blaise.com/dataentry/2013/09" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
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
  """

    x = """
          <a:CurrentVersion>
            <a:Month>6</a:Month>
            <a:Year>2019</a:Year>
          </a:CurrentVersion>
          <a:MinimumVersion>
            <a:Month>3</a:Month>
            <a:Year>2013</a:Year>
          </a:MinimumVersion>
  """

    v = parse_response_for_tag_contents(d, "GetVersionResponseResult")

    assert v == x


@pytest.mark.skip(reason="cannot parse self-terminating tags")
def test_parse_get_skills_response():
    d = """
  <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
    <s:Body>
      <GetSkillsResponse xmlns="http://www.blaise.com/security/2018/12">
        <GetSkillsResult xmlns:i="http://www.w3.org/2001/XMLSchema-instance"/>
      </GetSkillsResponse>
    </s:Body>
  </s:Envelope>
  """

    x = ""

    v = parse_response_for_tag_contents(d, "GetSkillsResult")

    assert v == x


def test_parse_list_of_instruments_response():
    d = """
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
  """

    x = 4
    v = list(parse_response_for_tags_contents(d, "InstrumentMeta"))
    assert len(v) == x


def test_parse_list_of_instruments_response_empty():
    d = """
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <GetListOfInstrumentsResponse xmlns="http://www.blaise.com/deploy/2013/03">
      <GetListOfInstrumentsResult xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
      </GetListOfInstrumentsResult>
    </GetListOfInstrumentsResponse>
  </s:Body>
</s:Envelope>
  """

    x = 0
    v = list(parse_response_for_tags_contents(d, "InstrumentMeta"))
    assert len(v) == x
