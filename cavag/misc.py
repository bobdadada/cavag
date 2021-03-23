from scipy import constants

from ._utils import PrintableObject

__all__ = [
    'RTL',
    'RTLConverter',
    'Position',
    'Wavelength'
]


class RTL(PrintableObject):
    name = 'RTL'

    # 反射率，透射率，损耗
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
    def r(self) -> float:
        """反射率[1]"""
        return self.get_property('r')

    @property
    def t(self) -> float:
        """透射率[1]"""
        return self.get_property('t')

    @property
    def l(self) -> float:
        """损耗[1]"""
        return self.get_property('l')
    
    def add_loss(self, loss):
        m = self.r, self.t, self.l
        r, t, l = RTLConverter.add_loss(m, loss)
        self.property_set['r'] = r
        self.property_set['t'] = t
        self.property_set['l'] = l
    
    def change_params(self, _norm=True, _filter=True, **kwargs):
        super().change_params(_filter=_filter, **kwargs)

        if _filter:
            kwargs = self.filter_properties(kwargs)

        if _norm and any(p in kwargs for p in RTL.modifiable_properties):
            r, t, l = kwargs.get('r', None), kwargs.get('t', None), kwargs.get('l', None)
            r, t, l = RTLConverter.normalize(r=r, t=t, l=l)
            kwargs.update({'r':r, 't':t, 'l':l})
            
        self.update_propset(**kwargs)


class RTLConverter:

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
    name = 'Position'

    # 位置
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
    name = 'Wavelength'

    # 波长
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
        """波矢[L^(-1)]"""
        return self.get_property('k', lambda: 2*constants.pi/self.wavelength)

    @property
    def nu(self):
        """频率[T^(-1)]"""
        return self.get_property('nu', lambda: constants.c/self.wavelength)
    
    @property
    def nu_angular(self):
        """角频率[T^(-1)]"""
        return self.get_property('nu_angular', lambda: 2*constants.pi*self.nu)

