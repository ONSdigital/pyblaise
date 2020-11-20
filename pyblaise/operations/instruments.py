"""
instrument resources

instruments are installed on blaise management nodes and replicated
to nodes with other roles in the serverparks.

They are an instance of a survey
"""
import logging

from pyblaise.soap_utils import (
    basic_soap_request,
    parse_response_for_tag_contents,
    parse_response_for_tags_contents,
)

from .exceptions import *

logger = logging.getLogger(__name__)


def get_list_of_instruments(protocol, host, port, token):
    R = basic_soap_request("get-list-of-instruments", protocol, host, port, TOKEN=token)
    logger.debug(R.text)

    has_instruments = parse_response_for_tag_contents(
        R.text, "GetListOfInstrumentsResult"
    )

    if not has_instruments:
        return R.status_code, []

    instruments = parse_response_for_tags_contents(has_instruments, "InstrumentMeta")

    data = [
        {
            "install-date": parse_response_for_tag_contents(instrument, "InstallDate"),
            "id": parse_response_for_tag_contents(instrument, "InstrumentId"),
            "name": parse_response_for_tag_contents(instrument, "InstrumentName"),
            "server-park": parse_response_for_tag_contents(instrument, "ServerPark"),
            "status": parse_response_for_tag_contents(instrument, "Status"),
        }
        for instrument in instruments
    ]

    return R.status_code, data


def remove_instrument(protocol, host, port, token, id, name, server_park):
    R = basic_soap_request(
        "remove-instrument",
        protocol,
        host,
        port,
        TOKEN=token,
        ID=id,
        NAME=name,
        SERVERPARK=server_park,
    )
    logger.debug(R.text)

    # parse
    removed = parse_response_for_tag_contents(R.text, "RemoveInstrumentResult")

    data = {
        "message": parse_response_for_tag_contents(removed, "Message"),
        "status_code": parse_response_for_tag_contents(removed, "Statuscode"),
    }

    return R.status_code, data
