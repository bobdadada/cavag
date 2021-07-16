## Physical Background

### Definition

The normalized Gaussian Beam or more general Hermite-Gaussian Beam has form
$$
\begin{aligned}
&f_{mn}(x,y,z,t)\\&=u_{mn}(x,y,z)e^{-jkz}e^{j2\pi \nu t}
\end{aligned} \tag{1}
$$
where
$$
\begin{aligned}
&u_{mn}(x,y,z)\\
&=\frac{c_{mn}}{\sqrt{1+z^2/z_0^2}}\\
&\;\cdot\psi_{m}\left(\frac{\sqrt{2}x}{\omega}\right)\psi_{n}\left(\frac{\sqrt{2}y}{\omega}\right)\\
&\;\cdot \exp\left[-\frac{jk}{2R}(x^2+y^2)\right]\\
&\;\cdot e^{j(m+n+1)\phi}
\end{aligned} \tag{2}
$$
for $m,n=0,1,2,\dots$, where 
$$
z_0=\pi \omega_0^2/\lambda  \tag{3}
$$
 which also called by Rayleigh length or Rayleigh range, and
$$
R=R(z)=z\left[1+\left(\frac{z_0}{z}\right)^2\right] \tag{4}
$$

$$
\omega=\omega(z)=\omega_0\left[1+\left(\frac{z}{z_0}\right)^2\right]^{1/2} \tag{5}
$$

$$
\tan\phi=\frac{z}{z_0} \tag{6}
$$

the normalization factor is given by
$$
c_{mn}=\left(\frac{2}{\omega_0^2 \pi 2^{m+n}m! n!}\right)^{1/2}
$$
And note $\psi_m(\xi)=H_m(\xi)e^{-\xi^2/2}$ is the $m$th order Hermite-Gaussian mode to equation
$$
-\frac{d^2 \psi_m}{d \xi^2}+\xi^2 \psi_m = \lambda_m \psi_m
$$
with eigenvalue $\lambda_m=2(m+1/2)$. The normalization factor $c'_m$ of $\psi_m(\xi)$ is given by
$$
c'_m=\frac{1}{\pi^{1/4}\sqrt{2^m m!}}
$$
with identity $\int^{\infty}_{-\infty}H^2_m(\xi)e^{-\xi^2}d\xi=\sqrt{\pi} 2^m m!$. At $z=0$, we can get the shape of the waist
$$
\begin{aligned}
&u_{mn}(x_0,y_0)\\
&=c_{mn}\psi_{m}\left(\frac{\sqrt{2}x_0}{\omega_0}\right)\psi_{n}\left(\frac{\sqrt{2}y_0}{\omega_0}\right)
\end{aligned} \tag{7}
$$
$c_{mn}$ can be chosen so that $\int^{\infty}_{-\infty}dx_0 \int^{\infty}_{-\infty}dy_0 |u_{mn}(x_0,y_0)|^2=1$. The Hermite-Gaussian forward traveling wave can also be computed by
$$
\begin{aligned}
&u_{mn}(x,y,z)\\
&=\frac{j}{\lambda z}\int^{\infty}_{-\infty}dx_0\int^{\infty}_{-\infty}dy_0 u_{mn}(x_0,y_0)\\
&\;\cdot\exp\left\{-\frac{jk}{2z}[(x-x_0)^2+(y-y_0)^2]\right\}
\end{aligned}
$$

Through Maxwell’s equations, 
$$
\begin{aligned}
\mu \mathbf{H} &= \nabla \times \mathbf{A}\\
\mathbf{E} &= -j2\pi\nu \nabla \times \mathbf{A}-\nabla\Phi\\
\end{aligned}
$$
where $\Phi$ in an environment without charged particles, is
$$
\Phi=\frac{j}{2\pi\nu \mu\epsilon}\nabla \cdot \mathbf{A}
$$
Suppose that $\mathbf{A}$ is polarized along $\hat{\mathbf{x}}$:
$$
\mathbf{A}=\hat{\mathbf{x}}u_{mn}(x,y,z)e^{-jkz}
$$
Then
$$
\begin{aligned}
\mathbf{E} &= -j2\pi\nu \left(\hat{\mathbf{x}}u_{mn}-j\hat{\mathbf{z}}\frac{\partial u_{mn}}{k\partial x} \right)e^{-jkz}\\
\mu \mathbf{H} &= -jk\left(\hat{\mathbf{y}}u_{mn}-j\hat{\mathbf{z}}\frac{\partial u_{mn}}{k\partial y} \right)e^{-jkz}
\end{aligned} \tag{8}
$$

#### Characteristics of Gaussian mode

The most commonly used laser is the fundamental mode of Hermite-Gaussian beam, that is, $m=n=0$. The equation of the fundamental Gaussian mode is given by
$$
\begin{aligned}
&u_{00}(x_0,y_0)\\
&=\left(\frac{2}{\omega_0^2 \pi}\right)^{1/2}\exp\left(-\frac{x_0^2+y_0^2}{\omega_0^2}\right) 
\end{aligned} \tag{9}
$$
And the equation $(5)$ also shows that
$$
\frac{\omega^2(z)}{\omega_0^2}-\frac{z^2}{z_0^2}=1
$$
So the asymptotic straight line of above equation gives divergence half angle $\theta_{0}$ of Gaussian mode
$$
\tan\theta_{0}=\frac{\omega_0}{z_0}=\frac{\lambda}{\pi \omega_0} \tag{10}
$$
Since the fiber is axis-symmetric, the divergence full angle should be $2\theta_{0}$. In some textbooks, the mode volume of the Gaussian mode is given by

$$
\begin{aligned}
V_{00eff}=&\int^{z_2}_{z_1}\pi\omega_0^2\left[1+\left(\frac{z}{z_0}\right)^2\right]dz\\
=&\pi\omega_0^2\left[z_2-z_1+\frac{1}{3z_0^2}\left(z_2^3-z_1^3\right)\right]
\end{aligned} \tag{11}
$$

#### Characteristics of Hermite-Gaussian mode

The waist radius of $x$-direction of a Hermite-Gaussian mode is
$$
\omega_{m}=\sqrt{2m+1}\omega_0 \tag{12}
$$
and the half divergence angle of this direction is
$$
\theta_{m}=\sqrt{2m+1}\theta_{0} \tag{13}
$$
The mode volume of the Hermite-Gaussian mode is
$$
V_{mneff}=\sqrt{(2m+1)(2n+1)}V_{00eff} \tag{14}
$$
where $V_{00eff}$ is the mode volume of the fundamental mode at the same location.

### Demonstration

<div><img src="_assets/picture/res/gaussbeam/waist_of_hermite_gaussian_modes.png" alt="waist_of_hermite_gaussian_modes" style="float:left; height:300px;"></div>

The figure on the left shows the waist shape of some modes. It is easy to find that although the equation $(3)$ is equivalently satisfied for each mode, the beam waist of different modes cannot be represented by $\omega_0$ only, and only the waist radius of fundamental Gaussian mode can be represented by $\omega_0$.

In addition, as $m$ or $n$ increases, the number of nodes increases and the range of the waist becomes larger and larger. 


