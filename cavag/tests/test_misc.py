import unittest

from scipy import constants
from cavag.misc import *


class Test_RTL(unittest.TestCase):

    def test_constructor(self):
        rtl = RTL(r=1, t=2, l=3)
        self.assertEqual(rtl.r, 1/6)
        self.assertEqual(rtl.t, 2/6)
        self.assertEqual(rtl.l, 3/6)
        self.assertEqual(rtl.property_set, {'r':1/6, 't':2/6, 'l':3/6})
    
    def test_change_properties(self):
        rtl = RTL(r=1, t=1, l=1)

        r, t, l = rtl.r, rtl.t, rtl.l
        rtl.add_loss(0.1)
        self.assertEqual(rtl.l, 0.9*l+0.1)
        self.assertEqual(rtl.r, 0.9*r)

        rtl.change_params(r=1, t=2, l=3)
        self.assertEqual(rtl.r, 1/6)
        self.assertEqual(rtl.t, 2/6)
        self.assertEqual(rtl.l, 3/6)


class Test_RTLConverter(unittest.TestCase):

    def test_normalize(self):
        r, t, l = None, None, None
        for o in RTLConverter.normalize(r, t, l):
            self.assertIsNone(o)
        
        r, t, l = 1, 4, 5
        d = RTLConverter.normalize(r, t, l)
        self.assertTupleEqual(d, (0.1, 0.4, 0.5))

        r, t = 0.2, 0.1
        d = RTLConverter.normalize(r=r, t=t)
        self.assertEqual(d[2], 1-r-t)
    
    def test_rtlconverter(self):
        r = 0.1
        t2l = 10
        r, t, l = RTLConverter.rtl_by_r_t2l(r, t2l)
        self.assertEqual(r, 0.1)
        self.assertEqual(t, 0.9*10/11)
        self.assertEqual(l, 0.9*1/11)

        t = 0.1
        r2l = 10
        r, t, l = RTLConverter.rtl_by_t_r2l(t, r2l)
        self.assertEqual(t, 0.1)
        self.assertEqual(r, 0.9*10/11)
        self.assertEqual(l, 0.9*1/11)
    
    def test_add_rtl(self):
        m0 = (0.1, 0.2, 0.7)
        print(m0)
        r, t, l = RTLConverter.add_reflectivity(m0, 0.1)
        print(r, t, l)
        self.assertEqual(r, 0.1*0.9+0.1)
        self.assertEqual(t, 0.2*0.9)
        self.assertEqual(l, 0.7*0.9)

        r, t, l = RTLConverter.add_transmittance(m0, 0.1)
        self.assertEqual(r, 0.1*0.9)
        self.assertEqual(t, 0.2*0.9+0.1)
        self.assertEqual(l, 0.7*0.9)

        r, t, l = RTLConverter.add_loss(m0, 0.1)
        self.assertEqual(r, 0.1*0.9)
        self.assertEqual(t, 0.2*0.9)
        self.assertEqual(l, 0.7*0.9+0.1)


class Test_Position(unittest.TestCase):

    def test_constructor(self):
        p = Position(position=1)
        self.assertEqual(p.position, 1)
        p.change_params(position=10)
        self.assertEqual(p.position, 10)
        p.change_params(a=1)
        self.assertEqual(p.property_set, {'position': 10})
    
    def test_inheritance_1(self):
        class A(Position):
            modifiable_properties = ('a', 'position')
            def __init__(self, a, position):
                super().__init__(position=position)
                self.property_set.add_required('a')
                self.property_set['a'] = a
            
            @property
            def a(self):
                return self.property_set.get_strictly('a')
        
        a = A(1, 2)
        self.assertEqual(a.a, 1)
        self.assertEqual(a.position, 2)

        a.change_params(a=4, position=10)
        self.assertEqual(a.a, 4)
        self.assertEqual(a.property_set, {'a':4, 'position':10})

    def test_inheritance_2(self):
        class A(Position):
            modifiable_properties = ('a', )
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

                self.property_set.add_required('a')
                self.property_set['a'] = kwargs.get('a', None)
            
            @property
            def a(self):
                return self.property_set.get_strictly('a')
        
        a = A(a=1, position=2)
        self.assertEqual(a.a, 1)
        self.assertEqual(a.position, 2)

        a.change_params(a=4, position=10)
        self.assertEqual(a.a, 4)
        self.assertEqual(a.property_set, {'a':4, 'position':2})


class Test_Wavelength(unittest.TestCase):

    def test_constructor(self):
        w = Wavelength(wavelength=1550)
        self.assertEqual(w.wavelength, 1550)
        w.change_params(wavelength=980)
        self.assertEqual(w.wavelength, 980)
        self.assertEqual(w.k, 2*constants.pi/980)
    
    def test_inheritance(self):
        class A(Wavelength):
            modifiable_properties = ('a', 'wavelength')
            def __init__(self, a, wavelength):
                super().__init__(wavelength=wavelength)
                self.property_set.add_required('a')
                self.property_set['a'] = a
            
            @property
            def a(self):
                return self.property_set.get_strictly('a')
        
        a = A(1, 2)
        self.assertEqual(a.a, 1)
        self.assertEqual(a.wavelength, 2)

        a.change_params(a=4, wavelength=10)
        self.assertEqual(a.a, 4)
        self.assertEqual(a.property_set, {'a':4, 'wavelength':10})
        self.assertEqual(a.k, 2*constants.pi/10)
        self.assertEqual(a.property_set, {'a':4, 'wavelength':10, 'k':2*constants.pi/10})
        a.change_params(a=1)
        self.assertEqual(a.property_set, {'a':1, 'wavelength':10})


if __name__ == '__main__':
    unittest.main()
