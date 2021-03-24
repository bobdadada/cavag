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


class Test_NormalizedHermiteGaussBeam2D(unittest.TestCase):

    def test_constructor(self):
        wavelength, p0, omega0x, omega0y, mx, my = 980e-9, 0, 1e-6, 1.2e-6, 1, 2

        cx = (2/constants.pi)**(1/4)/np.sqrt(omega0x*(2**mx)*special.factorial(mx))
        cy = (2/constants.pi)**(1/4)/np.sqrt(omega0y*(2**my)*special.factorial(my))
        c = np.sqrt(2/constants.pi)/np.sqrt(omega0x*omega0y*(2**(mx+my))*special.factorial(mx)*special.factorial(my))
        z0x = constants.pi*omega0x**2/wavelength
        z0y = constants.pi*omega0y**2/wavelength

        nhgb2d = NormalizedHermiteGaussBeam2D(wavelength=wavelength, 
                    p0=p0, omega0x=omega0x, omega0y=omega0y, mx=mx, my=my)
        
        self.assertEqual(nhgb2d.cx, cx)
        self.assertEqual(nhgb2d.cy, cy)
        self.assertAlmostEqual(nhgb2d.c, c) 
        self.assertEqual(nhgb2d.p0, p0)
        self.assertEqual(nhgb2d.omega0x, omega0x)
        self.assertEqual(nhgb2d.omega0y, omega0y)
        self.assertEqual(nhgb2d.mx, mx)
        self.assertEqual(nhgb2d.my, my)
        self.assertEqual(nhgb2d.z0x, z0x)
        self.assertEqual(nhgb2d.z0y, z0y)
    
    def test_change_properties(self):
        wavelength, p0, omega0x, omega0y, mx, my = 980e-9, 0, 1e-6, 1.2e-6, 1, 2

        nhgb2d = NormalizedHermiteGaussBeam2D(wavelength=wavelength, 
                    p0=p0, omega0x=omega0x, omega0y=omega0y, mx=mx, my=my)
        
        mx, my = 2, 3
        nhgb2d.change_params(mx=mx, my=my)

        cx = (2/constants.pi)**(1/4)/np.sqrt(omega0x*(2**mx)*special.factorial(mx))
        cy = (2/constants.pi)**(1/4)/np.sqrt(omega0y*(2**my)*special.factorial(my))
        c = np.sqrt(2/constants.pi)/np.sqrt(omega0x*omega0y*(2**(mx+my))*special.factorial(mx)*special.factorial(my))
        z0x = constants.pi*omega0x**2/wavelength
        z0y = constants.pi*omega0y**2/wavelength
        
        self.assertEqual(nhgb2d.cx, cx)
        self.assertEqual(nhgb2d.cy, cy)
        self.assertAlmostEqual(nhgb2d.c, c) 
        self.assertEqual(nhgb2d.p0, p0)
        self.assertEqual(nhgb2d.omega0x, omega0x)
        self.assertEqual(nhgb2d.omega0y, omega0y)
        self.assertEqual(nhgb2d.mx, mx)
        self.assertEqual(nhgb2d.my, my)
        self.assertEqual(nhgb2d.z0x, z0x)
        self.assertEqual(nhgb2d.z0y, z0y)


class Test_HermiteGaussBeam2D(unittest.TestCase):

    def test_constructor(self):
        A0, wavelength, p0, omega0x, omega0y, mx, my = 3, 980e-9, 0, 1e-6, 1.2e-6, 1, 2

        cx = (2/constants.pi)**(1/4)/np.sqrt(omega0x*(2**mx)*special.factorial(mx))
        cy = (2/constants.pi)**(1/4)/np.sqrt(omega0y*(2**my)*special.factorial(my))
        c = np.sqrt(2/constants.pi)/np.sqrt(omega0x*omega0y*(2**(mx+my))*special.factorial(mx)*special.factorial(my))
        z0x = constants.pi*omega0x**2/wavelength
        z0y = constants.pi*omega0y**2/wavelength

        hgb2d = HermiteGaussBeam2D(A0=A0, wavelength=wavelength, 
                    p0=p0, omega0x=omega0x, omega0y=omega0y, mx=mx, my=my)

        self.assertEqual(hgb2d.A0, A0)
        self.assertEqual(hgb2d.cx, cx)
        self.assertEqual(hgb2d.cy, cy)
        self.assertAlmostEqual(hgb2d.c, c) 
        self.assertEqual(hgb2d.p0, p0)
        self.assertEqual(hgb2d.omega0x, omega0x)
        self.assertEqual(hgb2d.omega0y, omega0y)
        self.assertEqual(hgb2d.mx, mx)
        self.assertEqual(hgb2d.my, my)
        self.assertEqual(hgb2d.z0x, z0x)
        self.assertEqual(hgb2d.z0y, z0y)

        self.assertAlmostEqual(hgb2d.A_f(10), A0/(1+(10-p0)**2/z0x**2)**(1/4)/(1+(10-p0)**2/z0y**2)**(1/4))  # 振幅


