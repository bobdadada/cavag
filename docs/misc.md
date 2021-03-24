## Codes

**This page corresponds to the module `misc`** 

### Classes

In this module, we define many commonly used auxiliary classes, all of which are subclasses of `_utils.PrintableObject`. Generally, we will not use these classes directly, but will combine them into more specific subclasses. 

#### 1. $R,T,L$

Since reflectivity $R$, transmittance $T$, and loss $L$ are important in the mirror-related applications and often given in an equivalent form in practical applications, we need $RTL$ abstract class and a helper class for $R,T,L$ conversion. 

Following classes are defined in the module:

----

<strong id="RTL">RTL</strong>: `class RTL(_utils.PrintableObject)`

This class define an abstract class describing $R,T,L$.

<font color="blue">The attributes are defined as follows</font>:

- <font color="red">modifiable_properties</font> - This attribute is set to `modifiable_properties = ('r', 't', 'l')` where

  - <font color="red">r</font> - $R$, optical reflectivity, the value must be between $0$ and $1$
  - <font color="red">t</font> - $T$, optical transmittance, the value must be between $0$ and $1$
  - <font color="red">l</font> - $L$, optical loss, the value must be between $0$ and $1$

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
  
- <font color="red">change_params(\_norm=True, \_filter=True, **kwargs)</font> - We rewrite the `change_params` method provided by <code>_utils.<a class="module-object-refer-to" module="introduction">Object</a></code> and provided an additional parameter <font color="red">\_norm</font>. If <font color="red">\_norm</font> is set to `True`, then the input parameters <font color="red">r</font>, <font color="red">t</font> and <font color="red">l</font> in <font color="red">kwargs</font> will be normalized, to make $R+T+L=1$.
  
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

#### 2. Position

The position is also an useful property of a real object. In this `cavag`, the commonly used position property is the position on the optical axis. So we need to define a one-dimensional position auxiliary class. 

Following classes are defined in the module:

----

<strong id="Position">Position</strong>: `class Position(_utils.PrintableObject)`

This class define a one-dimensional position.

<font color="blue">The attributes are defined as follows</font>:

- <font color="red">modifiable_properties</font> - This attribute is set to `modifiable_properties = ('position', )` where

  - <font color="red">position</font> - position of a real object, must be a number, default to $0$

  These attributes are also input parameters of the constructor. 

- <font color="red">name</font> - The name of instances or classes. The default is *Position*, which can be modified as required. 
  
- <font color="red">property_set</font> -  Property collection, which is an instance of `PropertySet`, inherited by `_utils.Object`. See [introduction](introduction.md) for details.
  
- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.
  
  - properties provided by this class
    
    - <font color="red">position</font> - position of a real object

<font color="blue">The methods are defined as follows</font>:

- <font color="red">\_\_init\_\_(name='Position', **kwargs)</font>  - Create a `Position` object by named parameters consistent with <font color="red">modifiable_properties</font>.

----

#### 3. Wavelength

For light, wavelength $\lambda$ is an important property. 

Following classes are defined in the module:

----

<strong id="Wavelength">Wavelength</strong>: `class Wavelength(_utils.PrintableObject)`

Light Wavelength Abstract Class.

<font color="blue">The attributes are defined as follows</font>:

- <font color="red">modifiable_properties</font> - This attribute is set to `modifiable_properties = ('wavelength', )` where

  - <font color="red">wavelength</font> - $\lambda$, wavelength of the light

  These attributes are also input parameters of the constructor. 

- <font color="red">name</font> - The name of instances or classes. The default is *Wavelength*, which can be modified as required. 

- <font color="red">property_set</font> -  Property collection, which is an instance of `PropertySet`, inherited by `_utils.Object`. See [introduction](introduction.md) for details.

- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.

  - properties provided by this class

    - <font color="red">wavelength</font> - $\lambda$, wavelength of transmitted light
    - <font color="red">k</font> - $k$, wave vector of transmitted light, where $k=2\pi/\lambda$.
    - <font color="red">nu</font> - $\nu$, frequency of transmitted light, wheres $\nu=c/\lambda$, where $c$ is speed of light in vacuum.
    - <font color="red">nu_angular</font> - $\nu_{angular}$, angular frequency of transmitted light, wheres $\nu_{angular}=2\pi \nu=2\pi c/\lambda=ck$.

<font color="blue">The methods are defined as follows</font>:

- <font color="red">\_\_init\_\_(name='Wavelength', **kwargs)</font>  - Create a `Wavelength` object by named parameters consistent with <font color="red">modifiable_properties</font>.

----

### Functions



## Examples

