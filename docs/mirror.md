## Physical Background



## Codes

**This page corresponds to the module `mirror`** 

### Classes

#### 1. The surface of a single mirror

In many cases, we need the optical properties of the surface of  an object. The most easily measured optical properties are reflectivity $R$, transmittance $T$, and loss $L$. Here, we define classes related to the mirror surface, which can be regarded as a surface with a thickness of $0$.

Following classes are defined in the module:

----

**MirrorSurface**: `class MirrorSurface(misc.Position)`

This class defines a mirror surface and is a subclass of `misc.Position` which provides attribute <font color="red">position</font>.  Almost all attributes cannot be assigned by `self.attr = value`. The attributes are defined as follows:

- <font color="red">name</font> - The name of instances or classes. The default is *MirrorSurface*, which can be modified as required. 
- <font color="red">property_set</font> - A dict-like object contains all the properties necessary for the class. It is an instance of `_utils.PropertySet` and is initialized in `self.__init__`. It should not be artificially modified at runtime. If the value of any property is `None` when used, it will cause a `_utils.PropertyLost` exception.
- <font color="red">roc</font> - $roc$, radius of curvature, cannot be assigned directly.
- <font color="red">r</font> - $R$, optical reflectivity, cannot be assigned directly, default to be $0$, the value must be between $0$ and $1$.
- <font color="red">t</font> - $T$, optical transmittance, cannot be assigned directly, default to be $1$, the value must be between $0$ and $1$.
- <font color="red">l</font> - $L$, optical loss, cannot be assigned directly, default to be $0$, the value must be between $0$ and $1$.
- <font color="red">position</font> - the position of the mirror, provided by `misc.Position`.

The methods are defined as follows:

- <font color="red">\_\_init\_\_(self, roc, r=0, t=1, l=0, position=0, name='MirrorSurface', **kwargs)</font> - create a `MirrorSurface` object by parameters shown above. Note $R,T,L$ are normalized in the constructor, i.e, $R+T+L=1$.
- <font color="red">add_loss(self, loss)</font> - this method provides a way to add <font color="red">loss</font> to the surface. In common cases, the loss can be divided into multiple parts. At this time, the loss will be added by this method, and the method will calculate the normalized $R,T,L$.
- <font color="red">change_params(self, **kwargs)</font> - This method is provided by `_utils._Object`, used to modify the value of parameters in `self.property_set`. The input of the method must be named parameters.

----

#### 2. Lens with partial functions

This module is not mainly for designing optical systems, so we only define simple lens classes.

Following classes are defined in the module:

----

**ThickLens**: `class ThickLens(misc.Position)`

A class for thick lens. For thick lenses, the left focal length is not equal to the right focal length. Almost all attributes cannot be assigned by `self.attr = value`. The attributes are defined as follows:

- <font color="red">name</font> - The name of instances or classes. The default is *ThickLens*, which can be modified as required.
- <font color="red">property_set</font> - A dict-like object contains all the properties necessary for the class. It is an instance of `_utils.PropertySet` and is initialized in `self.__init__`. It should not be artificially modified at runtime. If the value of any property is `None` when used, it will cause a `_utils.PropertyLost` exception.
- <font color="red">d</font> - $d$, Lens thickness, cannot be assigned directly.
- <font color="red">fl</font> - $f_l$, left focal distance, cannot be assigned directly.
- <font color="red">fr</font> - $f_r$, left focal distance, cannot be assigned directly.
- <font color="red">position</font> - the position of the mirror, provided by `misc.Position`.

The methods are defined as follows:

- <font color="red">\_\_init\_\_(self, d, fl, fr, position, name='ThickLens', **kwargs)</font> - create a `ThickLens` object by parameters shown above.
- <font color="red">change_params(self, **kwargs)</font> - This method is provided by `_utils._Object`, used to modify the value of parameters in `self.property_set`. The input of the method must be named parameters.

----

**ThinLens**: `class ThinLens(ThickLens)`

A class for thin lens, that is, lens with a thickness of $0$. It is a subclass of `ThickLens`. Almost all attributes cannot be assigned by `self.attr = value`. The attributes are defined as follows:

- <font color="red">name</font> - The name of instances or classes. The default is *ThinLens*, which can be modified as required.
- <font color="red">f</font> - $f$, focal distance, cannot be assigned directly.
- <font color="red">position</font> - the position of the mirror, provided by `misc.Position`.

The methods are defined as follows:

- <font color="red">\_\_init\_\_(self, f, position, name='ThinLens', **kwargs)</font> - create a `ThinLens` object by parameters shown above.
- <font color="red">change_params(self, **kwargs)</font> - This method is provided by `_utils._Object`, used to modify the value of parameters in `self.property_set`. The input of the method must be named parameters.

----

## Examples

