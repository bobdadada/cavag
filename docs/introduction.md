The modules in cavag are organized as shown below

<div style="text-align: center"><img src="_assets/pics/uml/cavag_uml.png" alt="UML of cavag"></div>

**Module Content:**

<!-- tabs:start -->

<!-- tab:fiber -->

Source Page: [fiber](fiber.md)

**Class[es]**

- `FiberEnd`
- `StepIndexFiberEnd`

<!-- tab:fpcavity -->

Source Page: [fpcavity](fpcavity)


<!-- tab:gaussbeam -->

Source Page: [gaussbeam](gaussbeam.md)


<!-- tab:mirror -->

Source Page: [mirror](mirror.md)

**Class[es]**

- `RTL`
- `RTLConverter`
- `MirrorSurface`
- `Mirror`

<!-- tab:misc -->

Source Page: [misc](misc.md) 

<!-- tab:utils -->

Source Page: [utils](utils.md)

<!-- tabs:end -->



The core functions of cavag are provided by `Object` and `PropertySet` in *_utils.py*. The UML diagram of this file is shown below

<div style="text-align: center"><img src="_assets/pics/uml/_utils_uml.png" alt="UML of _utils"></div>

1. **Definition**

! TO DO

2. **Usage**

In other modules, all abstract classes related to physical objects are subclasses of `PrintableObject`. A mature subclass needs to define its own **modifiable_properties** class attribute, which can be used in class method `cls.filter_properties(propdict)` to filter modifiable physical properties in the dict, <font color="red">kwargs</font>. In general, **modifiable_properties** contains the names of all input parameters defined in the constructor of the subclass, other than the <font color="red">name</font>.

An empty **property_set** is created if the subclass is constructed. It is a data type similar to the python dict. One can get and set the <font color="red">value</font> corresponding to <font color="red">key</font> by `value = property_set[key]` and `property_set[key] = value`. The private attribute **__required_props** of **property_set** is a set, when an instance of `PropertySet` is created, this attribute will be set to `set(props)` where <font color="red">props</font> is the input parameter of the constructor <font color="red">\_\_init\_\_(props=(), \*args, \*\*kwargs)</font>. **__required_props** contains all basic properties  that a physical object must have, and all other properties can be derived from these basic properties. These basic properties are initialized to `None`. The value of a property `prop` in **__required_props** can be normally obtained through `property_set[prop]`, but if the value of this property is `None`, obtaining the corresponding value through `property_set.get_strictly(prop)` will raise a `PropertyLost` exception.

3. **Example**

Implement a subclass `Example` of `PrintableObject`

```python
class Example(PrintableObject):
    
    # Set all modifiable parameters in a tuple.
    modifiable_properties = ('a', 'b')
    
    def __init__(self, name='Example', **kwargs):
        # Execute the initialization function of the parent class,
        # which define an empty property_set and add all necessary
        # properties of parent classes.
        super().__init__(**kwargs)
        
        self.name = name
        
        # Add the necessary own properties to property_set and set values.
        self.property_set.add_required(Example.modifiable_properties)
        
        for prop in Example.modifiable_properties:
            self.property_set[prop] = kwargs.get(prop, None)
    
    @property
    def a(self):
        """属性a"""
        # Use get_strictly to get the value corresponding to 'a'.
        # It will raise PropertyLost exception if the value is None.
        return self.property_set.get_strictly('a')
    
    @property
    def b(self):
        """属性b"""
        return self.property_set.get_strictly('b')
    
    @property
    def c(self):
        """属性c"""
        # 'c' is an exported property, and its value will be calculated
        # once with the function corresponding to the second parameter
        # of get_property. In this example c = a + b.
        return self.get_property('c', lambda: self.a+self.b)
```

Using the formatted output function provided by `PrintInfoMixin` to print out an instance of `Example` gives

```python
exm = Example(a=1, b=2)
print(exm)
"""
Example:
    属性ａ　　　　　　　　　　　　a        = 1
    属性ｂ　　　　　　　　　　　　b        = 2
    属性ｃ　　　　　　　　　　　　c        = 3

"""
```

Get and change the properties

```python
# Get the name of each property
proplist = exm.get_proplist()
print(proplist)
"""
['a', 'b', 'c']
"""

# Get the value of each property
for prop in proplist:
    print(getattr(exm, prop))
    
# Change the parameters. Generally, parameters are the properties
# defined in modifiable_properties, and setting _filter=True in change_params 
# will filter out these parameters.
exm.change_params(_filter=True, a=2)
print(exm)
"""
Example:
    属性ａ　　　　　　　　　　　　a        = 2
    属性ｂ　　　　　　　　　　　　b        = 2
    属性ｃ　　　　　　　　　　　　c        = 4

"""

# Changing parameters not in modifiable_properties do nothing
exm.change_params(_filter=True, k=1)
print(exm)
"""
Example:
    属性ａ　　　　　　　　　　　　a        = 2
    属性ｂ　　　　　　　　　　　　b        = 2
    属性ｃ　　　　　　　　　　　　c        = 4

"""

# Note that it is not recommended to use _filter=False, 
# which may cause the intermediate parameters stored in the
# property_set to be overwritten. 
# Using an empty parameter will clear the values of all properties
# except those defined in modifiable_properties, and they will be
# recalculated when queried.
exm.change_params()
print(exm.property_set)
"""
{'b': 2, 'a': 2}
"""
print(exm)
"""
Example:
    属性ａ　　　　　　　　　　　　a        = 2
    属性ｂ　　　　　　　　　　　　b        = 2
    属性ｃ　　　　　　　　　　　　c        = 4

"""
print(exm.property_set)
"""
{'b': 2, 'a': 2, 'c': 4}
"""

# Use update_propset can update property_set directly. Not recommended!! 
exm.update_propset(k=2)
print(exm.property_set)
"""
{'b': 2, 'a': 2, 'k': 2}
"""
print(exm)
"""
Example:
    属性ａ　　　　　　　　　　　　a        = 2
    属性ｂ　　　　　　　　　　　　b        = 2
    属性ｃ　　　　　　　　　　　　c        = 4

"""
print(exm.property_set)
"""
{'b': 2, 'a': 2, 'k': 2, 'c': 4}
"""
```

