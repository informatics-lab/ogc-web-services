from wcs.builders.wcs1_builder import build_getCapabilities_req,  \
                                      build_describeCoverage_req, \
                                      build_getCoverage_req
import requests

def send_request(requester, payload, stream=False):
    """
    Add the given payload to the existing parameters, send request and
    check response.

    """
    payload.update(requester.params)
    response = requests.get(requester.url, params=payload, stream=stream)
    return response

def send_getCapabilities_req(requester):
    """

    """
    payload = build_getCapabilities_req()
    return send_request(requester, payload)

def send_describeCoverage_req(requester, coverageId):
    """

    """
    payload = build_describeCoverage_req(coverageId)
    return send_request(requester, payload)

def send_getCoverage_req(requester, coverageID, **kwargs):
    """

    """
    stream = kwargs.pop("stream")
    payload = build_getCoverage_req(coverageID, **kwargs)
    return send_request(requester, payload, stream=stream)
