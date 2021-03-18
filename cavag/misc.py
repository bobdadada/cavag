from scipy import constants

from ._utils import PrintableObject

__all__ = [
    'Position',
    'Wavelength'
]

class Position(PrintableObject):
    name = 'Position'

    # 主平面位置
    modifiable_properties = ('position', )

    def __init__(self, name='Position', **kwargs):
        super().__init__(**kwargs)
        self.property_set.add_required(Position.modifiable_properties)
        self.name = name
        
        self.property_set['position'] = kwargs.get('position', 0)
    
    @property
    def position(self):
        """位置"""
        return self.property_set.get_strictly('position')


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
        """波长"""
        return self.property_set.get_strictly('wavelength')
    
    @property
    def k(self):
        """波矢"""
        return self.get_property('k', lambda: 2*constants.pi/self.wavelength)
