from collections import namedtuple

import numpy as np
import matplotlib.pyplot as plt
from scipy import constants

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

from typing import Union
from ._utils import PrintableObject
from .gaussbeam import AxisymmetricHermiteGaussBeam
from .misc import RTL

__all__ = [
    'AxisymmetricCavityStructure', 'SymmetricAxisymmetricCavityStructure',
    'AxisymmetricCavity', 'SymmetricAxisymmetricCavity',
    'AxisymmetricCavityHerimiteGaussMode', 'SymmetricAxisymmetricCavityHerimiteGaussMode'
    'judge_stable_cavity',
    'calculate_loss_clipping', 'calculate_loss_scattering',
    'calculate_g', 'calculate_C1', 'calculate_neta_e',
    'calculate_neta_ext', 'calculate_neta_mode', 'calculate_neta_trans',
    'plot_cavitygaussmode'
]


class AxisymmetricCavityStructure(PrintableObject):
    name = "AxisymmetricCavityStructure"

    modifiable_properties = ('length', 'rocl', 'rocr')

    def __init__(self, name="AxisymmetricCavityStructure", **kwargs):
        super().__init__(**kwargs)
        self.name = name
        
        self.property_set.add_required(AxisymmetricCavityStructure.modifiable_properties)
    
    @property
    def length(self):
        """腔长"""
        return self.get_property('length')
    
    @property
    def rocl(self):
        """左腔镜曲率半径"""
        return self.get_property('rocl')
    
    @property
    def rocr(self):
        """右腔镜曲率半径"""
        return self.get_property('rocr')
    
    @property
    def gl(self):
        """左腔镜g因子"""
        return self.get_property('gl', lambda: 1-self.length/self.rocl)

    @property
    def gr(self):
        """右腔镜g因子"""
        return self.get_property('gr', lambda: 1-self.length/self.rocr)


class SymmetricAxisymmetricCavityStructure(AxisymmetricCavityStructure):
    name = "SymmetricAxisymmetricCavityStructure"

    modifiable_properties = ('length', 'roc')

    def __init__(self, name="SymmetricAxisymmetricCavityStructure", **kwargs):
        roc = kwargs.get(roc, None)
        kwargs.update(rocl=roc, rocr=roc)

        super().__init__(**kwargs)
        self.name = name
        
        self.property_set.add_required(SymmetricAxisymmetricCavityStructure.modifiable_properties)
        self.property_set['roc'] = roc
    
    def change_params(self, **kwargs):
        roc = kwargs.get(roc, None)
        if roc is not None:
            kwargs.update(rocl=roc, rocr=roc)
            self.update_propset(roc=roc)

        super().change_params(**kwargs)

    @property
    def roc(self):
        """对称腔曲率半径"""
        return self.get_property('roc')
    
    @property
    def g(self):
        """腔镜g因子"""
        return self.get_property('g', lambda: 1-self.length/self.roc)


class AxisymmetricCavity(AxisymmetricCavityStructure):
    name = "AxisymmetricCavity"

    modifiable_properties = ('length', 'rocl', 'rocr', 'rl', 'tl', 'll', 'rr', 'tr', 'lr')

    def __init__(self, name="AxisymmetricCavity", **kwargs):
        super().__init__(**kwargs)
        self.name = name

        self.property_set.add_required(AxisymmetricCavity.modifiable_properties)

        __kwarg_rtls = [{}, {}]
        for prop in AxisymmetricCavity.modifiable_properties:
            val = kwargs.get(prop, None)
            self.property_set[prop] = val
            if prop.endswith('l'):
                __kwarg_rtls[0][prop] = val
            elif prop.endswith('r'):
                __kwarg_rtls[1][prop] = val
            else:
                __kwarg_rtls[0][prop] = __kwarg_rtls[1][prop] = val

        self.__rtls = (RTL(name='left_rtl', **(__kwarg_rtls[0])),
                        RTL(name='right_rtl', **(__kwarg_rtls[1])))

    def change_params(self, _filter=True, **kwargs):
        super().change_params(_filter=_filter, **kwargs)

        if _filter:
            kwargs = self.filter_properties(kwargs)
        
        self.update_propset(**kwargs)

        lkw, rkw = {}, {}
        for k, v in kwargs.items():
            if k.endswith('l'):
                lkw[k[:-1]] = v
            elif k.endswith('r'):
                rkw[k[:-1]] = v
            else:
                lkw[k] = rkw[k] = v
            
        if lkw:
            self.__rtls[0].change_params(**lkw)
        if rkw:
            self.__rtls[1].change_params(**rkw)        

    @property
    def rl(self):
        """左腔镜反射率"""
        return self.get_property('rl', lambda: self.__rtls[0].r)

    @property
    def tl(self):
        """左腔镜透射率"""
        return self.get_property('tl', lambda: self.__rtls[0].t)
    
    @property
    def ll(self):
        """左腔镜损耗"""
        return self.get_property('ll', lambda: self.__rtls[0].l)

    @property
    def rr(self):
        """右腔镜反射率"""
        return self.get_property('rr', lambda: self.__rtls[1].r)

    @property
    def tr(self):
        """右腔镜透射率"""
        return self.get_property('tr', lambda: self.__rtls[1].t)
    
    @property
    def lr(self):
        """右腔镜损耗"""
        return self.get_property('lr', lambda: self.__rtls[1].l)

    @property
    def kappa(self):
        """半波半宽(圆频率)"""
        return self.get_property('kappa', lambda: constants.c*(2-self.rr-self.rl)/(4*self.length))
    
    @property
    def fsr(self):
        """FSR(圆频率)"""
        return self.get_property('fsr', lambda: 2*constants.pi*constants.c/(2*self.length))

    @property
    def finesse(self):
        """精细度"""
        return self.get_property('finesse', lambda: self.fsr/(2*self.kappa))

    def isStable(self):
        return judge_stable_cavity(self.length, self.rocl, self.rocr)


