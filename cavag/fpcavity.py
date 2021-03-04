from collections import namedtuple

import matplotlib.pyplot as plt
import scipy as sp
from scipy import constants

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

from typing import Union
from ._utils import PrintInfoMixin
from .mirror import MirrorSurface

__all__ = [
    'Cavity', 'SymmetricCavity', 'CavityGaussMode', 'SymmetricCavity',
    'SymmetricCavityGaussMode', 'judge_stable_cavity',
    'calculate_loss_clipping', 'calculate_loss_scattering',
    'calculate_g', 'calculate_C1', 'calculate_neta_e',
    'calculate_neta_ext', 'calculate_neta_mode', 'calculate_neta_trans',
    'plot_cavitygaussmode'
]


class Cavity(PrintInfoMixin):
    name = "Cavity"

    def __init__(self, ROCl, ROCr, L, Rl, Rr, name="Cavity", **kwargs):
        self._property = {
            'mirrorsurface': [],  # 腔镜
            'L': None  # 腔长
        }
        self.name = name
        self._property.update(kwargs)
        self._property['mirrorsurface'] = (MirrorSurface(ROC=ROCl, R=Rl, name='leftmirror'),
                                           MirrorSurface(ROC=ROCr, R=Rr, name='rightmirror'))
        self._property['L'] = L

    def change_params(self, **kwargs):
        pass

    def isStable(self):
        return judge_stable_cavity(self.L, self.ROCl, self.ROCr)

    @classmethod
    def create_symmetric_cavity(cls, ROC, L, Rl, Rr, name=None, **kwargs):
        if not name:
            name = 'SymmetricCavity'
        return cls(ROC, ROC, L, Rl, Rr, name, **kwargs)

    @property
    def Rl(self):
        """左腔镜反射率"""
        return self._property['mirrorsurface'][0].R

    @property
    def Rr(self):
        """右腔镜反射率"""
        return self._property['mirrorsurface'][1].R

    @property
    def L(self):
        """腔长"""
        return self._property['L']

    @property
    def ROCl(self):
        """左腔镜曲率半径"""
        return self._property['mirrorsurface'][0].ROC

    @property
    def ROCr(self):
        """右腔镜曲率半径"""
        return self._property['mirrorsurface'][1].ROC

    @property
    def gl(self):
        """左腔镜g因子"""
        return 1 - self.L / self.ROCl

    @property
    def gr(self):
        """右腔镜g因子"""
        return 1 - self.L / self.ROCr

    @property
    def kappa(self):
        """半波半宽(圆频率)"""
        return constants.c * (2 - self.Rr - self.Rl) / (4 * self.L)

    @property
    def FSR(self):
        """FSR(圆频率)"""
        return 2 * constants.pi * constants.c / (2 * self.L)

    @property
    def finesse(self):
        """精细度"""
        return self.FSR / (2 * self.kappa)


class SymmetricCavity(Cavity, PrintInfoMixin):

    def __init__(self, ROC, L, Rr, Rl, *args, **kwargs):
        super().__init__(ROC, ROC, L, Rr, Rl, *args, **kwargs)

    @property
    def ROC(self):
        """对称腔曲率半径"""
        return self.ROCl

    @property
    def g(self):
        """对称腔g因子"""
        return self.gl


