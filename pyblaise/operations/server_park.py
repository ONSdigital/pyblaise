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


def get_server_park_definitions(protocol, host, port, token):
    """
    get server park information from the remote.

    response looks like:
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
        </Servers>
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