class Test_NormalizedGaussBeam2D(unittest.TestCase):

    def test_constructor(self):
        wavelength, p0, omega0x, omega0y = 980e-9, 0, 1e-6, 1.2e-6

        cx = (2/constants.pi)**(1/4)/np.sqrt(omega0x)
        cy = (2/constants.pi)**(1/4)/np.sqrt(omega0y)
        c = np.sqrt(2/constants.pi)/np.sqrt(omega0x*omega0y)
        z0x = constants.pi*omega0x**2/wavelength
        z0y = constants.pi*omega0y**2/wavelength

        ngb2d = NormalizedGaussBeam2D(wavelength=wavelength, 
                    p0=p0, omega0x=omega0x, omega0y=omega0y)

        self.assertEqual(ngb2d.cx, cx)
        self.assertEqual(ngb2d.cy, cy)
        self.assertAlmostEqual(ngb2d.c, c) 
        self.assertEqual(ngb2d.p0, p0)
        self.assertEqual(ngb2d.omega0x, omega0x)
        self.assertEqual(ngb2d.omega0y, omega0y)
        self.assertEqual(ngb2d.mx, 0)
        self.assertEqual(ngb2d.my, 0)
        self.assertEqual(ngb2d.z0x, z0x)
        self.assertEqual(ngb2d.z0y, z0y)


class Test_GaussBeam2D(unittest.TestCase):

    def test_constructor(self):
        A0, wavelength, p0, omega0x, omega0y = 4, 980e-9, 0, 1e-6, 1.2e-6

        cx = (2/constants.pi)**(1/4)/np.sqrt(omega0x)
        cy = (2/constants.pi)**(1/4)/np.sqrt(omega0y)
        c = np.sqrt(2/constants.pi)/np.sqrt(omega0x*omega0y)
        z0x = constants.pi*omega0x**2/wavelength
        z0y = constants.pi*omega0y**2/wavelength

        gb2d = GaussBeam2D(wavelength=wavelength, 
                    p0=p0, omega0x=omega0x, omega0y=omega0y, A0=A0)

        self.assertEqual(gb2d.cx, cx)
        self.assertEqual(gb2d.cy, cy)
        self.assertAlmostEqual(gb2d.c, c) 
        self.assertEqual(gb2d.p0, p0)
        self.assertEqual(gb2d.omega0x, omega0x)
        self.assertEqual(gb2d.omega0y, omega0y)
        self.assertEqual(gb2d.mx, 0)
        self.assertEqual(gb2d.my, 0)
        self.assertEqual(gb2d.z0x, z0x)
        self.assertEqual(gb2d.z0y, z0y)

        self.assertAlmostEqual(gb2d.A_f(10), A0/(1+(10-p0)**2/z0x**2)**(1/4)/(1+(10-p0)**2/z0y**2)**(1/4))  # 振幅


class Test_NormalizedSymmetricHermiteGaussBeam(unittest.TestCase):

    def test_constructor(self):
        wavelength, p0, omega0, m = 980e-9, 0, 1e-6, 3

        c = (2/constants.pi)**(1/2)/(omega0*(2**m)*special.factorial(m))
        z0 = constants.pi*omega0**2/wavelength

        nshgb = NormalizedSymmetricHermiteGaussBeam(wavelength=wavelength, p0=p0, omega0=omega0,
                    m=m)
        
        self.assertAlmostEqual(nshgb.c, c) 

        self.assertAlmostEqual(nshgb.A_f(10), 1/(1+(10-p0)**2/z0**2)**(1/2))  # 振幅


class Test_SymmetricHermiteGaussBeam(unittest.TestCase):

    def test_constructor(self):
        A0, wavelength, p0, omega0, m = 2, 980e-9, 0, 1e-6, 3

        c = (2/constants.pi)**(1/2)/(omega0*(2**m)*special.factorial(m))
        z0 = constants.pi*omega0**2/wavelength

        shgb = SymmetricHermiteGaussBeam(A0=A0, wavelength=wavelength, p0=p0, omega0=omega0,
                    m=m)
        
        self.assertAlmostEqual(shgb.c, c) 

        self.assertAlmostEqual(shgb.A_f(10), A0/(1+(10-p0)**2/z0**2)**(1/2))  # 振幅


class Test_NormalizedSymmetricGaussBeam(unittest.TestCase):

    def test_constructor(self):
        wavelength, p0, omega0 = 980e-9, 0, 1e-6

        c = (2/constants.pi)**(1/2)/(omega0)
        z0 = constants.pi*omega0**2/wavelength

        nsgb = NormalizedSymmetricGaussBeam(wavelength=wavelength, p0=p0, omega0=omega0)
        
        self.assertAlmostEqual(nsgb.c, c) 

        self.assertAlmostEqual(nsgb.A_f(10), 1/(1+(10-p0)**2/z0**2)**(1/2))  # 振幅


class Test_NormalizedSymmetricGaussBeam(unittest.TestCase):

    def test_constructor(self):
        A0, wavelength, p0, omega0 = 3, 980e-9, 0, 1e-6

        c = (2/constants.pi)**(1/2)/(omega0)
        z0 = constants.pi*omega0**2/wavelength

        nsgb = SymmetricGaussBeam(A0=A0, wavelength=wavelength, p0=p0, omega0=omega0)
        
        self.assertAlmostEqual(nsgb.c, c)
        self.assertAlmostEqual(nsgb.m, 0)

        self.assertAlmostEqual(nsgb.A_f(10), A0/(1+(10-p0)**2/z0**2)**(1/2))  # 振幅


if __name__ == '__main__':
    unittest.main()
