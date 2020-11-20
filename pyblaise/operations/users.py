"""
user resources exposed by Blaise

user objects authenticate and identify activies performed on against Blaise
"""
import logging

from pyblaise.soap_utils import (
    basic_soap_request,
    parse_response_for_tag_contents,
    parse_response_for_tags_contents,
)

from .exceptions import *

logger = logging.getLogger(__name__)


def get_all_users(protocol, host, port, token):
    R = basic_soap_request("get-all-users", protocol, host, port, TOKEN=token)
    logger.debug(R.text)

    has_users = parse_response_for_tag_contents(R.text, "GetAllUsers201812Result")

    if not has_users:
        return R.status_code, []

    users = parse_response_for_tags_contents(has_users, "User201812")

    data = [
        {
            "name": parse_response_for_tag_contents(user, "Name"),
            "last_activity": parse_response_for_tag_contents(user, "LastActivity"),
            "last_login": parse_response_for_tag_contents(user, "LastLogin"),
        }
        for user in users
    ]

    return R.status_code, data


def create_user(
    protocol, host, port, token, name, password, description, role_id, server_parks
):
    """
    create a user
    name: name of the user
    password: password to assign to user
    description: description of the user (can be empty)
    role_id: role is to assign to the user
    server_parks: list of server parks to assign to user

    return (status_code, "Created")
    FIXME: raise a CreateUserFailed (ala CreateRoleFailed exception)
    """

    R = basic_soap_request(
        "create-user",
        protocol,
        host,
        port,
        TOKEN=token,
        NAME=name,
        PASSWORD=password,
        DESCRIPTION=description,
        ROLE_ID=role_id,
        SERVER_PARKS=server_parks,
    )
    logger.debug(R.text)

    return R.status_code, "Created"