<div style="clear: both"></div>

<div><img src="_assets/picture/res/gaussbeam/random_comb_hermite_gaussian.png" alt="random_comb_hermite_gaussian" style="float:left; height:300px;"></div>

A waist of a random combinations of some mode are shown in this figure. It can be seen that the graph of a random combination of the Hermite-Gaussian modes becomes very weird. 

The state shown in the figure is a superposition state of multiple Hermite-Gaussian modes, that is
$$
u(x,y,z) = \sum_{m,n}u_{mn}(x,y,z)
$$
Note the intensity of this mode satisfies
$$
I(x,y,z)\propto \|u(x,y,z)\|^2=\left\|\sum_{m,n}u_{mn}(x,y,z)\right\|^2\ne\sum_{m,n}\left\|u_{mn}(x,y,z)\right\|^2
$$
The final inequality represents a typical difference between classical and quantum 

<div style="clear: both"></div>

<div><img src="_assets/picture/res/gaussbeam/intensity_center_waist_normalized_hg.png" alt="intensity_center_waist_normalized_hg" style="float:left; height:300px;"></div>

Using the orthogonality of the Hermite-Gaussian modes can we expand this graph. And the second figure shows the intensity at the center of the waist of each normalized Hermite-Gaussian mode. We also find an oscillation characteristic in this figure.

<div style="clear: both"></div>

The above pictures can be obtained from the notebook [hermite_gaussian_beam.ipynb](_assets/example/hermite_gaussian_beam.ipynb ':ignore :class=download').

### Transformation

#### Transformation by a lens

!> Please note that the definition of the symbol here is slightly different from elsewhere.

<div style="text-align:center"><img src="_assets/picture/model/model_gb_thin_lens.svg" alt="transformation of H-G by thin lens"></div>

