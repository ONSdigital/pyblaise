"""
basic functionality interface to blaise via the SOAP API.

These functions provide the interface between Blaise SOAP API and
some calling python process.

These functions should not be used directly, prefer the Blaise class
in blaise.py. However, these can be used for low-level interactions,
testing, etc.
"""
from .operations import *


from .auth import get_auth_token
from .users import get_all_users, create_user
from .instruments import get_list_of_instruments, remove_instrument
from .roles import get_roles, create_role
from .server_parks import get_server_park_definitions

from .survey_packages import get_manifest_id_from_zip, create_survey_manifest, create_survey_from_existing
