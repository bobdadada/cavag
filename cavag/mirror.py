from .misc import Position, RTL

__all__ = [
    'MirrorSurface',
    'Lens'
]


class MirrorSurface(RTL, Position):
    name = "MirrorSurface"

    # 曲率半径, 反射率, 透射率, 损耗率, 位置
    modifiable_properties = ('roc', 'r', 't', 'l', 'position')

    def __init__(self, name='MirrorSurface', **kwargs):
        super().__init__(**kwargs)
        self.property_set.add_required(MirrorSurface.modifiable_properties)
        self.name = name

        self.property_set['roc'] = kwargs.get('roc', None)

    @property
    def roc(self) -> float:
        """曲率半径[L]"""
        return self.get_property('roc')


class Lens(RTL, Position):
    name = "Lens"

    # 焦距, 反射率, 透射率, 损耗率, 位置
    modifiable_properties = ('f', 'r', 't', 'l', 'position')

    def __init__(self, name='Lens', **kwargs):
        super().__init__(**kwargs)
        self.property_set.add_required(Lens.modifiable_properties)
        self.name = name
        
        self.property_set['f'] = kwargs.get('f', None)
    
    @property
    def f(self) -> float:
        """焦距[L]"""
        return self.get_property('f')

