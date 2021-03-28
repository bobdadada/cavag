import logging

import numpy as np
from scipy import constants

from ._utils import PrintableObject
from .gaussbeam import AxisymmetricGaussBeam
from .misc import RTL, Position

__all__ = [
    'AxisymmetricCavityStructure', 'SymmetricAxisymmetricCavityStructure',
    'AxisymmetricCavity', 'SymmetricAxisymmetricCavity',
    'AxisymmetricCavityGaussMode', 'SymmetricAxisymmetricCavityGaussMode',
    'judge_cavity_type',
    'calculate_loss_clipping', 'calculate_loss_scattering',
    'calculate_g', 'calculate_C1', 'calculate_neta_e',
    'calculate_neta_ext',
]


class AxisymmetricCavityStructure(PrintableObject):
    name = "AxisymmetricCavityStructure"

    modifiable_properties = ('length', 'rocl', 'rocr')

    def __init__(self, name="AxisymmetricCavityStructure", **kwargs):
        super().__init__(**kwargs)
        self.name = name
        
        self.property_set.add_required(AxisymmetricCavityStructure.modifiable_properties)
        
        for prop in AxisymmetricCavityStructure.modifiable_properties:
            self.property_set[prop] = kwargs.get(prop, None)

    @property
    def length(self):
        """腔长[L]"""
        return self.get_property('length')
    
    @property
    def rocl(self):
        """左腔镜曲率半径[L]"""
        return self.get_property('rocl')
    
    @property
    def rocr(self):
        """右腔镜曲率半径[L]"""
        return self.get_property('rocr')
    
    @property
    def gl(self):
        """左腔镜g因子[1]"""
        return self.get_property('gl', lambda: 1-self.length/self.rocl)

    @property
    def gr(self):
        """右腔镜g因子[1]"""
        return self.get_property('gr', lambda: 1-self.length/self.rocr)
    
    def isStable(self):
        r1, r2 = judge_cavity_type(self.length, self.rocl, self.rocr)
        if r1 is True:
            if r2 is False:
                return True
            else:
                return None
        else:
            return False

    def isCritical(self):
        return judge_cavity_type(self.length, self.rocl, self.rocr)[1]


class SymmetricAxisymmetricCavityStructure(AxisymmetricCavityStructure):
    name = "SymmetricAxisymmetricCavityStructure"

    modifiable_properties = ('length', 'roc')

    def __init__(self, name="SymmetricAxisymmetricCavityStructure", **kwargs):
        roc = kwargs.get('roc', None)
        kwargs.update(rocl=roc, rocr=roc)

        super().__init__(**kwargs)
        self.name = name
        
        self.property_set.add_required(SymmetricAxisymmetricCavityStructure.modifiable_properties)
        self.property_set['roc'] = roc
    
    def preprocess_properties(self, **propdict):
        roc = propdict.get('roc', None)
        if roc is not None:
            propdict.update(rocl=roc, rocr=roc)
        return propdict

    @property
    def roc(self):
        """对称腔曲率半径[L]"""
        return self.get_property('roc')
    
    @property
    def g(self):
        """腔镜g因子[1]"""
        return self.get_property('g', lambda: 1-self.length/self.roc)


