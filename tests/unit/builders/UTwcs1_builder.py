import unittest
from webcoverageservice.builders import wcs1_builder

class Test_build_getCapabilities_req(unittest.TestCase):
    def test_return(self):
        req_dict = wcs1_builder.build_getCapabilities_req()
        self.assertEqual(req_dict["REQUEST"], "GetCapabilities")


class Test_build_describeCoverage_req(unittest.TestCase):
    def test_return(self):
        req_dict = wcs1_builder.build_describeCoverage_req("test_id")
        self.assertEqual(req_dict["REQUEST"], "DescribeCoverage")
        self.assertEqual(req_dict["COVERAGE"], "test_id")


class Test_build_getCoverage_req(unittest.TestCase):
    def setUp(self):
        self.coverage_id   = "test_id"
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
        self.assertRaises(UserWarning, wcs1_builder.build_getCoverage_req,
                          self.coverage_id, dim_run=self.dim_run,
                          time=self.time, dim_forecast=self.dim_forecast)

    def test_bad_grid_spec(self):
        # Cannot specify width/height with resx/resy respectively.
        self.assertRaises(UserWarning, wcs1_builder.build_getCoverage_req,
                          self.coverage_id, width=self.width, resx=self.resx)

        self.assertRaises(UserWarning, wcs1_builder.build_getCoverage_req,
                          self.coverage_id, height=self.height, resy=self.resy)

    def test_returned_dict(self):
        # What the dict should look like.
        test_dict = {'REQUEST'   : "GetCoverage",
                     'COVERAGE'  : self.coverage_id,
                     'CRS'       : self.crs,
                     'ELEVATION' : self.elevation,
                     'FORMAT'    : self.format,
                     'HEIGHT'    : self.height,
                     'WIDTH'     : self.width,
                     'DIM_RUN'   : self.dim_run,
                     'TIME'      : self.time}

        # Test against providing various valid formats. And check arguments
        # not specified (e.g. interpolation in this example) are not put in.
        param_dict = wcs1_builder.build_getCoverage_req(
                                  self.coverage_id,
                                  format=self.format,
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
