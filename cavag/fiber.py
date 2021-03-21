import logging
import scipy as sp
from scipy import constants
from .misc import Wavelength
from ._utils import PrintableObject, PropertySet

__all__ = [
    'FiberEnd',
    'StepIndexFiberEnd'
]


class FiberEnd(Wavelength):
    name = 'FiberEnd'

    # 折射率，波长，模场半径，光纤端面曲率半径
    modifiable_properties = ('nf', 'wavelength', 'omegaf', 'roc')

    def __init__(self, name='FiberEnd', **kwargs):
        super().__init__(**kwargs)
        self.property_set.add_required(FiberEnd.modifiable_properties)
        self.name = name

        if kwargs.get('roc') is None:
            kwargs['roc'] = sp.inf
        for prop in FiberEnd.modifiable_properties:
            self.property_set[prop] = kwargs.get(prop, None)

    @property
    def nf(self) -> float:
        """折射率[1]"""
        return self.get_property('nf')
    
    @property
    def omegaf(self) -> float:
        """模场半径[L]"""
        return self.get_property('omegaf')

    @property
    def roc(self) -> float:
        """端面曲率半径[L]"""
        return self.get_property('roc')

class StepIndexFiberEnd(FiberEnd):
    name = 'StepIndexFiberEnd'

    # 折射率，波长，光纤纤芯半径，数值孔径，光纤端面曲率半径
    modifiable_properties = ('nf', 'wavelength', 'a', 'naf', 'roc')

    def __init__(self, name='StepIndexFiberEnd', **kwargs):
        super().__init__(**kwargs)
        self.property_set.add_required(StepIndexFiberEnd.modifiable_properties)
        self.name = name

        for prop in ('naf', 'a'):
            self.property_set[prop] = kwargs.get(prop, None)

    @property
    def a(self) -> float:
        """光纤纤芯半径[L]"""
        return self.get_property('a')

    @property
    def naf(self) -> float:
        """数值孔径[1]"""
        return self.get_property('naf')

    @property
    def omegaf(self) -> float:
        """光纤模场半径[L]"""
        def v_f():
            k = self.k
            a = self.a
            naf = self.naf
            V = k * a * naf  # 归一化频率
            if V < 1.2:
                logging.warning('Normalized frequency for {}:{} is less than 1.2, ' \
                                'the approximate radius of mode field may be not ' \
                                'correct'.format(self.name, repr(self)))
            # empirically that the size w of the Gaussian approximation
            # to the fiber mode for V >~ 1.2 given by Marcuse
            return a * (0.65 + 1.619 * V ** (-1.5) + 2.879 * V ** (-6))
        return self.get_property('omegaf', v_f)
