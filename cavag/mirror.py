from ._utils import PrintInfoMixin

__all__ = [
    'MirrorSurface',
    'Mirror',
    'add_loss',
    'calculate_rtl'
]

class MirrorSurface(PrintInfoMixin):

    name = "MirrorSurface"

    def __init__(self, ROC, R=None, T=None, L=None, position=None, name='MirrorSurface', **kwargs):
        self._property = {
                "ROC": None,  # 曲率半径
                "R": None,  # 反射率
                "T": None,  # 透射率
                "L": None,  # 损耗率
                'position': None  # 位置
        }
        self.name = name
        self._property['ROC'] = ROC
        self._property['R'] = R
        self._property['L'] = L
        self._property['T'] = T
        self._property['position'] = position
        self._property.update(**kwargs)

    @property
    def ROC(self):
        """曲率半径"""
        return self._property['ROC']

    @property
    def R(self):
        """反射率"""
        return self._property['R']

    @property
    def T(self):
        """透射率"""
        return self._property['T']

    @property
    def L(self):
        """损耗率"""
        return self._property['L']

    @property
    def position(self):
        """位置"""
        return self._property['position']

class Mirror(PrintInfoMixin):

    name = "Mirror"

    def __init__(self, position, f, name='Mirror', **kwargs):
        self._property = {
                "f": None,  # 焦距
                'position': None  # 位置
        }
        self.name = name
        self._property['position'] = position
        self._property['f'] = f
        self._property.update(**kwargs)

    @property
    def f(self):
        """焦距"""
        return self._property['f']

    @property
    def position(self):
        """位置"""
        return self._property['position']

def add_loss(m, loss):
    """
    计算增添损耗后的(反射率，透射率，损耗)
    :param m: 原始的(反射率，透射率，损耗)
    :param loss: 添加的损耗
    :return: 反射率，透射率，损耗
    """
    r, t, l = m
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

