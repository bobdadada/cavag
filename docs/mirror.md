## Physical Background



## Codes

**This page corresponds to the module `mirror`** 

### Classes


#### 1. Mirror

In many cases, we need the optical properties of the surface of  an object. The most easily measured optical properties are reflectivity $R$, transmittance $T$, and loss $L$. Here, we define classes related to the mirror surface, which can be regarded as a surface with a thickness of $0$.

Following classes are defined in the module:

----

<strong id="Mirror">Mirror</strong>: `class Mirror(misc.RTL, misc.Position)`

This class defines a mirror surface and is a subclass of `misc.RTL` and `misc.Position` which provide attributes <font color="red">r</font>, <font color="red">t</font>, <font color="red">l</font> and <font color="red">position</font>.

<font color="blue">The attributes are defined as follows</font>:

- <font color="red">modifiable_properties</font> - This attribute is set to `modifiable_properties = ('roc', 'r', 't', 'l', 'position')` where
  
  - <font color="red">roc</font> - $roc$, radius of curvature
  - <font color="red">r</font> - $R$, optical reflectivity
  - <font color="red">t</font> - $T$, optical transmittance
  - <font color="red">l</font> - $L$, optical loss
  - <font color="red">position</font> - the position of the mirror

- <font color="red">name</font> - The name of instances or classes. The default is *Mirror*, which can be modified as required. 
  
- <font color="red">property_set</font> - Property collection, which is an instance of `PropertySet`, inherited by `_utils.Object`. See [introduction](introduction.md) for details.
  
- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.
  
  - properties provided by this class
    
    - <font color="red">roc</font> - $roc$, radius of curvature
  
  - properties provided by parent class
    
    - see <a class="module-object-refer">misc.RTL</a> and <a class="module-object-refer">misc.Position</a> for details

<font color="blue">The methods are defined as follows</font>:

- <font color="red">\_\_init\_\_(name='Mirror', **kwargs)</font>  - Create a `Mirror` object by named parameters consistent with <font color="red">modifiable_properties</font>.
  
-  See <a class="module-object-refer">misc.RTL</a>, <a class="module-object-refer">misc.PosItion</a>, <a class="module-object-refer-to" module="introduction">Object</a> from [introduction](introduction.md) for other methods.

----

#### 2. Lens

This module is not mainly for designing optical systems, so we only define simple Lens classes.

Following classes are defined in the module:

----

<strong id="Lens">Lens</strong>: `class Lens(misc.RTL, misc.Position)`

A class for a thin lens. In cavity-related applications, thin lens or `zero` aberration approximation can give good experimental results. Therefore, we only consider the effect of focal length $f$ of a mirror.

<font color="blue">The attributes are defined as follows</font>:

- <font color="red">modifiable_properties</font> - This attribute is set to `modifiable_properties = ('f', 'r', 't', 'l', 'position')` where
  
  - <font color="red">f</font> - $f$, focal distance
  - <font color="red">r</font> - $R$, optical reflectivity
  - <font color="red">t</font> - $T$, optical transmittance
  - <font color="red">l</font> - $L$, optical loss
  - <font color="red">position</font> - the position of the lens

- <font color="red">name</font> - The name of instances or classes. The default is *Lens*, which can be modified as required. 

- <font color="red">property_set</font> - Property collection, which is an instance of `PropertySet`, inherited by `_utils.Object`. See [introduction](introduction.md) for details.

- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.

  - properties provided by this class

    - <font color="red">f</font> - $f$, focal distance

  - properties provided by parent class

    - see <a class="module-object-refer">misc.RTL</a> and <a class="module-object-refer">misc.Position</a> for details

<font color="blue">The methods are defined as follows</font>:

- <font color="red">\_\_init\_\_(name='Lens', **kwargs)</font>  - Create a `Lens` object by named parameters consistent with <font color="red">modifiable_properties</font>.

- See <a class="module-object-refer">misc.RTL</a>, <a class="module-object-refer">misc.Position</a>, <a class="module-object-refer-to" module="introduction">Object</a> from [introduction](introduction.md) for other methods.

----

## Examples

