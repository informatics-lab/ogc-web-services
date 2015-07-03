"""
Build appropriate requests for WCS2 requests.

"""
import xml.dom.minidom as dom
from webcoverageservice.builders import param_checks as checker

def build_getCapabilities_req():
    return {"REQUEST" : "GetCapabilities"}

def build_describeCoverageCollection_req(collection_id, ref_time):
    return {"REQUEST" : "DescribeCoverageCollection",
            "CoverageCollectionId" : collection_id,
            "ReferenceTime" : ref_time}

def build_describeCoverage_req(coverage_id):
    xml = """<?xml version="1.0" encoding="UTF-8"?>
        <DescribeCoverage xmlns="http://www.opengis.net/wcs/2.0"
                          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                          xsi:schemaLocation="http://www.opengis.net/wcs/2.0
                                http://schemas.opengis.net/wcs/2.0/wcsAll.xsd"
                          service="WCS" version="2.0.0">
            <CoverageId>{cov_id}</CoverageId>
        </DescribeCoverage>""".format(cov_id=coverage_id)
    return xml

def build_getCoverage_req(coverage_id, components, format=None, elevation=None,
                          bbox=None, time=None, width=None, height=None,
                          interpolation=None):
    """
    Create an XML document of valid parameters for getCoverage method.

    Notes:

    This method does not verify if the given parameters are available, it
    only asserts correct formats.

    For parameters elevation and time, providing a list means you are
    specifying bounds, where a string means you are specifying a single level
    or time point.

    Args:

    * coverage_id: string
        Name of coverage

    * components: string or list
        Components of the coverage.

    Kwargs:

    * format: string
        The format for the data to be returned in, e.g. NetCDF3

    * elevation: string or list
        The veritcal level description. If list of 2 values given they are
        treated as bounds.

    * bbox: list
        Must contain 4 values in the format [x-min, y-min, x-max, y-max].
        Values can be given as integers, floats or strings. Default is the
        entire field.

    * time: string or list
        The forecast time. If list of 2 values given they are treated as
        bounds.

    * width/height: integer
        The number of gridpoints in the x (width) and y (height) within
        the bounding box. Interpolation is used.

    * interpolation: string
        The interpolation method used if data is re-gridded.

    returns:
        XML string

    """
    req = GetCoverageRequestBuilder()

    req.setCoverageId(coverage_id)
    if isinstance(components, str):
        components = [components]
    req.setComponents(*components)

    if format:
        req.setFormat(format)

    if elevation:
        if isinstance(elevation, list):
            req.setLevelRange(elevation[0], elevation[1])
        else:
            req.setLevel(elevation)

    if bbox:
        checker.check_bbox(bbox)
        req.setLongRange(bbox[0], bbox[2])
        req.setLatRange(bbox[1], bbox[3])

    if time:
        if isinstance(time, list):
            assert len(time) == 2, "Provide a list of 2 values if specifing "\
                                   "bounds."
            time_min = checker.sort_time(time[0])
            time_max = checker.sort_time(time[1])
            req.setTimeRange(time_min, time_max)
        else:
            time = checker.sort_time(time)
            req.setTime(time)

    # Resolution parameters.
    if not interpolation:
        interpolation = "linear"

    if width:
        width = checker.sort_grid_num(width)
        req.setInterpolation('Long', interpolation, samplesize=width)

    if height:
        height = checker.sort_grid_num(height)
        req.setInterpolation('Lat', interpolation, samplesize=height)

    return req.toXML()