# 高斯模式
class CavityGaussMode(PrintInfoMixin):
    name = 'CavityGaussMode'

    def __init__(self, ROCl, ROCr, L, wavelength, name="CavityGaussMode", **kwargs):
        self._property = {
            'mirrorsurface': [],  # 腔镜
            'L': None,
            'wavelength': None
        }
        self.name = name
        self._property['mirrorsurface'] = (MirrorSurface(ROC=ROCl, R=None, name='leftmirror'),
                                           MirrorSurface(ROC=ROCr, R=None, name='rightmirror'))
        self._property['L'] = L
        self._property['wavelength'] = wavelength
        self._property.update(kwargs)

    def change_params(self, **kwargs):
        pass

    def isStable(self):
        return judge_stable_cavity(self.L, self.ROCl, self.ROCr)

    def isValid(self):
        return self.isStable()

    @classmethod
    def create_symmetric_cavity(cls, ROC, L, wavelength, name=None, **kwargs):
        if not name:
            name = 'SymmetricCavityGaussMode'
        return cls(ROC, ROC, L, wavelength, name, **kwargs)

    @property
    def ROCr(self):
        """右腔镜曲率半径"""
        return self._property['mirrorsurface'][1].ROC

    @property
    def ROCl(self):
        """左腔镜曲率半径"""
        return self._property['mirrorsurface'][0].ROC

    @property
    def L(self):
        """腔长"""
        return self._property['L']

    @property
    def wavelength(self):
        """中心波长"""
        return self._property['wavelength']

    @property
    def gl(self):
        """左腔镜g因子"""
        return 1 - self.L / self.ROCl

    @property
    def gr(self):
        """右腔镜g因子"""
        return 1 - self.L / self.ROCr

    @property
    def z0(self):
        """瑞利长度"""
        gl = self.gl
        gr = self.gr
        glgr = self.gl * self.gr
        try:
            z0 = sp.sqrt(glgr * (1 - glgr) / (gl + gr - 2 * glgr) ** 2) * self.L
        except ZeroDivisionError:
            z0 = 1 / 2 * self.L
        return z0

    @property
    def zl(self):
        """左腔镜相对束腰位置"""
        gl = self.gl
        gr = self.gr
        glgr = self.gl * self.gr
        try:
            zl = gr * (1 - gl) / (gl + gr - 2 * glgr) * self.L
        except ZeroDivisionError:
            zl = self.L / 2
        return zl

    @property
    def zr(self):
        """右腔镜相对束腰位置"""
        gl = self.gl
        gr = self.gr
        glgr = self.gl * self.gr
        try:
            zr = gl * (1 - gr) / (gl + gr - 2 * glgr) * self.L
        except ZeroDivisionError:
            zr = self.L / 2
        return zr

    @property
    def omega0(self):
        """束腰半径"""
        return sp.sqrt(self.wavelength * self.z0 / sp.pi)

    @property
    def omegaml(self):
        """左腔面模场半径"""
        return self.omega0 * sp.sqrt(1 + (self.zl / self.z0) ** 2)

    @property
    def omegamr(self):
        """右腔面模场半径"""
        return self.omega0 * sp.sqrt(1 + (self.zr / self.z0) ** 2)

    # 模式体积(小NA近似)
    @property
    def V(self):
        """模式体积"""
        return self.L * (self.omega0) ** 2 * sp.pi / 4

    @property
    def nu(self):
        """中心频率"""
        return constants.c / self.wavelength

    @property
    def e(self):
        """单光子电场强度"""
        return sp.sqrt(constants.h * self.nu / (2 * constants.epsilon_0 * self.V))


# 对称腔Gauss模式
class SymmetricCavityGaussMode(CavityGaussMode, PrintInfoMixin):

    def __init__(self, ROC, L, wavelength, *args, **kwargs):
        super().__init__(ROC, ROC, L, wavelength, **kwargs)

    @property
    def ROC(self):
        """曲率半径"""
        return self.ROCl

    @property
    def z0(self):
        """瑞利长度"""
        L = self.L
        ROC = self.ROC
        return 1 / 2 * sp.sqrt(L * (2 * ROC - L))

    @property
    def z(self):
        """腔镜相对束腰位置"""
        return self.L / 2

    @property
    def omegam(self):
        """腔面模场半径"""
        L = self.L
        return self.omega0 * sp.sqrt(1 + (L / 2 / self.z0) ** 2)


def judge_stable_cavity(L, ROCl, ROCr):
    """
    判断腔是否稳定
    :param L: 腔长
    :param ROCl: 左边腔镜ROC
    :param ROCr: 右边腔镜ROC
    :return: True-腔稳定，False-腔不稳定
    """
    glgr = (1 - L / ROCl)*(1 - L / ROCr)
    if glgr >=0 and glgr<=1:
        return True
    else:
        return False


def calculate_loss_clipping(D, omegam):
    """
    计算腔面单次反射的clipping损耗
    :param D: 腔面有效直径
    :param omegam: 模场半径
    :return: clipping损耗
    """
    return sp.exp(-2 * (D / 2) ** 2 / omegam ** 2)


