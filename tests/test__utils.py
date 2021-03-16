import unittest

from cavag._utils import PropertySet, PropertyLost, Object

class Test_PropertySet(unittest.TestCase):

    def test_no_required_prop(self):
        pset = PropertySet()
        self.assertEqual(pset, {})
        pset['a'] = 1
        self.assertEqual(pset, {'a':1})
        self.assertEqual(pset['a'], 1)
        pset.change_params()
        self.assertEqual(pset, {})

    def test_initial_required_props(self):
        pset = PropertySet(('r_a', 'r_b'))
        self.assertRaises(PropertyLost, lambda:pset.get_strictly('r_a'))
        pset['r_a'] = 1
        pset['r_b'] = 2
        self.assertEqual(pset, {'r_a':1, 'r_b':2})
        pset['a'] = 3
        self.assertEqual(pset, {'r_a':1, 'r_b':2, 'a':3})
        pset.change_params()
        self.assertEqual(pset, {'r_a':1, 'r_b':2})
    
    def test_change_required_props(self):
        pset = PropertySet()
        pset.add_required('a')
        self.assertIn('a', pset)
        self.assertRaises(PropertyLost, lambda:pset.get_strictly('a'))
        pset['a'] = 1
        pset.change_params()
        self.assertEqual(pset, {'a':1})
        pset.add_required(('b', 'c'))
        self.assertEqual(pset, {'a':1, 'b':None, 'c':None})
        pset['b'] = 2
        pset['c'] = 3
        self.assertEqual(pset, {'a':1, 'b':2, 'c':3})
        pset.change_params(a=4, b=3)
        self.assertEqual(pset, {'a':4, 'b':3, 'c':3})
        pset.reset_required(('d', 'e'))
        pset.change_params()
        self.assertRaises(KeyError, lambda:pset['a'])
        pset.clear_required()
        self.assertEqual(pset, {'d':None, 'e':None})
        pset.change_params()
        self.assertEqual(pset, {})
        pset.add_required('a')
        self.assertEqual(pset, {'a':None})
        pset.del_required('a')
        self.assertEqual(pset, {'a':None})
        pset.change_params()
        self.assertEqual(pset, {})


class Test_Object(unittest.TestCase):

    def test_constructor(self):
        obj = Object()
        self.assertEqual(obj.name, 'Object')
        self.assertEqual(obj.property_set, {})
        self.assertEqual(obj.modifiable_properties, ())
        self.assertIsInstance(obj.property_set, PropertySet)
    
    def test_change_params(self):
        obj = Object()
        obj.change_params(a=1, b=2, _filter=False)
        self.assertEqual(obj.property_set, {'a':1, 'b':2})
        obj.change_params(a=3, b=4)
        self.assertEqual(obj.property_set, {})
        obj.property_set.add_required('a')
        obj.change_params(a=3, b=4, _filter=False)
        self.assertEqual(obj.property_set, {'a':3, 'b':4})
        obj.change_params(a=7, _filter=True)
        self.assertEqual(obj.property_set, {'a': 3})
        obj.property_set.add_required(('a', 'c'))
        obj.change_params(b=8)
        self.assertEqual(obj.property_set, {'a':3, 'c':None})
        obj.change_params(c=2, _filter=False)
        self.assertEqual(obj.property_set, {'a':3, 'c':2})

    def test_inheritance(self):
        class Example(Object):
    
            modifiable_properties = ('a', 'b')
            
            def __init__(self, a, b, name='Example'):
                super().__init__()
                self.name = name
                
                self.property_set.add_required(Example.modifiable_properties)
                self.property_set['a'] = a
                self.property_set['b'] = b
            
            @property
            def a(self):
                return self.property_set.get_strictly('a')
            
            @property
            def b(self):
                return self.property_set.get_strictly('b')
            
            @property
            def c(self):
                return self.get_property('c', lambda: self.a+self.b)
        
        exm = Example(1, 2)
        self.assertEqual(exm.c, 3)


if __name__ == '__main__':
    unittest.main()