class GetCoverageRequestBuilder(object):
    """
    Class for setting getCoverage request parameters.

    """
    def __init__(self):
        self.components = []
        self.crs_dict = {'crs0':None, 'crs1':None, 'crs2':None, 'crs3':None}
        self.interpolation_dict = {}
        self.coverageId = ""
        self.lat = None
        self.long = None
        self.IsobaricSurface = None
        self.ValidityTime = None
        self.format = "KML"
        self.mediaType = ""

    def setComponents(self, *components):
        """
        Args:

        * components: strings

        """
        self.components = components

    def addComponents(self, *components):
        """
        Args:

        * components: strings

        """
        newComponents = list(set(self.components + components))
        self.components = newComponents

    def removeComponents(self, *components):
        """
        Args:

        * components: strings

        """
        newComponents = [c for c in self.components if not c in components]
        self.components = newComponents

    def setCRS(self, crs, value):
        """
        Args:

        * crs: string (crs0, crs1, crs2, crs3)

        * value: string

        """
        self.crs_dict[crs] = value

    def setInterpolation(self, dimension, method=None, samplesize=None):
        """
        Args:

        * dimension: string

        * method: string

        * samplesize: int

        """
        self.interpolation_dict[dimension] = (method, samplesize)

    def setCoverageId(self, id):
        """
        Args:

        * id: string

        """
        self.coverageId = id

    def setLat(self, value, unit=None):
        """
        Args:

        * value: string, float

        * unit: string

        """
        self.lat = {'type':'slice', 'value':value, 'unit':unit}

    def setLong(self, value, unit=None):
        """
        Args:

        * value: string, float

        * unit: string

        """
        self.long = {'type':'slice', 'value':value, 'unit':unit}

    def setLatRange(self, start, end, unit=None):
        """
        Args:

        * start: string, float

        * end: string, float

        * unit: string

        """
        self.lat = {'type':'trim', 'low':start, 'high':end, 'unit':unit}

    def setLongRange(self, start, end, unit=None):
        """
        Args:

        * start: string, float

        * end: string, float

        * unit: string

        """
        self.long = {'type':'trim', 'low':start, 'high':end, 'unit':unit}

    def setLevel(self, value, unit=None):
        """
        Args:

        * value: string, float

        * unit: string

        """
        self.IsobaricSurface = {'type':'slice', 'value':value, 'unit':unit}

    def setLevelRange(self, start, end, unit=None):
        """
        Args:

        * start: string, float

        * end: string, float

        * unit: string

        """
        self.IsobaricSurface = {'type':'trim', 'low':start, 'high':end, 'unit':unit}

    def setTime(self, value, unit=None):
        """
        Args:

        * value: string, float

        * unit: string

        """
        self.ValidityTime = {'type':'slice', 'value':value, 'unit':unit}

    def setTimeRange(self, start, end, unit=None):
        """
        Args:

        * start: string, float

        * end: string, float

        * unit: string

        """
        self.ValidityTime = {'type':'trim', 'low':start, 'high':end, 'unit':unit}

    def setFormat(self, format):
        """
        Args:

        * format: string

        """
        self.format = format

    def setMediaType(self, type):
        """
        Args:

        * type: string

        """
        self.mediaType = type

    def setWCSLocation(self, address):
        """
        Args:

        * address: string

        """
        self.wcs_location = address

    def toXML(self):
        """
        Write out all parameters to XML.

        """
        return GetCoverageRequestWriter().returnXml(self)

    def saveXML(self, filename):
        """
        Write out all parameters to XML and save.

        Args:

        * filename: string

        """
        xml = self.toXML()
        with open(filename, "w") as outfile:
            outfile.write(xml)


