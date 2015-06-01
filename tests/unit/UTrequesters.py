import unittest
import os
from webcoverageservice import _Requester, WCS1Requester, WCS2Requester

# Create dummy response class.
class Response(object):
    def __init__(self, status_code, url, headers, text):
        self.status_code = status_code
        self.url = url
        self.headers = headers
        self.text = text
response = Response(200, "test_response_url", {}, "text")


class Test__Requester(unittest.TestCase):
    def setUp(self):
        self.request = _Requester(url="test_url", wcs_version="0.0")


class Test__check_api_key(Test__Requester):
    # See integration tests.
    pass


class Test__check_response_status(Test__Requester):
    def test_403_error(self):
        response.status_code = 403
        self.assertRaises(UserWarning, self.request._check_response_status, response)

    def test_404_error(self):
        response.status_code = 404
        self.assertRaises(UserWarning, self.request._check_response_status, response)

    def test_other_error(self):
        # Any status_code not 200 is considered an error.
        response.status_code = 101
        self.assertRaises(UserWarning, self.request._check_response_status,
                          response)


class Test__check_getCoverage_response(Test__Requester):
    def test_xml_response(self):
        # If getCoverage returns an XML response, an error has occured. The
        # response header specifies the type of response. Check XML raises an
        # error.
        response.headers["content-type"] = "text/xml"
        # Added dummy xml string.
        response.text = '<?xml version="1.0" encoding="UTF-8"?>'\
        '<ExceptionReport version="1.0" xmlns="http://www.opengis.net/ows">'\
          '<Exception exceptionCode="CoverageNotDefined">'\
            '<ExceptionText>Test error</ExceptionText>'\
          '</Exception>'\
        '</ExceptionReport>'
        self.assertRaises(UserWarning,
                          self.request._check_getCoverage_response,
                          response)


class Test_getCapabilities(Test__Requester):
    # See integration tests.
    pass


class Test_describeCoverage(Test__Requester):
    # See integration tests.
    pass


class Test_WCS1Requester(unittest.TestCase):
    pass


class Test_WCS1getCoverage(unittest.TestCase):
    # See integration tests.
    pass


class Test_WCS2Requester(unittest.TestCase):
    pass


class Test_describeCoverageCollection(unittest.TestCase):
    # See integration tests.
    pass


class Test_WCS2getCoverage(unittest.TestCase):
    # See integration tests.
    pass


if __name__ == '__main__':
    unittest.main()
