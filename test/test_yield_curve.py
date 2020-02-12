import unittest
from esg.yield_curve import CurveConstructor


# Solutions are found by running the original Excel VBA itself.

SOLUTION1 = [6.35531138164865E-03, 7.65041656219121E-03, 0.01, 1.38859543754594E-02, 1.69178279111794E-02,
             2.12083550093184E-02, 2.39801394847131E-02, 2.65544674231368E-02, 0.03, 3.11905822792592E-02]

SOLUTION2 = [6.36540887733794E-03, 7.66504878058516E-03, 1.00309102717255E-02, 1.39690641075763E-02,
             1.70726261953744E-02, 2.15388997508732E-02, 2.44866686479071E-02, 2.72931421815863E-02,
             3.13000514363615E-02, 3.27483621324332E-02]


class TestYieldCurveConstructor(unittest.TestCase):
    def test_interpolate(self):
        short_rate = 0.01
        long_rate = 0.03
        curve = CurveConstructor(short_rate, long_rate)
        for i in range(10):
            self.assertAlmostEqual(first=SOLUTION1[i], second=curve.interpolated_rates[i], delta=0.000001)

    def test_calculate_spot_rates(self):
        short_rate = 0.01
        long_rate = 0.03
        curve = CurveConstructor(short_rate, long_rate)
        spot_rates = curve.calculate_spot_rates()
        for i in range(10):
            self.assertAlmostEqual(first=SOLUTION2[i], second=spot_rates[i], delta=0.000001)

