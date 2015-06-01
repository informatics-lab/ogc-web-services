import unittest
from BDS.coverage import Coverage, CoverageList

class Test_Coverage(unittest.TestCase):
    def test_print_info(self):
        cov = Coverage(name="name2", bbox=[1,2,3,4])
        # Test _info_str() method which feeds print_info().
        self.assertEqual(cov._info_str("name"),
                         "*** NAME ***\nname2\n\n")
        self.assertEqual(cov._info_str("bbox", as_list=True),
                         "*** BBOX ***\n1, 2, 3, 4\n\n")

class Test_CoverageList(unittest.TestCase):
    def setUp(self):
        self.covs = []
        for i in range(3):
            self.covs.append(Coverage("name%s" % i))

    def test_inputs(self):
        # Check CoverageList can be implemented in various ways.
        # As list.
        covs1 = CoverageList(self.covs)
        # As tuple.
        covs2 = CoverageList(tuple(self.covs))
        # As args.
        covs3 = CoverageList(self.covs[0], self.covs[1], self.covs[2])
        self.assertEqual(covs1.coverage_list, covs2.coverage_list)
        self.assertEqual(covs2.coverage_list, covs3.coverage_list)

    def test_bad_inputs(self):
        self.assertRaises(TypeError, CoverageList,
                          Coverage("name"), "non-coverage")

    def test_addition(self):
        joined_covs = CoverageList(self.covs[:1]) + CoverageList(self.covs[1:])
        self.assertEqual(joined_covs.coverage_list,
                         CoverageList(self.covs).coverage_list)


if __name__ == '__main__':
    unittest.main()
