"""
Send WCS1 requests.

"""
from wcs.builders.wcs1_builder import build_getCapabilities_req,  \
                                      build_describeCoverage_req, \
                                      build_getCoverage_req
from wcs.senders.sender import send_get_request

def send_getCapabilities_req(requester):
    payload = build_getCapabilities_req()
    return send_get_request(requester, payload)

def send_describeCoverage_req(requester, coverage_id):
    payload = build_describeCoverage_req(coverage_id)
    return send_get_request(requester, payload)

def send_getCoverage_req(requester, coverage_id, stream=False, **kwargs):
    payload = build_getCoverage_req(coverage_id, **kwargs)
    return send_get_request(requester, payload, stream=stream)
