from ._utils import PrintableObject

class Position(PrintableObject):
    name = 'Position'

    def __init__(self, position=0, name='Position', **kwargs):
        super().__init__()
        self.name = name

        # 主平面位置
        self.property_set.add_required('position')
        self.property_set['position'] = position
        self.property_set.update(**kwargs)
    
    @property
    def position(self):
        """主平面位置"""
        return self.property_set['position']
