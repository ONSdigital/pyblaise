"""
basic functionality interface to blaise via the SOAP API.

These functions provide the interface between Blaise SOAP API and
some calling python process.

These functions should not be used directly, prefer the Blaise class
in blaise.py. However, these can be used for low-level interactions,
testing, etc.
"""
import logging

from pyblaise.soap_utils import (
    create_soap_from_template,
    basic_soap_request,
    parse_response_for_tag,
    parse_response_for_tags,
    parse_response_for_tag_contents,
    parse_response_for_tags_contents,
)

from .exceptions import *

logger = logging.getLogger(__name__)


def is_interactive_connection_allowed(protocol, host, port, token):
    R = basic_soap_request(
        "is-interactive-connection-allowed", protocol, host, port, TOKEN=token
    )
    logger.debug(R.text)
    retval = parse_response_for_tag_contents(
        R.text, "IsInteractiveConnectionAllowedResult"
    )
    return R.status_code, retval


def get_server_version(protocol, host, port, token):
    R = basic_soap_request("get-server-version", protocol, host, port, TOKEN=token)
    logger.debug(R.text)
    server_version = parse_response_for_tag_contents(R.text, "GetServerVersionResult")

    if server_version is None:
        return {}

    data = {
        "build": int(parse_response_for_tag_contents(server_version, "a:Build")),
        "major": int(parse_response_for_tag_contents(server_version, "a:Major")),
        "minor": int(parse_response_for_tag_contents(server_version, "a:Minor")),
        "release": int(parse_response_for_tag_contents(server_version, "a:Release")),
    }

    return R.status_code, data


def get_version(protocol, host, port, token):
    R = basic_soap_request("get-version", protocol, host, port, TOKEN=token)
    logger.debug(R.text)

    version = parse_response_for_tag_contents(R.text, "GetVersionResponseResponse")

    return R.status_code, version
