import os
import pytest
import xml.etree.ElementTree

import jinja2

from pyblaise.definitions import operations
from pyblaise.soap_utils import create_soap_from_template, env as template_env

template_filenames = [operations[k]["template"] for k in operations]



def test_template_env_is_PackageLoader():
    assert template_env is not None
    assert isinstance(template_env, jinja2.Environment)
    assert isinstance(template_env.loader, jinja2.PackageLoader)


def test_template_env_list_templates_is_not_empty():
    assert template_env.loader.list_templates()


@pytest.mark.parametrize("template_filename", template_env.loader.list_templates())
def test_each_template_loads(template_filename):
    tpl = template_env.loader.get_source(template_env, template_filename)
    assert tpl is not None
    assert len(tpl) > 0


@pytest.mark.parametrize("template_filename", template_filenames)
def test_operation_template_in_template_list(template_filename):
    assert template_filename in template_env.loader.list_templates()


@pytest.mark.skip(reason="templates require variables")
@pytest.mark.parametrize("template_filename", template_filenames)
def test_create_soap_from_template_is_not_none(template_filename):
    xml = create_soap_from_template(template_filename)
    assert xml is not None


@pytest.mark.skip(reason="templates require variables")
@pytest.mark.parametrize("template_filename", template_filenames)
def test_create_soap_from_template_returns_valid_xml(template_filename):
    xml = create_soap_from_template(template_filename)
    tree = xml.etree.ElementTree.parse(xml)
    assert tree is not None
