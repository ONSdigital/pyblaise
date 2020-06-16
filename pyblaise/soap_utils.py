import re
import requests
from os.path import join, dirname

from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape
from jinja2 import StrictUndefined

from .definitions import operations, default_headers


TEMPLATE_DIR = "templates"
TEMPLATE_PATH = join(dirname(__file__), TEMPLATE_DIR)


env = Environment(
    loader=PackageLoader("pyblaise", TEMPLATE_DIR),
    autoescape=select_autoescape(["xml"]),
    undefined=StrictUndefined
)


def create_soap_from_template(template_file, **kwargs):
  """
  creates the soap xml payload from a template
  env should be StrictUndefined so we get errors when
  variables are unmatched (default behaviour is silent fail)
  I've used a convention of UPPERCASE VARIABLE NAMES
  """
  template = env.get_template(template_file)
  instance = template.render(**kwargs)
  return instance


def parse_response_for_tags_contents(response, tagname):
  """
  returns the contents of an xml tag.
  currently matches:
    <tagname> matched content </tagname>
    <tagname a=b c=d> matched content </tagname>

  for a series of matches e.g., looking for b in:
  <a><b>c</b><b>d</b><b>e</b></a>
  the method will yield each tag contents in order of appearance
  """
  contents = re.findall("<%s.*?>(.*?)</%s>" % (tagname, tagname),
                        response,
                        re.DOTALL | re.MULTILINE)

  for content in contents:
    yield content


def parse_response_for_tag_contents(response, tagname):
  """
  returns the contents of the first xml tag matching tagname.
  """
  return next(parse_response_for_tags_contents(response, tagname))


def parse_response_for_tag(response, tagname):
  """
  returns true if a response contains a given xml tag
  """
  content = re.findall("<%s.*?>" % tagname, response)
  assert content is not None
  return len(content) > 0


def parse_response_for_tags(response, tagnames):
  """
  returns true if a response contains all the tagnames
  """
  return all([parse_response_for_tag(response, tagname) for tagname in tagnames])


def build_uri(protocol, host, port, path):
  return "%s://%s:%i%s" % (protocol, host, port, path)


def basic_soap_request(operation, protocol, host, port, **kwargs):
  op = operations[operation]

  data = create_soap_from_template(op["template"], **kwargs)

  headers = {}
  headers.update(default_headers)
  headers.update(op["headers"])

  R = requests.post(build_uri(protocol, host, port, op["path"]),
                    headers=headers,
                    data=data)

  return R
