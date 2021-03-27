import numpy as np
from scipy import constants

from ._utils import PrintableObject
from .gaussbeam import AxisymmetricHermiteGaussBeam
from .misc import RTL

__all__ = [
    'AxisymmetricCavityStructure', 'SymmetricAxisymmetricCavityStructure',
    'AxisymmetricCavity', 'SymmetricAxisymmetricCavity',
    'AxisymmetricCavityHerimiteGaussMode', 'SymmetricAxisymmetricCavityHerimiteGaussMode',
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
        return kwargs

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


class SymmetricAxisymmetricCavity(SymmetricAxisymmetricCavityStructure, AxisymmetricCavity):
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


def judge_cavity_type(length, rocl, rocr):
    """
    判断腔是否满足稳定条件，且判断是否为临界腔。注意临界腔虽然满足稳定条件，但是否稳定需要
    看具体结构。
    :param length: 腔长
    :param rocl: 左边腔镜ROC
    :param rocr: 右边腔镜ROC
    :return: (r1, r2)   r1: True-腔满足稳定条件，False-腔不满足稳定条件;
                        r2: True-临界腔，False-非临界腔
    """
    r1 = False
    r2 = False

    glgr = (1-length/rocl)*(1-length/rocr)
    if glgr >= 0 and glgr <= 1:
        r1 = True
        if glgr == 0 or glgr == 1:
            r2 = True

    return r1, r2


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


def calculate_g(v, nu, gamma):
    """
    计算腔模-离子耦合系数g因子
    :param v: 高斯驻波场模式体积
    :param nu: 光频率 = 光速/波长
    :param gamma: 驻波场对应频率跃迁的真空自发辐射速率
    :return: 耦合系数g
    """
    return np.sqrt((3*gamma*constants.pi*constants.c**3)/(2*v*(2*np.pi*nu)**2))


def calculate_C1(g, kappa, gamma):
    """
    计算单原子耦合系数
    :param g: 耦合系数
    :param kappa: 腔泄漏损耗
    :param gamma: 总自发辐射速率
    :return: 耦合因子
    """
    return g**2/(kappa*gamma)


def calculate_neta_e(C1):
    """
    计算单原子发射几率
    :param C1: 耦合因子
    :return: 光子发射几率
    """
    return 2*C1/(2*C1+1)


def calculate_neta_ext(kappa, gamma):
    """
    计算腔耦合光子提取几率
    :param kappa: 腔泄露损耗
    :param gamma: 总自发辐射速率
    return: 腔耦合提取几率
    """
    return 2*kappa/(2*kappa+gamma)

