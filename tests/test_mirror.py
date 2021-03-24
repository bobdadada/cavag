import unittest

from cavag.mirror import *


class Test_Mirror(unittest.TestCase):
    
    def test_constructor(self):
        m = Mirror(roc=300, r=1, t=2, l=3)
        self.assertEqual(m.roc, 300)
        self.assertEqual(m.r, 1/6)
        self.assertEqual(m.t, 1/3)
        self.assertEqual(m.l, 1/2)
        self.assertEqual(m.position, 0)
        self.assertEqual(m.property_set, {'roc':300, 'r':1/6, 't':1/3, 'l':1/2, 'position': 0})

    def test_change_properties(self):
        m = Mirror(roc=300, r=1/3, t=1/3, l=1/3, position=2)
        self.assertEqual(m.property_set, {'roc':300, 'r':1/3, 't':1/3, 'l':1/3, 'position': 2})
        m.change_params(_norm=False, r=1)
        self.assertEqual(m.property_set, {'roc':300, 'r':1, 't':1/3, 'l':1/3, 'position': 2})
        m.change_params(_norm=True, r=1, t=2, l=3)
        self.assertEqual(m.property_set, {'roc':300, 'r':1/6, 't':1/3, 'l':1/2, 'position': 2})
        m.change_params(position=4)
        self.assertEqual(m.property_set, {'roc':300, 'r':1/6, 't':1/3, 'l':1/2, 'position': 4})


class Test_Lens(unittest.TestCase):
    
    def test_constructor(self):
        lens = Lens(f=2, r=1, t=2, l=3, position=2)
        self.assertEqual(lens.f, 2)
        self.assertEqual(lens.r, 1/6)
        self.assertEqual(lens.t, 1/3)
        self.assertEqual(lens.l, 1/2)
        self.assertEqual(lens.position, 2)
        self.assertEqual(lens.property_set, {'f':2, 'r':1/6, 't':1/3, 'l':1/2, 'position': 2})
    
    def test_change_properties(self):
        lens = Lens(f=2, r=1/3, t=1/3, l=1/3)
        self.assertEqual(lens.property_set, {'f':2, 'r':1/3, 't':1/3, 'l':1/3, 'position': 0})
        lens.change_params(r=0.2, l=0.4)
        self.assertEqual(lens.property_set, {'f':2, 'r':0.2, 't':0.4, 'l':0.4, 'position': 0})
        lens.change_params(position=4)
        self.assertEqual(lens.property_set, {'f':2, 'r':0.2, 't':0.4, 'l':0.4, 'position': 4})
        lens.change_params(f=4)
        self.assertEqual(lens.property_set, {'f':4, 'r':0.2, 't':0.4, 'l':0.4, 'position': 4})


if __name__ == '__main__':
    unittest.main()
