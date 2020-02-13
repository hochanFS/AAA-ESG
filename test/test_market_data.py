import unittest
from esg.market_data import CommunityTreasuryCurveImporter
import datetime

# Solutions are found by running the original Excel VBA itself.

SOLUTION1 = [0.0156, 0.0157, 0.0157, 0.0156, 0.0146, 0.0136, 0.0134, 0.0135, 0.0145, 0.0154, 0.0184, 0.0201]


class TestCommunityTreasuryCurveImporter(unittest.TestCase):
    tenors = ['1M', '2M', '3M', '6M', '1Y', '2Y', '3Y', '5Y', '7Y', '10Y', '20Y', '30Y']

    def test_get_next(self):
        importer = CommunityTreasuryCurveImporter()
        values1 = importer.pull_data(datetime.date(2020, 2, 3))
        print(values1)
        values = importer.pull_data(datetime.date(2020, 2, 3))
        a = values
        for i in range(12):
            self.assertEqual(first=SOLUTION1[i], second=values[self.tenors[i]])
            pass



