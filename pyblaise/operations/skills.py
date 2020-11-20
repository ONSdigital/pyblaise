"""
skills resource

I don't know what skills are
"""
import logging

from pyblaise.soap_utils import (
    basic_soap_request,
    parse_response_for_tag
)

from .exceptions import *

logger = logging.getLogger(__name__)


def get_skills(protocol, host, port, token):
    R = basic_soap_request("get-skills", protocol, host, port, TOKEN=token)
    logger.debug(R.text)
    has_skills = parse_response_for_tag(R.text, "GetSkillsResponse")
    skills = []

    return R.status_code, skills
