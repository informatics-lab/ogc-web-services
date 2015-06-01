import unittest
import os
import requests
import xml.etree.ElementTree as ET
import random
import boto
from boto.s3.connection import S3Connection
from BDS.requester import BDSRequest
from BDS.coverage import Coverage, CoverageList

request = BDSRequest(api_key=os.environ['API_KEY'])

def random_item(lst):
    if len(lst) == 0:
        return None
    else:
        indx = random.randint(0, (len(lst) - 1))
        return lst[indx]

def create_random_paramDict(coverage):
    format    = random_item(coverage.formats)
    elevation = random_item(coverage.elevations)
    # Currently, some "available" CRSs return errors.
    crs       = "EPSG:4326" #random_item(coverage.CRSs)

    return request.getParameterDictionary(format, crs, elevation)

class Test_BDSRequest(unittest.TestCase):

    def test_requests(self):
        ##### Test getCapabilities #####
        getCap_path = "/tmp/testGetCap.xml"
        coverages   = request.getCapabilities(show=False, savepath=getCap_path)

        # Test returned type.
        self.assertEqual(type(coverages), CoverageList)

        # Test returned data.
        for cov in coverages:
            self.assertIsNotNone(cov.name)
            self.assertIsNotNone(cov.label)
            self.assertIsNotNone(cov.bbox)

        # Test saved XML. Element tree will only parse valid xml.
        ET.parse(getCap_path)


        ##### Test describeCoverage #####
        desCov_path = "/tmp/testDesCov.xml"
        # Choose random coverage as example.
        cov_name = random_item(coverages).name
        coverage = request.describeCoverage(cov_name, show=False,
                                            savepath=desCov_path)
        self.assertEqual(type(coverage), Coverage)

        # Test returned data.
        self.assertIsNotNone(coverage.name)
        self.assertIsNotNone(coverage.label)
        self.assertIsNotNone(coverage.bbox)
        self.assertIsNotNone(coverage.dim_runs)
        self.assertIsNotNone(coverage.times)
        self.assertIsNotNone(coverage.dim_forecasts)
        self.assertIsNotNone(coverage.formats)
        self.assertIsNotNone(coverage.CRSs)
        self.assertIsNotNone(coverage.elevations)
        self.assertIsNotNone(coverage.interpolations)

        # Test saved XML.
        ET.parse(desCov_path)


        ##### Test getCoverage #####
        param_dict = create_random_paramDict(coverage)
        response = request.getCoverage(cov_name, param_dict)

        self.assertEqual(type(response), requests.Response)
        self.assertNotEqual(response.headers['content-type'], 'text/xml')


        # ##### Test streamCoverageToAWS #####
        aws_bucket_name = "simons-test-bucket-2345"
        aws_filepath    = "test_data.nc"


        request.streamCoverageToAWS(
                    cov_name, param_dict, aws_bucket_name, aws_filepath,
                    aws_access_key_id=os.environ['AWS_KEY'],
                    aws_secret_access_key=os.environ['AWS_SECRET_KEY'])

        # Delete test data
        s3_conn = S3Connection(
                  aws_access_key_id=os.environ['AWS_KEY'],
                  aws_secret_access_key=os.environ['AWS_SECRET_KEY'])
        bucket  = s3_conn.get_bucket(aws_bucket_name)
        key     = bucket.new_key(aws_filepath)
        bucket.delete_key(key)


        ##### Test createCoverageCube #####
        # Currently, Iris does not read in certain ascii characters which some
        # variables have in there units. This is being dealt with so for now
        # ignore this error if it comes up.
        try:
            cube = request.createCoverageCubes(cov_name, param_dict)
        except UnicodeEncodeError:
            pass


if __name__ == '__main__':
    unittest.main()
