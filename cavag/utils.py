
__all__ = [
    'PrintInfoMixin',
    'calculate_total_efficiency'
]

class PrintInfoMixin(object):

    def _parse_property(self, p):
        if p.startswith('_'):
            return False
        elif callable(getattr(self, p)):
            return False
        else:
            return True

    def get_attrs(self):
        attrs = []
        for item in dir(self):
            if item is 'name':
                continue
            if self._parse_property(item):
                attrs.append(item)
        return attrs        

    def __str__(self):
        if getattr(self, 'name', None):
            info = "{}:\n".format(self.name)
        else:
            info = "{}:\n".format(self.__class__.__name__)
        for item in dir(self):
            if item is 'name':
                continue
            if self._parse_property(item):
                num = getattr(self, item)
                doc = getattr(self.__class__, item).__doc__
                if doc is None:
                    doc = ''
                # 格式化输出，中文对齐
                try:
                    info += "    {0:{3}<15}{1:<8} = {2:e}\n".format(str_half2full(doc), item, num, chr(12288))
                except:
                    info += "    {0:{3}<15}{1:<8} = {2:s}\n".format(str_half2full(doc), item, str(num), chr(12288))
        return info

    def __repr__(self):
        return "<class '{}'>".format(self.__class__.__name__)

def str_half2full(ins):
    """把字符串半角转全角"""
    outs = ""
    for c in ins:
        code = ord(c)
        if code < 0x0020 or code > 0x007E:
            outs += c
        else:
            if code == 0x0020:
                code += 0x3000
            else:
                code += 0xFEE0
            outs += chr(code)
    
    return outs

def calculate_total_efficiency(L, surL, fiberL, surR, fiberR, wavelength, gamma, direction='l'):
    """
    计算光纤腔系统总效率
    :param L: 腔长
    :param surL: 左边腔参数(ROC, D, R, T2L, sigmasc)分别为(曲率半径, 有效直径, 反射率, 透射损耗比, 端面粗糙度)
    :param fiberL: 左边光纤参数(nf, omegaf)分别为(折射率, 模场半径)
    :param surR: 右边腔参数(ROC, D, R, T2L, sigmasc)分别为(曲率半径, 有效直径, 反射率, 透射损耗比, 端面粗糙度)
    :param fiberR: 右边光纤参数(nf, omegaf)分别为(折射率, 模场半径)
    :param wavelength: 波长
    :param gamma: 对应波段总自发辐射速率
    :return: 某个方向上输出光子效率。如果计算失败，则返回-1。
    """
    import numpy as np
    from cavag.fiber import Fiber
    from cavag.fpcavity import (CavityGaussMode, Cavity, judge_stable_cavity,
            calculate_loss_clipping, calculate_loss_scattering, calculate_g,
            calculate_neta_ext, calculate_neta_e, calculate_C1,
            calculate_neta_mode, calculate_neta_trans)
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

