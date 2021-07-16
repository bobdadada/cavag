import unittest

import numpy as np
from scipy import constants
from scipy import special
from cavag.gaussbeam import *


class Test_NormalizedHermiteGaussBeam1D(unittest.TestCase):

    def test_constructor(self):
        wavelength, p0, omega0, m = 1550e-9, 0, 4e-6, 3
        cm = (2/constants.pi)**(1/4) / \
            np.sqrt(omega0*(2**m)*special.factorial(m))
        z0 = constants.pi*omega0**2/wavelength
        thetam = np.sqrt(2*m+1)*np.arctan(omega0/z0)

        nhgb1d = NormalizedHermiteGaussBeam1D(
            wavelength=wavelength, p0=p0, omega0=omega0, m=m)

        self.assertEqual(nhgb1d.cm, cm)
        self.assertEqual(nhgb1d.p0, p0)
        self.assertEqual(nhgb1d.omega0, omega0)
        self.assertEqual(nhgb1d.m, m)
        self.assertEqual(nhgb1d.z0, z0)
        self.assertAlmostEqual(nhgb1d.thetam, thetam)

        self.assertAlmostEqual(nhgb1d.a_f(
            10), 1/(1+(10-p0)**2/z0**2)**(1/4))  # 振幅
        self.assertAlmostEqual(nhgb1d.omega_f(
            10), omega0*np.sqrt(1+(10-p0)**2/z0**2))  # 模场半径
        self.assertAlmostEqual(nhgb1d.r_f(10), (10-p0)
                               * (1+z0**2/(10-p0)**2))  # 波前曲率半径
        self.assertAlmostEqual(nhgb1d.phi_f(
            10), np.arctan((10-p0)/z0))  # phi相位

    def test_change_properties(self):
        wavelength, p0, omega0, m = 980e-9, 0, 1e-6, 3
        nhgb1d = NormalizedHermiteGaussBeam1D(
            wavelength=wavelength, p0=p0, omega0=omega0, m=m)

        m = 0
        nhgb1d.change_params(m=m)

        cm = (2/constants.pi)**(1/4) / \
            np.sqrt(omega0*(2**m)*special.factorial(m))
        z0 = constants.pi*omega0**2/wavelength

        self.assertEqual(nhgb1d.cm, cm)
        self.assertEqual(nhgb1d.p0, p0)
        self.assertEqual(nhgb1d.omega0, omega0)
        self.assertEqual(nhgb1d.m, m)
        self.assertEqual(nhgb1d.z0, z0)


class Test_HermiteGaussBeam1D(unittest.TestCase):

    def test_constructor(self):
        a0, wavelength, p0, omega0, m = 2, 980e-9, 0, 1e-6, 3
        cm = (2/constants.pi)**(1/4) / \
            np.sqrt(omega0*(2**m)*special.factorial(m))
        z0 = constants.pi*omega0**2/wavelength

        hgb1d = HermiteGaussBeam1D(
            a0=a0, wavelength=wavelength, p0=p0, omega0=omega0, m=m)

        self.assertEqual(hgb1d.a0, a0)
        self.assertEqual(hgb1d.cm, cm)
        self.assertEqual(hgb1d.p0, p0)
        self.assertEqual(hgb1d.omega0, omega0)
        self.assertEqual(hgb1d.m, m)
        self.assertEqual(hgb1d.z0, z0)

        self.assertAlmostEqual(
            hgb1d.a_f(10), a0/(1+(10-p0)**2/z0**2)**(1/4))  # 振幅
        self.assertAlmostEqual(hgb1d.omega_f(
            10), omega0*np.sqrt(1+(10-p0)**2/z0**2))  # 模场半径
        self.assertAlmostEqual(hgb1d.r_f(10), (10-p0) *
                               (1+z0**2/(10-p0)**2))  # 波前曲率半径
        self.assertAlmostEqual(hgb1d.phi_f(10), np.arctan((10-p0)/z0))  # phi相位


