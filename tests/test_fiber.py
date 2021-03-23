import unittest

import numpy as np
from scipy import constants
from cavag.fiber import *

class Test_FiberEnd(unittest.TestCase):

    def test_constructor_1(self):
        ps = {'nf': 1.4, 'wavelength': 980, 'omegaf': 1.2, 'roc': 600}
        fe = FiberEnd(**ps)
        self.assertEqual(fe.nf, 1.4)
        self.assertEqual(fe.wavelength, 980)
        self.assertEqual(fe.omegaf, 1.2)
        self.assertEqual(fe.roc, 600)
        self.assertEqual(fe.k, 2*constants.pi/fe.wavelength)
    
    def test_constructor_2(self):
        ps = {'nf': 1.4, 'wavelength': 980, 'omegaf': 1.2}
        fe = FiberEnd(**ps)
        self.assertEqual(fe.nf, 1.4)
        self.assertEqual(fe.wavelength, 980)
        self.assertEqual(fe.omegaf, 1.2)
        self.assertEqual(fe.roc, np.inf)
        self.assertEqual(fe.k, 2*constants.pi/fe.wavelength)

class Test_StepIndexFiberEnd(unittest.TestCase):

    def test_constructor(self):
        nf = 1.4
        wavelength = 980e-9
        a = 3e-6
        naf = np.sqrt(0.01)
        roc = 600e-6

        V = 2*constants.pi*a*naf/wavelength
        omegaf = a * (0.65 + 1.619 * V ** (-1.5) + 2.879 * V ** (-6))

        sfe = StepIndexFiberEnd(nf=nf, wavelength=wavelength, a=a, naf=naf, roc=roc)

        self.assertEqual(sfe.nf, nf)
        self.assertEqual(sfe.wavelength, wavelength)
        self.assertEqual(sfe.roc, roc)
        self.assertAlmostEqual(sfe.omegaf, omegaf)


if __name__ == '__main__':
    unittest.main()
