import logging
from re import DOTALL

import numpy as np
from scipy import constants

from ._utils import PrintableObject
from .gaussbeam import EqualHermiteGaussBeam
from .misc import RTL, Position

__all__ = [
    'CavityStructure', 'EqualCavityStructure',
    'Cavity', 'EqualCavity',
    'CavityHermiteGaussMode', 'EqualCavityMode',
    'judge_cavity_type',
    'calculate_loss_clipping', 'calculate_loss_scattering'
]


class CavityStructure(PrintableObject):
    name = "CavityStructure"

    modifiable_properties = ('length', 'rocl', 'rocr')

    def __init__(self, name="CavityStructure", **kwargs):
        super().__init__(**kwargs)
        self.name = name

        self.property_set.add_required(CavityStructure.modifiable_properties)

        for prop in CavityStructure.modifiable_properties:
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


class EqualCavityStructure(CavityStructure):
    name = "EqualCavityStructure"

    modifiable_properties = ('length', 'roc')

    def __init__(self, name="EqualCavityStructure", **kwargs):
        roc = kwargs.get('roc', None)
        kwargs.update(rocl=roc, rocr=roc)

        super().__init__(**kwargs)
        self.name = name

        self.property_set.add_required(
            EqualCavityStructure.modifiable_properties)
        self.property_set['roc'] = roc

    def preprocess_properties(self, **propdict):
        roc = propdict.get('roc', None)
        if roc is not None:
            propdict.update(rocl=roc, rocr=roc)
        return super().preprocess_properties(**propdict)

    @property
    def roc(self):
        """对称腔曲率半径[L]"""
        return self.get_property('roc')

    @property
    def g(self):
        """腔镜g因子[1]"""
        return self.get_property('g', lambda: 1-self.length/self.roc)


class Cavity(CavityStructure):
    name = "Cavity"

    modifiable_properties = ('length', 'nc', 'lc', 'rocl',
                             'rocr', 'rl', 'tl', 'll', 'rr', 'tr', 'lr')

    def __init__(self, name="Cavity", **kwargs):
        kwargs.update(nc=kwargs.get('nc', 1))  # default air medium
        kwargs.update(lc=kwargs.get('lc', 0))

        super().__init__(**kwargs)
        self.name = name

        self.property_set.add_required(Cavity.modifiable_properties)

        __kwarg_rtls = [{}, {}]
        for prop in Cavity.modifiable_properties:
            val = kwargs.get(prop, None)
            self.property_set[prop] = val
            if prop in ('rl', 'tl', 'll'):
                __kwarg_rtls[0][prop[:-1]] = val
            elif prop in ('rr', 'tr', 'lr'):
                __kwarg_rtls[1][prop[:-1]] = val
            else:
                self.property_set[prop] = val

        # rtl cache

        self.__rtls = {
            'l': RTL(**(__kwarg_rtls[0])), 'r': RTL(**(__kwarg_rtls[1]))}

    def __get_rtl(self, d):
        if self.__rtls[d]:
            rtl = self.__rtls[d]
        else:
            rtl = RTL(r=getattr(self, 'r'+d),
                      t=getattr(self, 't'+d), l=getattr(self, 'l'+d))
            self.__rtls[d] = rtl
        return rtl

    def postprocess_properties(self, **propdict):
        propdict = super().postprocess_properties(**propdict)

        lkw, rkw = {}, {}
        for k, v in propdict.items():
            if k in ('rl', 'tl', 'll'):
                lkw[k[:-1]] = v
            elif k in ('rr', 'tr', 'lr'):
                rkw[k[:-1]] = v

        if lkw:
            for k in ('rl', 'tl', 'll'):
                self.property_set[k] = None
            self.__get_rtl('l').change_params(**lkw)
        if rkw:
            for k in ('rr', 'tr', 'lr'):
                self.property_set[k] = None
            self.__get_rtl('r').change_params(**rkw)

        return propdict

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
        return self.get_property('rl', lambda: self.__get_rtl('l').r)

    @property
    def tl(self):
        """左腔镜透射率[1]"""
        return self.get_property('tl', lambda: self.__get_rtl('l').t)

    @property
    def ll(self):
        """左腔镜损耗[1]"""
        return self.get_property('ll', lambda: self.__get_rtl('l').l)

    @property
    def rr(self):
        """右腔镜反射率[1]"""
        return self.get_property('rr', lambda: self.__get_rtl('r').r)

    @property
    def tr(self):
        """右腔镜透射率[1]"""
        return self.get_property('tr', lambda: self.__get_rtl('r').t)

    @property
    def lr(self):
        """右腔镜损耗[1]"""
        return self.get_property('lr', lambda: self.__get_rtl('r').l)

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
    def q(self):
        """品质因子[1]"""
        return self.get_property('q', lambda: constants.pi*self.nu/(self.kappa))


class EqualCavity(EqualCavityStructure, Cavity):
    name = "EqualCavity"

    modifiable_properties = ('length', 'nc', 'lc', 'roc',
                             'rl', 'tl', 'll', 'rr', 'tr', 'lr')

    def __init__(self, name="EqualCavity", **kwargs):
        roc = kwargs.get('roc', None)
        kwargs.update(rocl=roc, rocr=roc)

        super().__init__(**kwargs)
        self.name = name