class Test_NormalizedGaussBeam1D(unittest.TestCase):

    def test_constructor(self):
        wavelength, p0, omega0 = 980e-9, 0, 1e-6
        cm = (2/constants.pi)**(1/4)/np.sqrt(omega0)
        z0 = constants.pi*omega0**2/wavelength

        ngb1d = NormalizedGaussBeam1D(
            wavelength=wavelength, p0=p0, omega0=omega0)

        self.assertEqual(ngb1d.cm, cm)
        self.assertEqual(ngb1d.p0, p0)
        self.assertEqual(ngb1d.omega0, omega0)
        self.assertEqual(ngb1d.m, 0)
        self.assertEqual(ngb1d.z0, z0)

        self.assertAlmostEqual(
            ngb1d.a_f(10), 1/(1+(10-p0)**2/z0**2)**(1/4))  # 振幅
        self.assertAlmostEqual(ngb1d.omega_f(
            10), omega0*np.sqrt(1+(10-p0)**2/z0**2))  # 模场半径
        self.assertAlmostEqual(ngb1d.r_f(10), (10-p0) *
                               (1+z0**2/(10-p0)**2))  # 波前曲率半径
        self.assertAlmostEqual(ngb1d.phi_f(10), np.arctan((10-p0)/z0))  # phi相位


class Test_GaussBeam1D(unittest.TestCase):

    def test_constructor(self):
        a0, wavelength, p0, omega0 = 2, 980e-9, 0, 1e-6
        cm = (2/constants.pi)**(1/4)/np.sqrt(omega0)
        z0 = constants.pi*omega0**2/wavelength

        gb1d = GaussBeam1D(a0=a0, wavelength=wavelength, p0=p0, omega0=omega0)

        self.assertEqual(gb1d.cm, cm)
        self.assertEqual(gb1d.p0, p0)
        self.assertEqual(gb1d.omega0, omega0)
        self.assertEqual(gb1d.m, 0)
        self.assertEqual(gb1d.z0, z0)

        self.assertAlmostEqual(
            gb1d.a_f(10), a0/(1+(10-p0)**2/z0**2)**(1/4))  # 振幅
        self.assertAlmostEqual(gb1d.omega_f(
            10), omega0*np.sqrt(1+(10-p0)**2/z0**2))  # 模场半径
        self.assertAlmostEqual(gb1d.r_f(10), (10-p0) *
                               (1+z0**2/(10-p0)**2))  # 波前曲率半径
        self.assertAlmostEqual(gb1d.phi_f(10), np.arctan((10-p0)/z0))  # phi相位


