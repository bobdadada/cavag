import unittest

import numpy as np
from scipy import constants
from scipy import special
from cavag.gaussbeam import *


class Test_NormalizedHermiteGaussBeam1D(unittest.TestCase):
    
    def test_constructor(self):
        wavelength, p0, omega0, m = 1550e-9, 0, 4e-6, 3
        c = (2/constants.pi)**(1/4)/np.sqrt(omega0*(2**m)*special.factorial(m))
        z0 = constants.pi*omega0**2/wavelength
        theta = np.arctan(omega0/z0)

        nhgb1d = NormalizedHermiteGaussBeam1D(wavelength=wavelength, p0=p0, omega0=omega0, m=m)
        
        self.assertEqual(nhgb1d.c, c)
        self.assertEqual(nhgb1d.p0, p0)
        self.assertEqual(nhgb1d.omega0, omega0)
        self.assertEqual(nhgb1d.m, m)
        self.assertEqual(nhgb1d.z0, z0)
        self.assertAlmostEqual(nhgb1d.theta, theta)

        self.assertAlmostEqual(nhgb1d.A_f(10), 1/(1+(10-p0)**2/z0**2)**(1/4))  # 振幅
        self.assertAlmostEqual(nhgb1d.omega_f(10), omega0*np.sqrt(1+(10-p0)**2/z0**2))  # 模场半径
        self.assertAlmostEqual(nhgb1d.R_f(10), (10-p0)*(1+z0**2/(10-p0)**2))  # 波前曲率半径
        self.assertAlmostEqual(nhgb1d.phi_f(10), np.arctan((10-p0)/z0))  # phi相位

    def test_change_properties(self):
        wavelength, p0, omega0, m = 980e-9, 0, 1e-6, 3
        nhgb1d = NormalizedHermiteGaussBeam1D(wavelength=wavelength, p0=p0, omega0=omega0, m=m)

        m = 0
        nhgb1d.change_params(m=m)

        c = (2/constants.pi)**(1/4)/np.sqrt(omega0*(2**m)*special.factorial(m))
        z0 = constants.pi*omega0**2/wavelength

        self.assertEqual(nhgb1d.c, c)
        self.assertEqual(nhgb1d.p0, p0)
        self.assertEqual(nhgb1d.omega0, omega0)
        self.assertEqual(nhgb1d.m, m)
        self.assertEqual(nhgb1d.z0, z0)


class Test_HermiteGaussBeam1D(unittest.TestCase):

    def test_constructor(self):
        A0, wavelength, p0, omega0, m = 2, 980e-9, 0, 1e-6, 3
        c = (2/constants.pi)**(1/4)/np.sqrt(omega0*(2**m)*special.factorial(m))
        z0 = constants.pi*omega0**2/wavelength

        hgb1d = HermiteGaussBeam1D(A0=A0, wavelength=wavelength, p0=p0, omega0=omega0, m=m)

        self.assertEqual(hgb1d.A0, A0)
        self.assertEqual(hgb1d.c, c)
        self.assertEqual(hgb1d.p0, p0)
        self.assertEqual(hgb1d.omega0, omega0)
        self.assertEqual(hgb1d.m, m)
        self.assertEqual(hgb1d.z0, z0)

        self.assertAlmostEqual(hgb1d.A_f(10), A0/(1+(10-p0)**2/z0**2)**(1/4))  # 振幅
        self.assertAlmostEqual(hgb1d.omega_f(10), omega0*np.sqrt(1+(10-p0)**2/z0**2))  # 模场半径
        self.assertAlmostEqual(hgb1d.R_f(10), (10-p0)*(1+z0**2/(10-p0)**2))  # 波前曲率半径
        self.assertAlmostEqual(hgb1d.phi_f(10), np.arctan((10-p0)/z0))  # phi相位


