import unittest
from webcoverageservice.builders import wcs2_builder

class Test_build_getCapabilities_req(unittest.TestCase):
    def test_return(self):
        req_dict = wcs2_builder.build_getCapabilities_req()
        self.assertEqual(req_dict["REQUEST"], "GetCapabilities")


class Test_build_describeCoverageCollection_req(unittest.TestCase):
    def test_return(self):
        req_dict = wcs2_builder.build_describeCoverageCollection_req("test_id",
                                                                     "1/2/3")
        self.assertEqual(req_dict["REQUEST"], "DescribeCoverageCollection")
        self.assertEqual(req_dict["CoverageCollectionId"], "test_id")
        self.assertEqual(req_dict["ReferenceTime"], "1/2/3")


class Test_build_describeCoverage_req(unittest.TestCase):
    pass


class Test_build_getCoverage_req(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
