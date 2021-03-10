
__all__ = [
    'calculate_fpcavity_total_efficiency',
    'RTLConvertor'
]

class RTLConvertor(object):

    @staticmethod
    def rtl_by_r_t2l(r, t2l):
        """
        计算反射率，透射率，损耗
        :param r: 反射率
        :param t2l: 透射损耗比
        :return: 反射率，透射率，损耗
        """
        t, l = (1-r)*t2l/(t2l+1), (1-r)/(t2l+1)
        return r, t, l
    
    @staticmethod
    def rtl_by_t_r2l(t, r2l):
        """
        计算反射率，透射率，损耗
        :param t: 透射率
        :param r2l: 反射损耗比
        :return: 反射率，透射率，损耗
        """
        r, l = (1-t)*r2l/(r2l+1), (1-t)/(r2l+1)
        return r, t, l

    @staticmethod
    def add_loss(m0, l):
        """
        计算增添损耗后的(反射率，透射率，损耗)
        :param m0: 原始的(反射率，透射率，损耗)
        :param l: 添加的损耗
        :return: 反射率，透射率，损耗
        """
        r0, t0, l0 = m0
        r = r0*(1-l)
        t = t0*(1-l)
        l = l0*(1-l)+l
        return r, t, l

    @staticmethod
    def add_reflectivity(m0, r):
        """
        计算增添反射率后的(反射率，透射率，损耗)
        :param m0: 原始的(反射率，透射率，损耗)
        :param r: 添加的反射率
        :return: 反射率，透射率，损耗
        """
        r0, t0, l0 = m0
        r = r0*(1-r)+r
        t = t0*(1-r)
        l = l0*(1-r)
        return r, t, l

    @staticmethod
    def add_transmittance(m0, t):
        """
        计算增添透射率后的(反射率，透射率，损耗)
        :param m0: 原始的(反射率，透射率，损耗)
        :param t: 添加的透射率
        :return: 反射率，透射率，损耗
        """
        r0, t0, l0 = m0
        r = r0*(1-t)
        t = t0*(1-t)+t
        l = l0*(1-t)
        return r, t, l


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
            calculate_neta_ext, calculate_neta_e, calculate_C1,
            calculate_neta_mode, calculate_neta_trans)

    ROCl, Dl, Rl0, T2L0l, sigmascl = surL
    ROCr, Dr, Rr0, T2L0r, sigmascr = surR

    # 计算腔面R T L
    Rl0, Tl0, Ll0 = RTLConvertor.rtl_by_r_t2l(Rl0, T2L0l)
    Rr0, Tr0, Lr0 = RTLConvertor.rtl_by_r_t2l(Rr0, T2L0r)

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
    Rl, Tl, Ll = RTLConvertor.add_loss((Rl0, Tl0, Ll0), Lcll+Lscl)
    Rr, Tr, Lr = RTLConvertor.add_loss((Rr0, Tr0, Lr0), Lclr+Lscr)

    # 计算腔和腔模
    cavity = Cavity(ROCl=ROCl, ROCr=ROCr, L=L, Rl=Rl, Rr=Rr)
    gaussmode = CavityGaussMode(ROCl=ROCl, ROCr=ROCr, L=L, wavelength=wavelength)
    if not gaussmode.isStable():
        return -1

    # 计算相应的因子，并获得总效率
    g = calculate_g(gaussmode, gamma)
    kappa = cavity.kappa
    C1 = calculate_C1(g, kappa, gamma)
    neta_e = calculate_neta_e(C1)
    neta_ext = calculate_neta_ext(kappa, gamma)

    neta_mode_l, neta_mode_r = calculate_neta_mode(fiberl, gaussmode, 'l'), calculate_neta_mode(fiberr, gaussmode, 'r')
    neta_trans_l, neta_trans_r = calculate_neta_trans((Rl, Tl, Ll), (Rr, Tr, Lr), 'l'), calculate_neta_trans((Rl, Tl, Ll), (Rr, Tr, Lr), 'r')
    neta_modetrans_l = neta_mode_l * (1 - neta_mode_r) * neta_trans_l
    neta_modetrans_r = neta_mode_r * (1 - neta_mode_l) * neta_trans_r
    if direction == 'l':
        neta_modetrans_eff = neta_modetrans_l
    elif direction == 'r':
        neta_modetrans_eff = neta_modetrans_r
    else:
        neta_modetrans_eff = neta_modetrans_l + neta_modetrans_r

    return neta_e * neta_ext * neta_modetrans_eff
