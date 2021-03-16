import unittest

from scipy import constants
from cavag.misc import Position, Wavelength

class Test_Position(unittest.TestCase):

    def test_constructor(self):
        p = Position(1)
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
        self.assertEqual(a.property_set, {'a':4, 'position':2})


class Test_Wavelength(unittest.TestCase):

    def test_constructor(self):
        w = Wavelength(1550)
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
