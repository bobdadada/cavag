### Modules

The modules in `cavag` are organized as shown below

<div style="text-align: center"><img src="_assets/picture/uml/cavag_uml.svg" alt="UML of cavag"></div>

**Module Contents:**

<!-- tabs:start -->

<!-- tab:fiber -->

Source Page: [fiber](fiber.md)

**Class[es]**

- <a class="module-object-refer-to" module="fiber">Fiber</a>
- <a class="module-object-refer-to" module="fiber">StepIndexFiber</a>

<!-- tab:fpcavity -->

Source Page: [fpcavity](fpcavity)

**Class[es]**

- <a class="module-object-refer-to" module="fpcavity">CavityStructure</a>
- <a class="module-object-refer-to" module="fpcavity">EqualCavityStructure</a>
- <a class="module-object-refer-to" module="fpcavity">Cavity</a>
- <a class="module-object-refer-to" module="fpcavity">EqualCavity</a>
- <a class="module-object-refer-to" module="fpcavity">CavityMode</a>
- <a class="module-object-refer-to" module="fpcavity">EqualCavityMode</a>

**Function[s]**

- <a class="module-object-refer-to" module="fpcavity">judge_cavity_type</a>
- <a class="module-object-refer-to" module="fpcavity">calculate_loss_clipping</a>
- <a class="module-object-refer-to" module="fpcavity">calculate_loss_scattering</a>

<!-- tab:hgbeam -->

Source Page: [hgbeam](hgbeam.md)

**Class[es]**

- <a class="module-object-refer-to" module="hgbeam">NormalizedHGBeam1D</a>
- <a class="module-object-refer-to" module="hgbeam">HGBeam1D</a>
- <a class="module-object-refer-to" module="hgbeam">NormalizedGBeam1D</a>
- <a class="module-object-refer-to" module="hgbeam">GBeam1D</a>
- <a class="module-object-refer-to" module="hgbeam">NormalizedHGBeam</a>
- <a class="module-object-refer-to" module="hgbeam">HGBeam</a>
- <a class="module-object-refer-to" module="hgbeam">NormalizedGBeam</a>
- <a class="module-object-refer-to" module="hgbeam">GBeam</a>
- <a class="module-object-refer-to" module="hgbeam">NormalizedEqualHGBeam</a>
- <a class="module-object-refer-to" module="hgbeam">EqualHGBeam</a>
- <a class="module-object-refer-to" module="hgbeam">NormalizedEqualSymmetricHGBeam</a>
- <a class="module-object-refer-to" module="hgbeam">EqualSymmetricHGBeam</a>
- <a class="module-object-refer-to" module="hgbeam">NormalizedEqualGBeam</a>
- <a class="module-object-refer-to" module="hgbeam">EqualGBeam</a>

**Function[s]**

- <a class="module-object-refer-to" module="hgbeam">local2remote</a>
- <a class="module-object-refer-to" module="hgbeam">remote2local</a>
- <a class="module-object-refer-to" module="hgbeam">convert_through_mirror</a>
- <a class="module-object-refer-to" module="hgbeam">convert_through_lens</a>

<!-- tab:mirror -->

Source Page: [mirror](mirror.md)

**Class[es]**

- <a class="module-object-refer-to" module="mirror">Mirror</a>
- <a class="module-object-refer-to" module="Lens">Lens</a>

<!-- tab:misc -->

Source Page: [misc](misc.md) 

**Class[es]**

- <a class="module-object-refer-to" module="misc">RTL</a>
- <a class="module-object-refer-to" module="misc">RTLConverter</a>
- <a class="module-object-refer-to" module="misc">Position</a>
- <a class="module-object-refer-to" module="misc">Wavelength</a>

<!-- tab:extension[s] -->

Source Page: [extension[s]](extension)

- [fcqs](extension/fcqs.md)
  - <a class="module-object-refer-to" module="extension/fcqs">calculate_g</a>
  - <a class="module-object-refer-to" module="extension/fcqs">calculate_C1</a>
  - <a class="module-object-refer-to" module="extension/fcqs">calculate_neta_e</a>
  - <a class="module-object-refer-to" module="extension/fcqs">calculate_neta_ext</a>

<!-- tabs:end -->



### Core Implementation

The core functions of `cavag` are provided by `Object` and `PropertySet` in *_utils.py*. The UML diagram of this file is shown below

<div style="text-align: center"><img src="_assets/picture/uml/_utils_uml.svg" alt="UML of _utils"></div>

1. **Usage**

In other modules, all abstract classes related to physical objects are subclasses of `PrintableObject`. A mature subclass needs to define its own **modifiable\_properties** class attribute, which can be used in class method `cls.filter_properties(**propdict)` to filter modifiable physical properties in the `dict`, <span class="param" style="color:red;">propdict</span>. In general, **modifiable\_properties** contains the names of all input parameters defined in the constructor of the subclass, other than the <span class="attr" style="color:red;">name</span>.

