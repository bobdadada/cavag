from .misc import Position

__all__ = [
    'MirrorSurface',
    'ThinLens',
    'ThickLens',
    'add_loss',
    'calculate_rtl'
]


class MirrorSurface(Position):
    name = "MirrorSurface"

    def __init__(self, roc, r=0.0, t=1.0, l=0.0, position=0.0, name='MirrorSurface', **kwargs):
        super(Position, self).__init__(position=position)
        self.name = name

        # 曲率半径, 反射率, 透射率, 损耗率
        self.property_set.add_required(('roc', 'r', 't', 'l'))
        self.property_set['roc'] = roc
        self.property_set['r'] = r
        self.property_set['t'] = t
        self.property_set['l'] = l
        self.property_set.update(**kwargs)

    @property
    def roc(self):
        """曲率半径"""
        return self.property_set['roc']

    @property
    def r(self):
        """反射率"""
        return self.property_set['r']

    @property
    def t(self):
        """透射率"""
        return self.property_set['t']

    @property
    def l(self):
        """损耗率"""
        return self.property_set['l']
    
    def add_loss(self, loss):
        m = self.r, self.t, self.l
        r, t, l = add_loss(m, loss)
        self.property_set['r'] = r
        self.property_set['t'] = t
        self.property_set['l'] = l


class ThinLens(Position):
    name = "ThinLens"

    def __init__(self, f, position, name='ThinLens', **kwargs):
        super(Position, self).__init__(position=position)
        self.name = name

        # 焦距
        self.property_set.add_required('f')
        self.property_set['f'] = f
        self.property_set.update(**kwargs)

    @property
    def f(self):
        """焦距"""
        return self.property_set['f']


class ThickLens(Position):
    name = "ThickLens"

    def __init__(self, d, fl, fr, position, name='ThickLens', **kwargs):
        super(Position, self).__init__(position=position)
        self.name = name

        # 厚度, 左焦距, 右焦距
        self.property_set.add_required(('d', 'fl', 'fr'))
        self.property_set['d'] = d
        self.property_set['fl'] = fl
        self.property_set['fr'] = fr
        self.property_set.update(**kwargs)

    @property
    def d(self):
        """厚度"""
        return self.property_set['d']

    @property
    def fl(self):
        """左焦距"""
        return self.property_set['fl']

    @property
    def fr(self):
        """右焦距"""
        return self.property_set['fr']


def add_loss(m0, loss):
    """
    计算增添损耗后的(反射率，透射率，损耗)
    :param m0: 原始的(反射率，透射率，损耗)
    :param loss: 添加的损耗
    :return: 反射率，透射率，损耗
    """
    r, t, l = m0
    r = r*(1-loss)
    t = t*(1-loss)
    l = l*(1-loss)+loss
    return r, t, l


def calculate_rtl(r, t2l):
    """
    计算反射率，透射率，损耗
    :param r: 反射率
    :param t2l: 透射损耗比
    :return: 反射率，透射率，损耗
    """
    t, l = (1-r)*t2l/(t2l+1), (1-r)/(t2l+1)
    return r, t, l

