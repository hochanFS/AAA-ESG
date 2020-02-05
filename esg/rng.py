import numpy as np
import math

CONSTANT_M1 = 259200
CONSTANT_A1 = 7141
CONSTANT_C1 = 54773
CONSTANT_R1 = 0.0000038580247
CONSTANT_M2 = 134456
CONSTANT_A2 = 8121
CONSTANT_C2 = 28411
CONSTANT_R2 = 0.0000074373773
CONSTANT_M3 = 243000
CONSTANT_A3 = 4161
CONSTANT_C3 = 51349
NUM_ELEMENTS = 97


class AaaRandomNumberGenerator(object):
    """
    Generates Random numbers based on American Academy of Actuaries VBA code.
    """

    def __init__(self, seed_num):
        self.state_array = np.empty(NUM_ELEMENTS, dtype=float)
        self.current_seed = seed_num
        self.m1 = 0
        self.m2 = 0
        self.m3 = 0
        self.__reseed(seed_num)

    def __reseed(self, seed_num):
        """
        Reseed the instance for each random number generation
        :param seed_num: the seed number
        """
        intermediate1 = CONSTANT_C1 - seed_num
        intermediate1 = (CONSTANT_A1 * intermediate1 + CONSTANT_C1) % CONSTANT_M1
        intermediate2 = intermediate1 % CONSTANT_M2
        intermediate1 = (CONSTANT_A1 * intermediate1 + CONSTANT_C1) % CONSTANT_M1
        intermediate3 = intermediate1 % CONSTANT_M3
        for num in range(NUM_ELEMENTS):
            intermediate1 = (CONSTANT_A1 * intermediate1 + CONSTANT_C1) % CONSTANT_M1
            intermediate2 = (CONSTANT_A2 * intermediate2 + CONSTANT_C2) % CONSTANT_M2
            self.state_array[num] = (intermediate1 + intermediate2 * CONSTANT_R2) * CONSTANT_R1
        self.m1 = intermediate1
        self.m2 = intermediate2
        self.m3 = intermediate3

    def get_next(self) -> float:
        self.m1 = (CONSTANT_A1 * self.m1 + CONSTANT_C1) % CONSTANT_M1
        self.m2 = (CONSTANT_A2 * self.m2 + CONSTANT_C2) % CONSTANT_M2
        self.m3 = (CONSTANT_A3 * self.m3 + CONSTANT_C3) % CONSTANT_M3
        j = int(1 + 97 * self.m3 / CONSTANT_M3) - 1
        val = self.state_array[j]
        u = (self.m1 + self.m2 * CONSTANT_R2) * CONSTANT_R1
        if u < 0 or u >= 1:
            u = 1.0 + math.floor(u) - u
        self.state_array[j] = u
        return val


if __name__ == "__main__":
    print("Checking implementation..")
    rng = AaaRandomNumberGenerator(1)
    for i in range(100):
        print(rng.get_next())
