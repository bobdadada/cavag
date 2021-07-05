## Physical Background



## Codes

**This page corresponds to the module `mirror`** 

### Classes


#### 1. Mirror

In many cases, we need the optical properties of the surface of  an object. The most easily measured optical properties are reflectivity $R$, transmittance $T$, and loss $L$. Here, we define classes related to the mirror surface, which can be regarded as a surface with a thickness of $0$.

----

<strong class="object" id="Mirror">Mirror</strong>: `class Mirror(misc.RTL, misc.Position)`

This class defines a mirror surface and is a subclass of `misc.RTL` and `misc.Position` which provide attributes <span class="attr" style="color:red;">r</span>, <span class="attr" style="color:red;">t</span>, <span class="attr" style="color:red;">l</span> and <span class="attr" style="color:red;">position</span>.

<p style="color:blue;">The attributes are defined as follows:</p>

- <span class="attr" style="color:red;">modifiable_properties</span> - This attribute is set to `modifiable_properties = ('roc', 'r', 't', 'l', 'position')` where

  - <span class="attr" style="color:red;">roc</span> - $roc$, radius of curvature
  - <span class="attr" style="color:red;">r</span> - $R$, optical reflectivity
  - <span class="attr" style="color:red;">t</span> - $T$, optical transmittance
  - <span class="attr" style="color:red;">l</span> - $L$, optical loss
  - <span class="attr" style="color:red;">position</span> - the position of the mirror

- <span class="attr" style="color:red;">name</span> - The name of instances or classes. The default is *Mirror*, which can be modified as required. 
  
- <span class="attr" style="color:red;">property_set</span> - Property collection, which is an instance of `PropertySet`, inherited from `_utils.Object`. See [introduction](introduction.md) for details.
  
- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.
  
  - properties provided by this class
    
    - <span class="attr" style="color:red;">roc</span> - $roc$, radius of curvature
  
  - properties provided by parent class
    
    - see <a class="module-object-refer">misc.RTL</a> and <a class="module-object-refer">misc.Position</a> for details

<p style="color:blue;">The methods are defined as follows:</p>

- <span class="method" style="color:red;">\_\_init\_\_(<span class="param">name</span>='Mirror', \*\*<span class="param">kwargs</span>)</span>  - Create a `Mirror` object by named parameters consistent with <span class="attr" style="color:red;">modifiable_properties</span>.
  
-  See <a class="module-object-refer">misc.RTL</a>, <a class="module-object-refer">misc.PosItion</a>, <a class="module-object-refer-to" module="introduction">Object</a> from [introduction](introduction.md) for other methods.

----

#### 2. Lens

This module is not mainly for designing optical systems, so we only define simple Lens classes.

----

<strong class="object" id="Lens">Lens</strong>: `class Lens(misc.RTL, misc.Position)`

A class for a thin lens. In cavity-related applications, thin lens or `zero` aberration approximation can give good experimental results. Therefore, we only consider the effect of focal length $f$ of a mirror.

<p style="color:blue;">The attributes are defined as follows:</p>


- <span class="attr" style="color:red;">modifiable_properties</span> - This attribute is set to `modifiable_properties = ('f', 'r', 't', 'l', 'position')` where

  - <span class="attr" style="color:red;">f</span> - $f$, focal distance
  - <span class="attr" style="color:red;">r</span> - $R$, optical reflectivity
  - <span class="attr" style="color:red;">t</span> - $T$, optical transmittance
  - <span class="attr" style="color:red;">l</span> - $L$, optical loss
  - <span class="attr" style="color:red;">position</span> - the position of the lens
  
- <span class="attr" style="color:red;">name</span> - The name of instances or classes. The default is *Lens*, which can be modified as required. 

- <span class="attr" style="color:red;">property_set</span> - Property collection, which is an instance of `PropertySet`, inherited from `_utils.Object`. See [introduction](introduction.md) for details.

- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.

  - properties provided by this class

    - <span class="attr" style="color:red;">f</span> - $f$, focal distance

  - properties provided by parent class

    - see <a class="module-object-refer">misc.RTL</a> and <a class="module-object-refer">misc.Position</a> for details

<p style="color:blue;">The methods are defined as follows:</p>


- <span class="method" style="color:red;">\_\_init\_\_(<span class="param">name</span>='Lens', \*\*<span class="param">kwargs</span>)</span>  - Create a `Lens` object by named parameters consistent with <span class="attr" style="color:red;">modifiable\_properties</span>.

- See <a class="module-object-refer">misc.RTL</a>, <a class="module-object-refer">misc.Position</a>, <a class="module-object-refer-to" module="introduction">Object</a> from [introduction](introduction.md) for other methods.

----

## Examples