With the characteristics of Hermite-Gaussian beams and the notation in the figure, we get
$$
\begin{aligned}
&\omega = \omega_0\left[1+\left(\frac{\lambda s}{\pi{\omega_0}^2}\right)^2\right]^{1/2} \\
& R= s\left[1+\left(\frac{\pi \omega_0^2}{\lambda s}\right)^2\right] 
\end{aligned} \tag{15}
$$
and
$$
\begin{aligned}
&\omega'_0 = \frac{\omega'}{\left[1+\left(\frac{\pi{\omega'}^2}{\lambda R'}\right)^2\right]^{1/2}}\\
&s' =  \frac{R'}{1+\left(\frac{\lambda R'}{\pi{\omega'}^2}\right)^2} 
\end{aligned} \tag{16}
$$
With our notations, features of the thin lens imply that
$$
\omega' = \omega \ \text{and} \ \frac{1}{R'}-\frac{1}{R} = \frac{1}{f'}  \tag{17}
$$
Then with the order following
$$
\begin{aligned}
& (\omega_0,s)\overset{(15)}\rightarrow (\omega,R) \\
& \overset{(17)}\rightarrow(\omega',R')\overset{(16)}\rightarrow(\omega'_0,s')
\end{aligned}
$$
one can get radius and position of the waist of the Gaussian beam after passing through the thin lens. This is the same for any mode of Hermite-Gaussian.

#### Transformation by a mirror

<div style="text-align:center"><img src="_assets/picture/model/model_gb_mirror.svg" alt="transformation of H-G by thin mirror"></div>

A mirror of radius $R_0$ reflects the beam and changes the radius of curvature of the phase front. If we unfold the beam, we find that the incident phase delay $k(x^2+y^2)/(2R)$ is advanced by $2[k(x^2+y^2)/(2R_0)]$ because the path is shortened twice. Thus $R'$ of the unfolded reflected beam is given by
$$
\frac{1}{R'}=\frac{1}{R}-\frac{2}{R_0}
$$
A unfolded mirror acts like a lens with a focal distance $f'=R_0/2$.

If we move the origin of the coordinates to the position of the mirror surface, change the definition of symbols, then the features of unfold mirror gives the following.

!> The definitions of $R',R,R_0$ below have changed

With our notations, similar to $(17)$, features of the mirror imply that
$$
\omega' = \omega \ \text{and} \ \frac{1}{R'}-\frac{1}{R} = \frac{2}{R_0}  \tag{18}
$$
Then the waist position and waist radius of the beam after reflection can be calculated by the following steps
$$
\begin{aligned}
&(\omega_0,s)\overset{(15)}\rightarrow (\omega,R) \overset{(18)}\rightarrow(\omega',R')\\
&\overset{(16)}\rightarrow(\omega'_0,s')\overset{z\rightarrow -z}\rightarrow(\omega'_0,-s')
\end{aligned}
$$
In the last expression, the optical axis has undergone an axis-symmetric transformation with respect to the vertical axis. At this time, all parameters in the Gaussian beam should be calculated in the new optical axis. 

#### Transformation by a general linear system

A Gaussian beam is completely by the complex parameter $q$, where
$$
\frac{1}{q}=\frac{1}{R}-j\frac{\lambda}{\pi \omega^2} \tag{19}
$$
and the definition of $R$ and $\omega$ can be seen in formula $(4),(5)$. Because all higher-order Hermite-Gaussian modes are described by the same $R$ and $\omega$, the same $q$ parameter, their transformation is governed by the same law, except in so far as the phase change $(m+n+1)\phi$ is concerned. And a paraxial system can be described by $A,B,C,D$ matrix. The transformations of $q$ can be expressed as a bilinear transformation
$$
q'=\frac{Aq+B}{Cq+D} \tag{20}
$$
This can be verified in any linear system.

## Codes

**This page corresponds to the module `gaussbeam`**

### Classes

#### 1. One-dimensional Hermite-Gaussian beam

Generally speaking, Hermite-Gaussian beam needs to be described by all three coordinates $x,y,z$. However, it can be seen from formulas $(1)$ and $(2)$ that we can learn the characteristics of a Hermite-Gaussian Beam by studying the propagation characteristics in a certain direction.

----

<strong class="object" id="NormalizedHermiteGaussBeam1D">NormalizedHermiteGaussBeam1D</strong>: `class NormalizedHermiteGaussBeam1D(misc.Wavelength)`

This class defines a general normalized Hermite-Gaussian beam in one dimension. And it is a subclass of `misc.Wavelength`. The normalization condition required $\int^{\infty}_{-\infty}dx_0 |u(x_0)|^2=1$.

<p style="color:blue;">attributes:</p>

- <span class="attr" style="color:red;">modifiable_properties</span> - This attribute is set to `modifiable_properties = ('wavelength', 'p0', 'omega0', 'm')` where

  - <span class="attr" style="color:red;">wavelength</span> - $\lambda$, wavelength of the beam
  - <span class="attr" style="color:red;">p0</span> - $p_0$, position of the waist
  - <span class="attr" style="color:red;">omega0</span> - $\omega_0$, radius of the waist
  - <span class="attr" style="color:red;">m</span> - $m$, mode number

- <span class="attr" style="color:red;">name</span> - The name of instances or classes. default to be *NormalizedHermiteGaussBeam1D*, which can be modified as required. 

- <span class="attr" style="color:red;">property_set</span> - Property collection, which is an instance of `PropertySet`, inherited from `_utils.Object`. See [introduction](introduction.md) for details.

- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.

  - properties provided by this class

    - <span class="attr" style="color:red;">p0</span> - $p_0$, position of the waist
    - <span class="attr" style="color:red;">omega0</span> - $\omega_0$, radius of the waist
    - <span class="attr" style="color:red;">m</span> - $m$, mode number
    - <span class="attr" style="color:red;">cm</span> - $c_m$, normalization factor of beam, defined by $c_{m}=\left(2/\pi\right)^{1/4}/\sqrt{\omega_0  2^{m} m!}$
    - <span class="attr" style="color:red;">z0</span> - $z_0$, Rayleigh length, defined by $\pi\omega_0^2/\lambda$
    - <span class="attr" style="color:red;">thetam</span> - $\theta_m$, half divergence angle in radian, defined by $\theta_m=\sqrt{2m+1}\arctan(\lambda/(\pi \omega_0))$
    - <span class="attr" style="color:red;">hm</span> - $h_m$, Hermite polynomial $H_m$

  - properties provided by parent class

    - see <a class="module-object-refer">misc.Wavelength</a> for details

<p style="color:blue;">methods:</p>

- <span class="method" style="color:red;">\_\_init\_\_(<span class="param">name</span>='NormalizedHermiteGaussBeam1D', \*\*<span class="param">kwargs</span>)</span> - Create a `NormalizedHermiteGaussBeam1D` object by named parameters consistent with <span class="attr" style="color:red;">modifiable\_properties</span>.

- <span class="method" style="color:red;">a_f(<span class="param">z</span>)</span> - Compute the amplitude at position <span class="param">z</span>, the amplitude is defined by $1/(1+(z-p_0)^2/z_0^2)^{1/4}$.

- <span class="method" style="color:red;">omega_f(<span class="param">z</span>)</span> - Compute the mode field radius at position <span class="param">z</span>, which is defined by $\omega_0\sqrt{1+(z-p_0)^2/z_0^2}$.

- <span class="method" style="color:red;">r_f(<span class="param">z</span>)</span> - Compute the radius of curvature at position <span class="param">z</span>, which is defined by $(z-p_0)(1+z_0^2/(z-p_0)^2)$.

- <span class="method" style="color:red;">phi_f(<span class="param">z</span>)</span> - Compute $\phi$ phase at position <span class="param">z</span>, which is defined by $\arctan((z-p_0)/z_0)$.

- <span class="method" style="color:red;">psim_f(<span class="param">z</span>, <span class="param">x</span>)</span> - Compute $\psi_m$ at position <span class="param">z</span> and <span class="param">x</span>, which is defined by $H_m(\xi)e^{-\xi^2/2}$, where $\xi=\sqrt{2}x/\omega$.

- <span class="method" style="color:red;">u_f(<span class="param">z</span>, <span class="param">x</span>)</span> - Compute $u$ at position <span class="param">z</span> and <span class="param">x</span>, see the formula $(1)$. This function will return the total amplitude $a_t$ and total phase $\phi_t$, and $u=a_te^{j\phi_t}$.

- See <a class="module-object-refer">misc.Wavelength</a> and <a class="module-object-refer-to" module="introduction">Object</a> for other methods.

----

<strong class="object" id="HermiteGaussBeam1D">HermiteGaussBeam1D</strong>: `class HermiteGaussBeam1D(NormalizedHermiteGaussBeam1D)`

This class is a subclass of `NormalizedHermiteGaussBeam1D` with a given magnitude of amplitude. In classical physics, a single mode can have any magnitude of intensity. 

<p style="color:blue;">attributes:</p>

- <span class="attr" style="color:red;">modifiable_properties</span> - This attribute is set to `modifiable_properties = ('a0', 'wavelength', 'p0', 'omega0', 'm')` where

  - <span class="attr" style="color:red;">a0</span> - $a_0$, amplitude 
  - <span class="attr" style="color:red;">wavelength</span> - $\lambda$, wavelength of the beam
  - <span class="attr" style="color:red;">p0</span> - $p_0$, position of the waist
  - <span class="attr" style="color:red;">omega0</span> - $\omega_0$, radius of the waist
  - <span class="attr" style="color:red;">m</span> - $m$, mode number

- <span class="attr" style="color:red;">name</span> - The name of instances or classes. default to be *HermiteGaussBeam1D*, which can be modified as required. 

- <span class="attr" style="color:red;">property_set</span> - Property collection, which is an instance of `PropertySet`, inherited from `_utils.Object`. See [introduction](introduction.md) for details.

- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.

  - properties provided by this class

    - <span class="attr" style="color:red;">a0</span> - $a_0$, amplitude of the Hermite-Gaussian mode.

  - properties provided by parent class

    - see <a class="module-object-refer-to" module="gaussbeam">NormalizedHermiteGaussBeam1D</a> for details

<p style="color:blue;">methods:</p>

- <span class="method" style="color:red;">\_\_init\_\_(<span class="param">name</span>='HermiteGaussBeam1D', \*\*<span class="param">kwargs</span>)</span> - Create a `HermiteGaussBeam1D` object by named parameters consistent with <span class="attr" style="color:red;">modifiable\_properties</span>.

- <span class="method" style="color:red;">a_f(<span class="param">z</span>)</span> - Compute the amplitude of this mode at position <span class="param">z</span>. In our implementation, this amplitude is defined by $a_0/(1+(z-p_0)^2/z_0^2)^{1/4}$.

- See <a class="module-object-refer-to" module="gaussbeam">NormalizedHermiteGaussBeam1D</a> and <a class="module-object-refer-to" module="introduction">Object</a> for other methods.

----

<strong class="object" id="NormalizedGaussBeam1D">NormalizedGaussBeam1D</strong>: `class NormalizedGaussBeam1D(NormalizedHermiteGaussBeam1D)`

This class defines a class of Gaussian beam with mode number $m=0$.

<p style="color:blue;">attributes:</p>

- <span class="attr" style="color:red;">modifiable_properties</span> - This attribute is set to `modifiable_properties = ('wavelength', 'p0', 'omega0')` where

  - <span class="attr" style="color:red;">wavelength</span> - $\lambda$, wavelength of the beam
  - <span class="attr" style="color:red;">p0</span> - $p_0$, position of the waist
  - <span class="attr" style="color:red;">omega0</span> - $\omega_0$, radius of the waist

- <span class="attr" style="color:red;">name</span> - The name of instances or classes. default to be *NormalizedGaussBeam1D*, which can be modified as required. 

- <span class="attr" style="color:red;">property_set</span> - Property collection, which is an instance of `PropertySet`, inherited from `_utils.Object`. See [introduction](introduction.md) for details.

- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.

  - properties provided by parent class

    - see <a class="module-object-refer-to" module="gaussbeam">NormalizedHermiteGaussBeam1D</a> for details

<p style="color:blue;">methods:</p>

- <span class="method" style="color:red;">\_\_init\_\_(<span class="param">name</span>='NormalizedGaussBeam1D', \*\*<span class="param">kwargs</span>)</span> - Create a `NormalizedGaussBeam1D` object by named parameters consistent with <span class="attr" style="color:red;">modifiable\_properties</span>.

- See <a class="module-object-refer-to" module="gaussbeam">NormalizedHermiteGaussBeam1D</a> and <a class="module-object-refer-to" module="introduction">Object</a> for other methods.

----

<strong class="object" id="GaussBeam1D">GaussBeam1D</strong>: `class GaussBeam1D(HermiteGaussBeam1D)`

This class defines a Gaussian beam with arbitrary magnitude of amplitude.

<p style="color:blue;">attributes:</p>

- <span class="attr" style="color:red;">modifiable_properties</span> - This attribute is set to `modifiable_properties = ('a0', 'wavelength', 'p0', 'omega0')` where

  - <span class="attr" style="color:red;">a0</span> - $a_0$, amplitude 
  - <span class="attr" style="color:red;">wavelength</span> - $\lambda$, wavelength of the beam
  - <span class="attr" style="color:red;">p0</span> - $p_0$, position of the waist
  - <span class="attr" style="color:red;">omega0</span> - $\omega_0$, radius of the waist
  
- <span class="attr" style="color:red;">name</span> - The name of instances or classes. default to be *GaussBeam1D*, which can be modified as required. 

- <span class="attr" style="color:red;">property_set</span> - Property collection, which is an instance of `PropertySet`, inherited from `_utils.Object`. See [introduction](introduction.md) for details.

- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.

  - properties provided by parent class

    - see <a class="module-object-refer-to" module="gaussbeam">HermiteGaussBeam1D</a> for details

<p style="color:blue;">methods:</p>

- <span class="method" style="color:red;">\_\_init\_\_(<span class="param">name</span>='GaussBeam1D', \*\*<span class="param">kwargs</span>)</span> - Create a `GaussBeam1D` object by named parameters consistent with <span class="attr" style="color:red;">modifiable\_properties</span>.

- See <a class="module-object-refer-to" module="gaussbeam">HermiteGaussBeam1D</a> and <a class="module-object-refer-to" module="introduction">Object</a> for other methods.

----

#### 2. General Hermite-Gaussian beam

In practical applications, we often need to consider various Hermite-Gaussian modes. For example, in laser applications, the laser is usually not single mode. At this time, we need to consider the modes in both $x,y$ directions at the same time. 

----

<strong class="object" id="NormalizedHermiteGaussBeam">NormalizedHermiteGaussBeam</strong>: `class NormalizedHermiteGaussBeam(Wavelength)`

This class define a general normalized Hermite-Gaussian beam with definition $(1)$.

<p style="color:blue;">attributes:</p>

- <span class="attr" style="color:red;">modifiable_properties</span> - This attribute is set to `modifiable_properties = ('wavelength', 'p0', 'omega0x', 'omega0y', 'mx', 'my')` where

  - <span class="attr" style="color:red;">wavelength</span> - $\lambda$, wavelength of the beam
  - <span class="attr" style="color:red;">p0</span> - $p_0$, position of the waist
  - <span class="attr" style="color:red;">omega0x</span> - ${\omega_0}_x$, radius of the waist in $x$-direction
  - <span class="attr" style="color:red;">omega0y</span> - ${\omega_0}_y$, radius of the waist in $y$-direction
  - <span class="attr" style="color:red;">mx</span> - $m_x$, mode number in $x$-direction
  - <span class="attr" style="color:red;">my</span> - $m_y$, mode number in $y$-direction

- <span class="attr" style="color:red;">name</span> - The name of instances or classes. default to be *NormalizedHermiteGaussBeam*, which can be modified as required. 

- <span class="attr" style="color:red;">property_set</span> - Property collection, which is an instance of `PropertySet`, inherited from `_utils.Object`. See [introduction](introduction.md) for details.

- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.

  - properties provided by this class

    - <span class="attr" style="color:red;">p0</span> - $p_0$, position of the waist
    - <span class="attr" style="color:red;">omega0x</span> - ${\omega_0}_x$, radius of the waist in $x$-direction
    - <span class="attr" style="color:red;">omega0y</span> - ${\omega_0}_y$, radius of the waist in $y$-direction
    - <span class="attr" style="color:red;">mx</span> - $m_x$, mode number in $x$-direction
    - <span class="attr" style="color:red;">my</span> - $m_y$, mode number in $y$-direction
    - <span class="attr" style="color:red;">cmx</span> - ${c_m}_x$, normalization factor of beam in $x$-direction, defined by ${c_{m}}_x=\left(2/\pi\right)^{1/4}/\sqrt{{\omega_0}_x 2^{m_x} m_x !}$
    - <span class="attr" style="color:red;">cmy</span> - ${c_m}_y$, normalization factor of beam in $y$-direction, defined by ${c_{m}}_y=\left(2/\pi\right)^{1/4}/\sqrt{{\omega_0}_y 2^{m_y} m_y !}$
    - <span class="attr" style="color:red;">cm</span> - $c_m$, total normalization factor of beam, defined by $c_{m}={c_{m}}_x{c_{m}}_y$
    - <span class="attr" style="color:red;">z0x</span> - ${z_0}_x$, Rayleigh length in $x$-direction, defined by $\pi{\omega_0}_x^2/\lambda$
    - <span class="attr" style="color:red;">z0y</span> - ${z_0}_y$, Rayleigh length in $y$-direction, defined by $\pi{\omega_0}_y^2/\lambda$
    - <span class="attr" style="color:red;">thetamx</span> - ${\theta_m}_x$, half divergence angle in radian in $x$-direction, defined by ${\theta_m}_x=\sqrt{2m_x+1}\arctan(\lambda/(\pi {\omega_0}_x))$
    - <span class="attr" style="color:red;">thetamy</span> - ${\theta_m}_y$, half divergence angle in radian in $y$-direction, defined by ${\theta_m}_y=\sqrt{2m_y+1}\arctan(\lambda/(\pi {\omega_0}_y))$
    - <span class="attr" style="color:red;">hmx</span> - ${h_m}_x$, Hermite polynomial ${H_m}_x$
    - <span class="attr" style="color:red;">hmy</span> - ${h_m}_y$, Hermite polynomial ${H_m}_y$
  
  - properties provided by parent class
  
    - see <a class="module-object-refer">misc.Wavelength</a> for details

<p style="color:blue;">methods:</p>

- <span class="method" style="color:red;">\_\_init\_\_(<span class="param">name</span>='NormalizedHermiteGaussBeam', \*\*<span class="param">kwargs</span>)</span> - Create a `NormalizedHermiteGaussBeam` object by named parameters consistent with <span class="attr" style="color:red;">modifiable\_properties</span>.

- <span class="method" style="color:red;">a_f(<span class="param">z</span>)</span> - Compute the amplitude at position <span class="param">z</span>, the amplitude is defined by $1/[(1+(z-p_0)^2/{z_0}_x^2)^{1/4}(1+(z-p_0)^2/{z_0}_y^2)^{1/4}]$.

- <span class="method" style="color:red;">omegax_f(<span class="param">z</span>)</span> - Compute the mode field radius in $x$-direction at position <span class="param">z</span>

- <span class="method" style="color:red;">omegay_f(<span class="param">z</span>)</span> - Compute the mode field radius in $y$-direction at position <span class="param">z</span>

- <span class="method" style="color:red;">rx_f(<span class="param">z</span>)</span> - Compute the radius of curvature in $x$-direction at position <span class="param">z</span>

- <span class="method" style="color:red;">ry_f(<span class="param">z</span>)</span> - Compute the radius of curvature in $y$-direction at position <span class="param">z</span>

- <span class="method" style="color:red;">phix_f(<span class="param">z</span>)</span> - Compute $\phi$ phase in $x$-direction at position <span class="param">z</span>

- <span class="method" style="color:red;">phiy_f(<span class="param">z</span>)</span> - Compute $\phi$ phase in $y$-direction at position <span class="param">z</span>

- <span class="method" style="color:red;">psimx_f(<span class="param">z</span>, <span class="param">x</span>)</span> - Compute $\psi_{m_x}$ at position <span class="param">z</span> and <span class="param">x</span>, which is defined by $H_{m_x}(\xi_x)e^{-\xi_x^2/2}$, where $\xi_x=\sqrt{2}x/\omega_x$.

- <span class="method" style="color:red;">psimy_f(<span class="param">z</span>, <span class="param">y</span>)</span> - Compute $\psi_{m_y}$ at position <span class="param">z</span> and <span class="param">y</span>, which is defined by $H_{m_y}(\xi_y)e^{-\xi_y^2/2}$, where $\xi_y=\sqrt{2}y/\omega_y$.

- <span class="method" style="color:red;">u_f(<span class="param">z</span>, <span class="param">x</span>, <span class="param">y</span>)</span> - Compute $u$ at position <span class="param">z</span>, <span class="param">x</span> and <span class="param">y</span>, see the formula $(1)$. This function will return the total amplitude $a_t$ and total phase $\phi_t$, and $u=a_te^{j\phi_t}$.

- See <a class="module-object-refer">misc.Wavelength</a> and <a class="module-object-refer-to" module="introduction">Object</a> for other methods.

----

<strong class="object" id="HermiteGaussBeam">HermiteGaussBeam</strong>: `class HermiteGaussBeam(NormalizedHermiteGaussBeam)`

This class is a subclass of `NormalizedHermiteGaussBeam` with a given magnitude of amplitude. In classical physics, a single mode can have any magnitude of intensity. 

<p style="color:blue;">attributes:</p>

- <span class="attr" style="color:red;">modifiable_properties</span> - This attribute is set to `modifiable_properties = ('a0', 'wavelength', 'p0', 'omega0x', 'omega0y', 'mx', 'my')` where

  - <span class="attr" style="color:red;">a0</span> - $a_0$, amplitude 
  - <span class="attr" style="color:red;">wavelength</span> - $\lambda$, wavelength of the beam
  - <span class="attr" style="color:red;">p0</span> - $p_0$, position of the waist
  - <span class="attr" style="color:red;">omega0x</span> - ${\omega_0}_x$, radius of the waist in $x$-direction
  - <span class="attr" style="color:red;">omega0y</span> - ${\omega_0}_y$, radius of the waist in $y$-direction
  - <span class="attr" style="color:red;">mx</span> - $m_x$, mode number in $x$-direction
  - <span class="attr" style="color:red;">my</span> - $m_y$, mode number in $y$-direction

- <span class="attr" style="color:red;">name</span> - The name of instances or classes. default to be *HermiteGaussBeam*, which can be modified as required. 

- <span class="attr" style="color:red;">property_set</span> - Property collection, which is an instance of `PropertySet`, inherited from `_utils.Object`. See [introduction](introduction.md) for details.

- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.

  - properties provided by this class

    - <span class="attr" style="color:red;">a0</span> - $a_0$, amplitude of the Hermite-Gaussian mode.

  - properties provided by parent class

    - see <a class="module-object-refer-to" module="gaussbeam">NormalizedHermiteGaussBeam</a> for details

<p style="color:blue;">methods:</p>

- <span class="method" style="color:red;">\_\_init\_\_(<span class="param">name</span>='HermiteGaussBeam', \*\*<span class="param">kwargs</span>)</span> - Create a `HermiteGaussBeam` object by named parameters consistent with <span class="attr" style="color:red;">modifiable\_properties</span>.

- <span class="method" style="color:red;">a_f(<span class="param">z</span>)</span> - Compute the amplitude of this mode at position <span class="param">z</span>. In our implementation, this amplitude is defined by $a_0/[(1+(z-p_0)^2/{z_0}_x^2)^{1/4}(1+(z-p_0)^2/{z_0}_y^2)^{1/4}]$.

- See <a class="module-object-refer-to" module="gaussbeam">NormalizedHermiteGaussBeam</a> and <a class="module-object-refer-to" module="introduction">Object</a> for other methods.

----

<strong class="object" id="NormalizedGaussBeam">NormalizedGaussBeam</strong>: `class NormalizedGaussBeam(NormalizedHermiteGaussBeam)`

This class defines a class of Gaussian beam with mode number $m=0$.

<p style="color:blue;">attributes:</p>

- <span class="attr" style="color:red;">modifiable_properties</span> - This attribute is set to `modifiable_properties = ('wavelength', 'p0', 'omega0x', 'omega0y')` where

  - <span class="attr" style="color:red;">wavelength</span> - $\lambda$, wavelength of the beam
  - <span class="attr" style="color:red;">p0</span> - $p_0$, position of the waist
  - <span class="attr" style="color:red;">omega0x</span> - ${\omega_0}_x$, radius of the waist in $x$-direction
  - <span class="attr" style="color:red;">omega0y</span> - ${\omega_0}_y$, radius of the waist in $y$-direction

- <span class="attr" style="color:red;">name</span> - The name of instances or classes. default to be *NormalizedGaussBeam*, which can be modified as required. 

- <span class="attr" style="color:red;">property_set</span> - Property collection, which is an instance of `PropertySet`, inherited from `_utils.Object`. See [introduction](introduction.md) for details.

- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.

  - properties provided by parent class

    - see <a class="module-object-refer-to" module="gaussbeam">NormalizedHermiteGaussBeam</a> for details

<p style="color:blue;">methods:</p>

- <span class="method" style="color:red;">\_\_init\_\_(<span class="param">name</span>='NormalizedGaussBeam', \*\*<span class="param">kwargs</span>)</span> - Create a `NormalizedGaussBeam` object by named parameters consistent with <span class="attr" style="color:red;">modifiable\_properties</span>.

- See <a class="module-object-refer-to" module="gaussbeam">NormalizedHermiteGaussBeam</a> and <a class="module-object-refer-to" module="introduction">Object</a> for other methods.

----

<strong class="object" id="GaussBeam">GaussBeam</strong>: `class GaussBeam(HermiteGaussBeam)`

This class defines a Gaussian beam with arbitrary magnitude of amplitude.

<p style="color:blue;">attributes:</p>

- <span class="attr" style="color:red;">modifiable_properties</span> - This attribute is set to `modifiable_properties = ('a0', 'wavelength', 'p0', 'omega0x', 'omega0y')` where

  - <span class="attr" style="color:red;">a0</span> - $a_0$, amplitude 
  - <span class="attr" style="color:red;">wavelength</span> - $\lambda$, wavelength of the beam
  - <span class="attr" style="color:red;">p0</span> - $p_0$, position of the waist
  - <span class="attr" style="color:red;">omega0x</span> - ${\omega_0}_x$, radius of the waist in $x$-direction
  - <span class="attr" style="color:red;">omega0y</span> - ${\omega_0}_y$, radius of the waist in $y$-direction

- <span class="attr" style="color:red;">name</span> - The name of instances or classes. default to be *GaussBeam*, which can be modified as required. 

- <span class="attr" style="color:red;">property_set</span> - Property collection, which is an instance of `PropertySet`, inherited from `_utils.Object`. See [introduction](introduction.md) for details.

- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.

  - properties provided by parent class

    - see <a class="module-object-refer-to" module="gaussbeam">HermiteGaussBeam</a> for details

<p style="color:blue;">methods:</p>

- <span class="method" style="color:red;">\_\_init\_\_(<span class="param">name</span>='GaussBeam', \*\*<span class="param">kwargs</span>)</span> - Create a `GaussBeam` object by named parameters consistent with <span class="attr" style="color:red;">modifiable\_properties</span>.

- See <a class="module-object-refer-to" module="gaussbeam">HermiteGaussBeam</a> and <a class="module-object-refer-to" module="introduction">Object</a> for other methods.

----

#### 3. The radius of mode is the same in both x, y

In common cases, we think that the beam waist of the fundamental Gaussian beam is the same in both $x$ and $y$, that is, ${\omega_0}_x={\omega_0}_y$. At this time, the mode in the $x$ and $y$ directions is degenerate. For example, a general optical fiber is axisymmetric, and the output beam satisfies ${\omega_0}_x={\omega_0}_y$. For these modes, the properties $z_0,R(z),\omega(z),\phi(z)$ defined by $(3)-(6)$ are equal in both $x$ and $y$ directions.

----

<strong class="object" id="NormalizedEqualHermiteGaussBeam">NormalizedEqualHermiteGaussBeam</strong>: `class NormalizedEqualHermiteGaussBeam(NormalizedHermiteGaussBeam)`

This class defines a general Hermite Gaussian beam with ${\omega_0}_x={\omega_0}_y$.

<p style="color:blue;">attributes:</p>

- <span class="attr" style="color:red;">modifiable_properties</span> - This attribute is set to `modifiable_properties = ('wavelength', 'p0', 'omega0', 'mx', 'my')` where
  - <span class="attr" style="color:red;">wavelength</span> - $\lambda$, wavelength of the beam
  - <span class="attr" style="color:red;">p0</span> - $p_0$, position of the waist
  - <span class="attr" style="color:red;">omega0</span> - $\omega_0$, radius of the waist
  - <span class="attr" style="color:red;">mx</span> - $m_x$, mode number in $x$-direction
  - <span class="attr" style="color:red;">my</span> - $m_y$, mode number in $x$-direction
  
- <span class="attr" style="color:red;">name</span> - The name of instances or classes. default to be *NormalizedEqualHermiteGaussBeam*, which can be modified as required. 

- <span class="attr" style="color:red;">property_set</span> - Property collection, which is an instance of `PropertySet`, inherited from `_utils.Object`. See [introduction](introduction.md) for details.

- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.

  - properties provided by this class

    - <span class="attr" style="color:red;">omega0</span> - $\omega_0$, radius of the waist
    - <span class="attr" style="color:red;">z0</span> - $z_0$, Rayleigh length, defined by $\pi\omega_0^2/\lambda$

  - properties provided by parent class

    - see <a class="module-object-refer-to" module="gaussbeam">NormalizedHermiteGaussBeam</a> for details

<p style="color:blue;">methods:</p>

- <span class="method" style="color:red;">\_\_init\_\_(<span class="param">name</span>='NormalizedEqualHermiteGaussBeam', \*\*<span class="param">kwargs</span>)</span> - Create a `NormalizedEqualHermiteGaussBeam` object by named parameters consistent with <span class="attr" style="color:red;">modifiable\_properties</span>.

- <span class="method" style="color:red;">omega_f(<span class="param">z</span>)</span> - Compute the mode field radius at position <span class="param">z</span>.

- <span class="method" style="color:red;">r_f(<span class="param">z</span>)</span> - Compute the radius of curvature at position <span class="param">z</span>.

- <span class="method" style="color:red;">phi_f(<span class="param">z</span>)</span> - Compute $\phi$ phase at position <span class="param">z</span>.

- <span class="method" style="color:red;">preprocess_properties(\*\*<span class="param">propdict</span>)</span> - Pre-process properties, which are used to adjust the change of property names between this class and the parent class <a class="module-object-refer-to" module="gaussbeam">NormalizedHermiteGaussBeam</a>, see <a class="module-object-refer-to" module="introduction">Object</a> for more details.

- See <a class="module-object-refer-to" module="gaussbeam">NormalizedHermiteGaussBeam</a> for other methods.

----

<strong class="object" id="EqualHermiteGaussBeam">EqualHermiteGaussBeam</strong>: `class EqualHermiteGaussBeam(NormalizedEqualHermiteGaussBeam)`

This class defines a general Hermite Gaussian beam with ${\omega_0}_x={\omega_0}_y$ and a given magnitude of amplitude.

<p style="color:blue;">attributes:</p>

- <span class="attr" style="color:red;">modifiable_properties</span> - This attribute is set to `modifiable_properties = ('a0', 'wavelength', 'p0', 'omega0', 'mx', 'my')` where

  - <span class="attr" style="color:red;">a0</span> - $a_0$, amplitude 
  - <span class="attr" style="color:red;">wavelength</span> - $\lambda$, wavelength of the beam
  - <span class="attr" style="color:red;">p0</span> - $p_0$, position of the waist
  - <span class="attr" style="color:red;">omega0</span> - $\omega_0$, radius of the waist
  - <span class="attr" style="color:red;">mx</span> - $m_x$, mode number in $x$-direction
  - <span class="attr" style="color:red;">my</span> - $m_y$, mode number in $x$-direction

- <span class="attr" style="color:red;">name</span> - The name of instances or classes. default to be *EqualHermiteGaussBeam*, which can be modified as required. 

- <span class="attr" style="color:red;">property_set</span> - Property collection, which is an instance of `PropertySet`, inherited from `_utils.Object`. See [introduction](introduction.md) for details.

- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.

  - properties provided by this class

    - <span class="attr" style="color:red;">a0</span> - $a_0$, amplitude of the Hermite-Gaussian mode.

  - properties provided by parent class

    - see <a class="module-object-refer-to" module="gaussbeam">NormalizedEqualHermiteGaussBeam</a> for details

<p style="color:blue;">methods:</p>

- <span class="method" style="color:red;">\_\_init\_\_(<span class="param">name</span>='EqualHermiteGaussBeam', \*\*<span class="param">kwargs</span>)</span> - Create a `EqualHermiteGaussBeam` object by named parameters consistent with <span class="attr" style="color:red;">modifiable\_properties</span>.

- <span class="method" style="color:red;">a_f(<span class="param">z</span>)</span> - Compute the amplitude of this mode at position <span class="param">z</span>. In our implementation, this amplitude is defined by $a_0/[(1+(z-p_0)^2/z_0^2)^{1/2}]$.

- See <a class="module-object-refer-to" module="gaussbeam">NormalizedEqualHermiteGaussBeam</a> and <a class="module-object-refer-to" module="introduction">Object</a> for other methods.

----

#### 4. The mode is the same in both x, y

In practical applications, Hermite-Gaussian beams with $m_x=m_y$ and ${\omega_0}_x={\omega_0}_y$ are commonly used. And for these objects, we omit subscript $x$, $y$.

----

<strong class="object" id="NormalizedEqualSymmetricHermiteGaussBeam">NormalizedEqualSymmetricHermiteGaussBeam</strong>: `class NormalizedEqualSymmetricHermiteGaussBeam(NormalizedHermiteGaussBeam1D)`

This class defines a general normalized Hermite-Gaussian beam with $m_x=m_y$ and ${\omega_0}_x={\omega_0}_y$, and we omit the subscript in the definition of the class.

<p style="color:blue;">attributes:</p>

- <span class="attr" style="color:red;">modifiable_properties</span> - This attribute is set to `modifiable_properties = ('wavelength', 'p0', 'omega0', 'm')` where

  - <span class="attr" style="color:red;">wavelength</span> - $\lambda$, wavelength of the beam
  - <span class="attr" style="color:red;">p0</span> - $p_0$, position of the waist
  - <span class="attr" style="color:red;">omega0</span> - $\omega_0$, radius of the waist
  - <span class="attr" style="color:red;">m</span> - $m$, mode number

- <span class="attr" style="color:red;">name</span> - The name of instances or classes. default to be *NormalizedEqualSymmetricHermiteGaussBeam*, which can be modified as required. 

- <span class="attr" style="color:red;">property_set</span> - Property collection, which is an instance of `PropertySet`, inherited from `_utils.Object`. See [introduction](introduction.md) for details.

- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.

  - properties provided by this class

    - <span class="attr" style="color:red;">cm</span> - $c_m$, total normalization factor of beam, defined by $c_{m}=\left(2/\pi\right)^{1/2}/(\omega_0  2^{m} m!)$

  - properties provided by parent class

    - see <a class="module-object-refer-to" module="gaussbeam">NormalizedHermiteGaussBeam1D</a> for details

<p style="color:blue;">methods:</p>

- <span class="method" style="color:red;">\_\_init\_\_(<span class="param">name</span>='NormalizedEqualSymmetricHermiteGaussBeam', \*\*<span class="param">kwargs</span>)</span> - Create a `NormalizedEqualSymmetricHermiteGaussBeam` object by named parameters consistent with <span class="attr" style="color:red;">modifiable\_properties</span>.

- <span class="method" style="color:red;">a_f(<span class="param">z</span>)</span> - Compute the amplitude at position <span class="param">z</span>, the amplitude is defined by $1/(1+(z-p_0)^2/z_0^2)^{1/2}$.

- <span class="method" style="color:red;">u_f(<span class="param">z</span>, <span class="param">x</span>, <span class="param">y</span>)</span> - Compute $u$ at position <span class="param">z</span>, <span class="param">x</span> and <span class="param">y</span>, see the formula $(1)$. This function will return the total amplitude $a_t$ and total phase $\phi_t$, and $u=a_te^{j\phi_t}$.

- See <a class="module-object-refer-to" module="gaussbeam">NormalizedHermiteGaussBeam1D</a> and <a class="module-object-refer-to" module="introduction">Object</a> for other methods.

----

<strong class="object" id="EqualSymmetricHermiteGaussBeam">EqualSymmetricHermiteGaussBeam</strong>: `class EqualSymmetricHermiteGaussBeam(NormalizedEqualSymmetricHermiteGaussBeam)`

This class is a subclass of `NormalizedEqualSymmetricHermiteGaussBeam` with a given magnitude of amplitude. In classical physics, a single mode can have any magnitude of intensity. 

<p style="color:blue;">attributes:</p>

- <span class="attr" style="color:red;">modifiable_properties</span> - This attribute is set to `modifiable_properties = ('a0', 'wavelength', 'p0', 'omega0', 'm')` where

  - <span class="attr" style="color:red;">a0</span> - $a_0$, amplitude 
  - <span class="attr" style="color:red;">wavelength</span> - $\lambda$, wavelength of the beam
  - <span class="attr" style="color:red;">p0</span> - $p_0$, position of the waist
  - <span class="attr" style="color:red;">omega0</span> - $\omega_0$, radius of the waist
  - <span class="attr" style="color:red;">m</span> - $m$, mode number

- <span class="attr" style="color:red;">name</span> - The name of instances or classes. default to be *EqualSymmetricHermiteGaussBeam*, which can be modified as required. 

- <span class="attr" style="color:red;">property_set</span> - Property collection, which is an instance of `PropertySet`, inherited from `_utils.Object`. See [introduction](introduction.md) for details.

- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.

  - properties provided by this class

    - <span class="attr" style="color:red;">a0</span> - $a_0$, amplitude of the Hermite-Gaussian mode.

  - properties provided by parent class

    - see <a class="module-object-refer-to" module="gaussbeam">NormalizedEqualSymmetricHermiteGaussBeam</a> for details

<p style="color:blue;">methods:</p>

- <span class="method" style="color:red;">\_\_init\_\_(<span class="param">name</span>='EqualSymmetricHermiteGaussBeam', \*\*<span class="param">kwargs</span>)</span> - Create a `EqualSymmetricHermiteGaussBeam` object by named parameters consistent with <span class="attr" style="color:red;">modifiable\_properties</span>.

- <span class="method" style="color:red;">a_f(<span class="param">z</span>)</span> - Compute the amplitude of this mode at position <span class="param">z</span>. In our implementation, this amplitude is defined by $a_0/(1+(z-p_0)^2/z_0^2)^{1/2}$.

- See <a class="module-object-refer-to" module="gaussbeam">NormalizedEqualSymmetricHermiteGaussBeam</a> and <a class="module-object-refer-to" module="introduction">Object</a> for other methods.

----

<strong class="object" id="NormalizedEqualGaussBeam">NormalizedEqualGaussBeam</strong>: `class NormalizedEqualGaussBeam(NormalizedEqualSymmetricHermiteGaussBeam)`

This class defines a class of Gaussian beam with mode number $m=0$ and ${\omega_0}_x={\omega_0}_y$.

<p style="color:blue;">attributes:</p>

- <span class="attr" style="color:red;">modifiable_properties</span> - This attribute is set to `modifiable_properties = ('wavelength', 'p0', 'omega0')` where

  - <span class="attr" style="color:red;">wavelength</span> - $\lambda$, wavelength of the beam
  - <span class="attr" style="color:red;">p0</span> - $p_0$, position of the waist
  - <span class="attr" style="color:red;">omega0</span> - $\omega_0$, radius of the waist

- <span class="attr" style="color:red;">name</span> - The name of instances or classes. default to be *NormalizedEqualGaussBeam*, which can be modified as required. 

- <span class="attr" style="color:red;">property_set</span> - Property collection, which is an instance of `PropertySet`, inherited from `_utils.Object`. See [introduction](introduction.md) for details.

- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.

  - properties provided by parent class

    - see <a class="module-object-refer-to" module="gaussbeam">NormalizedEqualSymmetricHermiteGaussBeam</a> for details

<p style="color:blue;">methods:</p>

- <span class="method" style="color:red;">\_\_init\_\_(<span class="param">name</span>='NormalizedEqualGaussBeam', \*\*<span class="param">kwargs</span>)</span> - Create a `NormalizedEqualGaussBeam` object by named parameters consistent with <span class="attr" style="color:red;">modifiable\_properties</span>.

- See <a class="module-object-refer-to" module="gaussbeam">NormalizedEqualSymmetricHermiteGaussBeam</a> and <a class="module-object-refer-to" module="introduction">Object</a> for other methods.

----

<strong class="object" id="EqualGaussBeam">EqualGaussBeam</strong>: `class EqualGaussBeam(EqualSymmetricHermiteGaussBeam)`

This class defines a Gaussian beam with arbitrary magnitude of amplitude.

<p style="color:blue;">attributes:</p>

- <span class="attr" style="color:red;">modifiable_properties</span> - This attribute is set to `modifiable_properties = ('a0', 'wavelength', 'p0', 'omega0')` where

  - <span class="attr" style="color:red;">a0</span> - $a_0$, amplitude 
  - <span class="attr" style="color:red;">wavelength</span> - $\lambda$, wavelength of the beam
  - <span class="attr" style="color:red;">p0</span> - $p_0$, position of the waist
  - <span class="attr" style="color:red;">omega0</span> - $\omega_0$, radius of the waist

- <span class="attr" style="color:red;">name</span> - The name of instances or classes. default to be *EqualGaussBeam*, which can be modified as required. 

- <span class="attr" style="color:red;">property_set</span> - Property collection, which is an instance of `PropertySet`, inherited from `_utils.Object`. See [introduction](introduction.md) for details.

- The following attributes are all decorated by `@property`, which cannot be assigned directly. Some properties are provided by the parent class.

  - properties provided by parent class

    - see <a class="module-object-refer-to" module="gaussbeam">EqualSymmetricHermiteGaussBeam</a> for details

<p style="color:blue;">methods:</p>

- <span class="method" style="color:red;">\_\_init\_\_(<span class="param">name</span>='EqualGaussBeam', \*\*<span class="param">kwargs</span>)</span> - Create a `EqualGaussBeam` object by named parameters consistent with <span class="attr" style="color:red;">modifiable\_properties</span>.

- See <a class="module-object-refer-to" module="gaussbeam">EqualSymmetricHermiteGaussBeam</a> and <a class="module-object-refer-to" module="introduction">Object</a> for other methods.

----

### Functions

Here we define some helper functions. In order to facilitate the understanding of the physical meaning behind these functions, we use physical variables as parameters instead of an instance of Hermite-Gaussian beam.

----

<strong class="object" id="local2remote">local2remote</strong>: `def local2remote(wavelength, omega0, z)`

Given the wavelength and the waist radius of the fundamental mode beam, calculate the fundamental mode field radius at a certain position. The waist is at the origin, and the radius of curvature is positive in the positive direction of the coordinate axis. This function can be used directly in higher-order modes. 

See also <a class="module-object-refer-to" module="gaussbeam">remote2local</a>.

<p style="color:blue;">parameters:</p>

- <span class="param">wavelength</span> - $\lambda$, wavelength of the beam
- <span class="param">omega0</span> - $\omega_0$, radius of the waist
- <span class="param">z</span> - $z$, position

<p style="color:blue;">returns:</p>

- <span class="param">omega</span> - $\omega$, the mode field radius at $z$, see the definition $(5)$
- <span class="param">r</span> - $R$, radius of curvature at $z$, see the definition $(4)$

----

<strong class="object" id="remote2local">remote2local</strong>: `def remote2local(wavelength, omega, r)`

Given the wavelength, the fundamental mode radius and the radius of curvature at current position, calculate the radius of the waist of the fundamental mode beam and the distance between the waist and the current position. The waist is at the origin, and the radius of curvature in the positive direction of the coordinate axis is positive. This function can be used directly in higher order modes.

See also <a class="module-object-refer-to" module="gaussbeam">local2remote</a>.

<p style="color:blue;">parameters:</p>

- <span class="param">wavelength</span> - $\lambda$, wavelength of the beam
- <span class="param">omega</span> - $\omega$, radius of the fundamental mode field
- <span class="param">r</span> - $R$, radius of curvature

<p style="color:blue;">returns:</p>

- <span class="param">omega0</span> - $\omega_0$, radius of the waist
- <span class="param">z</span> - $z$, position

----

<strong class="object" id="convert_through_lens">convert_through_lens</strong>: `def convert_through_lens(wavelength, omega0, s, f)`

Compute the transformation of Hermite-Gaussian Beam through a perfect thin lens. The [model](#transformation-by-a-lens) is shown above.

See also <a class="module-object-refer-to" module="gaussbeam">convert_through_mirror</a>.

<p style="color:blue;">parameters:</p>

- <span class="param">wavelength</span> - $\lambda$, wavelength of the beam
- <span class="param">omega0</span> - $\omega_0$, radius of the waist
- <span class="param">s</span> - $s$, position of the waist from the lens
- <span class="param">f</span> - $f$, focal distance, positive for positive lens, negative for negative lens

<p style="color:blue;">returns:</p>

- <span class="param">omega0p</span> - $\omega_0'$, radius of the waist after the transformation
- <span class="param">sp</span> - $s'$, position of the waist after the transformation

----

<strong class="object" id="convert_through_mirror">convert_through_mirror</strong>: `def convert_through_mirror(wavelength, omega0, s, roc)`

Compute the transformation of Hermite-Gaussian Beam through a perfect mirror. The [model](#transformation-by-a-mirror) is shown above.

See also <a class="module-object-refer-to" module="gaussbeam">convert_through_lens</a>.

<p style="color:blue;">parameters:</p>

- <span class="param">wavelength</span> - $\lambda$, wavelength of the beam
- <span class="param">omega0</span> - $\omega_0$, radius of the waist
- <span class="param">s</span> - $s$, position of the waist from the mirror
- <span class="param">roc</span> - $roc$, radius of curvature of the mirror, positive for concave mirror, negative for convex mirror 

<p style="color:blue;">returns:</p>

- <span class="param">omega0p</span> - $\omega_0'$, radius of the waist after the transformation
- <span class="param">sp</span> - $s'$, position of the waist after the transformation

----

## Examples

<div id="refer-anchor"></div>

## References

[1]: Hermann A. Haus, "[WAVES AND FIELDS IN OPTOELECTRONICS](_assets/paper/waves-and-fields-in-optoelectronics.djvu ":ignore :class=download")," Prentice-Hall, Inc., Englewood Cliffs, New Jersey 07632.