class SymmetricAxisymmetricCavity(AxisymmetricCavity, SymmetricAxisymmetricCavityStructure):
    name = "SymmetricAxisymmetricCavity"

    modifiable_properties = ('length', 'roc', 'rl', 'tl', 'll', 'rr', 'tr', 'lr')

    def __init__(self, name="SymmetricAxisymmetricCavity", **kwargs):
        roc = kwargs.get('roc', None)
        kwargs.update(rocl=roc, rocr=roc)

        super().__init__(**kwargs)
        self.name = name

        self.property_set['roc'] = roc


class AxisymmetricCavityHerimiteGaussMode(AxisymmetricCavityStructure, AxisymmetricHermiteGaussBeam):
    name = 'AxisymmetricCavityHerimiteGaussMode'

    modifiable_properties = ('length', 'wavelength', 'rocl', 'rocr', 'A0', 'm')
    

    def __init__(self, name="AxisymmetricCavityHerimiteGaussMode", **kwargs):
        kwargs.update(A0=kwargs.get('A0', 1))

        super().__init__(**kwargs)
        self.name = name

    @property
    def z0(self):
        """瑞利长度"""
        def v_f():
            gl = self.gl
            gr = self.gr
            glgr = self.gl*self.gr
            try:
                z0 = np.sqrt(glgr*(1-glgr)/(gl+gr-2*glgr)** 2)*self.length
            except ZeroDivisionError:
                z0 = 1/2*self.length
            return z0
        return self.get_property('z0', v_f)

    @property
    def pl(self):
        """左腔镜相对束腰位置"""
        def v_f():
            gl = self.gl
            gr = self.gr
            glgr = self.gl*self.gr
            try:
                pl = gr*(1-gl)/(gl+gr-2*glgr)*self.length
            except ZeroDivisionError:
                pl = self.length/2
            return pl
        return self.get_property('pl', v_f)

    @property
    def pr(self):
        """右腔镜相对束腰位置"""
        def v_f():
            gl = self.gl
            gr = self.gr
            glgr = self.gl*self.gr
            try:
                zprr = gl*(1-gr)/(gl+gr-2*glgr)*self.length
            except ZeroDivisionError:
                pr = self.length/2
            return pr
        return self.get_property('pr', v_f)
    
    @property
    def p0(self):
        """束腰位置"""
        return self.get_property('p0', lambda: (self.pl-self.pr)/2)

    @property
    def omega0(self):
        """束腰半径"""
        return self.get_property('omega0', lambda: np.sqrt(self.wavelength*self.z0/constants.pi))

    @property
    def omegaml(self):
        """左腔面模场半径"""
        return self.get_property('omegaml', lambda: self.omega0*np.sqrt(1+(self.pl/self.z0)**2))

    @property
    def omegamr(self):
        """右腔面模场半径"""
        return self.get_property('omegamr', lambda: self.omega0*np.sqrt(1+(self.pr/self.z0)**2))

    # 模式体积(小NA近似)
    @property
    def v(self):
        """模式体积"""
        return self.get_property('v', lambda: self.length*(self.omega0)**2*constants.pi/4)

    @property
    def e(self):
        """单光子电场强度"""
        return self.get_property('e', np.sqrt(constants.h*self.nu/(2*constants.epsilon_0*self.v)))


class SymmetricAxisymmetricCavityHerimiteGaussMode(SymmetricAxisymmetricCavityStructure, AxisymmetricCavityHerimiteGaussMode):
    name = "SymmetricAxisymmetricCavityHerimiteGaussMode"

    modifiable_properties = ('length', 'wavelength', 'roc', 'A0', 'm')

    def __init__(self, name="SymmetricAxisymmetricCavityHerimiteGaussMode" ,**kwargs):
        roc = kwargs.get('roc', None)
        kwargs.update(rocl=roc, rocr=roc)

        super().__init__(**kwargs)
        self.name = name

        self.property_set['roc'] = roc

    @property
    def z0(self):
        """瑞利长度"""
        def v_f():
            length = self.length
            roc = self.roc
            return 1/2*np.sqrt(length*(2*roc-length))
        return self.get_property('z0', v_f)

    @property
    def p(self):
        """腔镜相对束腰位置"""
        return self.get_property('p', lambda: self.length/2)

    @property
    def p0(self):
        """束腰位置"""
        return self.get_property('p0', lambda: 0)
    
     @property
    def pl(self):
        """左腔镜相对束腰位置"""
        return self.get_property('pl', lambda: self.p)

    @property
    def pr(self):
        """右腔镜相对束腰位置"""
        return self.get_property('pr', lambda: self.p)

    @property
    def omegam(self):
        """腔面模场半径"""
        return self.get_property('omegam', self.omega0*np.sqrt(1+(self.length/2/ self.z0)**2))


#################################################################################
## TO DO


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
    return np.exp(-2 * (D / 2) ** 2 / omegam ** 2)


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
    return np.sqrt((3 * gamma * np.pi * constants.c ** 3) / (2 * gaussmode.V * (2 * np.pi * gaussmode.nu) ** 2))


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
    if np.isinf(ROC):
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

