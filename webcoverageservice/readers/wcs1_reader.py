"""
Module containing functions for reading XML responses from WCS1 requests.

"""
from webcoverageservice.readers.xml_reader import get_elements, \
                                                  get_elements_text, read_xml
from webcoverageservice.coverage import Coverage, CoverageList

def read_getCapabilities_res(xml_str):
    """
    Extract all coverage information from xml (given as string) returned
    by getCapabilities request and return as CoverageList object.

    Args:

    * xml_str: string
        The xml as a string.

    returns
        CoverageList

    """
    reader = CapabilitiesReader(xml_str)
    return reader.get_coverages()

def read_describeCoverage_res(xml_str):
    """
    Extract coverage information from xml (given as string) returned by
    describeCoverage request and return as Coverage object.

    Args:

    * xml_str: string
        The xml as a string.

    returns
        Coverage

    """
    reader = CoverageReader(xml_str)
    return reader.get_coverage()

class ResponseReader(object):
    """
    Read XML returned from WCS1.

    """
    def __init__(self, xml_str):
        self.root  = read_xml(xml_str)
        self.xmlns = "http://www.opengis.net/wcs"

    @staticmethod
    def _get_bbox(root, namespace=None):
        """
        There are two elements within the LonLatEnvelope element, the first is
        the longitude min and max, the second is the latitude. Extact this data
        and return a a list.

        returns:
            list

        """
        lon_lat_elem = get_elements("lonLatEnvelope", root, single_elem=True,
                                    namespace=namespace)
        lon_vals = lon_lat_elem[0].text.split()
        lat_vals = lon_lat_elem[1].text.split()
        return [float(lon_vals[0]), float(lat_vals[0]),
                float(lon_vals[1]), float(lat_vals[1])]

class CapabilitiesReader(ResponseReader):
    """
    Read getCapabilities response.

    """
    def get_coverages(self):
        cov_elems = get_elements("ContentMetadata/CoverageOffering", self.root,
                                 namespace=self.xmlns)
        coverages = []
        for cov_elem in cov_elems:
            name = get_elements_text("name", cov_elem, single_elem=True,
                                     namespace=self.xmlns)
            label = get_elements_text("label", cov_elem, single_elem=True,
                                      namespace=self.xmlns)
            bbox = self._get_bbox(cov_elem, namespace=self.xmlns)
            coverages.append(Coverage(name=name, label=label, bbox=bbox))

        return CoverageList(coverages)

class CoverageReader(ResponseReader):
    """
    Read describeCoverage response.

    """
    def __init__(self, xml_str):
        super(CoverageReader, self).__init__(xml_str)
        # For the describeCoverage xml, only one coverage element is returned
        # under the root.
        self.root = get_elements("CoverageOffering", self.root,
                                 single_elem=True, namespace=self.xmlns)

    def _get_values(self, root, namespace=None):
        """
        Values are given under the element path "values/singleValue". Given a root
        element, extract all values and return in list.

        Args:

        * root: xml.etree.ElementTree.Element
            The element inside which the values are nested.

        Kwargs:

        * single_elem: boolean
            If True, this raises an error if more than one element is found. It
            also changes the return type to a single value (instead of list).

        * namespace: string or None
            The xml namespace for the value element.

        returns:
            list of strings or string (if single_elem=True)


        """
        return get_elements_text("values/singleValue", root,
                                 namespace=namespace)

    def _get_axis_describer_values(self, name, root, namespace=None):
        """
        Get all elements that come under the AxisDescription element;
        e.g. initialisation, forecast time, elevation.

        Args:

        * name: string
            The name of the axis describer.

        * root: xml.etree.ElementTree.Element
            The element inside which the values are nested.

        Kwargs:

        * namespace: string or None
            The xml namespace for the AxisDescription element.

        """
        axis_elems = get_elements("rangeSet/RangeSet/axisDescription/"\
                                  "AxisDescription",
                                  root, namespace=namespace)
        for axis_elem in axis_elems:
            elem_name = get_elements_text("name", root=axis_elem,
                                          single_elem=True,
                                          namespace=namespace)
            if elem_name == name:
                return self._get_values(axis_elem, namespace=namespace)
        return []

    def get_name(self):
        return get_elements_text("name", self.root, single_elem=True,
                                 namespace=self.xmlns)

    def get_label(self):
        return get_elements_text("label", self.root, single_elem=True,
                                  namespace=self.xmlns)

    def get_bbox(self):
        """
        There are two elements within the LonLatEnvelope element, the first is
        the longitude min and max, the second is the latitude. Extact this data
        and return a a list.

        returns:
            list

        """
        return self._get_bbox(self.root, self.xmlns)

    def get_dim_runs(self):
        return self._get_axis_describer_values("DIM_RUN", self.root,
                                               namespace=self.xmlns)

    def get_dim_forecasts(self):
        return self._get_axis_describer_values("DIM_FORECAST", self.root,
                                               namespace=self.xmlns)

    def get_times(self):
        return self._get_axis_describer_values("TIME", self.root,
                                               namespace=self.xmlns)

    def get_elevations(self):
        return self._get_axis_describer_values("ELEVATION", self.root,
                                               namespace=self.xmlns)

    def get_CRSs(self):
        return get_elements_text("supportedCRSs/requestCRSs", self.root,
                                 namespace=self.xmlns)

    def get_formats(self):
        return get_elements_text("supportedFormats/formats", self.root,
                                 namespace=self.xmlns)

    def get_interpolations(self):
        return get_elements_text("supportedInterpolations/interpolationMethod",
                                 self.root, namespace=self.xmlns)

    def get_coverage(self):
        name       = self.get_name()
        label      = self.get_label()
        bbox       = self.get_bbox()
        dim_runs   = self.get_dim_runs()
        dim_fcsts  = self.get_dim_forecasts()
        times      = self.get_times()
        elevations = self.get_elevations()
        CRSs       = self.get_CRSs()
        formats    = self.get_formats()
        interps    = self.get_interpolations()

        return Coverage(name=name, label=label, bbox=bbox, dim_runs=dim_runs,
                        dim_forecasts=dim_fcsts, times=times,
                        elevations=elevations, CRSs=CRSs, formats=formats,
                        interpolations=interps)
