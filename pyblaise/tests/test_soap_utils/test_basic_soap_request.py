import pytest
import requests

from pyblaise.soap_utils import __do_soap_request
from pyblaise.exceptions import ServerConnectionError, ServerConnectionTimeout, ServerResponse500

host_infos = [
    {"uri": "http://my-host.com"},
]


@pytest.mark.parametrize("host_info", host_infos)
def test__do_soap_request_returns_200_ok(host_info, requests_mock):
    requests_mock.register_uri("POST", host_info["uri"], status_code=200, text="OK")

    resp = __do_soap_request(host_info["uri"], {}, {})

    assert requests_mock.called is True
    assert requests_mock.call_count == 1
    assert resp.status_code == 200


@pytest.mark.parametrize("host_info", host_infos)
def test__do_soap_request_raises_ServerConnectionError_on_requests_ConnectError(
    host_info, requests_mock
):
    requests_mock.register_uri(
        "POST", host_info["uri"], exc=requests.exceptions.ConnectionError
    )

    with pytest.raises(ServerConnectionError):
        __do_soap_request(host_info["uri"], {}, {})


@pytest.mark.parametrize("host_info", host_infos)
def test__do_soap_request_raises_ServerConnectionTimeout_on_requests_Timeout(
    host_info, requests_mock
):
    requests_mock.register_uri(
        "POST", host_info["uri"], exc=requests.exceptions.Timeout
    )

    with pytest.raises(ServerConnectionTimeout):
        __do_soap_request(host_info["uri"], {}, {})


@pytest.mark.parametrize("host_info", host_infos)
def test__do_soap_request_raises_ServerConnectionTimeout_on_requests_ConnectTimeout(
    host_info, requests_mock
):
    requests_mock.register_uri(
        "POST", host_info["uri"], exc=requests.exceptions.ConnectTimeout
    )

    with pytest.raises(ServerConnectionTimeout):
        __do_soap_request(host_info["uri"], {}, {})


@pytest.mark.parametrize("host_info", host_infos)
def test__do_soap_request_raises_ServerConnectionTimeout_on_requests_ReadTimeout(
    host_info, requests_mock
):
    requests_mock.register_uri(
        "POST", host_info["uri"], exc=requests.exceptions.ReadTimeout
    )

    with pytest.raises(ServerConnectionTimeout):
        __do_soap_request(host_info["uri"], {}, {})


@pytest.mark.parametrize("host_info", host_infos)
def test__do_soap_request_raises_ServerResponse500_on_500_status_code(host_info, requests_mock):
    requests_mock.register_uri("POST", host_info["uri"], status_code=500, text="OK")

    with pytest.raises(ServerResponse500):
        __do_soap_request(host_info["uri"], {}, {})


@pytest.mark.parametrize("host_info", host_infos)
def test__do_soap_request_raises_ServerResponse500_with_response_object(host_info, requests_mock):
    requests_mock.register_uri("POST", host_info["uri"], status_code=500, text="my-response-text")

    with pytest.raises(ServerResponse500) as e:
        __do_soap_request(host_info["uri"], {}, {})

        # FIXME: these aren't being checked for some reason
        # https://docs.pytest.org/en/stable/assert.html#assertions-about-expected-exceptions
        assert hasattr(e, "get_response_object")
        assert e.get_response_object() is not None
        assert isinstance(e.get_response_object(), flask.Response)
        assert False is True # dummy assert doesn't fail


@pytest.mark.parametrize("host_info", host_infos)
def test__do_soap_request_uses_session_object(host_info, requests_mock):
    # FIXMIE: We should test that the session object is used
    requests_mock.register_uri("POST", host_info["uri"], status_code=200, text="OK")
    S = requests.session()

    resp = __do_soap_request(host_info["uri"], {}, {}, session=S)

    assert requests_mock.called is True
    assert requests_mock.call_count == 1
    assert resp.status_code == 200
    assert S is not None
    assert isinstance(S, requests.Session)