class AxisymmetricCavity(AxisymmetricCavityStructure):
    name = "AxisymmetricCavity"

    modifiable_properties = ('length', 'nc', 'lc', 'rocl', 'rocr', 'rl', 'tl', 'll', 'rr', 'tr', 'lr')

    def __init__(self, name="AxisymmetricCavity", **kwargs):
        kwargs.update(nc=kwargs.get('nc', 1))  # default air medium 
        kwargs.update(lc=kwargs.get('lc', 0))

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

    def postprocess_properties(self, **kwargs):

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
    def nc(self):
        """腔介质的折射率[1]"""
        return self.get_property('nc')

    @property
    def lc(self):
        """腔有效单程损耗"""
        return self.get_property('lc')

    @property
    def rl(self):
        """左腔镜反射率[1]"""
        return self.get_property('rl', lambda: self.__rtls[0].r)

    @property
    def tl(self):
        """左腔镜透射率[1]"""
        return self.get_property('tl', lambda: self.__rtls[0].t)
    
    @property
    def ll(self):
        """左腔镜损耗[1]"""
        return self.get_property('ll', lambda: self.__rtls[0].l)

    @property
    def rr(self):
        """右腔镜反射率[1]"""
        return self.get_property('rr', lambda: self.__rtls[1].r)

    @property
    def tr(self):
        """右腔镜透射率[1]"""
        return self.get_property('tr', lambda: self.__rtls[1].t)
    
    @property
    def lr(self):
        """右腔镜损耗[1]"""
        return self.get_property('lr', lambda: self.__rtls[1].l)

    @property
    def kappa(self):
        """半波半宽(圆频率)[1/T]"""
        def v_f():
            if np.sqrt(self.rl*self.rr) < 0.9 or (self.lc > 0.01):
                logging.warning("The reflectivity of the cavity mirror is too low, or the loss of cavity is too high, "
                                "so the deviation of the `kappa` calculated by this approximate formula is large.")
            return constants.c*(2-(1-self.lc)*(self.rl+self.rr))/(4*self.length)
        return self.get_property('kappa', v_f)
    
    @property
    def fsr(self):
        """FSR(圆频率)[1/T]"""
        return self.get_property('fsr', lambda: 2*constants.pi*constants.c/(2*self.length))

    @property
    def finesse(self):
        """精细度[1]"""
        return self.get_property('finesse', lambda: self.fsr/(2*self.kappa))
    
    @property
    def Q(self):
        """品质因子[1]"""
        return self.get_property('Q', lambda: constants.pi*self.nu/(self.kappa))


class SymmetricAxisymmetricCavity(SymmetricAxisymmetricCavityStructure, AxisymmetricCavity):
    name = "SymmetricAxisymmetricCavity"

    modifiable_properties = ('length', 'nc', 'lc', 'roc', 'rl', 'tl', 'll', 'rr', 'tr', 'lr')

    def __init__(self, name="SymmetricAxisymmetricCavity", **kwargs):
        roc = kwargs.get('roc', None)
        kwargs.update(rocl=roc, rocr=roc)

        super().__init__(**kwargs)
        self.name = name

        self.property_set['roc'] = roc


class AxisymmetricCavityGaussMode(AxisymmetricCavityStructure, AxisymmetricGaussBeam, Position):
    name = 'AxisymmetricCavityGaussMode'

    modifiable_properties = ('length', 'wavelength', 'rocl', 'rocr', 'A0', 'position')

    def __init__(self, name="AxisymmetricCavityGaussMode", **kwargs):
        kwargs.update(A0=kwargs.get('A0', 1))

        super().__init__(**kwargs)
        self.name = name

    @property
    def z0(self):
        """瑞利长度[L]"""
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
        """左腔镜相对束腰位置[L]"""
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
        """右腔镜相对束腰位置[L]"""
        def v_f():
            gl = self.gl
            gr = self.gr
            glgr = self.gl*self.gr
            try:
                pr = gl*(1-gr)/(gl+gr-2*glgr)*self.length
            except ZeroDivisionError:
                pr = self.length/2
            return pr
        return self.get_property('pr', v_f)
    
    @property
    def p0(self):
        """束腰位置[L]"""
        return self.get_property('p0', lambda: (self.pl-self.pr)/2+self.position)

    @property
    def omega0(self):
        """束腰半径[L]"""
        return self.get_property('omega0', lambda: np.sqrt(self.wavelength*self.z0/constants.pi))

    @property
    def omegaml(self):
        """左腔面模场半径[L]"""
        return self.get_property('omegaml', lambda: self.omega0*np.sqrt(1+(self.pl/self.z0)**2))

    @property
    def omegamr(self):
        """右腔面模场半径[L]"""
        return self.get_property('omegamr', lambda: self.omega0*np.sqrt(1+(self.pr/self.z0)**2))

    # 模式体积(小NA近似)
    @property
    def V_mode(self):
        """模式体积[L^3]"""
        return self.get_property('V_mode', lambda: self.length*(self.omega0)**2*constants.pi/4)

    @property
    def e(self):
        """单光子电场强度[ML/T^3I]"""
        return self.get_property('e', lambda: np.sqrt(constants.h*self.nu/(2*constants.epsilon_0*self.V_mode)))


