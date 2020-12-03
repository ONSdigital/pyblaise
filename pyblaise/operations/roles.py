"""
roles resources

roles are groups of permissions which may be applied to nodes or users
"""
import logging

from pyblaise.soap_utils import (
    basic_soap_request,
    parse_response_for_tag,
    parse_response_for_tag_contents,
    parse_response_for_tags_contents,
)

from .exceptions import CreateRoleFailed

logger = logging.getLogger(__name__)


def get_roles(protocol, host, port, token):
    """read the roles from the server response.
    roles is an array and contains 'id', 'name', 'description' and 'permissions' fields.
    'permissions' is an array of permissions granted to that role.
    the XML actually responds with a '1' value for granted roles, but I've never
    seen a '0' value (for denied permission?).
    The interface below only returns the list of permissions on the role, not the 1 value.
    A guard checks that the value is '1' incase we ever get some weird info back

    return value is:
    (http_status_code, dict({role_name: {"id":str, "description":str, "permissions":[]}})
    """
    R = basic_soap_request("get-roles", protocol, host, port, TOKEN=token)
    logger.debug(R.text)

    role_definitions = {}

    has_tag = parse_response_for_tag(R.text, "GetRolesResult")

    if has_tag is False:
        logger.debug("could not find tag 'GetRolesResult'")
        return R.status_code, role_definitions

    results = parse_response_for_tag_contents(R.text, "GetRolesResult")

    if results is None:
        logger.debug("empty results returned in GetRolesResult")
        return R.status_code, role_definitions

    roles = parse_response_for_tags_contents(results, "Role")

    for idx, role in enumerate(roles):
        logger.debug("processing role '%i'" % idx)

        # parse the role info
        role_id = parse_response_for_tag_contents(role, "Id")
        role_name = parse_response_for_tag_contents(role, "Name")
        role_desc = parse_response_for_tag_contents(role, "Description")

        # parse the permissions
        permissions = parse_response_for_tag_contents(role, "Permissions")
        actions = parse_response_for_tags_contents(permissions, "ActionPermission")
        permission_names = [
            parse_response_for_tag_contents(action, "Action") for action in actions
        ]

        # sanity check that all permissions have the value '1'
        permission_values = [
            parse_response_for_tag_contents(action, "Permission") for action in actions
        ]
        assert all(
            [x == "1" for x in permission_values]
        ), "ERR: Not all permission values are '1': '%s'" % str(
            zip(permission_names, permission_values)
        )

        # append
        role_definitions.update(
            {
                role_name: {
                    "id": role_id,
                    "description": role_desc,
                    "permissions": permission_names,
                }
            }
        )

    return R.status_code, role_definitions


def create_role(protocol, host, port, token, name, description, permissions):
    """
    create a role and add selected permissions
    name: name of the role
    description: description of the role (can be empty)
    permissions: list of kv pairs [{action: permitted}, {action: permitted}...]
                 i.e., the name of the action and a boolean indicating whether it is permitted.

    return (status_code, role_id)
    """

    R = basic_soap_request(
        "create-role",
        protocol,
        host,
        port,
        TOKEN=token,
        NAME=name,
        DESCRIPTION=description,
        PERMISSIONS=permissions,
    )
    logger.debug(R.text)

    role_id = parse_response_for_tag_contents(R.text, "CreateRoleResult")

    if role_id is None:
        raise CreateRoleFailed

    return R.status_code, int(role_id)


def get_remote_defined_roles(
    protocol, host, port, token, binding, remote_host, remote_port
):
    """
    get the list of roles defined for the remote instance

    connects to the management server (host) to get a list of roles
    define on the slave node (remote_host).

    binding: (http|https)
    remote_host: name of the remote host (resolvable by host)
    remote_port: management communication port on the remote (usually 8031)
    """
    R = basic_soap_request(
        "get-remote-defined-roles",
        protocol,
        host,
        port,
        TOKEN=token,
        BINDING=binding,
        REMOTE_HOST=remote_host,
        REMOTE_PORT=remote_port,
    )
    logger.debug(R.text)

    response = parse_response_for_tag_contents(
        R.text, "GetRemoteDefinedRoles201711Result"
    )

    if response is None:
        return R.status_code, []

    remote_roles = parse_response_for_tags_contents(response, "a:RoleInfo2")

    roles = [
        {
            "name": parse_response_for_tag_contents(remote_role, "a:Name"),
            "binding": parse_response_for_tag_contents(remote_role, "a:Binding"),
            "port": parse_response_for_tag_contents(remote_role, "a:Port"),
        }
        for remote_role in remote_roles
    ]

    return R.status_code, roles
