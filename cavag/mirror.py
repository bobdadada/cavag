"""
用于描述mirror或类似的器件行为的模块。此模块描述了

    - class

    1.
    Mirror - 镜面
    
    2.
    Lens - 薄透镜
"""

from .misc import Position, RTL

__all__ = [
    'Mirror', 'Lens'
]


class Mirror(RTL, Position):
    """
    此类描述了圆形镜片。在实际应用中，镜片的透射率可为0。

    此类可以通过以下属性构建：
        roc - 曲率半径
        r - 反射率
        t - 透射率
        l - 损耗
        position - 镜片位置
    """
    name = "Mirror"

    modifiable_properties = ('roc', 'r', 't', 'l', 'position')

    def __init__(self, name='Mirror', **kwargs):
        super().__init__(**kwargs)
        self.name = name

        self.property_set.add_required(Mirror.modifiable_properties)

        self.property_set['roc'] = kwargs.get('roc', None)

    @property
    def roc(self) -> float:
        """曲率半径[L]"""
        return self.get_property('roc')


class Lens(RTL, Position):
    """
    此类描述了薄透镜。在实际应用中，薄透镜的反射率可为0。

    此类可以通过以下属性构建：
        f - 焦距
        r - 反射率
        t - 透射率
        l - 损耗
        position - 镜片位置
    """
    name = "Lens"

    modifiable_properties = ('f', 'r', 't', 'l', 'position')

    def __init__(self, name='Lens', **kwargs):
        super().__init__(**kwargs)
        self.name = name

        self.property_set.add_required(Lens.modifiable_properties)

        self.property_set['f'] = kwargs.get('f', None)

    @property
    def f(self) -> float:
        """焦距[L]"""
        return self.get_property('f')
