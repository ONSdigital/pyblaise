"""
survey package utility functions

survey packages are compiled packages which contain instruments.
Packages are deployed to server-parks as instruments.

These utility functions are for performing operations on the package files.
"""
import logging

from .soap_utils import (
    create_soap_from_template,
)

from .exceptions import *

logger = logging.getLogger(__name__)


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
