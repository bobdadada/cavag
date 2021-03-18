import unittest

from cavag.mirror import *


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


class Test_MirrorSurface(unittest.TestCase):
    
    def test_constructor(self):
        ms = MirrorSurface(roc=300, r=1, t=2, l=3)
        self.assertEqual(ms.roc, 300)
        self.assertEqual(ms.r, 1/6)
        self.assertEqual(ms.t, 1/3)
        self.assertEqual(ms.l, 1/2)
        self.assertEqual(ms.position, 0)
        self.assertEqual(ms.property_set, {'roc':300, 'r':1/6, 't':1/3, 'l':1/2, 'position': 0})

    def test_change_properties(self):
        ms = MirrorSurface(roc=300, r=1/3, t=1/3, l=1/3, position=2)
        self.assertEqual(ms.property_set, {'roc':300, 'r':1/3, 't':1/3, 'l':1/3, 'position': 2})
        ms.change_params(_norm=False, r=1)
        self.assertEqual(ms.property_set, {'roc':300, 'r':1, 't':1/3, 'l':1/3, 'position': 2})
        ms.change_params(_norm=True, r=1, t=2, l=3)
        self.assertEqual(ms.property_set, {'roc':300, 'r':1/6, 't':1/3, 'l':1/2, 'position': 2})
        ms.change_params(position=4)
        self.assertEqual(ms.property_set, {'roc':300, 'r':1/6, 't':1/3, 'l':1/2, 'position': 4})


class Test_Mirror(unittest.TestCase):
    
    def test_constructor(self):
        m = Mirror(f=2, r=1, t=2, l=3, position=2)
        self.assertEqual(m.f, 2)
        self.assertEqual(m.r, 1/6)
        self.assertEqual(m.t, 1/3)
        self.assertEqual(m.l, 1/2)
        self.assertEqual(m.position, 2)
        self.assertEqual(m.property_set, {'f':2, 'r':1/6, 't':1/3, 'l':1/2, 'position': 2})
    
    def test_change_properties(self):
        m = Mirror(f=2, r=1/3, t=1/3, l=1/3)
        self.assertEqual(m.property_set, {'f':2, 'r':1/3, 't':1/3, 'l':1/3, 'position': 0})
        m.change_params(r=0.2, l=0.4)
        self.assertEqual(m.property_set, {'f':2, 'r':0.2, 't':0.4, 'l':0.4, 'position': 0})
        m.change_params(position=4)
        self.assertEqual(m.property_set, {'f':2, 'r':0.2, 't':0.4, 'l':0.4, 'position': 4})
        m.change_params(f=4)
        self.assertEqual(m.property_set, {'f':4, 'r':0.2, 't':0.4, 'l':0.4, 'position': 4})


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
