"""
Testing is done on example xml files found in xml_examples directory. These can
be referred to to check what is being tested.

"""
import unittest
import xml.etree.ElementTree as ET
from BDS.coverage import Coverage, CoverageList
from BDS.xml_reader import *

def file_to_string(filename):
    """
    Read file contents and return string.

    """
    with open(filename, "r") as infile:
        file_str = infile.read()
    return file_str

xml_simple    = file_to_string("tests/unit/xml_examples/simple.xml")
xml_simple_ns = file_to_string("tests/unit/xml_examples/simple_ns.xml")
xml_getCaps   = file_to_string("tests/unit/xml_examples/getCapabilities.xml")
xml_desCov    = file_to_string("tests/unit/xml_examples/describeCoverage.xml")
xml_error     = file_to_string("tests/unit/xml_examples/error.xml")

xml_simple_root    = ET.fromstring(xml_simple)
xml_simple_ns_root = ET.fromstring(xml_simple_ns)
xml_getCaps_root   = ET.fromstring(xml_getCaps)
# All data lives under the first (and only) element of describeCoverage.xml
xml_desCov_root    = ET.fromstring(xml_desCov)[0]
xml_error_root     = ET.fromstring(xml_error)


class Test_get_elements(unittest.TestCase):
    def test_simple_path(self):
        # Get first element under the root, this is elemOne.
        required_elem = xml_simple_root[0]
        found_elems  = get_elements("elemOne", xml_simple_root)
        # get_elements returns a list, there is only one elemTwo element.
        self.assertEqual(found_elems[0], required_elem)

    def test_single_elem(self):
        required_elem = xml_simple_root[0]
        # If single_elem true, a single element (not a list) should be
        # returned.
        founds_elem = get_elements("elemOne", xml_simple_root,
                                   single_elem=True)
        self.assertEqual(founds_elem, required_elem)

        # An error should be raised if more than one are found.
        self.assertRaises(UserWarning, get_elements,
                          "elemTwo/values/singleValue", xml_simple_root,
                          single_elem=True)

    def test_namespace(self):
        # Get first element under the root, this is elemOne.
        required_elem = xml_simple_ns_root[0]
        # This xml has a namespace called "test_namespace".
        found_elems  = get_elements("elemOne", xml_simple_ns_root,
                                    namespace="test_namespace")
        # get_elements returns a list, there is only one elemOne element.
        self.assertEqual(found_elems[0], required_elem)

        # Nothing should be returned if namespace not given.
        found_elems  = get_elements("elemOne", xml_simple_ns_root)
        self.assertEqual(found_elems, [])


class Test_get_elements_text(unittest.TestCase):
    def test_simple_text(self):
        found_text = get_elements_text("elemTwo/name", xml_simple_root)
        self.assertEqual(found_text[0], "Element 2")

    def test_single_elem(self):
        # If single_elem true, a single string (not a list) should be
        # returned.
        found_text = get_elements_text("elemTwo/name", xml_simple_root,
                                       single_elem=True)
        self.assertEqual(found_text, "Element 2")

        # An error should be raised if more than one are found.
        self.assertRaises(UserWarning, get_elements_text,
                          "elemTwo/values/singleValue", xml_simple_root,
                          single_elem=True)

    def test_no_text(self):
        # If an element contains no text, an error should be raised.
        self.assertRaises(UserWarning, get_elements_text, "elemTwo",
                          xml_simple_root)


class Test_get_bbox(unittest.TestCase):
    def test_returned_val(self):
        expected_bbox = [-10, 0, 10, 20]
        # The bbox (lonLatEnvelope) element must be directly under the given
        # root.
        root_elem = get_elements("elemThree", xml_simple_root, single_elem=True)
        bbox = get_bbox(root_elem, namespace=None)
        self.assertEqual(bbox, expected_bbox)

    def test_bad_root(self):
        # There is no bbox in root element of simple.xml
        self.assertRaises(UserWarning, get_bbox, xml_simple_root)


class Test_get_values(unittest.TestCase):
    def test_returned_vals(self):
        expected_vals = ["1","2","3"]
        # The values live under elemTwo.
        root_elem = get_elements("elemTwo", xml_simple_root, single_elem=True)
        vals = get_values(root_elem, namespace=None)
        self.assertEqual(vals, expected_vals)


class Test_get_axis_describer_values(unittest.TestCase):
    # This function is for looking at XML files returned by BDS so use example
    # describeCoverage.xml given by xml_desCov_root.
    def test_returned_vals(self):
        expected_vals = ['4500-4400m']
        vals = get_axis_describer_values("ELEVATION", xml_desCov_root)
        self.assertEquals(vals, expected_vals)


class Test_check_xml(unittest.TestCase):
    def test_good_xml(self):
        check_xml(xml_desCov_root)

    def test_bad_xml(self):
        self.assertRaises(UserWarning, check_xml, xml_error_root)


class Test_read_xml(unittest.TestCase):
    def test_returned_val(self):
        root = read_xml(xml_getCaps)
        self.assertEqual(ET.tostring(root), ET.tostring(xml_getCaps_root))

    def test_bad_xml(self):
        self.assertRaises(UserWarning, read_xml, xml_error)


class Test_read_describeCoverage_xml(unittest.TestCase):
    def test_returned_type(self):
        cov = read_describeCoverage_xml(xml_desCov)
        self.assertEqual(type(cov), Coverage)


class Test_read_getCapabilities_xml(unittest.TestCase):
    def test_returned_type(self):
        covs = read_getCapabilities_xml(xml_getCaps)
        self.assertEqual(type(covs), CoverageList)


if __name__ == '__main__':
    unittest.main()