class SymmetricAxisymmetricCavityGaussMode(SymmetricAxisymmetricCavityStructure, AxisymmetricCavityGaussMode):
    name = "SymmetricAxisymmetricCavityGaussMode"

    modifiable_properties = ('length', 'wavelength', 'roc', 'A0')

    def __init__(self, name="SymmetricAxisymmetricCavityGaussMode" ,**kwargs):
        roc = kwargs.get('roc', None)
        kwargs.update(rocl=roc, rocr=roc)

        super().__init__(**kwargs)
        self.name = name

        self.property_set['roc'] = roc

    @property
    def z0(self):
        """瑞利长度[L]"""
        def v_f():
            length = self.length
            roc = self.roc
            return 1/2*np.sqrt(length*(2*roc-length))
        return self.get_property('z0', v_f)

    @property
    def p(self):
        """腔镜相对束腰位置[L]"""
        return self.get_property('p', lambda: self.length/2)

    @property
    def p0(self):
        """束腰位置[L]"""
        return self.get_property('p0', lambda: self.position)
    
    @property
    def pl(self):
        """左腔镜相对束腰位置[L]"""
        return self.get_property('pl', lambda: self.p)

    @property
    def pr(self):
        """右腔镜相对束腰位置[L]"""
        return self.get_property('pr', lambda: self.p)

    @property
    def omegam(self):
        """腔面模场半径[L]"""
        return self.get_property('omegam', self.omega0*np.sqrt(1+(self.length/2/ self.z0)**2))


def judge_cavity_type(length, rocl, rocr):
    """
    判断腔是否满足稳定条件，且判断是否为临界腔。注意临界腔虽然满足稳定条件，但是否稳定需要
    看具体结构。
    :param length: 腔长
    :param rocl: 左边腔镜ROC
    :param rocr: 右边腔镜ROC
    :return: (stable, critical) stable: True-腔满足稳定条件，False-腔不满足稳定条件;
                                critical: True-临界腔，False-非临界腔
    """
    stable = False
    critical = False

    glgr = (1-length/rocl)*(1-length/rocr)
    if glgr >= 0 and glgr <= 1:
        stable = True
        if glgr == 0 or glgr == 1:
            critical = True

    return stable, critical


def calculate_loss_clipping(d, omegam):
    """
    计算腔面单次反射的clipping损耗
    :param d: 腔面有效直径
    :param omegam: 模场半径
    :return: clipping损耗
    """
    return np.exp(-2*(d/2)**2/omegam**2)


def calculate_loss_scattering(sigmasc, wavelength):
    """
    计算腔面的散射损耗。若计算的损耗大于1，则可认为光被完全散射掉，没有光能原路返回。
    :param sigmasc: 腔面的粗糙度，通常为0.2nm左右
    :param wavelength: 光波波长
    :return: 腔面的散射损耗
    """
    return (4*constants.pi*sigmasc/wavelength)**2


def calculate_g(V_mode, nu, gamma):
    """
    计算腔模-离子耦合系数g因子
    :param V_mode: 高斯驻波场模式体积
    :param nu: 光频率 = 光速/波长
    :param gamma: 驻波场对应频率能级跃迁的真空自发辐射速率
    :return: 耦合系数g
    """
    return np.sqrt((3*gamma*constants.pi*constants.c**3)/(2*V_mode*(2*np.pi*nu)**2))


def calculate_C1(g, kappa, gammat):
    """
    计算单原子耦合系数
    :param g: 耦合系数
    :param kappa: 腔泄漏损耗
    :param gammat: 总自发辐射速率
    :return: 耦合因子
    """
    return g**2/(kappa*gammat)


def calculate_neta_e(C1):
    """
    计算单原子发射几率
    :param C1: 耦合因子
    :return: 光子发射几率
    """
    return 2*C1/(2*C1+1)


def calculate_neta_ext(kappa, gammat):
    """
    计算腔耦合光子提取几率
    :param kappa: 腔泄露损耗
    :param gammat: 总自发辐射速率
    return: 腔耦合提取几率
    """
    return 2*kappa/(2*kappa+gammat)

