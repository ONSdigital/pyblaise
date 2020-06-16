from .soap_utils import (create_soap_from_template,
                         basic_soap_request,
                         parse_response_for_tag,
                         parse_response_for_tags,
                         parse_response_for_tag_contents,
                         parse_response_for_tags_contents)


def get_auth_token(protocol, host, port, username, password):
  R = basic_soap_request("request-token", protocol, host, port, USERNAME=username, PASSWORD=password)
  token = parse_response_for_tag_contents(R.text, "AccessToken")
  return R.status_code, token



def get_all_users(protocol, host, port, token):
  R = basic_soap_request("get-all-users", protocol, host, port, TOKEN=token)
  has_users = parse_response_for_tag(R.text, "GetAllUsers201812Result")
  users = []

  return R.status_code, users

def is_interactive_connection_allowed(protocol, host, port, token):
  R = basic_soap_request("is-interactive-connection-allowed", protocol, host, port, TOKEN=token)
  retval = parse_response_for_tag_contents(R.text, "IsInteractiveConnectionAllowedResult")
  return R.status_code, retval


def get_list_of_instruments(protocol, host, port, token):
  R = basic_soap_request("get-list-of-instruments", protocol, host, port, TOKEN=token)

  results = parse_response_for_tag_contents(R.text, "GetListOfInstrumentsResult")
  instruments = parse_response_for_tags_contents(results, "InstrumentMeta")

  data = []

  for instrument in instruments:
    # create a dict
    data += [{"install-date": parse_response_for_tag_contents(instrument, "InstallDate"),
              "id": parse_response_for_tag_contents(instrument, "InstrumentId"),
              "name": parse_response_for_tag_contents(instrument, "InstrumentName"),
              "server-park": parse_response_for_tag_contents(instrument, "ServerPark"),
              "status": parse_response_for_tag_contents(instrument, "Status")
             }]

  # FIXME: we return a list here because we are "list_of_instruments"
  return R.status_code, data


def get_roles(protocol, host, port, token):
  R = basic_soap_request("get-roles", protocol, host, port, TOKEN=token)

  has_roles = parse_response_for_tag(R.text, "GetSkillsResponse")
  roles = []

  return R.status_code, roles


def get_server_park_definitions(protocol, host, port, token):
  R = basic_soap_request("get-all-server-park-definitions",
          protocol, host, port, TOKEN=token)

  has_tag = parse_response_for_tag(R.text, "GetAllServerParkDefinitions102906Result")
  server_park_defs = []

  # FIXME: parse the multiple Server tags and extract data

  return R.status_code, server_park_defs


def get_server_version(protocol, host, port, token):
  R = basic_soap_request("get-server-version", protocol, host, port, TOKEN=token)

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

  has_skills = parse_response_for_tag(R.text, "GetSkillsResponse")
  skills = []

  return R.status_code, skills


def get_version(protocol, host, port, token):
  R = basic_soap_request("get-version", protocol, host, port, TOKEN=token)

  version = parse_response_for_tag_contents(R.text, "GetVersionResponseResponse")

  return R.status_code, version


def remove_instrument(protocol, host, port, token, id, name, server_park):
  R = basic_soap_request("remove-instrument", protocol, host, port,
         TOKEN=token, ID=id, NAME=name, SERVERPARK=server_park)

  # parse
  removed = parse_response_for_tag_contents(R.text, "RemoveInstrumentResult")

  data = {
      "message": parse_response_for_tag_contents(removed, "Message"),
      "status_code": parse_response_for_tag_contents(removed, "Statuscode")
  }

  return R.status_code, data


def report_user_logout(protocol, host, port, token, username):
  R = basic_soap_request("report-user-logout", protocol, host, port,
         TOKEN=token, USERNAME=username)

  logged_out = parse_response_for_tag(R.text, "ReportUserLogoutResponse")

  return R.status_code


def create_survey_manifest(survey_name):
  from uuid import uuid4

  id = str(uuid4())
  x = create_soap_from_template("survey/opn2004.manifest.template",
     SURVEY_NAME=survey_name,
     SURVEY_UUID=str(uuid4())
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
      with ZipFile (existing_survey_filename, "r") as z_in:
        for item in z_in.infolist():
          if item.filename.endswith(".manifest"):
            continue

          # change the root dir in the archive to use our survey name
          #archive_name = join(survey_name, *item.filename.split("/")[1:])
          #print("writing '%s' to '%s'" % (item.filename, archive_name))
          archive_name = item.filename
          z_out.writestr(archive_name, z_in.read(item.filename))

      # write out the manifest
      manifest, id = create_survey_manifest(survey_name)
      #archive_name = join(survey_name, "shitty.manifest")
      archive_name = "shitty.manifest"
      z_out.writestr(archive_name, manifest)

    return tmp_out.name, id