class Test_NormalizedGaussBeam1D(unittest.TestCase):

    def test_constructor(self):
        wavelength, p0, omega0 = 980e-9, 0, 1e-6
        c = (2/constants.pi)**(1/4)/np.sqrt(omega0)
        z0 = constants.pi*omega0**2/wavelength

        ngb1d = NormalizedGaussBeam1D(wavelength=wavelength, p0=p0, omega0=omega0)

        self.assertEqual(ngb1d.c, c)
        self.assertEqual(ngb1d.p0, p0)
        self.assertEqual(ngb1d.omega0, omega0)
        self.assertEqual(ngb1d.m, 0)
        self.assertEqual(ngb1d.z0, z0)

        self.assertAlmostEqual(ngb1d.A_f(10), 1/(1+(10-p0)**2/z0**2)**(1/4))  # 振幅
        self.assertAlmostEqual(ngb1d.omega_f(10), omega0*np.sqrt(1+(10-p0)**2/z0**2))  # 模场半径
        self.assertAlmostEqual(ngb1d.R_f(10), (10-p0)*(1+z0**2/(10-p0)**2))  # 波前曲率半径
        self.assertAlmostEqual(ngb1d.phi_f(10), np.arctan((10-p0)/z0))  # phi相位


class Test_GaussBeam1D(unittest.TestCase):

    def test_constructor(self):
        A0, wavelength, p0, omega0 = 2, 980e-9, 0, 1e-6
        c = (2/constants.pi)**(1/4)/np.sqrt(omega0)
        z0 = constants.pi*omega0**2/wavelength

        gb1d = GaussBeam1D(A0=A0, wavelength=wavelength, p0=p0, omega0=omega0)

        self.assertEqual(gb1d.c, c)
        self.assertEqual(gb1d.p0, p0)
        self.assertEqual(gb1d.omega0, omega0)
        self.assertEqual(gb1d.m, 0)
        self.assertEqual(gb1d.z0, z0)

        self.assertAlmostEqual(gb1d.A_f(10), A0/(1+(10-p0)**2/z0**2)**(1/4))  # 振幅
        self.assertAlmostEqual(gb1d.omega_f(10), omega0*np.sqrt(1+(10-p0)**2/z0**2))  # 模场半径
        self.assertAlmostEqual(gb1d.R_f(10), (10-p0)*(1+z0**2/(10-p0)**2))  # 波前曲率半径
        self.assertAlmostEqual(gb1d.phi_f(10), np.arctan((10-p0)/z0))  # phi相位


class Test_NormalizedHermiteGaussBeam(unittest.TestCase):

    def test_constructor(self):
        wavelength, p0, omega0x, omega0y, mx, my = 980e-9, 0, 1e-6, 1.2e-6, 1, 2

        cx = (2/constants.pi)**(1/4)/np.sqrt(omega0x*(2**mx)*special.factorial(mx))
        cy = (2/constants.pi)**(1/4)/np.sqrt(omega0y*(2**my)*special.factorial(my))
        c = np.sqrt(2/constants.pi)/np.sqrt(omega0x*omega0y*(2**(mx+my))*special.factorial(mx)*special.factorial(my))
        z0x = constants.pi*omega0x**2/wavelength
        z0y = constants.pi*omega0y**2/wavelength

        nhgb = NormalizedHermiteGaussBeam(wavelength=wavelength, 
                    p0=p0, omega0x=omega0x, omega0y=omega0y, mx=mx, my=my)
        
        self.assertEqual(nhgb.cx, cx)
        self.assertEqual(nhgb.cy, cy)
        self.assertAlmostEqual(nhgb.c, c) 
        self.assertEqual(nhgb.p0, p0)
        self.assertEqual(nhgb.omega0x, omega0x)
        self.assertEqual(nhgb.omega0y, omega0y)
        self.assertEqual(nhgb.mx, mx)
        self.assertEqual(nhgb.my, my)
        self.assertEqual(nhgb.z0x, z0x)
        self.assertEqual(nhgb.z0y, z0y)
    
    def test_change_properties(self):
        wavelength, p0, omega0x, omega0y, mx, my = 980e-9, 0, 1e-6, 1.2e-6, 1, 2

        nhgb = NormalizedHermiteGaussBeam(wavelength=wavelength, 
                    p0=p0, omega0x=omega0x, omega0y=omega0y, mx=mx, my=my)
        
        mx, my = 2, 3
        nhgb.change_params(mx=mx, my=my)

        cx = (2/constants.pi)**(1/4)/np.sqrt(omega0x*(2**mx)*special.factorial(mx))
        cy = (2/constants.pi)**(1/4)/np.sqrt(omega0y*(2**my)*special.factorial(my))
        c = np.sqrt(2/constants.pi)/np.sqrt(omega0x*omega0y*(2**(mx+my))*special.factorial(mx)*special.factorial(my))
        z0x = constants.pi*omega0x**2/wavelength
        z0y = constants.pi*omega0y**2/wavelength
        
        self.assertEqual(nhgb.cx, cx)
        self.assertEqual(nhgb.cy, cy)
        self.assertAlmostEqual(nhgb.c, c) 
        self.assertEqual(nhgb.p0, p0)
        self.assertEqual(nhgb.omega0x, omega0x)
        self.assertEqual(nhgb.omega0y, omega0y)
        self.assertEqual(nhgb.mx, mx)
        self.assertEqual(nhgb.my, my)
        self.assertEqual(nhgb.z0x, z0x)
        self.assertEqual(nhgb.z0y, z0y)


