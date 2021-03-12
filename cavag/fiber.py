import scipy as sp
from scipy import constants
from ._utils import PrintableObject, PropertySet
from .mirror import MirrorSurface

__all__ = [
    'FiberEnd',
    'StepIndexFiberEnd'
]


class FiberEnd(PrintableObject):
    name = 'FiberEnd'

    def __init__(self, nf, wavelength, omegaf, roc=sp.inf, name='FiberEnd'):
        super(PrintableObject, self).__init__()
        self.name = name

        # 折射率，波长，模场半径，光纤端面
        self.property_set.add_required(('nf', 'wavelength', 'omegaf', 'mirrorsurface'))
        self.property_set['omegaf'] = omegaf
        self.property_set['nf'] = nf
        self.property_set['wavelength'] = wavelength
        self.property_set['mirrorsurface'] = MirrorSurface(roc=roc)

    @property
    def nf(self) -> float:
        """折射率"""
        return self.property_set['nf']

    @property
    def wavelength(self) -> float:
        """中心波长"""
        return self.property_set['wavelength']
    
    @property
    def omegaf(self) -> float:
        """模场半径"""
        return self.property_set['omegaf']

    @property
    def nu0(self) -> float:
        """中心圆频率"""
        return 2 * constants.pi / self.wavelength
    
    @property
    def roc(self) -> float:
        """端面曲率半径"""
        return self.property_set['mirrorsurface'].roc


class StepIndexFiberEnd(FiberEnd):
    name = 'StepIndexFiberEnd'

    def __init__(self, nf, wavelength, a, naf, roc=sp.inf, name='StepIndexFiberEnd'):

        # 折射率，波长，光纤纤芯半径，数值孔径，光纤端面
        self.property_set = PropertySet(('nf', 'wavelength', 'a', 'naf', 'mirrorsurface'))
        self.property_set['naf'] = naf
        self.property_set['nf'] = nf
        self.property_set['a'] = a
        self.property_set['wavelength'] = wavelength
        self.property_set['mirrorsurface'] = MirrorSurface(roc=roc)

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
        V = nu0 * a * naf  # 归一化频率
        # empirically that the size w of the Gaussian approximation
        # to the fiber mode for V >~ 1.2 given by Marcuse
        if 'omegaf' not in self.property_set:
            self.property_set['omegaf'] = a * (0.65 + 1.619 * V ** (-1.5) + 2.879 * V ** (-6))
        return self.property_set['omegaf'] 
