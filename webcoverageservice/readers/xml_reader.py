"""
Module for reading XML files, tailored towards WCS responses.

"""
import xml.etree.ElementTree as ET

ERR_XMLNS = "http://www.opengis.net/ows"

def read_xml(xml_str):
    """
    Read in XML string and check for error response.

    Args:

    * xml_str: string
        The xml as a string.

    returns:
        xml.etree.ElementTree.Element

    """
    root = ET.fromstring(xml_str)
    check_xml(root, namespace=ERR_XMLNS)
    return root

def check_xml(root, namespace=None):
    """
    Check the XML is not the error response.

    Args:

    * root: xml.etree.ElementTree.Element

    Kwargs:

    * namespace: string or None
        The xml namespace for the given path.

    """
    if namespace:
        error_tag = "{%s}ExceptionReport" % namespace
    else:
        error_tag = "ExceptionReport"
    if root.tag.strip() == error_tag:
        err_mess = get_elements_text("Exception/ExceptionText", root,
                                     single_elem=True, namespace=namespace)
        raise UserWarning(err_mess)

def get_elements(path, root, single_elem=False, namespace=None):
    """
    Extract elements at given xml path.

    Args:

    * path: string
        The path (in terms of nested elements) to the required element.

    * root: xml.etree.ElementTree.Element
        The element from which the given path starts.

    Kwargs:

    * single_elem: boolean
        If True, this raises an error if more than one (or no) element is
        found. It also changes the return type to a single value (instead of
        list).

    * namespace: string or None
        The xml namespace for the given path.

    returns:
        Single (if single_elem=True) or list of xml.etree.ElementTree.Element
        object(s).

    """
    if namespace:
        path = add_namespace(path, namespace)
    elems = root.findall(path)

    if single_elem:
        if len(elems) == 1:
            return elems[0]
        else:
            raise UserWarning("Expected to find exactly 1 {path} element,"\
                              " but found {fnd} instead."\
                              .format(path=path, fnd=len(elems)))
    else:
        return elems

def get_elements_text(path, root, single_elem=False, namespace=None):
    """
    Extract elements' text at given xml path.

    Args:

    * path: string
        The path (in terms of nested elements) to the required element.

    * root: xml.etree.ElementTree.Element
        The element from which the given path starts.

    Kwargs:

    * single_elem: boolean
        If True, this raises an error if more than one element is found. It
        also changes the return type to a single value (instead of list).

    * namespace: string or None
        The xml namespace for the given path.

    returns:
        list of strings or string (if single_elem=True)

    """
    elememts = get_elements(path, root, single_elem=single_elem,
                            namespace=namespace)
    if single_elem:
        # Put single element in list so the same code can be used to do text
        # checks.
        elememts = [elememts]
    elems_text = [elem.text.strip() for elem in elememts]

    # Not all elements contain text, so this must be checked.
    no_txt_count = elems_text.count("")
    if no_txt_count != 0:
        if no_txt_count == len(elems_text):
            raise UserWarning("{path} element(s) do not contain text."\
                              .format(path=path))
        else:
            elems_text = [txt for txt in elems_text if txt != ""]
            print "Warning! This is strange, {cnt} out of {tot} {path} "\
                  "elements contain text (normally its all or none!)."\
                  "\nThe element(s) with no text have not been returned."\
                  .format(cnt=len(elems_text) - no_txt_count,
                          tot=len(elems_text),
                          path=path)

    if single_elem:
        return elems_text[0]
    else:
        return elems_text

def get_elements_attr(name, elem, namespace=None):
    """
    Return the value of the named attribute.

    Args:

    * name: string
        The attribute name

    * elem: xml.etree.ElementTree.Element
        The elememt of the attribute.

    Kwargs:

    * namespace: string or None
        The xml namespace for the given path.


    """
    if namespace:
        name = add_namespace(name, namespace)
    attr = elem.attrib.get(name)
    if not attr:
        raise UserWarning("No attribute called {name} found in element."\
                          .format(name=name))
    return attr


def add_namespace(path, namespace):
    """
    Add namespace to each path element.

    Args:

    * path: string
        The element path.

    * namespace: string
        The xml namespace for the given path.

    """
    namespace = "{%s}" % namespace
    path = path.split('/')
    path = [namespace + elem_name for elem_name in path]
    return "/".join(path)
