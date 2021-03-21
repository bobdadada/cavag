import scipy as sp
from scipy import constants
from ._utils import PrintInfoMixin
from .mirror import MirrorSurface

__all__ = [
    'StepFiber',
    'Fiber'
]

class Fiber(PrintInfoMixin):
    name = 'Fiber'

    def __init__(self, nf, wavelength, omegaf, name='Fiber', **kwargs):
        self._property = {
            'nf': None,  # 折射率
            'omegaf': None,  # 模场半径
            'wavelength': None,  # 波长
        }
        self.name = name
        self._property['omegaf'] = omegaf
        self._property['nf'] = nf
        self._property['wavelength'] = wavelength
        self._property.update(kwargs)

    def change_params(self, **kwargs):
        self._property.update(kwargs)

    @property
    def omegaf(self) -> float:
        """模场半径"""
        return self._property['omegaf']

    @property
    def nf(self) -> float:
        """折射率"""
        return self._property['nf']

    @property
    def wavelength(self) -> float:
        """中心波长"""
        return self._property['wavelength']

    @property
    def k(self):
        """波矢"""
        return 2 * constants.pi / self.wavelength
    
    @property
    def nu(self):
        """中心频率"""
        return constants.c / self.wavelength

class StepFiber(PrintInfoMixin):
    name = 'StepFiber'

    def __init__(self, NAf, nf, a, wavelength, ROC=sp.inf, type='', name='StepFiber', **kwargs):
        self._property = {
            'NAf': None,  # 数值孔径
            'nf': None,  # 折射率
            'mirrorsurface': [],
            'a': None,  # 光纤半径
            'wavelength': None,  # 波长
            'type': ''  # 类型
        }
        self.name = name
        self._property['NAf'] = NAf
        self._property['nf'] = nf
        self._property['a'] = a
        self._property['wavelength'] = wavelength
        self._property['mirrorsurface'] = [MirrorSurface(ROC=ROC)]
        self._property.update(kwargs)

    def change_params(self, **kwargs):
        self._property.update(kwargs)

    @property
    def a(self) -> float:
        """光纤纤芯半径"""
        return self._property['a']

    @property
    def NAf(self) -> float:
        """数值孔径"""
        return self._property['NAf']

    @property
    def nf(self) -> float:
        """折射率"""
        return self._property['nf']

    @property
    def wavelength(self) -> float:
        """中心波长"""
        return self._property['wavelength']

    @property
    def omegaf(self):
        """光纤模场半径"""
        k = self.k
        a = self.a
        NAf = self.NAf
        V = k * a * NAf  # 归一化频率 <2.4单模
        return a * (0.65 + 1.619 * V ** (-1.5) + 2.879 * V ** (-6))

    @property
    def k(self):
        """波矢"""
        return 2 * constants.pi / self.wavelength
    
    @property
    def nu(self):
        """中心频率"""
        return constants.c / self.wavelength

    @property
    def ROC(self):
        """曲率半径"""
        return [m.ROC for m in self._property['mirrorsurface']]
