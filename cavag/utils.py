from typing import Union
from collections import namedtuple

import numpy as np
import matplotlib.pyplot as plt
from scipy import constants

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

__all__ = [
    'calculate_fpcavity_total_efficiency',
    'calculate_eta_mode'
]

_SCALE = {
    'nm': 1e-9,
    'um': 1e-6,
    'mm': 1e-3,
    'm': 1,
}


def plot_cavitygaussmode(gaussmode: Union[AxisymmetricCavityHerimiteGaussMode, SymmetricAxisymmetricCavityHerimiteGaussMode], unit='m'):
    """
    绘制腔内高斯模式
    :param gaussmode: 腔内高斯模式
    :param unit: 单位
    :return: (fig, ax) tuple of matplotlib figure and axe.
    """
    Prop = namedtuple('Prop', ('omega0', 'omegaml', 'omegamr', 'z0', 'zl', 'zr', 'ROCl', 'ROCr'))
    val = Prop(**{p: getattr(gaussmode, p) / _SCALE[unit] for p in Prop._fields})

    x = np.linspace(-val.zl, val.zr, 100)
    y = val.omega0 * np.sqrt(1 + (x / val.z0) ** 2)

    fig = plt.figure()
    ax = plt.axes()
    ax.vlines(0, -val.omega0, val.omega0)

    ax.plot(x, y)
    ax.plot(x, -y)

    if np.isinf(val.ROCl):
        ax.vlines(-val.zl, -val.omegaml, val.omegaml)
    else:
        t = np.arcsin(val.omegaml / val.zl)
        theta = np.linspace(-t, t, 100)
        y_t = val.ROCl * np.sin(theta)
        x_t = -(val.ROCl * np.cos(theta) + val.zl - val.ROCl)
        ax.plot(x_t, y_t)

    if np.isinf(val.ROCr):
        ax.vlines(val.zr, -val.omegamr, val.omegamr)
    else:
        t = np.arcsin(val.omegamr / val.zr)
        theta = np.linspace(-t, t, 100)
        y_t = val.ROCr * np.sin(theta)
        x_t = val.ROCr * np.cos(theta) + val.zr - val.ROCr
        ax.plot(x_t, y_t)

    try:
        name = gaussmode.name
    except:
        name = gaussmode.__class__.__name__
    ax.set_title(name)

    ax.set_xlabel('腔z方向/%s' % unit)
    ax.set_ylabel('束腰大小/%s' % unit)

    return fig, ax


def calculate_eta_trans(ml, mr, direction='l'):
    """
    计算单个方向光子的等效透过率，为某个方向上膜的透过率/(总损耗+总透过率)
    :param ml: 左边腔膜的(反射率, 透射率, 损耗)元胞
    :param mr: 右边腔膜的(反射率, 透射率, 损耗)元胞
    :param direction: 方向，可为'l'或者'r'
    :return: 单个方向光子的等效透过率
    """
    rl, tl, ll = ml
    rr, tr, lr = mr
    if direction == 'l':
        return tl / (1 - rl + 1 - rr)
    elif direction == 'r':
        return tr / (1 - rl + 1 - rr)
    else:
        raise AttributeError("方向只能为'l'或者'r'.")


def calculate_eta_mode(fiber, gaussmode, direction='l'):
    """
    计算光纤-腔模耦合效率
    """
    omegaf = fiber.omegaf
    try:
        omegam = getattr(gaussmode, 'omegam' + direction)
        ROC = getattr(gaussmode, 'ROC' + direction)
    except AttributeError:
        omegam = gaussmode.omegam
        ROC = gaussmode.ROC
    nf = fiber.nf
    wavelength = gaussmode.wavelength
    if np.isinf(ROC):
        return 4 / ((omegam / omegaf + omegaf / omegam) ** 2)
    else:
        return 4 / ((omegam / omegaf + omegaf / omegam) ** 2 + (
                    constants.pi * nf * omegam * omegaf / (wavelength * ROC)))


