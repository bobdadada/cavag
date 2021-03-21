from scipy import constants

from ._utils import PrintableObject

__all__ = [
    'Position',
    'Wavelength'
]

class Position(PrintableObject):
    name = 'Position'

    # 位置
    modifiable_properties = ('position', )

    def __init__(self, name='Position', **kwargs):
        super().__init__(**kwargs)
        self.property_set.add_required(Position.modifiable_properties)
        self.name = name
        
        self.property_set['position'] = kwargs.get('position', 0)
    
    @property
    def position(self):
        """位置[L]"""
        return self.get_property('position')


class Wavelength(PrintableObject):
    name = 'Wavelength'

    # 波长
    modifiable_properties = ('wavelength', )

    def __init__(self, name='Wavelenght', **kwargs):
        super().__init__(**kwargs)
        self.property_set.add_required(Wavelength.modifiable_properties)
        self.name = name
        
        self.property_set['wavelength'] = kwargs.get('wavelength', None)
    
    @property
    def wavelength(self):
        """波长[L]"""
        return self.get_property('wavelength')
    
    @property
    def k(self):
        """波矢[L^(-1)]"""
        return self.get_property('k', lambda: 2*constants.pi/self.wavelength)

    @property
    def nu(self):
        """频率[T^(-1)]"""
        return self.get_property('nu', lambda: constants.c/self.wavelength)
    
    @property
    def nu_angular(self):
        """角频率[T^(-1)]"""
        return self.get_property('nu_angular', lambda: 2*constants.pi*self.nu)
