import unittest

import numpy as np
from scipy import constants
from cavag.fiber import *

class Test_Fiber(unittest.TestCase):

    def test_constructor_1(self):
        ps = {'nf': 1.4, 'wavelength': 980, 'omegaf': 1.2}
        fiber = Fiber(**ps)
        self.assertEqual(fiber.nf, 1.4)
        self.assertEqual(fiber.wavelength, 980)
        self.assertEqual(fiber.omegaf, 1.2)
        self.assertEqual(fiber.k, 2*constants.pi/fiber.wavelength)
    
    def test_constructor_2(self):
        ps = {'nf': 1.4, 'wavelength': 980, 'omegaf': 1.2}
        fiber = Fiber(**ps)
        self.assertEqual(fiber.nf, 1.4)
        self.assertEqual(fiber.wavelength, 980)
        self.assertEqual(fiber.omegaf, 1.2)
        self.assertEqual(fiber.k, 2*constants.pi/fiber.wavelength)

class Test_StepIndexFiber(unittest.TestCase):

    def test_constructor(self):
        nf = 1.4
        wavelength = 980e-9
        a = 3e-6
        naf = np.sqrt(0.01)

        V = 2*constants.pi*a*naf/wavelength
        omegaf = a * (0.65 + 1.619 * V ** (-1.5) + 2.879 * V ** (-6))

        sfiber = StepIndexFiber(nf=nf, wavelength=wavelength, a=a, naf=naf)

        self.assertEqual(sfiber.nf, nf)
        self.assertEqual(sfiber.wavelength, wavelength)
        self.assertAlmostEqual(sfiber.omegaf, omegaf)


if __name__ == '__main__':
    unittest.main()
