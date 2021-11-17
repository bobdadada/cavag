
import unittest

import scipy.constants as C

from cavag.fpcavity import Cavity, CavityMode
from cavag.fiber import Fiber
from cavag.extension import fcqs

class Test_Application(unittest.TestCase):
    
    def test_app1(self):

        gamma_493 = 9.53e7
        gamma_650 = 3.1e7
        gamma = gamma_493 + gamma_650
        wavelength = 493.4077e-9


        fiber = Fiber(wavelength=wavelength,omegaf=5.9e-6/2,nf=1.486)

        cavity_params = dict(
            length=270e-6,
            rocl=270e-6,
            rocr=270e-6,
            Rl=0.995,
            Rr=0.9995,
            wavelength=wavelength
        )

        cavity = Cavity(**cavity_params)
        cavitymode = CavityMode(**cavity_params)

        mu = fcqs.calculate_mu(C.c/wavelength, gamma_493)

        print(cavitymode)
        """
        u = cavitymode.u_f(0,0,0)
        g = fcqs.calculate_g(mu, cavitymode.emax*u)

        kappa = cavity.kappa

        c1 = fcqs.calculate_c1(g, kappa, gamma)

        eta_e = fcqs.calculate_eta_cpemit(c1)

        eta_ext = fcqs.calculate_eta_cpext(kappa, gamma)

        eta_coupling = fcqs.calculate_eta_fccoupling(wavelength, fiber.nf, fiber.omegaf, cavity.rocl, cavitymode.omegaml)
        """

