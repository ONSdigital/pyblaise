"""
authentication resources exposed by Blaise
"""
import logging

from .soap_utils import (
    basic_soap_request,
    parse_response_for_tag_contents,
)

logger = logging.getLogger(__name__)


def get_auth_token(protocol, host, port, username, password):
    """
    get an OAuth access token from Blaise with the given credentials

    protocol: http or https
    host: dns or ip address of blaise host
    port: port number for blaise process (usually 8031)
    username: user...name?
    password: password

    returns tuple(HTTP status code, access token string)
    """
    R = basic_soap_request(
        "request-token", protocol, host, port, USERNAME=username, PASSWORD=password
    )
    logger.debug(R.text)
    token = parse_response_for_tag_contents(R.text, "AccessToken")
    return R.status_code, token


def report_user_logout(protocol, host, port, token, username):
    R = basic_soap_request(
        "report-user-logout", protocol, host, port, TOKEN=token, USERNAME=username
    )
    logger.debug(R.text)

    logged_out = parse_response_for_tag(R.text, "ReportUserLogoutResponse")

    return R.status_code