def calculate_fpcavity_total_efficiency(L, surL, fiberL, surR, fiberR, wavelength, gamma, direction='l'):
    """
    计算光纤腔系统总效率
    :param L: 腔长
    :param surL: 左边腔参数(ROC, D, R, T2L, sigmasc)分别为(曲率半径, 有效直径, 反射率, 透射损耗比, 端面粗糙度)
    :param fiberL: 左边光纤参数(nf, omegaf)分别为(折射率, 模场半径)
    :param surR: 右边腔参数(ROC, D, R, T2L, sigmasc)分别为(曲率半径, 有效直径, 反射率, 透射损耗比, 端面粗糙度)
    :param fiberR: 右边光纤参数(nf, omegaf)分别为(折射率, 模场半径)
    :param wavelength: 波长
    :param gamma: 对应波段总自发辐射速率
    :param direction: 光子的输出方向，默认为'l'。 可为'l', 'r'分别代表左端和右端。
    :return: 某个方向上输出光子效率。如果计算失败，则返回-1。
    """
    import numpy as np
    from cavag.fiber import Fiber
    from cavag.fpcavity import (CavityGaussMode, Cavity, judge_stable_cavity,
            calculate_loss_clipping, calculate_loss_scattering, calculate_g,
            calculate_eta_ext, calculate_eta_e, calculate_C1,
            calculate_eta_mode, calculate_eta_trans)
    from cavag.mirror import RTLConverter

    ROCl, Dl, Rl0, T2L0l, sigmascl = surL
    ROCr, Dr, Rr0, T2L0r, sigmascr = surR

    # 计算腔面R T L
    Rl0, Tl0, Ll0 = RTLConverter.rtl_by_r_t2l(Rl0, T2L0l)
    Rr0, Tr0, Lr0 = RTLConverter.rtl_by_r_t2l(Rr0, T2L0r)

    # 光纤类型
    fiberl = Fiber(nf=fiberL[0], omegaf=fiberL[1], wavelength=wavelength)
    fiberr = Fiber(nf=fiberR[0], omegaf=fiberR[1], wavelength=wavelength)

    # 腔模
    gaussmode0 = CavityGaussMode(ROCl=ROCl, ROCr=ROCr, L=L, wavelength=wavelength)
    if not gaussmode0.isStable():
        return -1

    # 计算clipping loss和scattering loss
    Lcll = calculate_loss_clipping(Dl, gaussmode0.omegaml)
    Lclr = calculate_loss_clipping(Dr, gaussmode0.omegamr)
    Lscl = calculate_loss_scattering(sigmascl, wavelength)
    Lscr = calculate_loss_scattering(sigmascr, wavelength)

    # 将上述损耗加在腔面上
    Rl, Tl, Ll = RTLConverter.add_loss((Rl0, Tl0, Ll0), Lcll+Lscl)
    Rr, Tr, Lr = RTLConverter.add_loss((Rr0, Tr0, Lr0), Lclr+Lscr)

    # 计算腔和腔模
    cavity = Cavity(ROCl=ROCl, ROCr=ROCr, L=L, Rl=Rl, Rr=Rr)
    gaussmode = CavityGaussMode(ROCl=ROCl, ROCr=ROCr, L=L, wavelength=wavelength)
    if not gaussmode.isStable():
        return -1

    # 计算相应的因子，并获得总效率
    g = calculate_g(gaussmode, gamma)
    kappa = cavity.kappa
    C1 = calculate_C1(g, kappa, gamma)
    eta_e = calculate_eta_e(C1)
    eta_ext = calculate_eta_ext(kappa, gamma)

    eta_mode_l, eta_mode_r = calculate_eta_mode(fiberl, gaussmode, 'l'), calculate_eta_mode(fiberr, gaussmode, 'r')
    eta_trans_l, eta_trans_r = calculate_eta_trans((Rl, Tl, Ll), (Rr, Tr, Lr), 'l'), calculate_eta_trans((Rl, Tl, Ll), (Rr, Tr, Lr), 'r')
    eta_modetrans_l = eta_mode_l * (1 - eta_mode_r) * eta_trans_l
    eta_modetrans_r = eta_mode_r * (1 - eta_mode_l) * eta_trans_r
    if direction == 'l':
        eta_modetrans_eff = eta_modetrans_l
    elif direction == 'r':
        eta_modetrans_eff = eta_modetrans_r
    else:
        eta_modetrans_eff = eta_modetrans_l + eta_modetrans_r

    return eta_e * eta_ext * eta_modetrans_eff
