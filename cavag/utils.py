
__all__ = [
    'calculate_fpcavity_total_efficiency'
]

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
    from cavag.mirror import calculate_rtl, add_loss

    ROCl, Dl, Rl0, T2L0l, sigmascl = surL
    ROCr, Dr, Rr0, T2L0r, sigmascr = surR

    # 计算腔面R T L
    Rl0, Tl0, Ll0 = calculate_rtl(Rl0, T2L0l)
    Rr0, Tr0, Lr0 = calculate_rtl(Rr0, T2L0r)

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
    Rl, Tl, Ll = add_loss((Rl0, Tl0, Ll0), Lcll+Lscl)
    Rr, Tr, Lr = add_loss((Rr0, Tr0, Lr0), Lclr+Lscr)

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
