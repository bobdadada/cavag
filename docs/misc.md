## Codes

**This page corresponds to the module `misc`** 

### Classes

In this module, we define many commonly used auxiliary classes, all of which are subclasses of `_utils.PrintableObject`. Generally, we will not use these classes directly, but will combine them into more specific subclasses. 

#### 1. $R,T,L$

Since reflectivity $R$, transmittance $T$, and loss $L$ are important in the mirror-related applications and often given in an equivalent form in practical applications, we need $RTL$ abstract class and a helper class for $R,T,L$ conversion. 

Following classes are defined in the module:

----

<strong class="object" id="RTL">RTL</strong>: `class RTL(_utils.PrintableObject)`

This class define an abstract class describing $R,T,L$.

<p style="color:blue;">The attributes are defined as follows:</p>

- <span class="attr" style="color:red;">modifiable_properties</span> - This attribute is set to `modifiable_properties = ('r', 't', 'l')` where

  - <span class="attr" style="color:red;">r</span> - $R$, optical reflectivity, the value must be between $0$ and $1$
  - <span class="attr" style="color:red;">t</span> - $T$, optical transmittance, the value must be between $0$ and $1$
  - <span class="attr" style="color:red;">l</span> - $L$, optical loss, the value must be between $0$ and $1$

  These attributes are also input parameters of the constructor. 

- <span class="attr" style="color:red;">name</span> - The name of instances or classes. The default is *RTL*, which can be modified as required. 

- <span class="attr" style="color:red;">property_set</span> -  Property collection, which is an instance of `PropertySet`, inherited by `_utils.Object`. See [introduction](introduction.md) for details.

- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.

  - properties provided by this class
    
    - <span class="attr" style="color:red;">r</span> - $R$, optical reflectivity
    - <span class="attr" style="color:red;">t</span> - $T$, optical transmittance
    - <span class="attr" style="color:red;">l</span> - $L$, optical loss

<p style="color:blue;">The methods are defined as follows:</p>

- <span class="method" style="color:red;">\_\_init\_\_(<span class="param">name</span>='RTL', \*\*<span class="param">kwargs</span>)</span>  - Create a `RTL` object by named parameters consistent with <span class="attr" style="color:red;">modifiable_properties</span>. For parameter <span class="attr" style="color:red;">r</span>, <span class="attr" style="color:red;">t</span> and <span class="attr" style="color:red;">l</span>, one can provide only two of them, and the remaining one can be calculated when the class is constructed. Note $R,T,L$ are normalized in the constructor, i.e, $R+T+L=1$.
  
- <span class="method" style="color:red;">preprocess\_properties(<span class="param">\_norm</span>=True, \*\*<span class="param">propdict</span>)</span> - We rewrite the `preprocess_properties` method provided by <code>_utils.<a class="module-object-refer-to" module="introduction">Object</a></code> and provided an additional parameter <span class="param" style="color:red;">\_norm</span>. If <span class="param" style="color:red;">\_norm</span> is set to `True`, then the input parameters <span class="attr" style="color:red;">r</span>, <span class="attr" style="color:red;">t</span> and <span class="attr" style="color:red;">l</span> in <span class="param" style="color:red;">propdict</span> will be normalized, to make $R+T+L=1$.
  
- <span class="method" style="color:red;">add_loss(<span class="param">loss</span>)</span> - This method provides a way to add <span class="param" style="color:red;">loss</span> to the surface. In common cases, the loss can be divided into multiple parts. At this time, the loss will be added by this method, and the method will calculate the normalized $R,T,L$.

----

<strong class="object" id="RTLConverter">RTLConverter</strong>: `class RTLConverter`

A helper class for the $R,T,L$ conversion. This class is mainly used to define a namespace, and all methods of the class are decorated as `@staticmethod`.

<p style="color:blue;">The methods are defined as follows:</p>

- <span class="method" style="color:red;">@(staticmethod): normalize(<span class="param">r</span>=None, <span class="param">t</span>=None, <span class="param">l</span>=None)</span> - The method is used to normalize the $R,T,L$, i.e. $R+T+L=1$. One can only provide only two of the parameters reflectivity - $R$ - <span class="param" style="color:red;">r</span>, transmittance - $T$ - <span class="param" style="color:red;">t</span>, loss - $L$ - <span class="param" style="color:red;">l</span>. Then this method will return the normalized $R,T,L$ in a tuple.
  
- <span class="method" style="color:red;">@(staticmethod): rtl_by_r_t2l(<span class="param">r</span>, <span class="param">t2l</span>)</span> - By parameters reflectivity - $R$ - <span class="param" style="color:red;">r</span> and the ratio of transmittance to loss - $T/L$ - <span class="param" style="color:red;">t2l</span>, this method returns the normalized $R,T,L$ in a tuple.
  
