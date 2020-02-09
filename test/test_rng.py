import unittest
from esg.rng import AaaRandomNumberGenerator


class TestAaaRandomNumberGenerator(unittest.TestCase):
    def test_get_next(self):
        rng = AaaRandomNumberGenerator(9917 - 1 + 10200)
        a = 0
        for i in range(360):
            for j in range(11):
                a = rng.get_next()
        self.assertAlmostEquals(first=0.791059921432467, second=a, delta=0.0001)

