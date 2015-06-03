"""
Testing is done on example xml files found in xml_examples directory. These can
be referred to to check what is being tested.

"""
import unittest
import xml.etree.ElementTree as ET
from webcoverageservice.coverage import Coverage, CoverageList
from webcoverageservice.readers import xml_reader

def file_to_string(filename):
    """
    Read file contents and return string.

    """
    with open(filename, "r") as infile:
        file_str = infile.read()
    return file_str

xml_example_dir = "tests/unit/readers/xml_examples/"
xml_simple    = file_to_string(xml_example_dir + "simple.xml")
xml_simple_ns = file_to_string(xml_example_dir + "simple_ns.xml")
xml_getCaps   = file_to_string(xml_example_dir + "getCapabilities.xml")
xml_desCov    = file_to_string(xml_example_dir + "describeCoverage.xml")
xml_error     = file_to_string(xml_example_dir + "error.xml")

xml_simple_root    = ET.fromstring(xml_simple)
xml_simple_ns_root = ET.fromstring(xml_simple_ns)
xml_getCaps_root   = ET.fromstring(xml_getCaps)
# All data lives under the first (and only) element of describeCoverage.xml
xml_desCov_root    = ET.fromstring(xml_desCov)[0]
xml_error_root     = ET.fromstring(xml_error)

class Test_read_xml(unittest.TestCase):
    def test_returned_val(self):
        root = xml_reader.read_xml(xml_getCaps)
        self.assertEqual(ET.tostring(root), ET.tostring(xml_getCaps_root))

    def test_bad_xml(self):
        self.assertRaises(UserWarning, xml_reader.read_xml, xml_error)


class Test_check_xml(unittest.TestCase):
    def test_good_xml(self):
        xml_reader.check_xml(xml_desCov_root)

    def test_bad_xml(self):
        self.assertRaises(UserWarning, xml_reader.check_xml, xml_error_root,
                          xml_reader.ERR_XMLNS)


class Test_get_elements(unittest.TestCase):
    def test_simple_path(self):
        # Get first element under the root, this is elemOne.
        required_elem = xml_simple_root[0]
        found_elems  = xml_reader.get_elements("elemOne", xml_simple_root)
        # get_elements returns a list, there is only one elemTwo element.
        self.assertEqual(found_elems[0], required_elem)

    def test_single_elem(self):
        required_elem = xml_simple_root[0]
        # If single_elem true, a single element (not a list) should be
        # returned.
        founds_elem = xml_reader.get_elements("elemOne", xml_simple_root,
                                   single_elem=True)
        self.assertEqual(founds_elem, required_elem)

        # An error should be raised if more than one are found.
        self.assertRaises(UserWarning, xml_reader.get_elements,
                          "elemTwo/values/singleValue", xml_simple_root,
                          single_elem=True)

    def test_namespace(self):
        # Get first element under the root, this is elemOne.
        required_elem = xml_simple_ns_root[0]
        # This xml has a namespace called "test_namespace".
        found_elems  = xml_reader.get_elements("elemOne", xml_simple_ns_root,
                                    namespace="test_namespace")
        # get_elements returns a list, there is only one elemOne element.
        self.assertEqual(found_elems[0], required_elem)

        # Nothing should be returned if namespace not given.
        found_elems  = xml_reader.get_elements("elemOne", xml_simple_ns_root)
        self.assertEqual(found_elems, [])


class Test_get_elements_text(unittest.TestCase):
    def test_simple_text(self):
        found_text = xml_reader.get_elements_text("elemTwo/name", xml_simple_root)
        self.assertEqual(found_text[0], "Element 2")

    def test_single_elem(self):
        # If single_elem true, a single string (not a list) should be
        # returned.
        found_text = xml_reader.get_elements_text("elemTwo/name", xml_simple_root,
                                       single_elem=True)
        self.assertEqual(found_text, "Element 2")

        # An error should be raised if more than one are found.
        self.assertRaises(UserWarning, xml_reader.get_elements_text,
                          "elemTwo/values/singleValue", xml_simple_root,
                          single_elem=True)

    def test_no_text(self):
        # If an element contains no text, an error should be raised.
        self.assertRaises(UserWarning, xml_reader.get_elements_text, "elemTwo",
                          xml_simple_root)


class Test_get_elements_attr(unittest.TestCase):
    pass


class Test_add_namespace(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