class Test_NormalizedHermiteGaussBeam(unittest.TestCase):

    def test_constructor(self):
        wavelength, p0, omega0x, omega0y, mx, my = 980e-9, 0, 1e-6, 1.2e-6, 1, 2

        cmx = (2/constants.pi)**(1/4) / \
            np.sqrt(omega0x*(2**mx)*special.factorial(mx))
        cmy = (2/constants.pi)**(1/4) / \
            np.sqrt(omega0y*(2**my)*special.factorial(my))
        cm = np.sqrt(2/constants.pi)/np.sqrt(omega0x*omega0y *
                                             (2**(mx+my))*special.factorial(mx)*special.factorial(my))
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

        cmx = (2/constants.pi)**(1/4) / \
            np.sqrt(omega0x*(2**mx)*special.factorial(mx))
        cmy = (2/constants.pi)**(1/4) / \
            np.sqrt(omega0y*(2**my)*special.factorial(my))
        cm = np.sqrt(2/constants.pi)/np.sqrt(omega0x*omega0y *
                                             (2**(mx+my))*special.factorial(mx)*special.factorial(my))
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
        a0, wavelength, p0, omega0x, omega0y, mx, my = 3, 980e-9, 0, 1e-6, 1.2e-6, 1, 2

        cmx = (2/constants.pi)**(1/4) / \
            np.sqrt(omega0x*(2**mx)*special.factorial(mx))
        cmy = (2/constants.pi)**(1/4) / \
            np.sqrt(omega0y*(2**my)*special.factorial(my))
        cm = np.sqrt(2/constants.pi)/np.sqrt(omega0x*omega0y *
                                             (2**(mx+my))*special.factorial(mx)*special.factorial(my))
        z0x = constants.pi*omega0x**2/wavelength
        z0y = constants.pi*omega0y**2/wavelength

        hgb = HermiteGaussBeam(a0=a0, wavelength=wavelength,
                               p0=p0, omega0x=omega0x, omega0y=omega0y, mx=mx, my=my)

        self.assertEqual(hgb.a0, a0)
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

        self.assertAlmostEqual(
            hgb.a_f(10), a0/(1+(10-p0)**2/z0x**2)**(1/4)/(1+(10-p0)**2/z0y**2)**(1/4))  # 振幅


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
        a0, wavelength, p0, omega0x, omega0y = 4, 980e-9, 0, 1e-6, 1.2e-6

        cmx = (2/constants.pi)**(1/4)/np.sqrt(omega0x)
        cmy = (2/constants.pi)**(1/4)/np.sqrt(omega0y)
        cm = np.sqrt(2/constants.pi)/np.sqrt(omega0x*omega0y)
        z0x = constants.pi*omega0x**2/wavelength
        z0y = constants.pi*omega0y**2/wavelength

        gb = GaussBeam(wavelength=wavelength,
                       p0=p0, omega0x=omega0x, omega0y=omega0y, a0=a0)

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

        self.assertAlmostEqual(
            gb.a_f(10), a0/(1+(10-p0)**2/z0x**2)**(1/4)/(1+(10-p0)**2/z0y**2)**(1/4))  # 振幅


class Test_NormalizedEqualHermiteGaussBeam(unittest.TestCase):

    def test_constructor(self):
        wavelength, p0, omega0, mx, my = 980e-9, 0, 1.2e-6, 1, 2

        cmx = (2/constants.pi)**(1/4) / \
            np.sqrt(omega0*(2**mx)*special.factorial(mx))
        cmy = (2/constants.pi)**(1/4) / \
            np.sqrt(omega0*(2**my)*special.factorial(my))
        cm = np.sqrt(2/constants.pi)/np.sqrt(omega0*omega0 *
                                             (2**(mx+my))*special.factorial(mx)*special.factorial(my))
        z0 = constants.pi*omega0**2/wavelength

        nehgb = NormalizedEqualHermiteGaussBeam(wavelength=wavelength,
                                                p0=p0, omega0=omega0, mx=mx, my=my)

        self.assertEqual(nehgb.mx, mx)
        self.assertEqual(nehgb.my, my)
        self.assertEqual(nehgb.cmx, cmx)
        self.assertEqual(nehgb.cmy, cmy)
        self.assertAlmostEqual(nehgb.cm, cm)
        self.assertEqual(nehgb.p0, p0)
        self.assertEqual(nehgb.omega0, omega0)
        self.assertEqual(nehgb.omega0x, omega0)
        self.assertEqual(nehgb.omega0y, omega0)
        self.assertEqual(nehgb.z0, z0)
        self.assertEqual(nehgb.z0x, z0)
        self.assertEqual(nehgb.z0y, z0)

    def test_change_properties(self):
        wavelength, p0, omega0, mx, my = 980e-9, 0, 1.2e-6, 1, 2

        nehgb = NormalizedEqualHermiteGaussBeam(wavelength=wavelength,
                                                p0=p0, omega0=omega0, mx=mx, my=my)

        mx, my = 2, 3
        nehgb.change_params(mx=mx, my=my)

        cmx = (2/constants.pi)**(1/4) / \
            np.sqrt(omega0*(2**mx)*special.factorial(mx))
        cmy = (2/constants.pi)**(1/4) / \
            np.sqrt(omega0*(2**my)*special.factorial(my))
        cm = np.sqrt(2/constants.pi)/np.sqrt(omega0*omega0 *
                                             (2**(mx+my))*special.factorial(mx)*special.factorial(my))
        z0 = constants.pi*omega0**2/wavelength

        self.assertEqual(nehgb.cmx, cmx)
        self.assertEqual(nehgb.cmy, cmy)
        self.assertAlmostEqual(nehgb.cm, cm)
        self.assertEqual(nehgb.p0, p0)
        self.assertEqual(nehgb.omega0, omega0)
        self.assertEqual(nehgb.omega0x, omega0)
        self.assertEqual(nehgb.omega0y, omega0)
        self.assertEqual(nehgb.mx, mx)
        self.assertEqual(nehgb.my, my)
        self.assertEqual(nehgb.z0, z0)
        self.assertEqual(nehgb.z0x, z0)
        self.assertEqual(nehgb.z0y, z0)


