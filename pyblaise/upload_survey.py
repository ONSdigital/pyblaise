import requests
from .soap_utils import build_uri


def upload_survey(
    protocol, host, port, server_park, survey_name, survey_id, token, filename
):
    headers = {
        "Authorization": "Bearer %s" % token,
        "Content-Type": "application/binary",
        "Expect": "100-continue",
    }

    REQUEST_PATH = f"/Blaise/Administer/Services/REST/{server_park}/{survey_name}/{survey_id}/uploadpackage"

    with open(filename, "r") as payload:
        R = requests.post(
            build_uri(protocol, host, port, REQUEST_PATH),
            headers=headers,
            data=payload,
        )

    return R.status_code
