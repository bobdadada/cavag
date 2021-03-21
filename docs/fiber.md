## Physical Background

<div class="float"><img src="_assets/picture/model/model_endface_step_fiber.svg" style="float:left;width:200px" alt="step-index fiber" title="step-index fiber"></div>

Optical fiber is a fibrous solid used to transmit light in a certain frequency range. A typical model of the end face of a simple step-index fiber without coating is shown in the figure. It is a two-layer structure. The inner layer is called core with higher refractive index, and the outer layer is called the cladding with lower refractive index. For a single-mode fiber, the relative refractive index difference between the two layers is generally 0.02~0.005.

<div style="clear: both"></div>

With the advancement of technology, manufacturers can produce optical fibers for a variety of different purposes, for example, graded-index fiber for optimized transmission, photonic crystal fiber for high coupling efficiency. 

## Codes

**This page corresponds to the module `fiber`** 

### Classes

#### 1. The input and output ends of a fiber

In optical coupling applications, we only need to consider the conditions of the input and output ends of the fiber. Three properties, $n_f$ (core refractive index), $\lambda$ (wavelength of transmitted light), and $w_f$ (radius of mode field), of the fiber must be considered. Any qualified manufacturer is fully capable of providing these data.  For the fiber cavity, the end face of the fiber is not necessarily flat. For this case, the radius of curvature $roc$ (radius of curvature) of the end face needs to be considered.

Following classes are defined in the module:

----

**FiberEnd**: `class FiberEnd(_utils.PrintableObject)`

This class define a fiber end face object. Almost all attributes cannot be assigned by `self.attr = value`. The attributes are defined as follows:

- <font color="red">name</font> - The name of instances or classes. The default is *FiberEnd*, which can be modified as required. 
- <font color="red">property_set</font> - A dict-like object contains all the properties necessary for the class. It is an instance of `_utils.PropertySet` and is initialized in `self.__init__`. It should not be artificially modified at runtime. If the value of any property is `None` when used, it will cause a `_utils.PropertyLost` exception.
- <font color="red">nf</font> - $n_f$, core refractive index, cannot be assigned directly.
- <font color="red">wavelength</font> - $\lambda$, wavelength of transmitted light, cannot be assigned directly.
- <font color="red">omegaf</font> - $w_f$, radius of mode field of fiber, cannot be assigned directly.
- <font color="red">nu0</font> - $\nu_0$, circular frequency of transmitted light, cannot be assigned directly, which equal to $2\pi/\lambda$.
- <font color="red">roc</font> - $roc$, radius of curvature, cannot be assigned directly. 

All important properties are initialized in the constructor. Only by using the constructor can we generate a `FiberEnd` object.

- <font color="red">\_\_init\_\_(self, nf, wavelength, omegaf, roc=sp.inf, name='FiberEnd')</font>  - Create a `FiberEnd` object by positional parameters <font color="red">nf</font>, <font color="red">wavelength</font>, <font color="red">omegaf</font>, <font color="red">roc</font> which defined above. `sp` is the abbreviation of package `scipy`.
- <font color="red">change_params(self, \_filter=True, **kwargs)</font> - This method is provided by `_utils.Object`, used to modify the value of parameters in `self.property_set`. The input of the method must be named parameters. If <font color="red">\_filter</font> is set to `True`, then only parameters consistent with in `self.__init__` can be set.

----

**StepIndexFiberEnd**: `class StepIndexFiberEnd(FiberEnd)`

This class is a subclass of `FiberEnd` and particularly used to describe a step-index fiber. The attributes are defined as follows:

- <font color="red">name</font> - The name of instances or classes. The default is *StepIndexFiberEnd*, which can be modified as required.
- <font color="red">a</font> - $a$ radius of fiber core,  cannot be assigned directly.
- <font color="red">naf</font> - $NA_f$ numerical aperture,  cannot be assigned directly. the numerical aperture by definition is given by $NA_{f}=\sqrt{n^2_{\text{core}}-n^2_{\text{clad}}}$.
- <font color="red">omegaf</font> - $w_f$ radius of mode field of fiber. For the step-index fiber, we can compute $w_f$ by approximation of Gaussian light. 
  $$
  w_f=a(0.65 +1.619V^{-1.5}+2.879V^{-6})
  $$
  for $V\gtrsim 1.2$ where
  $$
  V=\frac{2\pi a}{\lambda}\cdot NA_{f}
  $$
  is the normalized frequency. This is an empirical formula given by Marcuse<a class="refer">[2]</a>.

The constructor of `StepIndexFiberEnd` object is

- <font color="red">\_\_init\_\_(self, nf, wavelength, a, naf, roc=sp.inf, name='StepIndexFiberEnd')</font>  - Create a `StepIndexFiberEnd` object by positional parameters <font color="red">nf</font>, <font color="red">wavelength</font>, <font color="red">a</font>, <font color="red">naf</font>, <font color="red">roc</font> which defined above.
- <font color="red">change_params(self, \_filter=True, **kwargs)</font> - This method is provided by `_utils.Object`, used to modify the value of parameters in `self.property_set`. The input of the method must be named parameters. If <font color="red">\_filter</font> is set to `True`, then only parameters consistent with in `self.__init__` can be set.

----

## Examples

<div id="refer-anchor"></div>

## References

[1]: W. B. Joyce and B. C. DeLoach, "[Alignment of Gaussian beams](_assets/paper/alignment_of_gaussian_beams.pdf ':ignore :target=_blank')," APPLIED OPTICS 23, 23 (1984).

[2]: D. Marcuse, "Loss Analysis of Single-Mode Fiber Splices," Bell Syst. Tech. J. 56, 703 (1977).

