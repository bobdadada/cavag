import unittest

import numpy as np
from scipy import constants
from scipy import special
from cavag.gaussbeam import *


class Test_NormalizedHermiteGaussBeam1D(unittest.TestCase):
    
    def test_constructor(self):
        wavelength, p0, omega0, m = 1550e-9, 0, 4e-6, 3
        cm = (2/constants.pi)**(1/4)/np.sqrt(omega0*(2**m)*special.factorial(m))
        z0 = constants.pi*omega0**2/wavelength
        theta = np.sqrt(2*m+1)*np.arctan(omega0/z0)

        nhgb1d = NormalizedHermiteGaussBeam1D(wavelength=wavelength, p0=p0, omega0=omega0, m=m)
        
        self.assertEqual(nhgb1d.cm, cm)
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

        cm = (2/constants.pi)**(1/4)/np.sqrt(omega0*(2**m)*special.factorial(m))
        z0 = constants.pi*omega0**2/wavelength

        self.assertEqual(nhgb1d.cm, cm)
        self.assertEqual(nhgb1d.p0, p0)
        self.assertEqual(nhgb1d.omega0, omega0)
        self.assertEqual(nhgb1d.m, m)
        self.assertEqual(nhgb1d.z0, z0)


class Test_HermiteGaussBeam1D(unittest.TestCase):

    def test_constructor(self):
        A0, wavelength, p0, omega0, m = 2, 980e-9, 0, 1e-6, 3
        cm = (2/constants.pi)**(1/4)/np.sqrt(omega0*(2**m)*special.factorial(m))
        z0 = constants.pi*omega0**2/wavelength

        hgb1d = HermiteGaussBeam1D(A0=A0, wavelength=wavelength, p0=p0, omega0=omega0, m=m)

        self.assertEqual(hgb1d.A0, A0)
        self.assertEqual(hgb1d.cm, cm)
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
        cm = (2/constants.pi)**(1/4)/np.sqrt(omega0)
        z0 = constants.pi*omega0**2/wavelength

        ngb1d = NormalizedGaussBeam1D(wavelength=wavelength, p0=p0, omega0=omega0)

        self.assertEqual(ngb1d.cm, cm)
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
        cm = (2/constants.pi)**(1/4)/np.sqrt(omega0)
        z0 = constants.pi*omega0**2/wavelength

        gb1d = GaussBeam1D(A0=A0, wavelength=wavelength, p0=p0, omega0=omega0)

        self.assertEqual(gb1d.cm, cm)
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

        cmx = (2/constants.pi)**(1/4)/np.sqrt(omega0x*(2**mx)*special.factorial(mx))
        cmy = (2/constants.pi)**(1/4)/np.sqrt(omega0y*(2**my)*special.factorial(my))
        cm = np.sqrt(2/constants.pi)/np.sqrt(omega0x*omega0y*(2**(mx+my))*special.factorial(mx)*special.factorial(my))
        z0x = constants.pi*omega0x**2/wavelength
        z0y = constants.pi*omega0y**2/wavelength

        nhgb = NormalizedHermiteGaussBeam(wavelength=wavelength, 
                    p0=p0, omega0x=omega0x, omega0y=omega0y, mx=mx, my=my)
        
        self.assertEqual(nhgb.cmx, cmx)
        self.assertEqual(nhgb.cmy, cmy)
        self.assertAlmostEqual(nhgb.cm, cm) 
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

        cmx = (2/constants.pi)**(1/4)/np.sqrt(omega0x*(2**mx)*special.factorial(mx))
        cmy = (2/constants.pi)**(1/4)/np.sqrt(omega0y*(2**my)*special.factorial(my))
        cm = np.sqrt(2/constants.pi)/np.sqrt(omega0x*omega0y*(2**(mx+my))*special.factorial(mx)*special.factorial(my))
        z0x = constants.pi*omega0x**2/wavelength
        z0y = constants.pi*omega0y**2/wavelength
        
        self.assertEqual(nhgb.cmx, cmx)
        self.assertEqual(nhgb.cmy, cmy)
        self.assertAlmostEqual(nhgb.cm, cm) 
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

        cmx = (2/constants.pi)**(1/4)/np.sqrt(omega0x*(2**mx)*special.factorial(mx))
        cmy = (2/constants.pi)**(1/4)/np.sqrt(omega0y*(2**my)*special.factorial(my))
        cm = np.sqrt(2/constants.pi)/np.sqrt(omega0x*omega0y*(2**(mx+my))*special.factorial(mx)*special.factorial(my))
        z0x = constants.pi*omega0x**2/wavelength
        z0y = constants.pi*omega0y**2/wavelength

        hgb = HermiteGaussBeam(A0=A0, wavelength=wavelength, 
                    p0=p0, omega0x=omega0x, omega0y=omega0y, mx=mx, my=my)

        self.assertEqual(hgb.A0, A0)
        self.assertEqual(hgb.cmx, cmx)
        self.assertEqual(hgb.cmy, cmy)
        self.assertAlmostEqual(hgb.cm, cm) 
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

        cmx = (2/constants.pi)**(1/4)/np.sqrt(omega0x)
        cmy = (2/constants.pi)**(1/4)/np.sqrt(omega0y)
        cm = np.sqrt(2/constants.pi)/np.sqrt(omega0x*omega0y)
        z0x = constants.pi*omega0x**2/wavelength
        z0y = constants.pi*omega0y**2/wavelength

        ngb = NormalizedGaussBeam(wavelength=wavelength, 
                    p0=p0, omega0x=omega0x, omega0y=omega0y)

        self.assertEqual(ngb.cmx, cmx)
        self.assertEqual(ngb.cmy, cmy)
        self.assertAlmostEqual(ngb.cm, cm) 
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

        cmx = (2/constants.pi)**(1/4)/np.sqrt(omega0x)
        cmy = (2/constants.pi)**(1/4)/np.sqrt(omega0y)
        cm = np.sqrt(2/constants.pi)/np.sqrt(omega0x*omega0y)
        z0x = constants.pi*omega0x**2/wavelength
        z0y = constants.pi*omega0y**2/wavelength

        gb = GaussBeam(wavelength=wavelength, 
                    p0=p0, omega0x=omega0x, omega0y=omega0y, A0=A0)

        self.assertEqual(gb.cmx, cmx)
        self.assertEqual(gb.cmy, cmy)
        self.assertAlmostEqual(gb.cm, cm) 
        self.assertEqual(gb.p0, p0)
        self.assertEqual(gb.omega0x, omega0x)
        self.assertEqual(gb.omega0y, omega0y)
        self.assertEqual(gb.mx, 0)
        self.assertEqual(gb.my, 0)
        self.assertEqual(gb.z0x, z0x)
        self.assertEqual(gb.z0y, z0y)

        self.assertAlmostEqual(gb.A_f(10), A0/(1+(10-p0)**2/z0x**2)**(1/4)/(1+(10-p0)**2/z0y**2)**(1/4))  # 振幅


