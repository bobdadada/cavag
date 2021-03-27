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

<strong class="object" id="FiberEnd">FiberEnd</strong>: `class FiberEnd(misc.Wavelength)`

This class define a fiber end face object. Almost all attributes cannot be assigned by `self.attr = value`.

<p style="color:blue;">The attributes are defined as follows:</p>

- <span class="attr" style="color:red;">modifiable_properties</span> - This attribute is set to `modifiable_properties = ('nf', 'wavelength', 'omegaf', 'roc')` where
  
  - <span class="attr" style="color:red;">nf</span> - $n_f$, core refractive index
  - <span class="attr" style="color:red;">wavelength</span> - $\lambda$, wavelength of transmitted light
  - <span class="attr" style="color:red;">omegaf</span> - $\omega_f$, radius of mode field of fiber
  - <span class="attr" style="color:red;">roc</span> - $roc$, radius of curvature, default to `inf`
  
  These attributes are also input parameters of the constructor. 

- <span class="attr" style="color:red;">name</span> - The name of instances or classes. The default is *FiberEnd*, which can be modified as required. 

- <span class="attr" style="color:red;">property_set</span> -  Property collection, which is an instance of `PropertySet`, inherited by `_utils.Object`. See [introduction](introduction.md) for details.

- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.

  - properties provided by this class

    - <span class="attr" style="color:red;">nf</span> - $n_f$, core refractive index
    - <span class="attr" style="color:red;">omegaf</span> - $\omega_f$, radius of mode field of fiber
    - <span class="attr" style="color:red;">roc</span> - $roc$, radius of curvature

  - properties provided by parent class

    - see <a class="module-object-refer">misc.Wavelength</a> for details

<p style="color:blue;">The methods are defined as follows:</p>

- <span class="attr" style="color:red;">\_\_init\_\_(name='FiberEnd', **kwargs)</span>  - Create a `FiberEnd` object by named parameters consistent with <span class="attr" style="color:red;">modifiable_properties</span>. 

- See <a class="module-object-refer">misc.Wavelength</a>, <a class="module-object-refer-to" module="introduction">Object</a> from [introduction](introduction.md) for other methods.

----

<strong class="object" id="StepIndexFiberEnd">StepIndexFiberEnd</strong>: `class StepIndexFiberEnd(FiberEnd)`

This class is a subclass of `FiberEnd` and particularly used to describe a step-index fiber.

<p style="color:blue;">The attributes are defined as follows:</p>

- <span class="attr" style="color:red;">modifiable_properties</span> - This attribute is set to `modifiable_properties = ('nf', 'wavelength', 'a', 'naf', 'roc')` where
  
  - <span class="attr" style="color:red;">nf</span> - $n_f$, core refractive index
  - <span class="attr" style="color:red;">wavelength</span> - $\lambda$, wavelength of transmitted light
  - <span class="attr" style="color:red;">a</span> - $a$, radius of fiber core
  - <span class="attr" style="color:red;">naf</span> - $NA_f$, numerical aperture
  - <span class="attr" style="color:red;">roc</span> - $roc$, radius of curvature, default to `inf`
  
  These attributes are also input parameters of the constructor. 

- <span class="attr" style="color:red;">name</span> - The name of instances or classes. The default is *StepIndexFiberEnd*, which can be modified as required.

- <span class="attr" style="color:red;">property_set</span> -  Property collection, which is an instance of `PropertySet`, inherited by `_utils.Object`. See [introduction](introduction.md) for details.

- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.

  - properties provided by this class
  
    - <span class="attr" style="color:red;">a</span> - $a$, radius of fiber core
    - <span class="attr" style="color:red;">naf</span> - $NA_f$, numerical aperture. the numerical aperture by definition is given by $NA_{f}=\sqrt{n^2_{\text{core}}-n^2_{\text{clad}}}$.
    - <span class="attr" style="color:red;">omegaf</span> - $\omega_f$, radius of mode field of fiber. For the step-index fiber, we can compute $w_f$ by approximation of Gaussian light. 
      $$
      \omega_f=a(0.65 +1.619V^{-1.5}+2.879V^{-6})
      $$
      for $V\gtrsim 1.2$ where
      $$
      V=\frac{2\pi a}{\lambda}\cdot NA_{f}
      $$
      is the normalized frequency. This is an empirical formula given by Marcuse<a class="refer">[2]</a>. The normalized frequency of single-mode fiber satisfies $V<2.405$.

  - properties provided by parent class

    - see <a class="module-object-refer-to" module="fiber">FiberEnd</a> for details

<p style="color:blue;">The methods are defined as follows:</p>

- <span class="attr" style="color:red;">\_\_init\_\_(name='StepIndexFiberEnd', **kwargs)</span>  - Create a `StepIndexFiberEnd` object by named parameters consistent with <span class="attr" style="color:red;">modifiable_properties</span>. 

- See <a class="module-object-refer-to" module="fiber">FiberEnd</a>, <a class="module-object-refer-to" module="introduction">Object</a> from [introduction](introduction.md) for other methods.

----

## Examples

<div id="refer-anchor"></div>

## References

[1]: W. B. Joyce and B. C. DeLoach, "[Alignment of Gaussian beams](_assets/paper/alignment_of_gaussian_beams.pdf ':ignore :target=_blank')," APPLIED OPTICS 23, 23 (1984).

[2]: D. Marcuse, "Loss Analysis of Single-Mode Fiber Splices," Bell Syst. Tech. J. 56, 703 (1977).