class Test_EqualHermiteGaussBeam(unittest.TestCase):

    def test_constructor(self):
        a0,  wavelength, p0, omega0, mx, my = 4, 980e-9, 0, 1.2e-6, 1, 2

        cmx = (2/constants.pi)**(1/4) / \
            np.sqrt(omega0*(2**mx)*special.factorial(mx))
        cmy = (2/constants.pi)**(1/4) / \
            np.sqrt(omega0*(2**my)*special.factorial(my))
        cm = np.sqrt(2/constants.pi)/np.sqrt(omega0*omega0 *
                                             (2**(mx+my))*special.factorial(mx)*special.factorial(my))
        z0 = constants.pi*omega0**2/wavelength

        ehgb = EqualHermiteGaussBeam(a0=a0, wavelength=wavelength,
                                     p0=p0, omega0=omega0, mx=mx, my=my)

        self.assertEqual(ehgb.cmx, cmx)
        self.assertEqual(ehgb.cmy, cmy)
        self.assertAlmostEqual(ehgb.cm, cm)
        self.assertEqual(ehgb.p0, p0)
        self.assertEqual(ehgb.omega0, omega0)
        self.assertEqual(ehgb.omega0x, omega0)
        self.assertEqual(ehgb.omega0y, omega0)
        self.assertEqual(ehgb.mx, mx)
        self.assertEqual(ehgb.my, my)
        self.assertEqual(ehgb.z0, z0)
        self.assertEqual(ehgb.z0x, z0)
        self.assertEqual(ehgb.z0y, z0)

        self.assertAlmostEqual(
            ehgb.a_f(10), a0/(1+(10-p0)**2/z0**2)**(1/4)/(1+(10-p0)**2/z0**2)**(1/4))  # 振幅


class Test_NormalizedEqualSymmetricHermiteGaussBeam(unittest.TestCase):

    def test_constructor(self):
        wavelength, p0, omega0, m = 980e-9, 0, 1e-6, 3

        cm = (2/constants.pi)**(1/2)/(omega0*(2**m)*special.factorial(m))
        z0 = constants.pi*omega0**2/wavelength

        neshgb = NormalizedEqualSymmetricHermiteGaussBeam(wavelength=wavelength, p0=p0, omega0=omega0,
                                                          m=m)

        self.assertAlmostEqual(neshgb.cm, cm)

        self.assertAlmostEqual(neshgb.a_f(
            10), 1/(1+(10-p0)**2/z0**2)**(1/2))  # 振幅

    def test_subclass(self):

        class Subclass(NormalizedEqualSymmetricHermiteGaussBeam):

            @property
            def cm(self):
                self.a_v = 1
                return super().cm

        wavelength, p0, omega0, m = 980e-9, 0, 1e-6, 3

        cm = (2/constants.pi)**(1/2)/(omega0*(2**m)*special.factorial(m))
        z0 = constants.pi*omega0**2/wavelength

        instance = Subclass(wavelength=wavelength, p0=p0, omega0=omega0, m=m)

        self.assertAlmostEqual(instance.cm, cm)
        self.assertAlmostEqual(instance.a_v, 1)