An empty **property\_set** is created if the subclass is constructed. It is a data type similar to the python `dict`. One can get and set the <span class="param" style="color:red;">value</span> corresponding to <span class="param" style="color:red;">key</span> by `value = property_set[key]` and `property_set[key] = value`. The private attribute **\_\_required_props** of **property_set** is a set, when an instance of `PropertySet` is created, this attribute will be set to `set(props)` where <span class="param" style="color:red;">props</span> is the input parameter of the constructor <span class="method" style="color:red;">\_\_init\_\_(<span class="param">props</span>=(), \*<span class="param">args</span>, \*\*<span class="param">kwargs</span>)</span>. **\_\_required\_props** contains all basic properties that a physical object must have, and all other properties can be derived from these basic properties. These basic properties are initialized to `None`. The value of a property `prop` in **\_\_required_props** can be normally obtained through `property_set[prop]`, but if the value of this property is `None`, obtaining the corresponding value through `property_set.get_strictly(prop)` will raise a `PropertyLost` exception.

----

<strong class="object" id="Object">Object</strong>: `class Object`

This class defines an abstraction of real object.

<p style="color:blue">The attributes are defined as follows:</p>

- <span class="attr" style="color:red;">modifiable\_properties</span> - An Iterable object, contains all the names of modifiable properties.

- <span class="attr" style="color:red;">name</span> - The name of instances or classes. The default is *Object*, which can be modified as required. 

- <span class="attr" style="color:red;">property\_set</span> - Property collection, which is an instance of `PropertySet`.

<p style="color:blue;">The methods are defined as follows:</p>

- <span class="method" style="color:red;">\_\_init\_\_(<span class="param">name</span>="Object", \*\*<span class="param">kwargs</span>)</span> - Create an instance of `Object`, the name is set to be <span class="param" style="color:red;">name</span>. In <span class="param" style="color:red;">kwargs</span>, only the key name consistent with the property name in <span class="attr" style="color:red;">modifiable\_properties</span> will be set.
  
- <span class="method" style="color:red;">get\_property(<span class="param">k</span>, <span class="param">v_f</span>=None)</span> - Use the property name <span class="param" style="color:red;">k</span> to get the property value saved in the <span class="attr" style="color:red;">property\_set</span>. If the property does not exist, use the function <span class="param" style="color:red;">v\_f</span> to calculate its value and save it in the <span class="attr" style="color:red;">property\_set</span>. Then this method use <span class="method" style="color:red;">get\_strictly</span> of `PropertySet` to get the value of this property. Usually we don't use this method directly, but define a method decorated with `@property` in the subclass, and call the <span class="method" style="color:red;">get\_property</span> in this method.
  
- <span class="method" style="color:red;">get\_proplist()</span> - Get all the method names decorated with `@property` in the class. It is a concrete implementation of an abstract method <span class="method" style="color:red;">get\_proplist</span> in `PrintInfoMixin`. 
  
- <span class="method" style="color:red;">change\_params(<span class="param">\_filter</span>=True, \*\*kwargs)</span> - This method is used to modify the value of parameters in <span class="attr" style="color:red;">property\_set</span>. Inside the method, it will call <span class="method" style="color:red;">filter\_properties</span> if <span class="param" style="color:red;">\_filter</span> is `True`, then it  will call <span class="method" style="color:red;">preprocess\_properties</span> to pre-process the properties, then it will call <span class="method" style="color:red;">update\_propset</span> to update the property\_set, and finally it will call <span class="method" style="color:red;">postprocess\_properties</span> to post-process the properties. 
  
- <span class="method" style="color:red;">filter\_properties(\*\*<span class="param">propdict</span>)</span> - This method filters the <span class="param" style="color:red;">propdict</span> and returns the corresponding sub-dictionary in the <span class="param" style="color:red;">propdict</span> with only properties in the <span class="attr" style="color:red;">modifiable\_properties</span>. Note that any key-value pair in <span class="param" style="color:red;">propdict</span> with key starting "\_" will be retained as a configuration property.
  
- <span class="method" style="color:red;">preprocess\_properties(\*\*<span class="param">propdict</span>)</span> - Pre-process the <span class="param" style="color:red;">propdict</span>. It is often used to calculate and update properties which are not in the <span class="attr" style="color:red;">modifiable\_properties</span>. This method is often overridden by subclasses.

- <span class="method" style="color:red;">update\_propset(\*\*<span class="param">propdict</span>)</span> - This method directly uses <span class="param" style="color:red;">propdict</span> to update properties in <span class="attr" style="color:red;">property\_set</span> with method <span class="method" style="color:red;">change\_params</span> of <span class="attr" style="color:red;">property\_set</span>. Note that any key-value pair in <span class="param" style="color:red;">propdict</span> with key starting "\_" will be ignored. Not recommended to use this method directly, use <span class="method" style="color:red;">change\_params</span> of this class instead.
  
- <span class="method" style="color:red;">postprocess\_properties(\*\*<span class="param">propdict</span>)</span> - Post-process the <span class="param" style="color:red;">propdict</span>. Commonly used to perform other update operations of the instance. This method is often overridden by subclasses.

----

<strong class="object" id="PropertySet">PropertySet</strong>: `class PropertySet(collections.UserDict)`

This class define a data structure which store all properties of a physical object. It is a `dict`-like object, subclass of `collections.UserDict`.