class GetCoverageRequestWriter(dom.Document):
    """
    Write XML specifically for getCoverage request.

    """
    def __init__(self):
        dom.Document.__init__(self)
        self.xlink = "http://www.w3.org/1999/xlink"
        self.wcs = "http://www.opengis.net/wcs/2.0"
        self.wcsCRS = "http://www.opengis.net/wcs_service-extension_crs/1.0"
        self.int = "http://www.opengis.net/WCS_service-extension_interpolation/1.0"
        self.rsub = "http://www.opengis.net/wcs/range-subsetting/1.0"
        self.xsi = "http://www.w3.org/2001/XMLSchema-instance"
        self.metocean = "http://def.wmo.int/metce/2013/metocean"

        self.crs0 = "http://www.opengis.net/def/crs-combine?"
        self.crs1 = "http://www.opengis.net/def/crs/EPSG/0/4326&amp;"
        self.crs2 = "http://www.codes.wmo.int/GRIB2/table4.5/IsobaricSurface&amp;"
        self.crs3 = "http://www.opengis.net/def/temporal/ISO8601"

    def _mkAttribute(self, name, value):
        """
        Args:

        * name: string

        * value: string, float

        """
        attr = self.createAttribute(name)
        attr.value = value
        return attr

    def mkRangeComponentNode(self, component):
        """
        Args:

        * component: string

        """
        textNode = self.createTextNode(component)
        rangeComponentNode = self.createElementNS(self.rsub, 'rsub:rangeComponent')
        rangeComponentNode.appendChild(textNode)
        return rangeComponentNode

    def mkRangeSubsetNode(self, *components):
        """
        Args:

        * components: rangeComponentNodes

        """
        rangeSubsetNode = self.createElementNS(self.rsub, 'rsub:rangeSubset')
        for rangeComponentNode in components:
            rangeSubsetNode.appendChild(rangeComponentNode)
        return rangeSubsetNode

    def mkSubsettingCrsNode(self, crs0=None, crs1=None, crs2=None, crs3=None):
        """
        Args:

        * crs#: string or None

        """
        crsstring = ""
        crsstring += crs0 if crs0!=None else self.crs0
        crsstring += '\n1='
        crsstring += crs1 if crs1!=None else self.crs1
        crsstring += '\n2='
        crsstring += crs2 if crs2!=None else self.crs2
        crsstring += '\n3='
        crsstring += crs3 if crs3!=None else self.crs3
        crsNode = self.createTextNode(crsstring)
        subsettingCrsNode = self.createElementNS(self.wcsCRS, 'wcsCRS:subsettingCrs')
        subsettingCrsNode.appendChild(crsNode)
        return subsettingCrsNode

    def mkGetCoverageCrsNode(self, subsettingCrs):
        """
        Args:

        * subsettingCrs: subsettingCrsNode

        """
        getCoverageCrsNode = self.createElementNS(self.wcsCRS, 'wcsCRS:GetCoverageCrs')
        getCoverageCrsNode.appendChild(subsettingCrs)
        return getCoverageCrsNode

    def _mkInterpolationMethodAttribute(self, method, samplesize):
        """
        Args:

        * method: string

        * samplesize: int

        """
        if samplesize != None:
            method += '/samplesize=%d'%(samplesize)
        interpolationMethodAttribute = self._mkAttribute('interpolationMethod', method)
        return interpolationMethodAttribute

    def mkInterpolationAxisNode(self, axis, interpolation, samplesize=None):
        """
        Args:

        * axis: string

        * interpolation: string

        * samplesize: int

        """
        axisAttribute = self._mkAttribute('axis', axis)
        interpolationMethodAttribute = self._mkInterpolationMethodAttribute(interpolation, samplesize)
        interpolationAxisNode = self.createElementNS(self.int, 'int:InterpolationAxis')
        interpolationAxisNode.setAttributeNode(axisAttribute)
        interpolationAxisNode.setAttributeNode(interpolationMethodAttribute)
        return interpolationAxisNode

    def mkInterpolationAxesNode(self, *axes):
        """
        Args:

        * axes: interpolationAxisNodes

        """
        interpolationAxesNode = self.createElementNS(self.int, 'int:InterpolationAxes')
        for axisNode in axes:
            interpolationAxesNode.appendChild(axisNode)
        return interpolationAxesNode

    def mkInterpolationNode(self, interpolationAxesNode):
        """
        Args:

        * interpolationAxesNode: interpolationAxesNode

        """
        interpolationNode = self.createElementNS(self.int, 'int:Interpolation')
        interpolationNode.appendChild(interpolationAxesNode)
        return interpolationNode

    def mkExtensionNode(self, rangeSubset, getCoverageCrs, interpolation):
        """
        Args:

        * rangeSubset: rangeSubsetNode

        * getCoverageCrs: getCoverageCrsNode

        * interpolation: interpolationNode

        """
        extensionNode = self.createElementNS(self.wcs, 'wcs:Extension')
        extensionNode.appendChild(rangeSubset)
        extensionNode.appendChild(getCoverageCrs)
        extensionNode.appendChild(interpolation)
        return extensionNode

    def mkCoverageIdNode(self, id):
        """
        Args:

        * id: string

        """
        idNode = self.createTextNode(id)
        coverageIdNode = self.createElementNS(self.wcs, 'wcs:CoverageId')
        coverageIdNode.appendChild(idNode)
        return coverageIdNode

    def mkDimensionNode(self, dim):
        """
        Args:

        * dim: string

        """
        dimNode = self.createTextNode(dim)
        dimensionNode = self.createElementNS(self.wcs, 'wcs:Dimension')
        dimensionNode.appendChild(dimNode)
        return dimensionNode

    def _mkTrimNode(self, trim, value, unit=None):
        """
        Args:

        * trim: string

        * value: string, float

        * unit: string

        """
        trim = 'metocean:'+trim
        valNode = self.createTextNode(str(value))
        trimNode = self.createElementNS(self.metocean, trim)
        if unit!=None:
            unitAttribute = self._mkAttribute('uomLabels', unit)
            trimNode.setAttributeNode(unitAttribute)
        trimNode.appendChild(valNode)
        return trimNode

    def mkTrimLowNode(self, value, unit):
        """
        Args:

        * value: string, float

        * unit: string

        """
        return self._mkTrimNode('TrimLow', value, unit)

    def mkTrimHighNode(self, value, unit):
        """
        Args:

        * value: string, float

        * unit: string

        """
        return self._mkTrimNode('TrimHigh', value, unit)

    def mkDimensionTrimNode(self, dim, low, high):
        """
        Args:

        * dim: dimensionNode

        * low: trimLowNode

        * high: trimHighNode

        """
        dimensionTrimNode = self.createElementNS(self.metocean, 'metocean:DimensionTrim')
        dimensionTrimNode.appendChild(dim)
        dimensionTrimNode.appendChild(low)
        dimensionTrimNode.appendChild(high)
        return dimensionTrimNode

    def mkSlicePointNode(self, value, unit):
        """
        Args:

        * value: string, float

        """
        valNode = self.createTextNode(str(value))
        slicePointNode = self.createElementNS(self.metocean, 'metocean:SlicePoint')
        if unit!=None:
            unitAttribute = self._mkAttribute('uomLabels', unit)
            slicePointNode.setAttributeNode(unitAttribute)
        slicePointNode.appendChild(valNode)
        return slicePointNode

    def mkDimensionSliceNode(self, dim, slicepoint):
        """
        Args:

        * dim: dimensionNode

        * slicepoint: slicePointNode

        """
        dimensionSliceNode = self.createElementNS(self.metocean, 'metocean:DimensionSlice')
        dimensionSliceNode.appendChild(dim)
        dimensionSliceNode.appendChild(slicepoint)
        return dimensionSliceNode

    def mkFormatNode(self, format):
        """
        Args:

        * format: string

        """
        textNode = self.createTextNode(format)
        formatNode = self.createElementNS(self.wcs, 'wcs:format')
        formatNode.appendChild(textNode)
        return formatNode

    def mkMediaTypeNode(self, type):
        """
        Args:

        * type: string

        """
        typeNode = self.createTextNode(type)
        mediaTypeNode = self.createElementNS(self.wcs, 'wcs:mediaType')
        mediaTypeNode.appendChild(typeNode)
        return mediaTypeNode

    def mkGetCoverageNode(self, extension, coverageId, lat, long, level, time, format, media, service='WCS', version='2.0.0'):
        """
        Args:

        * extension: extensionNode

        * coverageId: coverageIdNode

        * lat, long, level, time: dimensionSliceNode or dimensionTrimNode

        * format: formatNode

        * media: mediaTypeNode

        * service, version: string

        """
        xlinkAttr = self._mkAttribute('xmlns:xlink', self.xlink)
        wcsAttr = self._mkAttribute('xmlns:wcs', self.wcs)
        wcsCRSAttr = self._mkAttribute('xmlns:wcsCRS', self.wcsCRS)
        intAttr = self._mkAttribute('xmlns:int', self.int)
        rsubAttr = self._mkAttribute('xmlns:rsub', self.rsub)
        xsiAttr = self._mkAttribute('xmlns:xsi', self.xsi)
        metoceanAttr = self._mkAttribute('xmlns:metocean', self.metocean)
        serviceAttr = self._mkAttribute('service', service)
        versionAttr = self._mkAttribute('version', version)
        attrs = [xlinkAttr, wcsAttr, wcsCRSAttr, intAttr, rsubAttr, xsiAttr, metoceanAttr, serviceAttr, versionAttr]
        getCoverageNode = self.createElementNS(self.wcs, 'wcs:GetCoverage')
        for attr in attrs:
            getCoverageNode.setAttributeNode(attr)
        for arg in [extension, coverageId, lat, long, level, time, format, media]:
            if arg is not None:
                getCoverageNode.appendChild(arg)
        return getCoverageNode

    def createExtensionNode(self, request):
        """
        Args:

        * request: GetCoverageRequest

        """
        #rangeSubsetNode
        rangeComponentNodes = []
        for component in request.components:
            rangeComponentNodes.append(self.mkRangeComponentNode(component))
        rangeSubsetNode = self.mkRangeSubsetNode(*rangeComponentNodes)

        #GetCoverageCrs
        subsettingCrsNode = self.mkSubsettingCrsNode(**request.crs_dict)
        getCoverageCrsNode = self.mkGetCoverageCrsNode(subsettingCrsNode)

        #Interpolation
        interpolationAxisNodes = []
        for (name, (method, samplesize)) in request.interpolation_dict.items():
            if method != None:
                interpolationAxisNodes.append(self.mkInterpolationAxisNode(name, method, samplesize))
        interpolationAxesNode = self.mkInterpolationAxesNode(*interpolationAxisNodes)
        interpolationNode = self.mkInterpolationNode(interpolationAxesNode)

        extensionNode = self.mkExtensionNode(rangeSubsetNode, getCoverageCrsNode, interpolationNode)
        return extensionNode

    def createCoverageIdNode(self, request):
        """
        Args:

        * request: GetCoverageRequest

        """
        coverageIdNode = self.mkCoverageIdNode(request.coverageId)
        return coverageIdNode

    def _createDimNode(self, name, item):
        """
        Args:

        * name: string

        * item: dict

        """
        if item is None:
            return None
        else:
            dimensionNode = self.mkDimensionNode(name)
            if item['type'] == 'trim':
                trimLowNode = self.mkTrimLowNode(item['low'], item['unit'])
                trimHighNode = self.mkTrimHighNode(item['high'], item['unit'])
                dimNode = self.mkDimensionTrimNode(dimensionNode, trimLowNode,
                                                   trimHighNode)
            else:
                slicePointNode = self.mkSlicePointNode(item['value'],
                                                       item['unit'])
                dimNode = self.mkDimensionSliceNode(dimensionNode,
                                                    slicePointNode)
            return dimNode

    def createLatNode(self, request):
        """
        Args:

        * request: GetCoverageRequest

        """
        return self._createDimNode('lat', request.lat)

    def createLongNode(self, request):
        """
        Args:

        * request: GetCoverageRequest

        """
        return self._createDimNode('long', request.long)

    def createLevelNode(self, request):
        """
        Args:

        * request: GetCoverageRequest

        """
        return self._createDimNode('IsobaricSurface', request.IsobaricSurface)

    def createTimeNode(self, request):
        """
        Args:

        * request: GetCoverageRequest

        """
        return self._createDimNode('ValidityTime', request.ValidityTime)

    def createFormatNode(self, request):
        """
        Args:

        * request: GetCoverageRequest

        """
        return self.mkFormatNode(request.format)

    def createMediaTypeNode(self, request):
        """
        Args:

        * request: GetCoverageRequest

        """
        return self.mkMediaTypeNode(request.mediaType)

    def createGetCoverageNode(self, request):
        """
        Args:

        * request: GetCoverageRequest

        """
        extension = self.createExtensionNode(request)
        coverageId = self.createCoverageIdNode(request)
        lat = self.createLatNode(request)
        long = self.createLongNode(request)
        level = self.createLevelNode(request)
        time = self.createTimeNode(request)
        format = self.createFormatNode(request)
        media = self.createMediaTypeNode(request)
        return self.mkGetCoverageNode(extension, coverageId, lat, long, level,
                                      time, format, media)

    def returnXml(self, request):
        """
        Args:

        * request: GetCoverageRequest

        """
        self.appendChild(self.createGetCoverageNode(request))
        return self.toxml()
