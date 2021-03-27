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
            
            def __init__(self, name='Example', **kwargs):
                super().__init__(**kwargs)
                self.name = name
                
                self.property_set.add_required(Example.modifiable_properties)

                for prop in Example.modifiable_properties:
                    self.property_set[prop] = kwargs.get(prop, None)
            
            @property
            def a(self):
                return self.property_set.get_strictly('a')
            
            @property
            def b(self):
                return self.property_set.get_strictly('b')
            
            @property
            def c(self):
                return self.get_property('c', lambda: self.a+self.b)

        class ExampleE(Example):

            modifiable_properties = ('ae', 'a')
            
            def __init__(self, name='ExampleE', **kwargs):
                super().__init__(**kwargs)
                self.name = name
                
                self.property_set.add_required(ExampleE.modifiable_properties)

                for prop in ExampleE.modifiable_properties:
                    self.property_set[prop] = kwargs.get(prop, None)
            
            @property
            def ae(self):
                return self.property_set.get_strictly('ae')

            def change_params(self, **kwargs):
                a = kwargs.get('a', None)
                if a is not None:
                    self.update_propset(a=a, b=a**2)
                super().change_params(**kwargs)

        exm = Example(a=1, b=2)
        self.assertEqual(exm.c, 3)

        exme = ExampleE(ae=2, a=2)
        self.assertEqual(exme.ae, 2)
        self.assertEqual(exme.a, 2)

        exme.change_params(ae=4, a=4)
        self.assertEqual(exme.ae, 4)
        self.assertEqual(exme.a, 4)
        self.assertEqual(exme.b, 16)

if __name__ == '__main__':
    unittest.main()
