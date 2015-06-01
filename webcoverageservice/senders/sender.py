"""
Send get and post requests, tailored for WCS requests.

"""
import requests

def send_get_request(requester, params={}, stream=False):
    """
    Add the given parameters to the existing parameters, send request and
    check response.

    Args:

    * requester: wcs.Requester

    Kwargs:

    * params: dictionary

    * stream: boolean
        If False (default), the response content will be immediately
        downloaded.

    returns:
        requests.response

    """
    params.update(requester.params)
    response = requests.get(requester.url, params=params, stream=stream)
    return response

def send_post_request(requester, payload, params={}, stream=False):
    """
    Add the given parameters to the existing parameters, send request with
    payload and check response.

    Args:

    * requester: wcs.Requester

    * payload: string
        The data to be posted to the url, e.g. an XML file.

    Kwargs:

    * params: dictionary

    * stream: boolean
        If False (default), the response content will be immediately
        downloaded.

    returns:
        requests.response

    """
    params.update(requester.params)
    response = requests.post(requester.url, data=payload, params=params,
                             stream=stream,
                             headers={'Content-Type': 'application/xml'})
    return response
