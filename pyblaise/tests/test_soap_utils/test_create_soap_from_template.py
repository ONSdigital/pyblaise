import os
import pytest
import xml.etree.ElementTree

from pyblaise.definitions import operations
from pyblaise.soap_utils import create_soap_from_template, env as template_env

test_template_filenames = [operations[k]["template"] for k in operations]


@pytest.mark.skip(reason="jinja2.Environment has template dir")
@pytest.mark.parametrize("template_filename", test_template_filenames)
def test_template_file_exists(template_filename):
    assert os.path.exists(template_filename)


@pytest.mark.skip(reason="templates require variables")
@pytest.mark.parametrize("template_filename", test_template_filenames)
def test_create_soap_from_template_is_not_none(template_filename):
    xml = create_soap_from_template(template_filename)
    assert xml is not None


@pytest.mark.skip(reason="templates require variables")
@pytest.mark.parametrize("template_filename", test_template_filenames)
def test_create_soap_from_template_returns_valid_xml(template_filename):
    xml = create_soap_from_template(template_filename)
    tree = xml.etree.ElementTree.parse(xml)
    assert tree is not None