def calculate_loss_scattering(sigmasc, wavelength):
    """
    计算腔面的散射损耗
    :param sigmasc: 腔面的粗糙度，通常为0.2nm左右
    :param wavelength: 光波波长
    :return: 腔面的散射损耗
    """
    return (4 * constants.pi * sigmasc / wavelength) ** 2


def calculate_g(gaussmode, gamma):
    """
    计算腔模-离子耦合效率
    :param gaussmode: 高斯驻波场
    :param gamma: 驻波场对应频率跃迁的真空自发辐射速率
    :return: 耦合系数g
    """
    return sp.sqrt((3 * gamma * sp.pi * constants.c ** 3) / (2 * gaussmode.V * (2 * sp.pi * gaussmode.nu) ** 2))


def calculate_C1(g, kappa, gamma):
    """
    计算单原子耦合系数
    :param g: 耦合系数
    :param kappa: 腔泄漏损耗
    :param gamma: 总自发辐射速率
    :return: 耦合因子
    """
    return g ** 2 / (kappa * gamma)


def calculate_neta_e(C1):
    """
    计算单原子发射几率
    :param C1: 耦合因子
    :return: 光子发射几率
    """
    return 2 * C1 / (2 * C1 + 1)


def calculate_neta_ext(kappa, gamma):
    """
    计算腔耦合光子提取几率
    :param kappa: 腔泄露损耗
    :param gamma: 总自发辐射速率
    return: 腔耦合提取几率
    """
    return 2 * kappa / (2 * kappa + gamma)


def calculate_neta_mode(fiber, gaussmode, direction='l'):
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
    if sp.isinf(ROC):
        return 4 / ((omegam / omegaf + omegaf / omegam) ** 2)
    else:
        return 4 / ((omegam / omegaf + omegaf / omegam) ** 2 + (
                    constants.pi * nf * omegam * omegaf / (wavelength * ROC)))


def calculate_neta_trans(ml, mr, direction='l'):
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


_SCALE = {
    'nm': 1e-9,
    'um': 1e-6,
    'mm': 1e-3,
    'm': 1,
}


def plot_cavitygaussmode(gaussmode: Union[CavityGaussMode, SymmetricCavityGaussMode], unit='m'):
    """
    绘制腔内高斯模式
    :param gaussmode: 腔内高斯模式
    :param unit: 单位
    :return: ax: matplotlib axes
    """
    Prop = namedtuple('Prop', ('omega0', 'omegaml', 'omegamr', 'z0', 'zl', 'zr', 'ROCl', 'ROCr'))
    val = Prop(**{p: getattr(gaussmode, p) / _SCALE[unit] for p in Prop._fields})

    x = sp.linspace(-val.zl, val.zr, 100)
    y = val.omega0 * sp.sqrt(1 + (x / val.z0) ** 2)

    plt.figure()
    ax = plt.axes()
    ax.vlines(0, -val.omega0, val.omega0)

    ax.plot(x, y)
    ax.plot(x, -y)

    if sp.isinf(val.ROCl):
        ax.vlines(-val.zl, -val.omegaml, val.omegaml)
    else:
        t = sp.arcsin(val.omegaml / val.zl)
        theta = sp.linspace(-t, t, 100)
        y_t = val.ROCl * sp.sin(theta)
        x_t = -(val.ROCl * sp.cos(theta) + val.zl - val.ROCl)
        ax.plot(x_t, y_t)

    if sp.isinf(val.ROCr):
        ax.vlines(val.zr, -val.omegamr, val.omegamr)
    else:
        t = sp.arcsin(val.omegamr / val.zr)
        theta = sp.linspace(-t, t, 100)
        y_t = val.ROCr * sp.sin(theta)
        x_t = val.ROCr * sp.cos(theta) + val.zr - val.ROCr
        ax.plot(x_t, y_t)

    try:
        name = gaussmode.name
    except:
        name = gaussmode.__class__.__name__
    ax.set_title(name)

    ax.set_xlabel('腔z方向/%s' % unit)
    ax.set_ylabel('束腰大小/%s' % unit)

    return ax

