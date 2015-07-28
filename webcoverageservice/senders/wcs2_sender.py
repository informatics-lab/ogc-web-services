"""
Send WCS2 requests.

"""
from webcoverageservice.builders.wcs2_builder import \
     build_getCapabilities_req,                      \
     build_describeCoverageCollection_req,           \
     build_describeCoverage_req,                     \
     build_getCoverage_req
from webcoverageservice.senders.sender import send_get_request, \
                                              send_post_request

def send_getCapabilities_req(requester):
    params = build_getCapabilities_req()
    return send_get_request(requester, params)

def send_describeCoverageCollection_req(requester, collection_id, ref_time):
    params = build_describeCoverageCollection_req(collection_id, ref_time)
    return send_get_request(requester, params)

def send_describeCoverage_req(requester, coverage_id):
    payload = build_describeCoverage_req(coverage_id)
    return send_post_request(requester, payload)

def send_getCoverage_req(requester, coverage_id, components, stream=False,
                         **kwargs):
    savepath_xml_req = kwargs.pop("savepath_xml_req")
    payload = build_getCoverage_req(coverage_id, components, **kwargs)

    if savepath_xml_req is not None:
        with open(savepath_xml_req, 'w') as outfile:
            outfile.write(payload)

    return send_post_request(requester, payload, stream=stream)
