import unittest
import os
from BDS.requester import BDSRequest

# Set up global variables.
request = BDSRequest(api_key=os.environ['API_KEY'])

# Create dummy response class.
class Response(object):
    def __init__(self, status_code, url, headers, text):
        self.status_code = status_code
        self.url = url
        self.headers = headers
        self.text = text
response = Response(200, "www.test.com", {}, "text")

class Test__check_model_feed(unittest.TestCase):
    def test_bad_model_feed(self):
        self.assertRaises(UserWarning, request._check_model_feed, "bad_feed")


class Test__check_service(unittest.TestCase):
    def test_bad_service(self):
        self.assertRaises(UserWarning, request._check_service, "bad_service",
                          "1.0")

    def test_bad_version(self):
        self.assertRaises(UserWarning, request._check_service, "WCS",
                          "bad_version")


class Test__check_api_key(unittest.TestCase):
    # See integration tests.
    pass


class Test__check_response_status(unittest.TestCase):
    def test_403_error(self):
        response.status_code = 403
        self.assertRaises(UserWarning, request._check_response_status, response)

    def test_404_error(self):
        response.status_code = 404
        self.assertRaises(UserWarning, request._check_response_status, response)

    def test_other_error(self):
        # Any status_code not 200 is considered an error.
        response.status_code = 101
        self.assertRaises(UserWarning, request._check_response_status,
                          response)


class Test__check_getCoverage_response(unittest.TestCase):
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
        self.assertRaises(UserWarning, request._check_getCoverage_response,
                          response)


class Test__check_dim_forecast(unittest.TestCase):
    def test_bad_dim_forecast(self):
        self.assertRaises(ValueError, request._check_dim_forecast, 24)


class Test__sort_grid_num(unittest.TestCase):
    def test_bad_grid_num(self):
        self.assertRaises(ValueError, request._sort_grid_num, 10.5)

    def test_returned_val_type(self):
        self.assertEqual(int, type(request._sort_grid_num(10.0)))
        self.assertEqual(int, type(request._sort_grid_num("10")))


class Test__sort_grid_size(unittest.TestCase):
    def test_bad_grid_size(self):
        self.assertRaises(ValueError, request._sort_grid_size, "big")

    def test_returned_val_type(self):
        self.assertEqual(float, type(request._sort_grid_size(1)))
        self.assertEqual(float, type(request._sort_grid_size("1.5")))


class Test__sort_time(unittest.TestCase):
    def test_bad_dates(self):
        self.assertRaises(ValueError, request._sort_time, "bad_date")

    def test_valid_dates(self):
        vaild_date = "2015-04-21T00:00:00Z"
        self.assertEqual(vaild_date, request._sort_time("2015-04-21T"))
        self.assertEqual(vaild_date, request._sort_time("21/4/2015"))
        self.assertEqual(vaild_date, request._sort_time("21st April 2015"))


class Test__sort_bbox(unittest.TestCase):
    def test_bad_type(self):
        # Must be a list (or tuple).
        self.assertRaises(UserWarning, request._sort_bbox, "not a list")

    def test_bad_length(self):
        # Must have four items.
        self.assertRaises(UserWarning, request._sort_bbox, [1,2,3])

    def test_bad_value(self):
        # Values must be numeric.
        self.assertRaises(UserWarning, request._sort_bbox, [1,2,3,"d"])

    def test_bad_format(self):
        # Must have format [x-min, y-min, x-max, y-max].
        self.assertRaises(UserWarning, request._sort_bbox, [10,20,1,2])

    def test_mix_type_values(self):
        # The type does not matter so long as values are numeric.
        self.assertEqual("1,2.2,3,4.4", request._sort_bbox(["1",2.2,3,"4.4"]))

    def test_return_str(self):
        self.assertEqual("1,2,3,4", request._sort_bbox([1,2,3,4]))


class Test__send_request(unittest.TestCase):
    # See integration tests.
    pass


class Test_getCapabilities(unittest.TestCase):
    # See integration tests.
    pass


class Test_describeCoverage(unittest.TestCase):
    # See integration tests.
    pass


class Test_getCoverage(unittest.TestCase):
    # See integration tests.
    pass


class Test_streamCoverageToAWS(unittest.TestCase):
    # See integration tests.
    pass


class Test_createCoverageCubes(unittest.TestCase):
    # See integration tests.
    pass


class Test_getParameterDictionary(unittest.TestCase):
    def setUp(self):
        super(Test_getParameterDictionary, self).setUp()
        self.format        = "NetCDF3"
        self.crs           = "EPSG:4326"
        self.elevation     = "0-1500m"
        self.bbox          = [-14.0, 7.0, 47.5, 61.0]
        self.dim_run       = "2015-04-22T00:00:00Z"
        self.time          = "2015-04-23T00:00:00Z"
        self.dim_forecast  = "PT12H"
        self.width         = 100
        self.height        = 100
        self.resx          = 0.5
        self.resy          = 0.5
        self.interpolation = "bilinear"

    def test_bad_time_spec(self):
        # Cannot specify times with all three time parameters.
        self.assertRaises(UserWarning, request.getParameterDictionary,
                          format=self.format, crs=self.crs,
                          elevation=self.elevation, dim_run=self.dim_run,
                          time=self.time, dim_forecast=self.dim_forecast)

    def test_bad_grid_spec(self):
        # Cannot specify width/height with resx/resy respectively.
        self.assertRaises(UserWarning, request.getParameterDictionary,
                          format=self.format, crs=self.crs,
                          elevation=self.elevation, width=self.width,
                          resx=self.resx)

        self.assertRaises(UserWarning, request.getParameterDictionary,
                          format=self.format, crs=self.crs,
                          elevation=self.elevation, height=self.height,
                          resy=self.resy)

    def test_returned_dict(self):
        # What the dict should look like.
        test_dict = {'CRS'       : self.crs,
                     'ELEVATION' : self.elevation,
                     'FORMAT'    : self.format,
                     'HEIGHT'    : self.height,
                     'WIDTH'     : self.width,
                     'DIM_RUN'   : self.dim_run,
                     'TIME'      : self.time}

        # Test against providing various valid formats. And check arguments
        # not specified (e.g. interpolation in this example) are not put in.
        param_dict = request.getParameterDictionary(format=self.format,
                                                     crs=self.crs,
                                                     elevation=self.elevation,
                                                     height="100",
                                                     width=100.0,
                                                     dim_run="22nd April 2015",
                                                     time="23/4/2015")
        self.assertEqual(sorted(test_dict.keys()),
                         sorted(param_dict.keys()))
        self.assertEqual(sorted(test_dict.values()),
                         sorted(param_dict.values()))

if __name__ == '__main__':
    unittest.main()
