"""
basic functionality interface to blaise via the SOAP API.

These functions provide the interface between Blaise SOAP API and
some calling python process.

These functions should not be used directly, prefer the Blaise class
in blaise.py. However, these can be used for low-level interactions,
testing, etc.

Each Blaise resource should have functions to:
+ list instances
+ get specific instance
+ create a new instance
+ update an existing instance
+ delete a specific instance
This is following the CRUD interface for resources (create, read, update, delete, NB we substitute get for read)

Exception raising should follow a pattern:
+ list -> no exception, return empty list
+ get -> no exception, return None
+ create -> raise Create*Failed
+ update -> raise Update*Failed
+ delete -> raise Delete*Failed
where * is replaced with the name of the resource.

Authentication errors are exceptions when authentication tokens are provided.
"""

# defined blaise resources
from .auth import get_auth_token, report_user_logout
from .instruments import get_list_of_instruments, remove_instrument
from .misc import is_interactive_connection_allowed, get_server_version, get_version
from .roles import get_roles, create_role, get_remote_defined_roles
from .server_park import (
    get_all_server_parks,
    get_server_park,
    update_server_park,
    update_server_type,
)
from .skills import get_skills
from .users import get_all_users, create_user

# utility unctions
from .survey_packages import (
    get_manifest_id_from_zip,
    create_survey_manifest,
    create_survey_from_existing,
)
