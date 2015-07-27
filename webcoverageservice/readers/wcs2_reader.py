"""
Module containing functions for reading XML responses from WCS2 requests.

"""
from webcoverageservice.readers.xml_reader import get_elements, \
                                                  get_elements_text, \
                                                  get_elements_attr, read_xml
from webcoverageservice.coverage import Coverage, CoverageList, \
                                        CoverageCollection

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

def read_describeCoverageCollection_res(xml_str):
    """
    Extract coverage collection information from xml (given as string) returned
    by describeCoverageCollection request and return as Coverage object.

    Args:

    * xml_str: string
        The xml as a string.

    returns
        Coverage

    """
    reader = CollectionReader(xml_str)
    return reader.get_coverage_collection()

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
    Read XML returned from WCS2.

    """
    def __init__(self, xml_str):
        self.root     = read_xml(xml_str)
        self.ows      = "http://www.opengis.net/ows/2.0"
        self.wcs      = "http://www.opengis.net/wcs/2.0"
        self.metocean = "http://def.wmo.int/metce/2013/metocean"
        self.gml      = "http://www.opengis.net/gml/3.2"
        self.gmlcov   = "http://www.opengis.net/gmlcov/1.0"
        self.xlink    = "http://www.w3.org/1999/xlink"
        self.om       = "http://www.opengis.net/om/2.0"
        self.sam      = "http://www.opengis.net/sampling/2.0"
        self.sams     = "http://www.opengis.net/samplingSpatial/2.0"

    @staticmethod
    def _bbox_as_list(lower_vals, upper_vals):
        """
        Return the values from bbox elements as floats and in the format
        [x-min, y-min, x-max, y-max].

        """
        lower_vals = lower_vals.split()
        upper_vals = upper_vals.split()
        return [float(lower_vals[0]), float(lower_vals[1]),
                float(upper_vals[0]), float(upper_vals[1])]

    def _get_bbox(self, root, namespace=None):
        """
        Extact the bounding spatial values and return in a list.

        returns:
            list

        """
        bbox_lower = get_elements_text("boundedBy/Envelope/lowerCorner",
                                       root, single_elem=True,
                                       namespace=namespace)
        bbox_upper = get_elements_text("boundedBy/Envelope/upperCorner",
                                       root, single_elem=True,
                                       namespace=namespace)
        return self._bbox_as_list(bbox_lower, bbox_upper)

class CapabilitiesReader(ResponseReader):
    """
    Read getCapabilities response.

    """
    def get_address(self):
        op_meta_elem = get_elements("OperationsMetadata", self.root,
                                    single_elem=True, namespace=self.ows)
        op_elems = get_elements("Operation", op_meta_elem, namespace=self.ows)
        # Just use firt element.
        get_elem = get_elements("DCP/HTTP/Get", op_elems[0], single_elem=True,
                                namespace=self.ows)
        return get_elements_attr("href", get_elem, namespace=self.xlink)

    def get_operations(self):
        op_meta_elem = get_elements("OperationsMetadata", self.root,
                                    single_elem=True, namespace=self.ows)
        op_elems = get_elements("Operation", op_meta_elem, namespace=self.ows)
        operations = [elem.attrib["name"] for elem in op_elems]
        return operations

    def get_coverage_ids(self):
        contents_elem = get_elements("Contents", self.root, single_elem=True,
                                     namespace=self.wcs)
        return get_elements_text("CoverageSummary/CoverageId", contents_elem,
                                 namespace=self.wcs)

    def _get_collection_summary_elems(self):
        extension_elem = get_elements("Contents/Extension", self.root,
                                      single_elem=True, namespace=self.wcs)
        col_summary_elems = get_elements("CoverageCollectionSummary",
                                         extension_elem,
                                         namespace=self.metocean)
        return col_summary_elems

    def _get_collection_id(self, col_elem):
        return get_elements_text("coverageCollectionId", col_elem,
                                 single_elem=True,
                                 namespace=self.metocean)

    def _get_reference_times(self, root):
        ref_time_elem = get_elements("referenceTimeList/ReferenceTime",
                                     root, single_elem=True,
                                     namespace=self.metocean)
        return get_elements_text("timePosition", ref_time_elem,
                                 namespace=self.gml)

    def get_coverages(self):
        covs = self.get_coverage_ids()
        return CoverageList([Coverage(cov) for cov in covs])

    def get_coverage_collections(self):
        col_summary_elems = self._get_collection_summary_elems()
        cov_collections = []
        for col_elem in col_summary_elems:
            col_id = self._get_collection_id(col_elem)
            col_bbox = self._get_bbox(col_elem, namespace=self.gml)
            col_ref_times = self._get_reference_times(col_elem)
            cov_collections.append(CoverageCollection(col_id, col_bbox,
                                                      col_ref_times))
        return cov_collections

class CollectionReader(ResponseReader):
    """
    Read getCoverageCollection response.

    """
    def __init__(self, xml_str):
        super(CollectionReader, self).__init__(xml_str)
        # Describe coverage XML only contains one coverage description.
        self.root = get_elements("CoverageCollectionDescription", self.root,
                                 single_elem=True, namespace=self.metocean)

    def get_collection_id(self):
        return get_elements_text("coverageCollectionId", self.root,
                                 single_elem=True, namespace=self.metocean)

    def get_bbox(self):
        return self._get_bbox(self.root, namespace=self.gml)

    def get_ref_time(self):
        ref_time_elem = get_elements("referenceTime", self.root,
                                     single_elem=True,
                                     namespace=self.metocean)
        return get_elements_text("TimeInstant/timePosition", ref_time_elem,
                                 namespace=self.gml)

    def get_coverages(self):
        cov_ids_elem = get_elements("coverageIdList", self.root,
                                    single_elem=True,
                                    namespace=self.metocean)
        cov_ids = get_elements_text("CoverageSummary/CoverageId", cov_ids_elem,
                                    namespace=self.wcs)
        return CoverageList([Coverage(cov_id) for cov_id in cov_ids])


    def get_coverage_collection(self):
        col_id = self.get_collection_id()
        col_bbox = self.get_bbox()
        col_ref_times = self.get_ref_time()
        col_covs = self.get_coverages()
        return CoverageCollection(col_id, col_bbox, col_ref_times, col_covs)


class CoverageReader(ResponseReader):
    """
    Read describeCoverage response.

    """
    def __init__(self, xml_str):
        super(CoverageReader, self).__init__(xml_str)
        # Describe coverage XML only contains one coverage description.
        self.root = get_elements("CoverageDescription", self.root,
                                 single_elem=True, namespace=self.wcs)

    def get_coverage_name(self):
        return get_elements_text("CoverageId", self.root, single_elem=True,
                                 namespace=self.wcs)

    def get_components(self):
        components = []
        extension_elem = get_elements("metadata/Extension", self.root,
                                      single_elem=True, namespace=self.gmlcov)
        member_list_elems = get_elements("extensionProperty/"\
                                         "MetOceanCoverageMetadata/"\
                                         "dataMaskReferenceProperty/"\
                                         "DataMaskReferenceMemberList/"\
                                         "dataMaskReference",
                                         extension_elem,
                                         namespace=self.metocean)
        for elem in member_list_elems:
            components.append(get_elements_attr("fieldName", elem))
        return components

    def get_bbox(self):
        return self._get_bbox(self.root, namespace=self.gml)

    def get_ref_time(self):
        extension_elem = get_elements("metadata/Extension", self.root,
                                      single_elem=True, namespace=self.gmlcov)
        source_obs_elem = get_elements("extensionProperty/"\
                                       "MetOceanCoverageMetadata/"\
                                       "sourceObservationProperty/"\
                                       "SourceObservation", extension_elem,
                                       single_elem=True,
                                       namespace=self.metocean)
        value_elem = get_elements("parameter/NamedValue/value",
                                  source_obs_elem, single_elem=True,
                                  namespace=self.om)
        return get_elements_text("TimeInstant/timePosition", value_elem,
                                 single_elem=True, namespace=self.gml)

    def get_crss(self):
        extension_elem = get_elements("metadata/Extension", self.root,
                                      single_elem=True, namespace=self.gmlcov)
        source_obs_elem = get_elements("extensionProperty/"\
                                       "MetOceanCoverageMetadata/"\
                                       "sourceObservationProperty/"\
                                       "SourceObservation", extension_elem,
                                       single_elem=True,
                                       namespace=self.metocean)
        intrst_elem = get_elements("featureOfInterest", source_obs_elem,
                                   single_elem=True, namespace=self.om)
        SF_spatial_elem = get_elements("SF_SpatialSamplingFeature",
                                       intrst_elem, single_elem=True,
                                       namespace=self.sams)
        sample_feat_elem = get_elements("sampledFeature", SF_spatial_elem,
                                        single_elem=True, namespace=self.sam)
        horzon_proj_elem = get_elements("ModelDescription/geometryComponent/"\
                                        "ModelDomain/horizontalProjection",
                                        sample_feat_elem, single_elem=True,
                                        namespace=self.metocean)
        poly_elem = get_elements("Polygon", horzon_proj_elem, single_elem=True,
                                 namespace=self.gml)
        return get_elements_attr("srsName", poly_elem)

    def get_coverage(self):
        cov_name   = self.get_coverage_name()
        components = self.get_components()
        cov_bbox   = self.get_bbox()
        cov_ref_time = self.get_ref_time()
        return Coverage(name=cov_name, components=components, bbox=cov_bbox,
                        dim_runs=cov_ref_time)