class CavityHermiteGaussMode(CavityStructure, EqualHermiteGaussBeam, Position):
    name = 'CavityHermiteGaussMode'

    modifiable_properties = ('length', 'wavelength',
                             'rocl', 'rocr', 'a0', 'position', 'mx', 'my', 'xi')

    def __init__(self, name="CavityHermiteGaussMode", **kwargs):
        kwargs.update(a0=kwargs.get('a0', 1))

        super().__init__(**kwargs)
        self.name = name

        self.property_set.reset_required(
            CavityHermiteGaussMode.modifiable_properties)

        self.property_set['psi'] = kwargs.get('psi', 0)

    @property
    def z0(self):
        """瑞利长度[L]"""
        def v_f():
            gl = self.gl
            gr = self.gr
            glgr = self.gl*self.gr
            try:
                z0 = np.sqrt(glgr*(1-glgr)/(gl+gr-2*glgr) ** 2)*self.length
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
        """等价基模束腰半径[L]"""
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
    def v_mode(self):
        """模式体积[L^3]"""
        def v_f():
            if self.mx > 0:
                cx = (6.927*self.mx-2.104)**(1/6)
                logging.warning(
                    "mx > 0, mode volumn is computed by an approximation")
            else:
                cx = 1
            if self.my > 0:
                cy = (6.927*self.my-2.104)**(1/6)
                logging.warning(
                    "my > 0, mode volumn is computed by an approximation")
            else:
                cy = 1
            if (self.pl < 0) or (self.pr < 0):
                logging.warning("The waist is not in the cavity,"
                                "so the calculated mode volume is slightly different.")
            return cx*cy*self.length*(self.omega0)**2*constants.pi/4
        return self.get_property('v_mode', v_f)

    @property
    def e(self):
        """单光子电场强度[ML/T^3I]"""
        return self.get_property('e', lambda: np.sqrt(constants.h*self.nu/(2*constants.epsilon_0*self.v_mode)))

    def u_f(self, z, x, y):
        ampl, phase = super().u_f(z, x, y)
        return ampl, np.cos(phase-self.xi-self.k*z)


class EqualCavityHermiteGaussMode(EqualCavityStructure, CavityHermiteGaussMode):
    name = "EqualCavityHermiteGaussMode"

    modifiable_properties = ('length', 'wavelength',
                             'roc', 'a0', 'position', 'mx', 'my', 'xi')

    def __init__(self, name="EqualCavityHermiteGaussMode", **kwargs):
        roc = kwargs.get('roc', None)
        kwargs.update(rocl=roc, rocr=roc)

        super().__init__(**kwargs)
        self.property_set.add_required('roc')
        self.name = name

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
        return self.get_property('omegam', self.omega0*np.sqrt(1+(self.length/2 / self.z0)**2))


## -------------------------------------------
# TO DO

def get_wavelengthf(length, rocl, rocr, mx, my):
    """
    获取满足腔相位条件的波长函数
    :param length: 腔长
    :param rocl: 左边腔镜ROC
    :param rocR: 右边腔镜ROC
    :param mx: x方向模式数
    :param my: y方向模式数
    :return: func(p) -> wavelength 用于计算每个横模级数对应的波长的函数
    """
    gl, gr = 1-length/rocl, 1-length/rocr
    glgr = gl*gr
    try:
        pl = gr*(1-gl)/(gl+gr-2*glgr)*length
        pr = gl*(1-gr)/(gl+gr-2*glgr)*length
        z0 = np.sqrt(glgr*(1-glgr)/(gl+gr-2*glgr)**2)*length
    except ZeroDivisionError:
        z0 = pl = pr = length/2

    def func(p):
        return 2*np.pi*length/(p*np.pi+(mx+my+1)*(np.arctan(pl/z0)+np.arctan(pr/z0)))
    return func

def get_available_wavelength(wavelength0, length, rocl, rocr, mx, my):
    """
    获取满足腔相位条件的波长
    :param wavelength0: 所要接近的波长
    :param length: 腔长
    :param rocl: 左边腔镜ROC
    :param rocR: 右边腔镜ROC
    :param mx: x方向模式数
    :param my: y方向模式数
    :return: wavelength 满足条件的波长
    """
    gl, gr = 1-length/rocl, 1-length/rocr
    glgr = gl*gr
    try:
        pl = gr*(1-gl)/(gl+gr-2*glgr)*length
        pr = gl*(1-gr)/(gl+gr-2*glgr)*length
        z0 = np.sqrt(glgr*(1-glgr)/(gl+gr-2*glgr)**2)*length
    except ZeroDivisionError:
        z0 = pl = pr = length/2
    
    p0 = 2*length/wavelength0-(mx+my+1)*(np.arctan(pl/z0)+np.arctan(pr/z0))/np.pi

    wavelength1 = 2*np.pi*length/(int(p0)*np.pi+(mx+my+1)*(np.arctan(pl/z0)+np.arctan(pr/z0)))
    wavelength2 = 2*np.pi*length/(int(p0)*np.pi+np.pi+(mx+my+1)*(np.arctan(pl/z0)+np.arctan(pr/z0)))

    if abs(wavelength1-wavelength0) < abs(wavelength2-wavelength0):
        return int(p0), wavelength1
    else:
        return int(p0)+1, wavelength2

# -----------------------------------------------------------------------------------

def judge_cavity_type(length, rocl, rocr):
    """
    判断腔是否满足稳定条件，且判断是否为临界腔。注意临界腔虽然满足稳定条件，但是否稳定需要
    看具体结构。
    :param length: 腔长
    :param rocl: 左边腔镜ROC
    :param rocr: 右边腔镜ROC
    :return: (s, c) s: True-腔满足稳定条件，False-腔不满足稳定条件;
                    c: True-临界腔，False-非临界腔
    """
    s = False
    c = False

    glgr = (1-length/rocl)*(1-length/rocr)
    if glgr >= 0 and glgr <= 1:
        s = True
        if glgr == 0 or glgr == 1:
            c = True

    return s, c


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