class Test_NormalizedEqualSymmetricHermiteGaussBeam(unittest.TestCase):

    def test_constructor(self):
        wavelength, p0, omega0, m = 980e-9, 0, 1e-6, 3

        cm = (2/constants.pi)**(1/2)/(omega0*(2**m)*special.factorial(m))
        z0 = constants.pi*omega0**2/wavelength

        neshgb = NormalizedEqualSymmetricHermiteGaussBeam(wavelength=wavelength, p0=p0, omega0=omega0,
                    m=m)
        
        self.assertAlmostEqual(neshgb.cm, cm) 

        self.assertAlmostEqual(neshgb.A_f(10), 1/(1+(10-p0)**2/z0**2)**(1/2))  # 振幅
    
    def test_subclass(self):

        class A(NormalizedEqualSymmetricHermiteGaussBeam):

            @property
            def cm(self):
                self.a_v = 1
                return super().cm
        
        wavelength, p0, omega0, m = 980e-9, 0, 1e-6, 3

        cm = (2/constants.pi)**(1/2)/(omega0*(2**m)*special.factorial(m))
        z0 = constants.pi*omega0**2/wavelength

        a = A(wavelength=wavelength, p0=p0, omega0=omega0, m=m)

        self.assertAlmostEqual(a.cm, cm)
        self.assertAlmostEqual(a.a_v, 1)


class Test_EqualSymmetricHermiteGaussBeam(unittest.TestCase):

    def test_constructor(self):
        A0, wavelength, p0, omega0, m = 2, 980e-9, 0, 1e-6, 3

        cm = (2/constants.pi)**(1/2)/(omega0*(2**m)*special.factorial(m))
        z0 = constants.pi*omega0**2/wavelength

        eshgb = EqualSymmetricHermiteGaussBeam(A0=A0, wavelength=wavelength, p0=p0, omega0=omega0,
                    m=m)
        
        self.assertAlmostEqual(eshgb.cm, cm) 

        self.assertAlmostEqual(eshgb.A_f(10), A0/(1+(10-p0)**2/z0**2)**(1/2))  # 振幅


class Test_NormalizedEqualSymmetricGaussBeam(unittest.TestCase):

    def test_constructor(self):
        wavelength, p0, omega0 = 980e-9, 0, 1e-6

        cm = (2/constants.pi)**(1/2)/(omega0)
        z0 = constants.pi*omega0**2/wavelength

        nesgb = NormalizedEqualSymmetricGaussBeam(wavelength=wavelength, p0=p0, omega0=omega0)
        
        self.assertAlmostEqual(nesgb.cm, cm) 

        self.assertAlmostEqual(nesgb.A_f(10), 1/(1+(10-p0)**2/z0**2)**(1/2))  # 振幅


class Test_EqualSymmetricGaussBeam(unittest.TestCase):

    def test_constructor(self):
        A0, wavelength, p0, omega0 = 3, 980e-9, 0, 1e-6

        cm = (2/constants.pi)**(1/2)/(omega0)
        z0 = constants.pi*omega0**2/wavelength

        esgb = EqualSymmetricGaussBeam(A0=A0, wavelength=wavelength, p0=p0, omega0=omega0)
        
        self.assertAlmostEqual(esgb.cm, cm)
        self.assertAlmostEqual(esgb.m, 0)

        self.assertAlmostEqual(esgb.A_f(10), A0/(1+(10-p0)**2/z0**2)**(1/2))  # 振幅


class Test_transformation(unittest.TestCase):

    def test_local2remote(self):
        wavelength = 493e-9

        omega0 = 10e-6
        z = 100e-6
        omega, R = local2remote(wavelength, omega0, z)

        zr = constants.pi * omega0 ** 2 / wavelength

        self.assertTrue(R > 0)
        self.assertEqual(omega, omega0 * np.sqrt(1 + ( z / zr) ** 2))
        self.assertEqual(R, z * (1 + (zr / z) ** 2))
    
    def test_remote2local(self):
        pass

if __name__ == '__main__':
    unittest.main()
