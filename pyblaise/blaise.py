import logging
import socket

from .operations import (
    create_role,
    create_user,
    get_auth_token,
    get_all_users,
    get_all_server_parks,
    get_list_of_instruments,
    get_roles,
    get_server_park,
    get_server_version,
    get_skills,
    get_version,
    update_server_park,
)


class Blaise:
    """manage a connection to a blaise remote and perform soap actions.
    example:

    with Blaise("https", "my.blaise.com", 8031, "username", "password") as blaise:
      roles = blaise.get_roles()
      users = blaise.get_users()
      server_parks = blaise.get_server_park_definitions()
    """

    def __init__(self, protocol, host, port, username, password):
        self.logger = logging.getLogger(__name__)
        self.open(protocol, host, port, username, password)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return self

    def open(self, protocol, host, port, username, password):
        """open a connection to a remote blaise server"""
        self.connection_info = {"protocol": protocol, "host": host, "port": port}
        self.username = username
        self.password = password

        _, self.token = get_auth_token(
            **self.connection_info, username=self.username, password=self.password
        )

    def close(self):
        """close a connection with a blaise remote"""
        self.token = None

    def version(self):
        """get the version of of the remote"""
        return get_version(**self.connection_info)

    def server_version(self):
        """get the version of blaise on the remote"""
        return get_server_version(**self.connection_info)

    def create_role(self, name, description, permissions):
        """create a role on the server with the given name and description
        name: string identifying the role
        description: text associated with the role
        permissions: list of strings as permission names
        returns: id of the created role
        throws: CreateRoleFailed (usually because a role with the name already exists)
        """
        _, role_id = create_role(
            **self.connection_info,
            token=self.token,
            name=name,
            description=description,
            permissions=permissions
        )
        return role_id

    def roles(self):
        """get a list of roles from the server
        returns: dict of roles indexed by name ({role_name: {"id": string, "description": string, "permissions": list of strings}})
        """
        _, roles = get_roles(**self.connection_info, token=self.token)
        return roles

    def users(self):
        """get a list of users from the server"""
        return get_all_users(**self.connection_info, token=self.token)

    def create_user(self, name, password, description, role_id, server_parks):
        """create a user on the server with the given variables
        name: name of the user
        password: password to assign to user
        description: description of the user (can be empty)
        role_id: role is to assign to the user
        server_parks: list of server parks to assign to user
        returns: "Created" String
        """
        return create_user(
            **self.connection_info,
            token=self.token,
            name=name,
            password=password,
            description=description,
            role_id=role_id,
            server_parks=server_parks
        )

    def instruments(self):
        """get a list of instruments from the server"""
        return get_list_of_instruments(**self.connection_info, token=self.token)

    def skills(self):
        """get a list of skills from the server"""
        return get_skills(**self.connection_info, token=self.token)

    def server_parks(self):
        """get a list of server parks and definitions from the server"""
        return get_all_server_parks(**self.connection_info, token=self.token)

    def server_park(self, server_park_name):
        """get info about a server-park"""
        return get_server_park(
            **self.connection_info, token=self.token, server_park_name=server_park_name
        )

    def add_server_to_server_park(self, server_park_name, server_name):
        """add an existing server to an existing server park"""
        import json

        # get the remote IP
        # FIXME: there is soap action: http://www.blaise.com/deploy/2013/03/IDeployService/GetIpAddresses
        #        which gets the ipv4 and ipv6 addresses (and I assume checks the mgmt server can connect)
        self.logger.debug("getting ipv4 and ipv6 address for '%s'" % server_name)
        remote_ipv4 = socket.gethostbyname(server_name)
        remote_ipv6 = socket.getaddrinfo(server_name, remote_port, socket.AF_INET6)[0][
            4
        ][0]

        # FIXME: where does remote_binding initially come from?
        remote_binding = "http"
        # FIXME: where does remote_port come from?
        remote_port = 8031

        # get the remote ROLES
        status_code, roles = get_remote_defined_roles(
            **self.connection_info,
            token=self.token,
            binding=remote_binding,
            remote_host=server_name,
            remote_port=remote_port
        )
        self.logger.debug(
            "get_remote_defined_roles '%s' returned [%i](%i roles)'%s'"
            % (server_name, status_code, len(roles), json.dumps(roles))
        )

        # create the server definition
        # FIXME: we need to create a new server definition for each role defined on the remote
        #        the 'roles' dict contains the ports and bindings to use for the server def
        new_server_roles = [
            {
                "binding": role["binding"],
                "ip-v4": remote_ipv4,
                "ip-v6": remote_ipv6,
                "hostname": server_name,
                "port": role["port"],
                "roles": role["name"],
            }
            for role in roles
        ]
        self.logger.debug("created %i roles from remote" % (len(new_server_roles)))
        self.logger.debug(json.dumps(new_server_roles))

        # get the existing server park definition
        status_code, server_park_definition = self.server_park(server_park_name)
        self.logger.debug(
            "get_server_park '%s' returned: [%i]'%s'"
            % (server_park_name, status_code, json.dumps(server_park_definition))
        )

        # update the definition with the new roles
        server_park_definition["servers"].append(new_server_roles)

        # update the server park
        status_code, message = update_server_park(
            **self.connection_info,
            token=self.token,
            server_park_definition=server_park_definition
        )
        self.logger.debug(
            "update_server_park '%s' returned: [%i]'%s'"
            % (server_park_name, status_code, message)
        )

        # FIXME: confirm the node is added to the server park by calling:
        #          http://www.blaise.com/deploy/2017/11/IDeployService/GetRemoteMasterAddress201711
