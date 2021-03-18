import logging
import scipy as sp
from scipy import constants
from ._utils import PrintableObject, PropertySet

__all__ = [
    'FiberEnd',
    'StepIndexFiberEnd'
]


class FiberEnd(PrintableObject):
    name = 'FiberEnd'

    # 折射率，波长，模场半径，光纤端面曲率半径
    modifiable_properties = ('nf', 'wavelength', 'omegaf', 'roc')

    def __init__(self, nf, wavelength, omegaf, roc=sp.inf, name='FiberEnd'):
        super().__init__()
        self.property_set.add_required(FiberEnd.modifiable_properties)
        self.name = name

        self.property_set['omegaf'] = omegaf
        self.property_set['nf'] = nf
        self.property_set['wavelength'] = wavelength
        self.property_set['roc'] = roc

    @property
    def nf(self) -> float:
        """折射率"""
        return self.property_set.get_strictly('nf')

    @property
    def wavelength(self) -> float:
        """中心波长"""
        return self.property_set.get_strictly('wavelength')
    
    @property
    def omegaf(self) -> float:
        """模场半径"""
        return self.property_set.get_strictly('omegaf')

    @property
    def roc(self) -> float:
        """端面曲率半径"""
        return self.property_set.get_strictly('roc')

    @property
    def nu0(self) -> float:
        """中心圆频率"""
        if 'nu0' not in self.property_set:
            self.property_set['nu0'] = 2 * constants.pi / self.wavelength
        return self.property_set['nu0']


class StepIndexFiberEnd(FiberEnd):
    name = 'StepIndexFiberEnd'

    # 折射率，波长，光纤纤芯半径，数值孔径，光纤端面曲率半径
    modifiable_properties = ('nf', 'wavelength', 'a', 'naf', 'roc')

    def __init__(self, nf, wavelength, a, naf, roc=sp.inf, name='StepIndexFiberEnd'):
        self.property_set = PropertySet(StepIndexFiberEnd.modifiable_properties)
        self.name = name

        self.property_set['naf'] = naf
        self.property_set['nf'] = nf
        self.property_set['a'] = a
        self.property_set['wavelength'] = wavelength
        self.property_set['roc'] = roc

    @property
    def a(self) -> float:
        """光纤纤芯半径"""
        return self.property_set.get_strictly('a')

    @property
    def naf(self) -> float:
        """数值孔径"""
        return self.property_set.get_strictly('naf')

    @property
    def omegaf(self) -> float:
        """光纤模场半径"""
        if 'omegaf' not in self.property_set:
            nu0 = self.nu0
            a = self.a
            naf = self.naf
            V = nu0 * a * naf  # 归一化频率
            if V < 1.2:
                logging.warning('Normalized frequency for {}:{} is less than 1.2, ' \
                                'the approximate radius of mode field may be not ' \
                                'correct'.format(self.name, repr(self))
                        )
            # empirically that the size w of the Gaussian approximation
            # to the fiber mode for V >~ 1.2 given by Marcuse
            self.property_set['omegaf'] = a * (0.65 + 1.619 * V ** (-1.5) + 2.879 * V ** (-6))
        return self.property_set['omegaf'] 
