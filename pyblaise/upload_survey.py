import requests
from .soap_utils import build_uri

REQUEST_PATH="/Blaise/Administer/Services/REST/ftf/OPN2004A/8a2d121e-6dba-4bf5-a6bf-d1b0e6c36160/uploadpackage"


def upload_survey(protocol, host, port, token, filename):
  headers = {"Authorization": "Bearer %s" % token,
             "Content-Type": "application/binary",
             "Expect": "100-continue",
            }

  with open(filename, "rb") as payload:
    R = requests.post(build_uri(protocol, host, port, REQUEST_PATH),
                      headers=headers,
                      data=payload)

  return R.status_code