- <span class="method" style="color:red;">@(staticmethod): rtl_by_t_r2l(<span class="param">t</span>, <span class="param">r2l</span>)</span> - By parameters transmittance - $T$ - <span class="param" style="color:red;">t</span> and the ratio of reflectivity to loss - $R/L$ - <span class="param" style="color:red;">r2l</span>, this method returns the normalized $R,T,L$ in a tuple.
  
- <span class="method" style="color:red;">@(staticmethod): add_reflectivity(<span class="param">m0</span>, <span class="param">re</span>)</span> - This method adds extra reflectivity - <span class="param" style="color:red;">re</span> to the original (reflectivity, transmittance, loss) tuple - <span class="param" style="color:red;">m0</span>, and returns the normalized $R,T,L$ in a tuple.
  
- <span class="method" style="color:red;">@(staticmethod): add_transmittance(<span class="param">m0</span>, <span class="param">te</span>)</span> - This method adds extra transmittance - <span class="param" style="color:red;">te</span> to the original (reflectivity, transmittance, loss) tuple - <span class="param" style="color:red;">m0</span>, and returns the normalized $R,T,L$ in a tuple.
  
- <span class="method" style="color:red;">@(staticmethod): add_loss(<span class="param">m0</span>, <span class="param">le</span>)</span> - This method adds extra loss - <span class="param" style="color:red;">le</span> to the original (reflectivity, transmittance, loss) tuple - <span class="param" style="color:red;">m0</span>, and returns the normalized $R,T,L$ in a tuple.

----

#### 2. Position

The position is also an useful property of a real object. In this `cavag`, the commonly used position property is the position on the optical axis. So we need to define a one-dimensional position auxiliary class. 

Following classes are defined in the module:

----

<strong class="object" id="Position">Position</strong>: `class Position(_utils.PrintableObject)`

This class define a one-dimensional position.

<p style="color:blue;">The attributes are defined as follows:</p>

- <span class="attr" style="color:red;">modifiable_properties</span> - This attribute is set to `modifiable_properties = ('position', )` where

  - <span class="attr" style="color:red;">position</span> - position of a real object, must be a number, default to $0$

  These attributes are also input parameters of the constructor. 

- <span class="attr" style="color:red;">name</span> - The name of instances or classes. The default is *Position*, which can be modified as required. 
  
- <span class="attr" style="color:red;">property_set</span> -  Property collection, which is an instance of `PropertySet`, inherited by `_utils.Object`. See [introduction](introduction.md) for details.
  
- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.
  
  - properties provided by this class
    
    - <span class="attr" style="color:red;">position</span> - position of a real object

<p style="color:blue;">The methods are defined as follows:</p>

- <span class="method" style="color:red;">\_\_init\_\_(<span class="param">name</span>='Position', \*\*<span class="param">kwargs</span>)</span>  - Create a `Position` object by named parameters consistent with <span class="attr" style="color:red;">modifiable_properties</span>.

----

#### 3. Wavelength

For light, wavelength $\lambda$ is an important property. 

Following classes are defined in the module:

----

<strong class="object" id="Wavelength">Wavelength</strong>: `class Wavelength(_utils.PrintableObject)`

Light Wavelength Abstract Class.

<p style="color:blue;">The attributes are defined as follows:</p>

- <span class="attr" style="color:red;">modifiable_properties</span> - This attribute is set to `modifiable_properties = ('wavelength', )` where

  - <span class="attr" style="color:red;">wavelength</span> - $\lambda$, wavelength of the light

  These attributes are also input parameters of the constructor. 

- <span class="attr" style="color:red;">name</span> - The name of instances or classes. The default is *Wavelength*, which can be modified as required. 

- <span class="attr" style="color:red;">property_set</span> -  Property collection, which is an instance of `PropertySet`, inherited by `_utils.Object`. See [introduction](introduction.md) for details.

- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.

  - properties provided by this class

    - <span class="attr" style="color:red;">wavelength</span> - $\lambda$, wavelength of transmitted light
    - <span class="attr" style="color:red;">k</span> - $k$, wave vector of transmitted light, where $k=2\pi/\lambda$.
    - <span class="attr" style="color:red;">nu</span> - $\nu$, frequency of transmitted light, wheres $\nu=c/\lambda$, where $c$ is speed of light in vacuum.
    - <span class="attr" style="color:red;">nu_angular</span> - $\nu_{angular}$, angular frequency of transmitted light, wheres $\nu_{angular}=2\pi \nu=2\pi c/\lambda=ck$.

<p style="color:blue;">The methods are defined as follows:</p>

- <span class="method" style="color:red;">\_\_init\_\_(<span class="param">name</span>='Wavelength', \*\*<span class="param">kwargs</span>)</span>  - Create a `Wavelength` object by named parameters consistent with <span class="attr" style="color:red;">modifiable_properties</span>.

----

### Functions



## Examples