class Test_EqualSymmetricHermiteGaussBeam(unittest.TestCase):

    def test_constructor(self):
        a0, wavelength, p0, omega0, m = 2, 980e-9, 0, 1e-6, 3

        cm = (2/constants.pi)**(1/2)/(omega0*(2**m)*special.factorial(m))
        z0 = constants.pi*omega0**2/wavelength

        eshgb = EqualSymmetricHermiteGaussBeam(a0=a0, wavelength=wavelength, p0=p0, omega0=omega0,
                                               m=m)

        self.assertAlmostEqual(eshgb.cm, cm)

        self.assertAlmostEqual(
            eshgb.a_f(10), a0/(1+(10-p0)**2/z0**2)**(1/2))  # 振幅


class Test_NormalizedEqualGaussBeam(unittest.TestCase):

    def test_constructor(self):
        wavelength, p0, omega0 = 980e-9, 0, 1e-6

        cm = (2/constants.pi)**(1/2)/(omega0)
        z0 = constants.pi*omega0**2/wavelength

        negb = NormalizedEqualGaussBeam(
            wavelength=wavelength, p0=p0, omega0=omega0)

        self.assertAlmostEqual(negb.cm, cm)

        self.assertAlmostEqual(
            negb.a_f(10), 1/(1+(10-p0)**2/z0**2)**(1/2))  # 振幅


class Test_EqualGaussBeam(unittest.TestCase):

    def test_constructor(self):
        a0, wavelength, p0, omega0 = 3, 980e-9, 0, 1e-6

        cm = (2/constants.pi)**(1/2)/(omega0)
        z0 = constants.pi*omega0**2/wavelength

        egb = EqualGaussBeam(a0=a0, wavelength=wavelength,
                             p0=p0, omega0=omega0)

        self.assertAlmostEqual(egb.cm, cm)
        self.assertAlmostEqual(egb.m, 0)

        self.assertAlmostEqual(
            egb.a_f(10), a0/(1+(10-p0)**2/z0**2)**(1/2))  # 振幅


class Test_transformation(unittest.TestCase):

    def test_local2remote(self):
        wavelength = 493e-9

        omega0 = 10e-6
        z = 100e-6
        omega, r = local2remote(wavelength, omega0, z)

        zr = constants.pi * omega0 ** 2 / wavelength

        self.assertTrue(r > 0)
        self.assertEqual(omega, omega0 * np.sqrt(1 + (z / zr) ** 2))
        self.assertEqual(r, z * (1 + (zr / z) ** 2))

    def test_remote2local(self):
        wavelength = 493e-9

        omega = 30e-6
        r = 200e-6

        omega0, z = remote2local(wavelength, omega, r)

        zrp = constants.pi * omega ** 2 / wavelength

        self.assertTrue(omega0 > 0)
        self.assertTrue(z > 0)
        self.assertEqual(omega0, omega / np.sqrt(1 + (zrp / r) ** 2))
        self.assertEqual(z, r / (1 + (r / zrp) ** 2))

    def test_convert_through_lens(self):
        wavelength = 493e-9

        omega0 = 10e-6
        s = -20  # 2f
        f = abs(s)/2

        omega0p, sp = convert_through_lens(wavelength, omega0, s, f)

        self.assertTrue(omega0p > 0)
        self.assertTrue(sp > 0)
        self.assertAlmostEqual(sp, abs(s))
        self.assertAlmostEqual(omega0p, omega0)

    def test_convert_through_mirror(self):
        wavelength = 493e-9

        omega0 = 10e-6
        s = -20  # 2f
        roc = abs(s)

        omega0p, sp = convert_through_mirror(wavelength, omega0, s, roc)

        self.assertTrue(omega0p > 0)
        self.assertTrue(sp < 0)
        self.assertAlmostEqual(sp, s)
        self.assertAlmostEqual(omega0p, omega0)


if __name__ == '__main__':
    unittest.main()
