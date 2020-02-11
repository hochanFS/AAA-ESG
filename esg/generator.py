from . import rng


class Generator(object):
    def generate_random_numbers_for_ir(self):
        #         If(m_RNG
        #         Is
        #         Nothing) Then
        #         Set
        #         m_RNG = New
        #         C3RNG
        #         Call
        #         m_RNG.Reseed(scenNumber - 1 + 200)
        #         'Re-seed the generator based on scenario number
        #
        #         For
        #         i = 1
        #         To
        #         numCurves
        #         'First generate the uncorrelated random numbers
        #         For
        #         j = 1
        #         To
        #         3
        #         temp = m_RNG.GetNext()
        #         randNums(i, j) = InverseNormal(temp)
        #
        #     Next
        #     j
        #     'Now apply formulas to correlate the random numbers
        #     'The order of the next two lines was reversed before version 7.1,
        #     'leading to incorrect correlations if the user overrode default parameters
        #     'and specified non-zero correlations between the third random number and the other two.
        #     randNums(i, 3) = randNums(i, 1) * correl13 + randNums(i, 2) * const2 + randNums(i, 3) * const3
        #     randNums(i, 2) = randNums(i, 1) * correl12 + randNums(i, 2) * const1
        #     'The random numbers are now a correlated sample
        #
        #
        # Next
        # i
        pass
    pass


if __name__ == "__main__":
    pass
