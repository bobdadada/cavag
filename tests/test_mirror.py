import unittest

from cavag.mirror import *


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


if __name__ == '__main__':
    unittest.main()
