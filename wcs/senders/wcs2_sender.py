from wcs.builders.wcs2_builder import build_getCapabilities_req,            \
                                      build_describeCoverageCollection_req, \
                                      build_describeCoverage_req,           \
                                      build_getCoverage_req
import requests

def send_get_request(requester, params={}, stream=False):
    """
    Add the given payload to the existing parameters, send request and
    check response.

    """
    params.update(requester.params)
    response = requests.get(requester.url, params=params, stream=stream)
    return response

def send_post_request(requester, payload, params={}, stream=False):
    """

    """
    params.update(requester.params)
    response = requests.post(requester.url, data=payload, params=params,
                             stream=stream,
                             headers={'Content-Type': 'application/xml'})
    return response

def save_request_payload(payload, savepath):
    """

    """
    with open(savepath, "w") as outfile:
        outfile.write(payload)

def send_getCapabilities_req(requester):
    """

    """
    params = build_getCapabilities_req()
    return send_get_request(requester, params)

def send_describeCoverageCollection_req(requester, collection_id, ref_time):
    """

    """
    params = build_describeCoverageCollection_req(collection_id, ref_time)
    return send_get_request(requester, params)


def send_describeCoverage_req(requester, coverage_id):
    """

    """
    payload = build_describeCoverage_req(coverage_id)
    return send_post_request(requester, payload)


def send_getCoverage_req(requester, coverage_id, components, **kwargs):
    """

    """
    stream = kwargs.pop("stream")
    payload = build_getCoverage_req(coverage_id, components, **kwargs)
    return send_post_request(requester, payload, stream=stream)
