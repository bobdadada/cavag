## Physical Background



## Codes

**This page corresponds to the module `mirror`** 

### Classes

#### 1. $R,T,L$

Since reflectivity $R$, transmittance $T$, and loss $L$ are important in the mirror-related applications and often given in an equivalent form in practical applications, we need $RTL$ abstract class and a helper class for $R,T,L$ conversion. 

Following classes are defined in the module:

----

<strong id="RTL">RTL</strong>: `class RTL(PrintableObject)`

This class define an abstract class describing $R,T,L$.

<font color="blue">The attributes are defined as follows</font>:

- <font color="red">modifiable_properties</font> - This attribute is set to `modifiable_properties = ('r', 't', 'l')` where

  - <font color="red">r</font> - $R$, optical reflectivity, the value must be between $0$ and $1$.
  - <font color="red">t</font> - $T$, optical transmittance, the value must be between $0$ and $1$.
  - <font color="red">l</font> - $L$, optical loss, the value must be between $0$ and $1$.

  These attributes are also input parameters of the constructor. 

- <font color="red">name</font> - The name of instances or classes. The default is *RTL*, which can be modified as required. 

- <font color="red">property_set</font> -  Property collection, which is an instance of `PropertySet`, inherited by `_utils.Object`. See [introduction](introduction.md) for details.

- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.

  - properties provided by this class
    
    - <font color="red">r</font> - $R$, optical reflectivity
    - <font color="red">t</font> - $T$, optical transmittance
    - <font color="red">l</font> - $L$, optical loss

<font color="blue">The methods are defined as follows</font>:

- <font color="red">\_\_init\_\_(name='RTL', **kwargs)</font>  - Create a `RTL` object by named parameters consistent with <font color="red">modifiable_properties</font>. For parameter <font color="red">r</font>, <font color="red">t</font> and <font color="red">l</font>, one can provide only two of them, and the remaining one can be calculated when the class is constructed. Note $R,T,L$ are normalized in the constructor, i.e, $R+T+L=1$.
  
- <font color="red">add_loss(loss)</font> - This method provides a way to add <font color="red">loss</font> to the surface. In common cases, the loss can be divided into multiple parts. At this time, the loss will be added by this method, and the method will calculate the normalized $R,T,L$.

----

<strong id="RTLConverter">RTLConverter</strong>: `class RTLConverter`

A helper class for the $R,T,L$ conversion. This class is mainly used to define a namespace, and all methods of the class are decorated as `@staticmethod`.

<font color="blue">The methods are defined as follows</font>:

- <font color="red">@(staticmethod): normalize(r=None, t=None, l=None)</font> - The method is used to normalize the $R,T,L$, i.e. $R+T+L=1$. One can only provide only two of the parameters reflectivity - $R$ - <font color="red">r</font>, transmittance - $T$ - <font color="red">t</font>, loss - $L$ - <font color="red">l</font>. Then this method will return the normalized $R,T,L$ in a tuple.
  
- <font color="red">@(staticmethod): rtl_by_r_t2l(r, t2l)</font> - By parameters reflectivity - $R$ - <font color="red">r</font> and the ratio of transmittance to loss - $T/L$ - <font color="red">t2l</font>, this method returns the normalized $R,T,L$ in a tuple.
  
- <font color="red">@(staticmethod): rtl_by_t_r2l(t, r2l)</font> - By parameters transmittance - $T$ - <font color="red">t</font> and the ratio of reflectivity to loss - $R/L$ - <font color="red">r2l</font>, this method returns the normalized $R,T,L$ in a tuple.
  
- <font color="red">@(staticmethod): add_reflectivity(m0, re)</font> - This method adds extra reflectivity - <font color="red">re</font> to the original (reflectivity, transmittance, loss) tuple - <font color="red">m0</font>, and returns the normalized $R,T,L$ in a tuple.
  
- <font color="red">@(staticmethod): add_transmittance(m0, te)</font> - This method adds extra transmittance - <font color="red">te</font> to the original (reflectivity, transmittance, loss) tuple - <font color="red">m0</font>, and returns the normalized $R,T,L$ in a tuple.
  
