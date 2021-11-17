import unittest

import numpy as np
from scipy import constants
from cavag.extension.fcqs import *

class Test_functions(unittest.TestCase):

    def test_calculate_g(self):
        wavelength = 980e-9
        nu = constants.c/wavelength
        v_mode = 100*3**2*1e-18
        gamma = 1e6
        mu = calculate_mu(nu, gamma)
        emax = calculate_emax(v_mode, nu)
        g = np.sqrt((3*gamma*constants.pi*constants.c**3)/(2*v_mode*(2*np.pi*nu)**2))
        self.assertAlmostEqual(calculate_g(mu, emax), g)
    
    def test_calculate_c1(self):
        wavelength = 980e-9
        nu = constants.c/wavelength
        v_mode = 100*3**2*1e-18
        kappa = 3e8
        gamma = 1e6
        g = np.sqrt((3*gamma*constants.pi*constants.c**3)/(2*v_mode*(2*np.pi*nu)**2))
        gammat = 3e6
        c1 = g**2/(kappa*gammat)
        self.assertEqual(calculate_c1(g, kappa, gammat), c1)