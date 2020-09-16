import pytest

from pyblaise.soap_utils import parse_response_for_tag, parse_response_for_tag_contents


def test_parse_get_auth_token_response():
    from hashlib import md5
    from time import time

    e0 = ".".join([md5(str(time()).encode()).hexdigest() for _ in range(3)])
    e1 = ".".join([md5(str(time()).encode()).hexdigest() for _ in range(3)])

    d = """
  <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
    <s:Body>
      <RequestTokenResponse xmlns="http://www.blaise.com/security/2016/06">
        <RequestTokenResult xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
          <AccessToken>%s</AccessToken>
          <RefreshToken>%s</RefreshToken>
        </RequestTokenResult>
      </RequestTokenResponse>
    </s:Body>
  </s:Envelope>
  """ % (
        e0,
        e1,
    )

    assert parse_response_for_tag(d, "AccessToken") is True
    assert parse_response_for_tag(d, "RefreshToken") is True
    assert parse_response_for_tag(d, "RequestTokenResponse") is True

    assert parse_response_for_tag_contents(d, "AccessToken") == e0
    assert parse_response_for_tag_contents(d, "RefreshToken") == e1


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

    assert parse_response_for_tag(d, "GetVersionResponseResponse") is True
    assert parse_response_for_tag(d, "GetVersionResponseResult") is True


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

    assert parse_response_for_tag(d, "GetSkillsResult") is True
    assert parse_response_for_tag(d, "GetSkillsResponse") is True
