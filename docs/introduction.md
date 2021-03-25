### Modules

The modules in `cavag` are organized as shown below

<div style="text-align: center"><img src="_assets/picture/uml/cavag_uml.svg" alt="UML of cavag"></div>

**Module Contents:**

<!-- tabs:start -->

<!-- tab:fiber -->

Source Page: [fiber](fiber.md)

**Class[es]**

- <a class="module-object-refer-to" module="fiber">FiberEnd</a>
- <a class="module-object-refer-to" module="fiber">StepIndexFiberEnd</a>

<!-- tab:fpcavity -->

Source Page: [fpcavity](fpcavity)

<!-- tab:gaussbeam -->

Source Page: [gaussbeam](gaussbeam.md)

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

<!-- tab:utils -->

Source Page: [utils](utils.md)

<!-- tabs:end -->



### Core Implementation

The core functions of `cavag` are provided by `Object` and `PropertySet` in *_utils.py*. The UML diagram of this file is shown below

<div style="text-align: center"><img src="_assets/picture/uml/_utils_uml.svg" alt="UML of _utils"></div>

1. **Usage**

In other modules, all abstract classes related to physical objects are subclasses of `PrintableObject`. A mature subclass needs to define its own **modifiable_properties** class attribute, which can be used in class method `cls.filter_properties(propdict)` to filter modifiable physical properties in the `dict`, <span class="prop" style="color:red;">kwargs</span>. In general, **modifiable_properties** contains the names of all input parameters defined in the constructor of the subclass, other than the <span class="prop" style="color:red;">name</span>.

An empty **property_set** is created if the subclass is constructed. It is a data type similar to the python `dict`. One can get and set the <span class="prop" style="color:red;">value</span> corresponding to <span class="prop" style="color:red;">key</span> by `value = property_set[key]` and `property_set[key] = value`. The private attribute **__required_props** of **property_set** is a set, when an instance of `PropertySet` is created, this attribute will be set to `set(props)` where <span class="prop" style="color:red;">props</span> is the input parameter of the constructor <span class="prop" style="color:red;">\_\_init\_\_(props=(), \*args, \*\*kwargs)</span>. **__required_props** contains all basic properties that a physical object must have, and all other properties can be derived from these basic properties. These basic properties are initialized to `None`. The value of a property `prop` in **__required_props** can be normally obtained through `property_set[prop]`, but if the value of this property is `None`, obtaining the corresponding value through `property_set.get_strictly(prop)` will raise a `PropertyLost` exception.

The detailed definitions are as follows:

----

<strong class="object" id="Object">Object</strong>: `class Object`

This class defines an abstraction of real object.

<p style="color:blue">The attributes are defined as follows:</p>

- <span class="prop" style="color:red;">modifiable_properties</span> - Iterable object, contains all the names of modifiable properties.

- <span class="prop" style="color:red;">name</span> - The name of instances or classes. The default is *Object*, which can be modified as required. 

- <span class="prop" style="color:red;">property_set</span> - Property collection, which is an instance of `PropertySet`.

<p style="color:blue;">The methods are defined as follows:</p>

- <span class="prop" style="color:red;">\_\_init\_\_(name="Object", **kwargs)</span> - Create an instance of `Object`, the name is set to be <span class="prop" style="color:red;">name</span>. In <span class="prop" style="color:red;">kwargs</span>, only the key name consistent with the property name in <span class="prop" style="color:red;">modifiable_properties</span> will be set.

- <span class="prop" style="color:red;">get_property(k, v_f=None)</span> - Use the property name <span class="prop" style="color:red;">k</span> to get the property value saved in the <span class="prop" style="color:red;">property_set</span>. If the property does not exist, use the function <span class="prop" style="color:red;">v_f</span> to calculate its value and save it in the <span class="prop" style="color:red;">property_set</span>. Then this method use <span class="prop" style="color:red;">get_strictly</span> of `PropertySet` to get the value of this property. Usually we don't use this method directly, but define a method decorated with `@property` in the subclass, and call the <span class="prop" style="color:red;">get_property</span> in this method.

- <span class="prop" style="color:red;">get_proplist()</span> - Get all the method names decorated with `@property` in the class. It is a concrete implementation of an abstract method <span class="prop" style="color:red;">get_proplist</span> in `PrintInfoMixin`. 

