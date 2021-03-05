## Physical Background

<div class="float"><img src="_assets/pics/model_endface_step_fiber.svg" style="float:left;width:200px" alt="step-index fiber" title="step-index fiber"></div>

Optical fiber is a fibrous solid used to transmit light in a certain frequency range. A typical model of the end face of a simple step-index fiber without coating is shown in the figure. It is a two-layer structure. The inner layer is called core with higher refractive index, and the outer layer is called the cladding with lower refractive index. For a single-mode fiber, the relative refractive index difference between the two layers is generally 0.02~0.005.

<div style="clear: both"></div>

With the advancement of technology, manufacturers can produce optical fibers for a variety of different purposes, for example, graded-index fiber for optimized transmission, photonic crystal fiber for high coupling efficiency. 

## Codes

**This page corresponds to the module `cavag.fiber`** 

### Classes

1. The input and output ends of a fiber

In optical coupling applications, we only need to consider the conditions of the input and output ends of the fiber. Three properties ($n_f$, $\lambda$, and $w_f$) of the fiber must be considered. Any qualified manufacturer is fully capable of providing these data.  For the fiber cavity, the end face of the fiber is not necessarily flat. For this case, the radius of curvature $roc$ of the end face needs to be considered.

Following classes are defined in the module:

- **FiberEnd**

 

- **StepIndexFiberEnd**



## Examples

