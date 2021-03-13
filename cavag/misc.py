from ._utils import PrintableObject

class Position(PrintableObject):
    name = 'Position'

    # 主平面位置
    modifiable_properties = ('position', )

    def __init__(self, position=0, name='Position'):
        super().__init__()
        self.property_set.add_required(Position.modifiable_properties)
        self.name = name
        
        self.property_set['position'] = position
    
    @property
    def position(self):
        """主平面位置"""
        return self.property_set.get_strictly('position')
