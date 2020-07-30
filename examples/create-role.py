import sys
import logging
import json

import pyblaise

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logging.getLogger('pyblaise').addHandler(handler)
logging.getLogger('pyblaise').setLevel(logging.INFO)

# remote info
protocol = "https"
hostname = os.environ["HOSTNAME"]
username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]
port = os.environ["PORT"]

# create the role info
new_role = {"name": "test-role-005",
            "description": "none",
            "permissions": {
               "user.createuser": 1,
               "user.updateuser": 1,
               "user.removeuser": 1,
               "CATI": 1,
               "CATI.setcatispecification": 1,
               "CATI.setgeneralparameters": 1,
               "CATI.setgeneralparameters.setsurveydescription": 1
             }
           }

print("attempting to add role info to '%s'" % hostname)
print(json.dumps(new_role, indent=2))

# connect and stuff
# NB: the with block will swallow up any exceptions, to see any exceptions, use:
#blaise = pyblaise.Blaise(protocol, hostname, 8031, username, password)
#if blaise is not None:
with pyblaise.Blaise(protocol, hostname, port, username, password) as blaise:
  roles = blaise.roles()
  print("existing role names: '%s'" % roles.keys())

  if new_role["name"] in roles.keys():
    print("role already on server.")
    sys.exit()

  # create the role
  try:
    new_role_id = blaise.create_role(**new_role)
    print("created role: '%s'" % new_role_id)
  except pyblaise.CreateRoleFailed:
    print("create-role failed")

  # get updated list of roles
  updated_roles = blaise.roles()
  print("updated roles names: '%s'" % updated_roles.keys())