- <font color="red">@(staticmethod): add_loss(m0, le)</font> - This method adds extra loss - <font color="red">le</font> to the original (reflectivity, transmittance, loss) tuple - <font color="red">m0</font>, and returns the normalized $R,T,L$ in a tuple.

----


#### 2. The surface of a single mirror

In many cases, we need the optical properties of the surface of  an object. The most easily measured optical properties are reflectivity $R$, transmittance $T$, and loss $L$. Here, we define classes related to the mirror surface, which can be regarded as a surface with a thickness of $0$.

Following classes are defined in the module:

----

<strong id="MirrorSurface">MirrorSurface</strong>: `class MirrorSurface(RTL, misc.Position)`

This class defines a mirror surface and is a subclass of `RTL` and `misc.Position` which provide attributes <font color="red">r</font>, <font color="red">t</font>, <font color="red">l</font> and <font color="red">position</font>.

<font color="blue">The attributes are defined as follows</font>:

- <font color="red">modifiable_properties</font> - This attribute is set to `modifiable_properties = ('roc', 'r', 't', 'l', 'position')` where
  
  - <font color="red">roc</font> - $roc$, radius of curvature
  - <font color="red">r</font> - $R$, optical reflectivity
  - <font color="red">t</font> - $T$, optical transmittance
  - <font color="red">l</font> - $L$, optical loss
  - <font color="red">position</font> - the position of the mirror

- <font color="red">name</font> - The name of instances or classes. The default is *MirrorSurface*, which can be modified as required. 
  
- <font color="red">property_set</font> - Property collection, which is an instance of `PropertySet`, inherited by `_utils.Object`. See [introduction](introduction.md) for details.
  
- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.
  
  - properties provided by this class
    
    - <font color="red">roc</font> - $roc$, radius of curvature
  
  - properties provided by parent class
    
    - see <a class="class-refer">mirror.RTL</a> and <a class="class-refer">misc.Position</a> for details

<font color="blue">The methods are defined as follows</font>:

- <font color="red">\_\_init\_\_(name='MirrorSurface', **kwargs)</font>  - Create a `MirrorSurface` object by named parameters consistent with <font color="red">modifiable_properties</font>.
  
-  See <a class="class-refer">mirror.RTL</a>, <a class="class-refer">misc.PosItion</a>, <a class="class-refer-to" module="introduction">Object</a> from [introduction](introduction.md) for other methods.

----

#### 3. Mirror

This module is not mainly for designing optical systems, so we only define simple mirror classes.

Following classes are defined in the module:

----

<strong id="Mirror">Mirror</strong>: `class Mirror(RTL, misc.Position)`

A class for a thin mirror. In cavity-related applications, thin lens or `zero` aberration approximation can give good experimental results. Therefore, we only consider the effect of focal length $f$ of a mirror.

<font color="blue">The attributes are defined as follows</font>:

- <font color="red">modifiable_properties</font> - This attribute is set to `modifiable_properties = ('f', 'r', 't', 'l', 'position')` where
  
  - <font color="red">f</font> - $f$, focal distance
  - <font color="red">r</font> - $R$, optical reflectivity
  - <font color="red">t</font> - $T$, optical transmittance
  - <font color="red">l</font> - $L$, optical loss
  - <font color="red">position</font> - the position of the mirror

- <font color="red">name</font> - The name of instances or classes. The default is *Mirror*, which can be modified as required. 

- <font color="red">property_set</font> - Property collection, which is an instance of `PropertySet`, inherited by `_utils.Object`. See [introduction](introduction.md) for details.

- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.

  - properties provided by this class

    - <font color="red">f</font> - $f$, focal distance

  - properties provided by parent class

    - see <a class="class-refer">mirror.RTL</a> and <a class="class-refer">misc.Position</a> for details

<font color="blue">The methods are defined as follows</font>:

- <font color="red">\_\_init\_\_(name='Mirror', **kwargs)</font>  - Create a `Mirror` object by named parameters consistent with <font color="red">modifiable_properties</font>.

- See <a class="class-refer">mirror.RTL</a>, <a class="class-refer">misc.PosItion</a>, <a class="class-refer-to" module="introduction">Object</a> from [introduction](introduction.md) for other methods.

----

## Examples

