from .operations import (create_role,
                         get_auth_token,
                         get_all_users,
                         get_list_of_instruments,
                         get_roles,
                         get_server_park_definitions,
                         get_server_version,
                         get_skills,
                         get_version,
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

    def instruments(self):
        """get a list of instruments from the server"""
        return get_list_of_instruments(**self.connection_info, token=self.token)

    def skills(self):
        """get a list of skills from the server"""
        return get_skills(**self.connection_info, token=self.token)

    def server_park_definitions(self):
        """get a list of server parks and definitions from the server"""
        return get_server_park_definitions(**self.connection_info, token=self.token)
