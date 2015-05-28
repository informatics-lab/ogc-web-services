# ogc-web-services
Open Geospatial Consortium (OGC) defines open standards for retrieving
geospatial data.
http://www.opengeospatial.org/

### wcs
Web Coverage Service (WCS). Service for retrieving direct data.

This is a Python wrapper for WCS requests.

The module is currently in its early stages.
Current supported requests:

WCS1:
* getCapabilities
* describeCoverage
* getCoverage

WCS2:
* getCapabilities
* describeCoverageCollection
* describeCoverage
* getCoverage

Current unsupported requests:

WCS2:
* getPolygonCoverage
* getCorridorCoverage