class Test_HermiteGaussBeam(unittest.TestCase):

    def test_constructor(self):
        A0, wavelength, p0, omega0x, omega0y, mx, my = 3, 980e-9, 0, 1e-6, 1.2e-6, 1, 2

        cx = (2/constants.pi)**(1/4)/np.sqrt(omega0x*(2**mx)*special.factorial(mx))
        cy = (2/constants.pi)**(1/4)/np.sqrt(omega0y*(2**my)*special.factorial(my))
        c = np.sqrt(2/constants.pi)/np.sqrt(omega0x*omega0y*(2**(mx+my))*special.factorial(mx)*special.factorial(my))
        z0x = constants.pi*omega0x**2/wavelength
        z0y = constants.pi*omega0y**2/wavelength

        hgb = HermiteGaussBeam(A0=A0, wavelength=wavelength, 
                    p0=p0, omega0x=omega0x, omega0y=omega0y, mx=mx, my=my)

        self.assertEqual(hgb.A0, A0)
        self.assertEqual(hgb.cx, cx)
        self.assertEqual(hgb.cy, cy)
        self.assertAlmostEqual(hgb.c, c) 
        self.assertEqual(hgb.p0, p0)
        self.assertEqual(hgb.omega0x, omega0x)
        self.assertEqual(hgb.omega0y, omega0y)
        self.assertEqual(hgb.mx, mx)
        self.assertEqual(hgb.my, my)
        self.assertEqual(hgb.z0x, z0x)
        self.assertEqual(hgb.z0y, z0y)

        self.assertAlmostEqual(hgb.A_f(10), A0/(1+(10-p0)**2/z0x**2)**(1/4)/(1+(10-p0)**2/z0y**2)**(1/4))  # 振幅


class Test_NormalizedGaussBeam(unittest.TestCase):

    def test_constructor(self):
        wavelength, p0, omega0x, omega0y = 980e-9, 0, 1e-6, 1.2e-6

        cx = (2/constants.pi)**(1/4)/np.sqrt(omega0x)
        cy = (2/constants.pi)**(1/4)/np.sqrt(omega0y)
        c = np.sqrt(2/constants.pi)/np.sqrt(omega0x*omega0y)
        z0x = constants.pi*omega0x**2/wavelength
        z0y = constants.pi*omega0y**2/wavelength

        ngb = NormalizedGaussBeam(wavelength=wavelength, 
                    p0=p0, omega0x=omega0x, omega0y=omega0y)

        self.assertEqual(ngb.cx, cx)
        self.assertEqual(ngb.cy, cy)
        self.assertAlmostEqual(ngb.c, c) 
        self.assertEqual(ngb.p0, p0)
        self.assertEqual(ngb.omega0x, omega0x)
        self.assertEqual(ngb.omega0y, omega0y)
        self.assertEqual(ngb.mx, 0)
        self.assertEqual(ngb.my, 0)
        self.assertEqual(ngb.z0x, z0x)
        self.assertEqual(ngb.z0y, z0y)


