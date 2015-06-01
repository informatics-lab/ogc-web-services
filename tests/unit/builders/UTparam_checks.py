import unittest
from webcoverageservice.builders import param_checks as pchecks

class Test__check_dim_forecast(unittest.TestCase):
    def test_bad_dim_forecast(self):
        self.assertRaises(ValueError, pchecks.check_dim_forecast, 24)


class Test__sort_grid_num(unittest.TestCase):
    def test_bad_grid_num(self):
        self.assertRaises(ValueError, pchecks.sort_grid_num, 10.5)

    def test_returned_val_type(self):
        self.assertEqual(int, type(pchecks.sort_grid_num(10.0)))
        self.assertEqual(int, type(pchecks.sort_grid_num("10")))


class Test__sort_grid_size(unittest.TestCase):
    def test_bad_grid_size(self):
        self.assertRaises(ValueError, pchecks.sort_grid_size, "big")

    def test_returned_val_type(self):
        self.assertEqual(float, type(pchecks.sort_grid_size(1)))
        self.assertEqual(float, type(pchecks.sort_grid_size("1.5")))


class Test__sort_time(unittest.TestCase):
    def test_bad_dates(self):
        self.assertRaises(ValueError, pchecks.sort_time, "bad_date")

    def test_valid_dates(self):
        vaild_date = "2015-04-21T00:00:00Z"
        self.assertEqual(vaild_date, pchecks.sort_time("2015-04-21T"))
        self.assertEqual(vaild_date, pchecks.sort_time("21/4/2015"))
        self.assertEqual(vaild_date, pchecks.sort_time("21st April 2015"))


class Test__check_bbox(unittest.TestCase):
    def test_bad_type(self):
        # Must be a list (or tuple).
        self.assertRaises(UserWarning, pchecks.check_bbox, "not a list")

    def test_bad_length(self):
        # Must have four items.
        self.assertRaises(UserWarning, pchecks.check_bbox, [1,2,3])

    def test_bad_value(self):
        # Values must be numeric.
        self.assertRaises(UserWarning, pchecks.check_bbox, [1,2,3,"d"])

    def test_bad_format(self):
        # Must have format [x-min, y-min, x-max, y-max].
        self.assertRaises(UserWarning, pchecks.check_bbox, [10,20,1,2])


class Test__sort_bbox(unittest.TestCase):
    def test_mix_type_values(self):
        # The type does not matter so long as values are numeric.
        self.assertEqual("1,2.2,3,4.4", pchecks.sort_bbox(["1",2.2,3,"4.4"]))

if __name__ == '__main__':
    unittest.main()
