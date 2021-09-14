"""
用于描述只有少数属性的帮助类的模块。此模块描述了

    - class

    1.
    RTL - 反射-透射-损耗
    RTLConverter - RTL转换类
    
    2.
    Position - 位置

    3.
    Wavelength - 波长
"""

from scipy import constants
from ._utils import PrintableObject

__all__ = [
    'RTL', 'RTLConverter',
    'Position', 'Wavelength'
]


class RTL(PrintableObject):
    """
    此类描述了反射-透射-损耗抽象类。

    此类可以通过以下属性构建：
        r - 反射率
        t - 透射率
        l - 损耗
    """
    name = 'RTL'

    modifiable_properties = ('r', 't', 'l')

    def __init__(self, name='RTL', **kwargs):
        super().__init__(**kwargs)
        self.property_set.add_required(RTL.modifiable_properties)
        self.name = name

        dt = {}
        for mp in RTL.modifiable_properties:
            dt[mp] = kwargs.get(mp, None)
        r, t, l = RTLConverter.normalize(r=dt['r'], t=dt['t'], l=dt['l'])

        self.property_set['r'] = r
        self.property_set['t'] = t
        self.property_set['l'] = l

    @property
    def r(self):
        """反射率[1]"""
        return self.get_property('r')

    @property
    def t(self):
        """透射率[1]"""
        return self.get_property('t')

    @property
    def l(self):
        """损耗[1]"""
        return self.get_property('l')

    def add_loss(self, loss):
        m = self.r, self.t, self.l
        r, t, l = RTLConverter.add_loss(m, loss)
        self.property_set['r'] = r
        self.property_set['t'] = t
        self.property_set['l'] = l

    def preprocess_properties(self, _norm=True, **propdict):
        if _norm and any(p in propdict for p in RTL.modifiable_properties):
            r, t, l = propdict.get('r', None), propdict.get(
                't', None), propdict.get('l', None)
            r, t, l = RTLConverter.normalize(r=r, t=t, l=l)
            propdict.update({'r': r, 't': t, 'l': l})
        return propdict


class RTLConverter:
    """
    反射-透射-损耗转换类，可以实现反射、透射、损耗的转换运算。
    此类将所有转换运算都包含在一起。
    """

    @staticmethod
    def normalize(r=None, t=None, l=None):
        """
        归一化反射率，透射率，损耗
        :param r: 反射率
        :param t: 透射率
        :param l: 损耗
        :return: 反射率，透射率，损耗
        """
        m = (r, t, l)
        N_ct = m.count(None)
        if N_ct >= 2:
            return m
        elif N_ct == 0:
            m_sum = sum(m)
            return r/m_sum, t/m_sum, l/m_sum
        else:
            i = m.index(None)
            if i == 0:
                return 1-t-l, t, l
            elif i == 1:
                return r, 1-r-l, l
            else:
                return r, t, 1-r-t

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
    def add_reflectivity(m0, re):
        """
        计算增添反射率后的(反射率，透射率，损耗)
        :param m0: 原始的(反射率，透射率，损耗)
        :param re: 添加的反射率
        :return: 反射率，透射率，损耗
        """
        r0, t0, l0 = m0
        r = r0*(1-re)+re
        t = t0*(1-re)
        l = l0*(1-re)
        return r, t, l

    @staticmethod
    def add_transmittance(m0, te):
        """
        计算增添透射率后的(反射率，透射率，损耗)
        :param m0: 原始的(反射率，透射率，损耗)
        :param te: 添加的透射率
        :return: 反射率，透射率，损耗
        """
        r0, t0, l0 = m0
        r = r0*(1-te)
        t = t0*(1-te)+te
        l = l0*(1-te)
        return r, t, l

    @staticmethod
    def add_loss(m0, le):
        """
        计算增添损耗后的(反射率，透射率，损耗)
        :param m0: 原始的(反射率，透射率，损耗)
        :param le: 添加的损耗
        :return: 反射率，透射率，损耗
        """
        r0, t0, l0 = m0
        r = r0*(1-le)
        t = t0*(1-le)
        l = l0*(1-le)+le
        return r, t, l


class Position(PrintableObject):
    """
    位置抽象类。

    此类可以通过以下属性构建：
        position - 位置
    """
    name = 'Position'

    modifiable_properties = ('position', )

    def __init__(self, name='Position', **kwargs):
        super().__init__(**kwargs)
        self.property_set.add_required(Position.modifiable_properties)
        self.name = name

        self.property_set['position'] = kwargs.get('position', 0)

    @property
    def position(self):
        """位置[L]"""
        return self.get_property('position')


class Wavelength(PrintableObject):
    """
    波长抽象类。

    此类可以通过以下属性构建：
        wavelength - 波长
    """
    name = 'Wavelength'

    modifiable_properties = ('wavelength', )

    def __init__(self, name='Wavelenght', **kwargs):
        super().__init__(**kwargs)
        self.property_set.add_required(Wavelength.modifiable_properties)
        self.name = name

        self.property_set['wavelength'] = kwargs.get('wavelength', None)

    @property
    def wavelength(self):
        """波长[L]"""
        return self.get_property('wavelength')

    @property
    def k(self):
        """波矢[1/L]"""
        return self.get_property('k', lambda: 2*constants.pi/self.wavelength)

    @property
    def nu(self):
        """频率[1/T]"""
        return self.get_property('nu', lambda: constants.c/self.wavelength)

    @property
    def nu_angular(self):
        """角频率[1/T]"""
        return self.get_property('nu_angular', lambda: 2*constants.pi*self.nu)
