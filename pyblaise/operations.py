import logging

from .soap_utils import (
    create_soap_from_template,
    basic_soap_request,
    parse_response_for_tag,
    parse_response_for_tags,
    parse_response_for_tag_contents,
    parse_response_for_tags_contents,
)

from .exceptions import *

logger = logging.getLogger(__name__)


def get_auth_token(protocol, host, port, username, password):
    R = basic_soap_request(
        "request-token", protocol, host, port, USERNAME=username, PASSWORD=password
    )
    logger.debug(R.text)
    token = parse_response_for_tag_contents(R.text, "AccessToken")
    return R.status_code, token


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


def is_interactive_connection_allowed(protocol, host, port, token):
    R = basic_soap_request(
        "is-interactive-connection-allowed", protocol, host, port, TOKEN=token
    )
    logger.debug(R.text)
    retval = parse_response_for_tag_contents(
        R.text, "IsInteractiveConnectionAllowedResult"
    )
    return R.status_code, retval


def get_list_of_instruments(protocol, host, port, token):
    R = basic_soap_request("get-list-of-instruments", protocol, host, port, TOKEN=token)
    logger.debug(R.text)

    has_instruments = parse_response_for_tag_contents(
        R.text, "GetListOfInstrumentsResult"
    )

    if not has_instruments:
        return R.status_code, []

    instruments = parse_response_for_tags_contents(has_instruments, "InstrumentMeta")

    data = [
        {
            "install-date": parse_response_for_tag_contents(instrument, "InstallDate"),
            "id": parse_response_for_tag_contents(instrument, "InstrumentId"),
            "name": parse_response_for_tag_contents(instrument, "InstrumentName"),
            "server-park": parse_response_for_tag_contents(instrument, "ServerPark"),
            "status": parse_response_for_tag_contents(instrument, "Status"),
        }
        for instrument in instruments
    ]

    return R.status_code, data


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


def get_skills(protocol, host, port, token):
    R = basic_soap_request("get-skills", protocol, host, port, TOKEN=token)
    logger.debug(R.text)
    has_skills = parse_response_for_tag(R.text, "GetSkillsResponse")
    skills = []

    return R.status_code, skills


def get_version(protocol, host, port, token):
    R = basic_soap_request("get-version", protocol, host, port, TOKEN=token)
    logger.debug(R.text)

    version = parse_response_for_tag_contents(R.text, "GetVersionResponseResponse")

    return R.status_code, version


def remove_instrument(protocol, host, port, token, id, name, server_park):
    R = basic_soap_request(
        "remove-instrument",
        protocol,
        host,
        port,
        TOKEN=token,
        ID=id,
        NAME=name,
        SERVERPARK=server_park,
    )
    logger.debug(R.text)

    # parse
    removed = parse_response_for_tag_contents(R.text, "RemoveInstrumentResult")

    data = {
        "message": parse_response_for_tag_contents(removed, "Message"),
        "status_code": parse_response_for_tag_contents(removed, "Statuscode"),
    }

    return R.status_code, data


def report_user_logout(protocol, host, port, token, username):
    R = basic_soap_request(
        "report-user-logout", protocol, host, port, TOKEN=token, USERNAME=username
    )
    logger.debug(R.text)

    logged_out = parse_response_for_tag(R.text, "ReportUserLogoutResponse")

    return R.status_code


def get_manifest_id_from_zip(existing_survey_filename):
    """
    Returns the survey ID from the manifest file within provided zip file
    """

    from zipfile import ZipFile

    # Import required library
    import xml.etree.ElementTree as ET

    # Find the manifest file from the ZIP
    with ZipFile(existing_survey_filename, "r") as z_in:
        for item in z_in.infolist():
            if item.filename.endswith(".manifest"):
                with z_in.open(item.filename) as file:
                    # Read from the file
                    manifest_file = file.read().decode("utf-8")
                    # Convert file to xml Element
                    root = ET.fromstring(manifest_file)
                    return root.attrib["ID"]
    return None


def create_survey_manifest(survey_name):
    from uuid import uuid4

    id = str(uuid4())
    x = create_soap_from_template(
        "survey/opn2004.manifest.template",
        SURVEY_NAME=survey_name,
        SURVEY_UUID=str(uuid4()),
    )
    return x, id


def create_survey_from_existing(existing_survey_filename, survey_name):
    """
    create a new survey package from existing
    returns the filename of the new archive and the UUID in the manifest
    opens an existing survey zip file,
    writes the contents to a new file,
    replaces the manifest with the new
    """
    from zipfile import ZipFile
    from tempfile import NamedTemporaryFile
    from os.path import join

    with NamedTemporaryFile(delete=False) as tmp_out:
        with ZipFile(tmp_out, "w") as z_out:

            # copy the existing zip
            with ZipFile(existing_survey_filename, "r") as z_in:
                for item in z_in.infolist():
                    if item.filename.endswith(".manifest"):
                        continue

                    # change the root dir in the archive to use our survey name
                    # archive_name = join(survey_name, *item.filename.split("/")[1:])
                    # print("writing '%s' to '%s'" % (item.filename, archive_name))
                    archive_name = item.filename
                    z_out.writestr(archive_name, z_in.read(item.filename))

            # write out the manifest
            manifest, id = create_survey_manifest(survey_name)
            # archive_name = join(survey_name, "shitty.manifest")
            archive_name = "shitty.manifest"
            z_out.writestr(archive_name, manifest)

        return tmp_out.name, id


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


def change_user_name(protocol, host, port, token, name, new_password):
    """
    create a role and add selected permissions
    name: name of the user
    new_password: new password to assign to user
    return (status_code, role_id)
    """

    R = basic_soap_request(
        "change-user-password",
        protocol,
        host,
        port,
        TOKEN=token,
        NAME=name,
        NEW_PASSWORD=new_password,
    )
    logger.debug(R.text)

    role_id = parse_response_for_tag_contents(R.text, "CreateRoleResult")

    if role_id is None:
        raise CreateRoleFailed

    return R.status_code, int(role_id)
