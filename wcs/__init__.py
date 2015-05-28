"""

"""
import requests
import dateutil.parser
import iris
from boto.s3.connection import S3Connection, Location
from wcs.readers import wcs1_reader, wcs2_reader
from wcs.senders import wcs1_sender, wcs2_sender

class Requester(object):
    """
    Send requests.

    Args:

    * url: string
        URL to web coverage service.

    Kwargs:

    * api_key: string
        If coverage service requires an api key provide it here.

    * validate_api: boolean
        If True a dummy request is made during intialisation to check the api
        key is valid. This is not entirely necessary as the same check is done
        with all requests.

    """
    def __init__(self, url, wcs_version, api_key=None, validate_api=False):
        self.url = url
        self.version = wcs_version
        self.params = {"SERVICE" : "WCS",
                       "VERSION" : self.version}
        if api_key:
            self.params["key"] = api_key
            if validate_api:
                # Uses self.params (which contains the api_key) to send a
                # dummy request.
                self._check_api_key()
        self.api_key = api_key

    def _check_api_key(self):
        """
        Send dummy request to BDS and check response.

        """
        response = requests.get(self.url, params=self.params)
        self._check_response_status(response)

    @staticmethod
    def _check_response_status(response):
        """
        Check the status code returned by the request.

        """
        status = response.status_code
        if status != 200:
            url_message = "Here's the url that was sent:\n%s" % response.url
            if status == 403:
                raise UserWarning("403 Error, request forbidden. This is "\
                                  "likely due to an incorrect API key, but "\
                                  "sometimes the service is temporarily "\
                                  "down. If you know your key is fine, try "\
                                  "again.\n%s" % url_message)
            elif status == 404:
                raise UserWarning("404 Error, server not found.\n%s"\
                                  % url_message)
            else:
                raise UserWarning("%s Error\n%s" % (status, url_message))

    def _check_getCoverage_response(self, response):
        """
        Check if response is an XML file, if it is, there has been an error.

        """
        if response.headers["content-type"] == 'text/xml':
            xml_str = response.text
            # This function checks for an error XML response.
            self.response_reader.read_xml(xml_str)
            # If read_xml does not detect an error XML something has gone
            # wrong.

            raise UserWarning("getCoverage has returned an XML file (not what"\
                              " we want) but the format is not recognised. "\
                              "Here it is to look at:\n%s" % xml_str)

    def getCapabilities(self, show=True, savepath=None):
        """
        Send a request to BDS to get an XML file containing all available
        coverages. Coverages are returned as Coverage objects in a
        CoverageList. The coverage names (seen when a coverage is printed) are
        all that are needed to send a describeCoverage request, but there are
        more attributes available and can be seen using the print_info() method
        on any coverage.

        Kwargs:

        * show: boolean
            If True, print out all the returned coverage names.

        * savepath: string or None
            If a filepath (and name) is provided, save the returned XML
            (unless it is an XML error response).

        returns:
            CoverageList

        """
        response  = self.request_sender.send_getCapabilities_req(self)
        self._check_response_status(response)
        xml_str   = response.text
        coverages = self.response_reader.read_getCapabilities_res(xml_str)

        if show:
            for cov in coverages:
                print cov

        if savepath:
            with open(savepath, "w") as outfile:
                outfile.write(xml_str)

        return coverages

    def describeCoverage(self, coverage_id, show=True, savepath=None):
        """
        Send a request to get an XML file containing details of a
        particular coverage. The coverage is returned as a Coverage object.
        Use the print_info() method to print out all available parameters for
        a coverage.

        Args:

        * coverage_name: string
            Available coverage names are printed by getCapabilities method.

        Kwargs:

        * show: boolean
            If True, print out all the coverage information.

        * savepath: string or None
            If a filepath (and name) is provided, save the returned XML
            (unless it is an XML error response).

        returns:
            Coverage

        """
        response = self.request_sender.send_describeCoverage_req(self,
                                                                 coverage_id)
        self._check_response_status(response)
        xml_str  = response.text
        coverage = self.response_reader.read_describeCoverage_res(xml_str)

        if show:
            print coverage.print_info()

        if savepath:
            with open(savepath, "w") as outfile:
                outfile.write(xml_str)

        return coverage


class WCS1Requester(Requester):
    """

    """
    def __init__(self, url, api_key=None, validate_api=False):
        self.version = "1.0"
        super(WCS1Requester, self).__init__(url, self.version, api_key,
                                            validate_api)
        self.response_reader = wcs1_reader
        self.request_sender  = wcs1_sender

    def getCoverage(self, coverage_id, format=None, crs=None, elevation=None,
                    bbox=None, dim_run=None, time=None, dim_forecast=None,
                    width=None, height=None, resx=None, resy=None,
                    interpolation=None, stream=False, savepath=None):
        """
        Send a request to URL for data specified by the coverage name and a
        parameters.

        Args:

        * coverage_name: string
            Available coverage names are printed by getCapabilities method.

        *

        Kwargs:

        * stream: boolean
            If False (default), the response content will be immediately
            downloaded.

        returns
            requests.Response

        """
        response = self.request_sender.send_getCoverage_req(self, coverage_id,
                        format=format, crs=crs, elevation=elevation, bbox=bbox,
                        dim_run=dim_run, time=time, dim_forecast=dim_forecast,
                        width=width, height=height, resx=resx, resy=resy,
                        interpolation=interpolation, stream=stream)
        self._check_response_status(response)
        self._check_getCoverage_response(response)

        if savepath:
            with open(savepath, "w") as outfile:
                outfile.write(response.content)

        return response

class WCS2Requester(Requester):
    """

    """
    def __init__(self, url, api_key=None, validate_api=False):
        self.version = "2.0.0"
        super(WCS2Requester, self).__init__(url, self.version, api_key,
                                            validate_api)
        self.response_reader = wcs2_reader
        self.request_sender  = wcs2_sender

    def describeCoverageCollection(self, collection_id, ref_time, show=True,
                                   savepath=None):
        """

        """
        response = self.request_sender.send_describeCoverageCollection_req(
                                       self, collection_id, ref_time)
        self._check_response_status(response)
        xml_str  = response.text
        collection = self.response_reader.read_describeCoverageCollection_res(
                                          xml_str)

        if show:
            print collection.print_info()

        if savepath:
            with open(savepath, "w") as outfile:
                outfile.write(xml_str)

        return collection

    def getCoverage(self, coverage_id, components, format=None,
                    elevation=None, bbox=None, time=None, dim_forecast=None,
                    width=None, height=None, interpolation=None, stream=False,
                    savepath=None):
        """
        Send a request to URL for data specified by the coverage name and a
        parameters.

        Args:

        * coverage_name: string
            Available coverage names are printed by getCapabilities method.

        * param_dict: dictionary
            Use describeCoverage method to see available parameters and
            getParameterDictionary method to help build the param_dict
            correctly.

        Kwargs:

        * stream: boolean
            If False (default), the response content will be immediately
            downloaded.

        returns
            requests.Response

        """
        response = self.request_sender.send_getCoverage_req(self, coverage_id,
                        components, format=format, elevation=elevation,
                        bbox=bbox, time=time, dim_forecast=dim_forecast,
                        width=width, height=height,
                        interpolation=interpolation, stream=stream)
        self._check_response_status(response)
        self._check_getCoverage_response(response)

        if savepath:
            with open(savepath, "w") as outfile:
                outfile.write(response.content)

        return response
