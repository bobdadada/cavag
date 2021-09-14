"""
用于描述fiber行为的模块。此模块描述了

    - class

    1.
    Fiber -
        通用光纤
    StepIndexFiber -
        阶跃光纤
"""

import logging
from .misc import Wavelength

__all__ = [
    'Fiber', 'StepIndexFiber'
]


class Fiber(Wavelength):
    """
    此类描述了通用光纤。在实际应用中，厂家可以提供波长，折射率，模场半径等参数。

    此类可以通过以下属性构建：
        nf - 折射率
        wavelength - 波长
        omegaf - 模场半径
    """
    name = 'Fiber'

    modifiable_properties = ('nf', 'wavelength', 'omegaf')

    def __init__(self, name='Fiber', **kwargs):
        super().__init__(**kwargs)

        self.property_set.add_required(Fiber.modifiable_properties)
        self.name = name

        for prop in Fiber.modifiable_properties:
            self.property_set[prop] = kwargs.get(prop, None)

    @property
    def nf(self):
        """折射率[1]"""
        return self.get_property('nf')

    @property
    def omegaf(self):
        """模场半径[L]"""
        return self.get_property('omegaf')


class StepIndexFiber(Fiber):
    """
    此类描述了阶跃光纤。

    此类可以通过以下属性构建：
        nf - 折射率
        wavelength - 波长
        a - 纤芯半径
        naf - 数值孔径
    """
    name = 'StepIndexFiber'

    modifiable_properties = ('nf', 'wavelength', 'a', 'naf')

    def __init__(self, name='StepIndexFiber', **kwargs):
        super().__init__(**kwargs)
        self.property_set.add_required(StepIndexFiber.modifiable_properties)
        self.name = name

        for prop in ('naf', 'a'):
            self.property_set[prop] = kwargs.get(prop, None)

    @property
    def a(self):
        """光纤纤芯半径[L]"""
        return self.get_property('a')

    @property
    def naf(self):
        """数值孔径[1]"""
        return self.get_property('naf')

    @property
    def omegaf(self):
        """光纤模场半径[L]"""
        def v_f():
            k = self.k
            a = self.a
            naf = self.naf
            V = k * a * naf  # 归一化频率
            if V < 1.2:
                logging.warning('Normalized frequency for {}:{} is less than 1.2, '
                                'the approximate radius of mode field may be not '
                                'correct'.format(self.name, repr(self)))
            # empirically that the size w of the Gaussian approximation
            # to the fiber mode for V >~ 1.2 given by Marcuse
            return a * (0.65 + 1.619 * V ** (-1.5) + 2.879 * V ** (-6))
        return self.get_property('omegaf', v_f)
