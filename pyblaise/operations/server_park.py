"""
server park resources

server parks are communicating groups of blaise processes, which may be on
one or more virtual or physical machines on the same network.
"""
import logging

from pyblaise.soap_utils import (
    basic_soap_request,
    parse_response_for_tag,
    parse_response_for_tags,
    parse_response_for_tag_contents,
    parse_response_for_tags_contents,
)

from .exceptions import *

logger = logging.getLogger(__name__)


def get_all_server_parks(protocol, host, port, token):
    """
    get information about all server parks on the remote
    """
    R = basic_soap_request(
        "get-all-server-park-definitions", protocol, host, port, TOKEN=token
    )
    logger.debug(R.text)
    has_tag = parse_response_for_tag(R.text, "GetAllServerParkDefinitions201906Result")

    if has_tag is False:
        return R.status_code, []

    results = parse_response_for_tag_contents(
        R.text, "GetAllServerParkDefinitions201906Result"
    )
    servers = parse_response_for_tags_contents(results, "Servers")

    server_park_defs = []

    for server in servers:
        for server_def in parse_response_for_tags_contents(
            server, "ServerDefinition201906"
        ):
            server_park_defs += [
                {
                    "binding": parse_response_for_tag_contents(server_def, "Binding"),
                    "ip-v4": parse_response_for_tag_contents(server_def, "IPAddressV4"),
                    "ip-v6": parse_response_for_tag_contents(server_def, "IPAddressV6"),
                    "hostname": parse_response_for_tag_contents(server_def, "Name"),
                    "port": parse_response_for_tag_contents(server_def, "Port"),
                }
            ]

    return R.status_code, server_park_defs


def get_server_park(protocol, host, port, token, server_park_name):
    """
    get information about a particular server park
    """
    R = basic_soap_request(
        "get-server-park-definition",
        protocol,
        host,
        port,
        TOKEN=token,
        SERVER_PARK_NAME=server_park_name,
    )
    logger.debug(R.text)

    has_tag = parse_response_for_tag(R.text, "GetServerParkDefinition201906Response")

    if has_tag is False:
        return R.status_code, []

    results = parse_response_for_tag_contents(
        R.text, "GetServerParkDefinition201906Result"
    )

    server_park_def = {}

    # get the admin details
    server_park_def = {
        "audit-trail-mode": parse_response_for_tag_contents(results, "AuditTrailMode"),
        "delete-data-after-upload": parse_response_for_tag_contents(
            results, "DeleteDataAfterUpload"
        ),
        "download-surveys-only-if-cases-are-available": parse_response_for_tag_contents(
            results, "DownloadSurveysOnlyIfCasesAreAvailable"
        ),
        "is-public": parse_response_for_tag_contents(results, "IsPublic"),
        "location": parse_response_for_tag_contents(results, "Location"),
        "master-address": parse_response_for_tag_contents(results, "MasterAddress"),
        "name": parse_response_for_tag_contents(results, "Name"),
        "run-mode": parse_response_for_tag_contents(results, "RunMode"),
        "session-mode": parse_response_for_tag_contents(results, "SessionMode"),
        "sync-data-when-connected": parse_response_for_tag_contents(
            results, "SyncDataWhenConnected"
        ),
        "sync-surveys-when-connected": parse_response_for_tag_contents(
            results, "SyncSurveysWhenConnected"
        ),
        "website-name": parse_response_for_tag_contents(results, "WebsiteName"),
    }

    # parse the servers in the server park
    for server in parse_response_for_tags_contents(results, "Servers"):
        server_park_def["servers"] = []

        for server_def in parse_response_for_tags_contents(
            server, "ServerDefinition201906"
        ):
            # get the roles info
            role_data = parse_response_for_tag_contents(server_def, "Roles")
            roles = [x for x in parse_response_for_tags_contents(role_data, "a:string")]

            # get the server info
            server_park_def["servers"] += [
                {
                    "binding": parse_response_for_tag_contents(server_def, "Binding"),
                    "ip-v4": parse_response_for_tag_contents(server_def, "IPAddressV4"),
                    "ip-v6": parse_response_for_tag_contents(server_def, "IPAddressV6"),
                    "hostname": parse_response_for_tag_contents(server_def, "Name"),
                    "port": parse_response_for_tag_contents(server_def, "Port"),
                    "roles": roles,
                }
            ]

    return R.status_code, server_park_def


def update_server_park(protocol, host, port, token, server_park_definition):
    """
    update a server park with a new definition

    call 'get_server_park' to get the initial defintion, alter this spec and
    pass it to this function for updating.

    protocol = (http|https)
    host = management server host
    port = management communication port (usually 8031)
    token = authentication token
    server_park_definition = definition of the server park to affect (retval of get_server_park)
    """
    R = basic_soap_request(
        "update-server-park-definition",
        protocol,
        host,
        port,
        TOKEN=token,
        SERVER_PARK=server_park_definition,
    )
    logger.debug(R.text)

    has_tag = parse_response_for_tag(R.text, "UpdateServerParkDefinition201906Response")

    if has_tag is False:
        return R.status_code, []

    results = parse_response_for_tag_contents(
        R.text, "UpdateServerParkDefinition201906Result"
    )
    message = parse_response_for_tag_contents(results, "a:Message")
    status_code = parse_response_for_tag_contents(results, "a:StatusCode")

    return R.status_code, message


def update_server_type(protocol, host, port, token, new_server_type, master_hostname):
    """
    update a server type

    new_server_type: (Slave)
    master_hostname: DNS resolvable name of the new master node

    sets the 'slave' mode on a node added to a server-park.
    Unsure if/how we change it back, what other types are,
    and if the master hostname is optional for non-slave types

    NB: new_server_type is passed into the xml directly and is an enum
    type in the underlying blaise API on the remote, the type is:
        StatNeth.Blaise.Administer.DataContract.Deploy.ServerType
    And it is case sensitive.
    """
    R = basic_soap_request(
        "update-server-type",
        protocol,
        host,
        port,
        TOKEN=token,
        NEW_TYPE=new_server_type,
        MASTER_HOSTNAME=master_hostname,
    )
    logger.debug(R.text)

    has_tag = parse_response_for_tag(R.text, "UpdateServerTypeResponse")

    if has_tag is False:
        return R.status_code, False

    results = parse_response_for_tag_contents(R.text, "UpdateServerTypeResult")
    message = parse_response_for_tag_contents(results, "Message")
    status_code = parse_response_for_tag_contents(results, "Statuscode")

    return R.status_code, message