<p style="color:blue;">The attributes are defined as follows:</p>

- <span class="attr" style="color:red;">\_\_required_props</span> - `set` object, contains all the names of the necessary properties. All the other properties not in <span class="attr" style="color:red;">\_\_required_props</span> will be cleared when the <span class="method" style="color:red;">change_params</span> method of this class is called, see <span class="method" style="color:red;">change\_params</span> for more details. Only <span class="method" style="color:red;">reset\_required</span>, <span class="method" style="color:red;">add\_required</span>, <span class="method" style="color:red;">del\_required</span>, and <span class="method" style="color:red;">clear\_required</span> can modify <span class="attr" style="color:red;">\_\_required\_props</span>.

<p style="color:blue;">The methods are defined as follows:</p>

- <span class="method" style="color:red;">\_\_init\_\_(<span class="param">required\_props</span>=(), \*<span class="param">args</span>, \*\*<span class="param">kwargs</span>)</span> - Create an instance of `PropertySet`. The <span class="attr" style="color:red;">required\_props</span> is used to set the attribute <span class="attr" style="color:red;">\_\_required\_props</span> of this instance. And <span class="param" style="color:red;">args</span>, <span class="param" style="color:red;">kwargs</span> are parameters which are consistent with the input parameters of python's `dict`.

- <span class="method" style="color:red;">get\_strictly(<span class="param">key</span>, <span class="param">default</span>=None)</span> - Similar to method `get(key, default=None)` provided by `collections.UserDict`. But if <span class="param" style="color:red;">key</span> is a property in <span class="attr" style="color:red;">\_\_required\_props</span> and the value of this property is `None`, then a `PropertyLost` exception will be raised.

- <span class="method" style="color:red;">change\_params(\*\*<span class="param">kwargs</span>)</span> - This method updates the value of properties in the instance, and all saved properties except the properties in <span class="attr" style="color:red;">\_\_required\_props</span> will be deleted. 

- <span class="method" style="color:red;">reset\_required(<span class="param">props</span>=())</span> - Reset <span class="attr" style="color:red;">\_\_required\_props</span> by <span class="param" style="color:red;">props</span>, where <span class="param" style="color:red;">props</span> must be an iterable object containing the necessary properties.

- <span class="method" style="color:red;">add\_required(<span class="param">props</span>=())</span> - If <span class="param" style="color:red;">props</span> is of type `str`, add this as a necessary property to <span class="attr" style="color:red;">\_\_required\_props</span>; if <span class="param" style="color:red;">props</span> is an iterable object with elements of `str` type, add these elements Into <span class="attr" style="color:red;">\_\_required\_props</span>.

- <span class="method" style="color:red;">del\_required(<span class="param">props</span>=())</span> - If <span class="param" style="color:red;">props</span> is of type `str`, remove this element from <span class="attr" style="color:red;">\_\_required\_props</span>; if <span class="param" style="color:red;">props</span> is an iterable object with elements of `str` type, remove these elements from <span class="attr" style="color:red;">\_\_required\_props</span>. If the element is not a member of <span class="attr" style="color:red;">\_\_required\_props</span>, do nothing.

- <span class="method" style="color:red;">clear\_required()</span> - Remove all elements from <span class="attr" style="color:red;">\_\_required\_props</span>.

----

2. **Example**

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
        return self.get_property('a')
    
    @property
    def b(self):
        """属性b"""
        return self.get_property('b')
    
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
    属性ａ　　　　　　　　　　　　a          =
        1
    属性ｂ　　　　　　　　　　　　b          =
        2
    属性ｃ　　　　　　　　　　　　c          =
        3

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
    属性ａ　　　　　　　　　　　　a          =
        2
    属性ｂ　　　　　　　　　　　　b          =
        2
    属性ｃ　　　　　　　　　　　　c          =
        4

"""

# Changing parameters not in modifiable_properties do nothing
exm.change_params(_filter=True, k=1)
print(exm)
"""
Example:
    属性ａ　　　　　　　　　　　　a          =
        2
    属性ｂ　　　　　　　　　　　　b          =
        2
    属性ｃ　　　　　　　　　　　　c          =
        4

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
    属性ａ　　　　　　　　　　　　a          =
        2
    属性ｂ　　　　　　　　　　　　b          =
        2
    属性ｃ　　　　　　　　　　　　c          =
        4

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
    属性ａ　　　　　　　　　　　　a          =
        2
    属性ｂ　　　　　　　　　　　　b          =
        2
    属性ｃ　　　　　　　　　　　　c          =
        4

"""
print(exm.property_set)
"""
{'b': 2, 'a': 2, 'k': 2, 'c': 4}
"""
exm.change_params()
print(exm.property_set)
"""
{'b': 2, 'a': 2}
"""
print(exm)
"""
Example:
    属性ａ　　　　　　　　　　　　a          =
        2
    属性ｂ　　　　　　　　　　　　b          =
        2
    属性ｃ　　　　　　　　　　　　c          =
        4

"""
```

*This example is stored in [show_printable_object](_assets/example/show_printable_object.py ':ignore :class=download')*

