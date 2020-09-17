import logging
import re
import requests
from os.path import join, dirname

from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape
from jinja2 import StrictUndefined

from .definitions import operations, default_headers


logger = logging.getLogger(__name__)


TEMPLATE_DIR = "templates"
TEMPLATE_PATH = join(dirname(__file__), TEMPLATE_DIR)


env = Environment(
    loader=PackageLoader("pyblaise", TEMPLATE_DIR),
    autoescape=select_autoescape(["xml"]),
    undefined=StrictUndefined,
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

    logger.debug(
        "searching for '%s[%s]' in '%s[%s]'"
        % (tagname, str(type(tagname)), response, str(type(response)))
    )
    contents = re.findall(
        "<%s.*?>(.*?)</%s>" % (tagname, tagname), response, re.DOTALL | re.MULTILINE
    )

    for content in contents:
        logger.debug("found: '%s'" % content)
        yield content.strip()


def parse_response_for_tag_contents(response, tagname):
    """
    returns the contents of the first xml tag matching tagname.
    """
    x = parse_response_for_tags_contents(response, tagname)

    logger.debug("parse response found: '%s'" % str(x))

    # return the first item from the generator
    try:
        return next(x)
    except StopIteration:
        return None


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
    """construct a soap request from a jinja template
    ¯\_(ツ)_/¯
    """
    op = operations[operation]

    data = create_soap_from_template(op["template"], **kwargs)

    headers = {}
    headers.update(default_headers)
    headers.update(op["headers"])

    request = requests.Request(
        "POST", build_uri(protocol, host, port, op["path"]), headers=headers, data=data
    )

    R = request.prepare()

    logger.debug(R.method, R.url, str(R.headers), str(R.body))

    # FIXME: maintain a session object for keepalive?
    S = requests.session()
    return S.send(R)
