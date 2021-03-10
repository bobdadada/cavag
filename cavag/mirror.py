from .misc import Position
from .utils import RTLConvertor

__all__ = [
    'MirrorSurface',
    'ThinLens',
    'ThickLens'
]


class MirrorSurface(Position):
    name = "MirrorSurface"

    def __init__(self, roc, r=0, t=1, l=0, position=0, name='MirrorSurface', **kwargs):
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
        r, t, l = RTLConvertor.add_loss(m, loss)
        self.property_set['r'] = r
        self.property_set['t'] = t
        self.property_set['l'] = l


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


class ThinLens(ThickLens):
    name = "ThinLens"

    def __init__(self, f, position, name='ThinLens', **kwargs):
        super(ThickLens, self).__init__(self, d=0, fl=f, fr=f, position=position)
        self.name = name

        # 焦距
        self.property_set.add_required('f')
        self.property_set['f'] = f
        self.property_set.update(**kwargs)

    @property
    def f(self):
        """焦距"""
        return self.property_set['f']
