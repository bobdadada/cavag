## Physical Background

Fiber Cavity - Particle Coupling system

<div style="text-align:center"><img class="path-append" src="../_assets/picture/model/model_fiber_cavity_particle.svg" alt="fiber cavity and particle coupling"></div>

In addition to loss, we also need to consider the coupling efficiency between the various components, including:

the power coupling efficiency $\eta_{fc,coupling}$ between the fiber and cavity modes can be approximated simply by the overlap integral of the fiber and cavity mode intensity distributions, neglecting phase mismatch,
$$
\eta_{fc,coupling}=\frac{4}{\left(\frac{\omega_f}{\omega_m}+\frac{\omega_m}{\omega_f}\right)^2+\left(\frac{\pi n_f \omega_f \omega_m}{\lambda\cdot \text{ROC}}\right)^2}
$$
where $n_f$ is the refractive index of the fiber and $\text{ROC}$ the $\text{ROC}$ of the mirror

The electric dipole moment
$$
\mu_{eg}=\sqrt{\frac{3\pi\epsilon_0\hbar c^3\gamma_{eg}}{\omega^3}}
$$
Peak electric field intensity of the mode 
$$
\epsilon=\sqrt{\frac{\hbar\omega}{2\epsilon_0V}}
$$
Coupling $g$ coefficients
$$
g=\frac{\mu_{eg}e}{\hbar}=\frac{\mu_{eg}A\epsilon}{\hbar}=\frac{\mu_{eg}A}{\hbar}\sqrt{\frac{\hbar\omega}{2\epsilon_0V}}=A\sqrt{\frac{3\gamma_{eg}\pi c^3}{2V\omega^2}}
$$
where $e$ is the electric field strength at the particle's location.

single-atom cooperativity parameter
$$
C_1=\frac{g^2}{\kappa\gamma}
$$
where $\gamma$ is full width of the atomic absorption line and $\kappa$ is one half width of the cavity transmission line.

the coupling efficiency $\eta_{cp,emit}$ of the emitter to the cavity mode
$$
\eta_{cp,emit}=\frac{2C_1}{2C_1+1}
$$
the extraction efficiency $\eta_{cp,ext}$ of the single photon into a single-mode traveling wavepacket.
$$
\eta_{cp,ext}=\frac{2\kappa}{2\kappa+\gamma}
$$
the quantum efficiency of SPS in the cavity-QED strong-coupling regime
$$
\eta_q = \eta_{cp,emit}\cdot \eta_{cp,ext}
$$
the quantum efficiency of SPS in the cavity-QED bad cavity regime
$$
\eta_q = \eta_{cp,emit}
$$
equivalent transmission probability of photon in the cavity 
$$
\eta_{l,c,trans}=T_l\frac{1+R_r}{2(1-R_l R_r)}
$$

$$
\eta_{r,c,trans}=T_r\frac{1+R_l}{2(1-R_l R_r)}
$$

Natural broadening of atomic absorption line

[能量-时间的不确定关系如何导出光谱自然展宽？ - 知乎 (zhihu.com)](https://www.zhihu.com/question/33565055)



## Codes

### Classes



### Functions



## Examples