class Test_GaussBeam(unittest.TestCase):

    def test_constructor(self):
        A0, wavelength, p0, omega0x, omega0y = 4, 980e-9, 0, 1e-6, 1.2e-6

        cx = (2/constants.pi)**(1/4)/np.sqrt(omega0x)
        cy = (2/constants.pi)**(1/4)/np.sqrt(omega0y)
        c = np.sqrt(2/constants.pi)/np.sqrt(omega0x*omega0y)
        z0x = constants.pi*omega0x**2/wavelength
        z0y = constants.pi*omega0y**2/wavelength

        gb = GaussBeam(wavelength=wavelength, 
                    p0=p0, omega0x=omega0x, omega0y=omega0y, A0=A0)

        self.assertEqual(gb.cx, cx)
        self.assertEqual(gb.cy, cy)
        self.assertAlmostEqual(gb.c, c) 
        self.assertEqual(gb.p0, p0)
        self.assertEqual(gb.omega0x, omega0x)
        self.assertEqual(gb.omega0y, omega0y)
        self.assertEqual(gb.mx, 0)
        self.assertEqual(gb.my, 0)
        self.assertEqual(gb.z0x, z0x)
        self.assertEqual(gb.z0y, z0y)

        self.assertAlmostEqual(gb.A_f(10), A0/(1+(10-p0)**2/z0x**2)**(1/4)/(1+(10-p0)**2/z0y**2)**(1/4))  # 振幅


class Test_NormalizedAxisymmetricHermiteGaussBeam(unittest.TestCase):

    def test_constructor(self):
        wavelength, p0, omega0, m = 980e-9, 0, 1e-6, 3

        c = (2/constants.pi)**(1/2)/(omega0*(2**m)*special.factorial(m))
        z0 = constants.pi*omega0**2/wavelength

        nashgb = NormalizedAxisymmetricHermiteGaussBeam(wavelength=wavelength, p0=p0, omega0=omega0,
                    m=m)
        
        self.assertAlmostEqual(nashgb.c, c) 

        self.assertAlmostEqual(nashgb.A_f(10), 1/(1+(10-p0)**2/z0**2)**(1/2))  # 振幅


class Test_AxisymmetricHermiteGaussBeam(unittest.TestCase):

    def test_constructor(self):
        A0, wavelength, p0, omega0, m = 2, 980e-9, 0, 1e-6, 3

        c = (2/constants.pi)**(1/2)/(omega0*(2**m)*special.factorial(m))
        z0 = constants.pi*omega0**2/wavelength

        ashgb = AxisymmetricHermiteGaussBeam(A0=A0, wavelength=wavelength, p0=p0, omega0=omega0,
                    m=m)
        
        self.assertAlmostEqual(ashgb.c, c) 

        self.assertAlmostEqual(ashgb.A_f(10), A0/(1+(10-p0)**2/z0**2)**(1/2))  # 振幅


class Test_NormalizedAxisymmetricGaussBeam(unittest.TestCase):

    def test_constructor(self):
        wavelength, p0, omega0 = 980e-9, 0, 1e-6

        c = (2/constants.pi)**(1/2)/(omega0)
        z0 = constants.pi*omega0**2/wavelength

        nasgb = NormalizedAxisymmetricGaussBeam(wavelength=wavelength, p0=p0, omega0=omega0)
        
        self.assertAlmostEqual(nasgb.c, c) 

        self.assertAlmostEqual(nasgb.A_f(10), 1/(1+(10-p0)**2/z0**2)**(1/2))  # 振幅


class Test_AxisymmetricGaussBeam(unittest.TestCase):

    def test_constructor(self):
        A0, wavelength, p0, omega0 = 3, 980e-9, 0, 1e-6

        c = (2/constants.pi)**(1/2)/(omega0)
        z0 = constants.pi*omega0**2/wavelength

        asgb = AxisymmetricGaussBeam(A0=A0, wavelength=wavelength, p0=p0, omega0=omega0)
        
        self.assertAlmostEqual(asgb.c, c)
        self.assertAlmostEqual(asgb.m, 0)

        self.assertAlmostEqual(asgb.A_f(10), A0/(1+(10-p0)**2/z0**2)**(1/2))  # 振幅


if __name__ == '__main__':
    unittest.main()
