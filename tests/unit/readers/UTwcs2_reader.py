import unittest
import xml.etree.ElementTree as ET
from webcoverageservice.coverage import Coverage, CoverageList
from webcoverageservice.readers import wcs2_reader
from webcoverageservice.readers.xml_reader import get_elements

def file_to_string(filename):
    """
    Read file contents and return string.

    """
    with open(filename, "r") as infile:
        file_str = infile.read()
    return file_str

xml_simple    = file_to_string("tests/unit/wcs1_xml_examples/simple.xml")
xml_simple_ns = file_to_string("tests/unit/wcs1_xml_examples/simple_ns.xml")
xml_getCaps   = file_to_string("tests/unit/wcs2_xml_examples/getCapabilities.xml")
xml_desCov    = file_to_string("tests/unit/wcs2_xml_examples/describeCoverage.xml")
xml_error     = file_to_string("tests/unit/wcs1_xml_examples/error.xml")

xml_simple_root    = ET.fromstring(xml_simple)
xml_simple_ns_root = ET.fromstring(xml_simple_ns)
xml_getCaps_root   = ET.fromstring(xml_getCaps)
# All data lives under the first (and only) element of describeCoverage.xml
xml_desCov_root    = ET.fromstring(xml_desCov)[0]
xml_error_root     = ET.fromstring(xml_error)


class Test_read_getCapabilities_res(unittest.TestCase):
    def test_returned_type(self):
        covs = wcs2_reader.read_getCapabilities_res(xml_getCaps)
        self.assertEqual(type(covs), CoverageList)


class Test_read_describeCoverage_res(unittest.TestCase):
    def test_returned_type(self):
        cov = wcs2_reader.read_describeCoverage_res(xml_desCov)
        self.assertEqual(type(cov), Coverage)


class Test_ResponseReader(unittest.TestCase):
    pass


class Test__get_bbox(unittest.TestCase):
    def setUp(self):
        self.reader = wcs2_reader.CoverageReader(xml_desCov)

    def test_return_val(self):
        expected_bbox = [-14.0, 47.5, 7.0, 61.0]
        bbox = self.reader._get_bbox(self.reader.root,
                                     namespace=self.reader.gml)
        self.assertEqual(bbox, expected_bbox)

    def test_bad_root(self):
        # There is no bbox in root element of simple.xml
        self.assertRaises(UserWarning, self.reader._get_bbox,
                          xml_simple_root)


class Test_CapabilitiesReader(unittest.TestCase):
    pass


class Test_get_coverages(unittest.TestCase):
    def setUp(self):
        self.reader = wcs2_reader.CapabilitiesReader(xml_getCaps)

    def test_return_val(self):
        covs = self.reader.get_coverages()
        self.assertNotEqual(len(covs), 0)
        self.assertEqual(type(covs), CoverageList)


if __name__ == '__main__':
    unittest.main()
