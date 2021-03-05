import scipy as sp
from scipy import constants
from ._utils import PrintInfoMixin, PropertySet
from .mirror import MirrorSurface

__all__ = [
    'StepIndexFiberEnd',
    'FiberEnd'
]

class FiberEnd(PrintInfoMixin):
    name = 'FiberEnd'

    def __init__(self, nf, wavelength, omegaf, roc=sp.inf, name='FiberEnd', **kwargs):
        self.name = name

        # 折射率，波长，模场半径，光纤端面
        self.property_set = PropertySet(('nf', 'wavelength', 'omegaf', 'mirrorsurface'))
        self.property_set['omegaf'] = omegaf
        self.property_set['nf'] = nf
        self.property_set['wavelength'] = wavelength
        self.property_set['mirrorsurface'] = MirrorSurface(ROC=roc)
        self.property_set.update(kwargs)

    def change_params(self, **kwargs):
        self.property_set.update(kwargs)

    @property
    def omegaf(self) -> float:
        """模场半径"""
        return self.property_set['omegaf']

    @property
    def nf(self) -> float:
        """折射率"""
        return self.property_set['nf']

    @property
    def wavelength(self) -> float:
        """中心波长"""
        return self.property_set['wavelength']

    @property
    def nu0(self) -> float:
        """中心频率"""
        return 2 * constants.pi / self.wavelength
    
    @property
    def roc(self) -> float:
        """端面曲率半径"""
        return self.property_set['mirrorsurface'].ROC

class StepIndexFiberEnd(FiberEnd, PrintInfoMixin):
    name = 'StepIndexFiberEnd'

    def __init__(self, nf, wavelength, a, naf, roc=sp.inf, name='StepIndexFiberEnd', **kwargs):
        self.name = name

        # 折射率，波长，光纤纤芯半径，数值孔径，光纤端面
        self.property_set = PropertySet(('nf', 'wavelength', 'a', 'naf', 'mirrorsurface'))
        self.property_set['naf'] = naf
        self.property_set['nf'] = nf
        self.property_set['a'] = a
        self.property_set['wavelength'] = wavelength
        self.property_set['mirrorsurface'] = MirrorSurface(ROC=roc)
        self.property_set.update(kwargs)

    def change_params(self, **kwargs):
        self.property_set.update(kwargs)

    @property
    def a(self) -> float:
        """光纤纤芯半径"""
        return self.property_set['a']

    @property
    def naf(self) -> float:
        """数值孔径"""
        return self.property_set['naf']

    @property
    def omegaf(self) -> float:
        """光纤模场半径"""
        nu0 = self.nu0
        a = self.a
        naf = self.naf
        V = nu0 * a * naf  # 归一化频率 <2.4单模
        return a * (0.65 + 1.619 * V ** (-1.5) + 2.879 * V ** (-6))
