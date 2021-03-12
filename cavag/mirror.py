from .misc import Position

__all__ = [
    'MirrorSurface',
    'ThinLens',
    'ThickLens',
    'RTLConverter'
]


class MirrorSurface(Position):
    name = "MirrorSurface"

    def __init__(self, roc, r=None, t=None, l=None, position=0, name='MirrorSurface'):
        super(Position, self).__init__(position=position)
        self.name = name

        r, t, l = RTLConverter.normalize(r=r, t=t, l=l)

        # 曲率半径, 反射率, 透射率, 损耗率
        self.property_set.add_required(('roc', 'r', 't', 'l'))
        self.property_set['roc'] = roc
        self.property_set['r'] = r
        self.property_set['t'] = t
        self.property_set['l'] = l

    @property
    def roc(self) -> float:
        """曲率半径"""
        return self.property_set['roc']

    @property
    def r(self) -> float:
        """反射率"""
        return self.property_set['r']

    @property
    def t(self) -> float:
        """透射率"""
        return self.property_set['t']

    @property
    def l(self) -> float:
        """损耗率"""
        return self.property_set['l']
    
    def add_loss(self, loss):
        m = self.r, self.t, self.l
        r, t, l = RTLConverter.add_loss(m, loss)
        self.property_set['r'] = r
        self.property_set['t'] = t
        self.property_set['l'] = l


class RTLConverter(object):

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


class ThickLens(Position):
    name = "ThickLens"

    def __init__(self, d, fl, fr, position, name='ThickLens'):
        super(Position, self).__init__(position=position)
        self.name = name

        # 厚度, 左焦距, 右焦距
        self.property_set.add_required(('d', 'fl', 'fr'))
        self.property_set['d'] = d
        self.property_set['fl'] = fl
        self.property_set['fr'] = fr

    @property
    def d(self) -> float:
        """厚度"""
        return self.property_set['d']

    @property
    def fl(self) -> float:
        """左焦距"""
        return self.property_set['fl']

    @property
    def fr(self) -> float:
        """右焦距"""
        return self.property_set['fr']


class ThinLens(ThickLens):
    name = "ThinLens"

    def __init__(self, f, position, name='ThinLens'):
        super(ThickLens, self).__init__(self, d=0, fl=f, fr=f, position=position)
        self.name = name

        # 焦距
        self.property_set.add_required('f')
        self.property_set['f'] = f

    @property
    def f(self) -> float:
        """焦距"""
        return self.property_set['f']

