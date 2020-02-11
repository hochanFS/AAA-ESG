import datetime
import math
import numpy as np
from esg.market_data import CommunityTreasuryCurveImporter


class CurveConstructor(object):
    MINIMUM_SHORT_RATE = 0.0001
    MINIMUM_LONG_RATE = 0.0001
    __CONSTANT_K = 0.4
    __CONSTANT1 = (1 - math.exp(-__CONSTANT_K * 1)) / (__CONSTANT_K * 1)
    __CONSTANT20 = (1 - math.exp(-__CONSTANT_K * 20)) / (__CONSTANT_K * 20)

    def __init__(self, short_rate: float, long_rate: float):
        self.interpolated_rates = np.empty(10, dtype=float)
        self.__interpolate(short_rate, long_rate)

    def __interpolate(self, short_rate: float, long_rate: float):
        """
        Uses Nelson Siegel two point interpolation
        :param short_rate: interest rate at 1Y tenor
        :param long_rate: interest rate at 20Y tenor
        """
        b1 = (short_rate - long_rate) / (self.__CONSTANT1 - self.__CONSTANT20)
        b0 = short_rate - b1 * self.__CONSTANT1
        maturities = [0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30]
        for i in range(10):
            self.interpolated_rates[i] = b0 + b1 * (1 - math.exp(-self.__CONSTANT_K * maturities[i])
                                                    / (self.__CONSTANT_K * maturities[i]))

    def _calculate_bond_curves(self):
        bond_curves = np.empty(61, dtype=float)  # nth element indicates bond curve for n/2 Y tenor except 0th element
        bond_curves[0] = self.interpolated_rates[0]  # 0th element indicates 3M tenor
        bond_curves[1] = self.interpolated_rates[1]
        bond_curves[2] = self.interpolated_rates[2]
        bond_curves[3] = (self.interpolated_rates[2] + self.interpolated_rates[3]) / 2.0
        bond_curves[4] = (self.interpolated_rates[3])
        bond_curves[5] = (self.interpolated_rates[3] + self.interpolated_rates[4]) / 2.0
        bond_curves[6] = self.interpolated_rates[4]
        for i in range(1, 5):
            bond_curves[6 + i] = self.interpolated_rates[4] +\
                                 (i * 0.25 * (self.interpolated_rates[5] - self.interpolated_rates[4]))
        for i in range(1, 5):
            bond_curves[10 + i] = self.interpolated_rates[5] +\
                                  (i * 0.25 * (self.interpolated_rates[6] - self.interpolated_rates[5]))
        for i in range(1, 7):
            bond_curves[14 + i] = self.interpolated_rates[6] +\
                                  (i / 6.0 * (self.interpolated_rates[7] - self.interpolated_rates[6]))
        for i in range(1, 21):
            bond_curves[20 + i] = self.interpolated_rates[7] +\
                                  (i / 20.0 * (self.interpolated_rates[8] - self.interpolated_rates[7]))
        for i in range(1, 21):
            bond_curves[40 + i] = self.interpolated_rates[8] +\
                                  (i / 20.0 * (self.interpolated_rates[9] - self.interpolated_rates[8]))
        for i in range(1, 61):
            bond_curves[i] /= 2.0
        return bond_curves

    def calculate_spot_rates(self):
        bond_curves = self._calculate_bond_curves()
        s = np.empty(10, dtype=float)
        spot_rates = np.empty(10, dtype=float)
        s[0] = bond_curves[0]
        s[1] = bond_curves[1]
        annuity_factor = 1.0 / (1.0 + s[1])
        for i in range(2, 61):
            pv_factor = (1 - bond_curves[i] * annuity_factor) / (1 + bond_curves[i])
            if pv_factor > 0:
                s[i] = 1 / pv_factor ** (1.0 / i) - 1.0
            annuity_factor += pv_factor
        matching_tenor_indices = [0, 1, 2, 4, 6, 10, 14, 20, 40, 60]
        for i in range(10):
            spot_rates[i] = (1 + s[matching_tenor_indices[i]]) ** 2 - 1


if __name__ == "__main__":
    now_date = datetime.date(2020, 2, 6)
    importer = CommunityTreasuryCurveImporter()
    imported_data = importer.pull_data(now_date)
    print(imported_data)