- <span class="prop" style="color:red;">change_params(\_filter=True, **kwargs)</span> - This method is used to modify the value of parameters in <span class="prop" style="color:red;">property_set</span>. The input of the method must be named parameters. If <span class="prop" style="color:red;">\_filter</span> is set to `True`, then only parameters in <span class="prop" style="color:red;">kwargs</span> consistent with the properties in <span class="prop" style="color:red;">modifiable_properties</span> will be filtered out by method <span class="prop" style="color:red;">filter_properties</span>. This method uses <span class="prop" style="color:red;">update_propset</span> to update <span class="prop" style="color:red;">property_set</span>. 

- <span class="prop" style="color:red;">update_propset(**kwargs)</span> - This method directly uses <span class="prop" style="color:red;">kwargs</span> to update properties in <span class="prop" style="color:red;">property_set</span> with method <span class="prop" style="color:red;">change_params</span> of <span class="prop" style="color:red;">property_set</span>. Note that any key-value pair in <span class="prop" style="color:red;">kwargs</span> with key starting "\_" will be ignored. Not recommended to use this method directly, use <span class="prop" style="color:red;">change_params</span> of this class instead.

- <span class="prop" style="color:red;">filter_properties(propdict)</span> - This method filters the <span class="prop" style="color:red;">propdict</span> and returns the corresponding sub-dictionary in the <span class="prop" style="color:red;">propdict</span> with only properties in the <span class="prop" style="color:red;">modifiable_properties</span>.

----

<strong class="object" id="PropertySet">PropertySet</strong>: `class PropertySet(collections.UserDict)`

This class define a data structure which store all properties of a physical object. It is a `dict`-like object, subclass of `collections.UserDict`.

<p style="color:blue;">The attributes are defined as follows:</p>

- <span class="prop" style="color:red;">\_\_required_props</span> - `set` object, contains all the names of the necessary properties. All the other properties not in <span class="prop" style="color:red;">\_\_required_props</span> will be cleared when the <span class="prop" style="color:red;">change_params</span> method of this class is called, see <span class="prop" style="color:red;">change_params</span> for more details. Only <span class="prop" style="color:red;">reset_required</span>, <span class="prop" style="color:red;">add_required</span>, <span class="prop" style="color:red;">del_required</span>, and <span class="prop" style="color:red;">clear_required</span> can modify <span class="prop" style="color:red;">\_\_required_props</span>.

<p style="color:blue;">The methods are defined as follows:</p>

- <span class="prop" style="color:red;">\_\_init\_\_(required\_props=(), *args, **kwargs)</span> - Create an instance of `PropertySet`. The <span class="prop" style="color:red;">required\_props</span> is used to set the attribute <span class="prop" style="color:red;">\_\_required_props</span> of this instance. And <span class="prop" style="color:red;">args</span>, <span class="prop" style="color:red;">kwargs</span> are parameters which are consistent with the input parameters of python's `dict`.

- <span class="prop" style="color:red;">get_strictly(key, default=None)</span> - Similar to method `get(key, default=None)` provided by `collections.UserDict`. But if <span class="prop" style="color:red;">key</span> is a property in <span class="prop" style="color:red;">\_\_required_props</span> and the value of this property is `None`, then a `PropertyLost` exception will be raised.

- <span class="prop" style="color:red;">change_params(**kwargs)</span> - This method updates the value of properties in the instance, and all saved properties except the properties in <span class="prop" style="color:red;">\_\_required_props</span> will be deleted. 

- <span class="prop" style="color:red;">reset_required(props=())</span> - Reset <span class="prop" style="color:red;">\_\_required_props</span> by <span class="prop" style="color:red;">props</span>, where <span class="prop" style="color:red;">props</span> must be an iterable object containing the necessary properties.

- <span class="prop" style="color:red;">add_required(props=())</span> - If <span class="prop" style="color:red;">props</span> is of type `str`, add this as a necessary property to <span class="prop" style="color:red;">\_\_required_props</span>; if <span class="prop" style="color:red;">props</span> is an iterable object with elements of `str` type, add these elements Into <span class="prop" style="color:red;">\_\_required_props</span>.

- <span class="prop" style="color:red;">del_required(props=())</span> - If <span class="prop" style="color:red;">props</span> is of type `str`, remove this element from <span class="prop" style="color:red;">\_\_required_props</span>; if <span class="prop" style="color:red;">props</span> is an iterable object with elements of `str` type, remove these elements from <span class="prop" style="color:red;">\_\_required_props</span>. If the element is not a member, do nothing.

- <span class="prop" style="color:red;">clear_required()</span> - Remove all elements from <span class="prop" style="color:red;">\_\_required_props</span>.

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

