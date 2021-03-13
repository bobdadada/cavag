from copy import copy
from collections import UserDict
from collections.abc import Sequence


class PropertyLost(Exception):
    """Exception raised when necessary property are lost."""


class PropertySet(UserDict):
    def __init__(self, props=(), *args, **kwargs):
        self.__required_props = set(props)
        super().__init__(*args, **kwargs)
        for prop in props:
            if prop not in self:
                self[prop] = None
    
    def __getitem__(self, item):
        value = super().__getitem__(item)
        if (item in self.__required_props) and (value is None):
            raise PropertyLost("property '%s' lost!"%item)
        return value
    
    def change_params(self, **kwargs):
        """
        This function will firstly clear all other keys except the necessary keys.
        And Then change the value in the input parameters **kwargs.
        """

        dt = {}
        for prop in self.__required_props:
            dt[prop] = self[prop]
        dt.update(**kwargs)

        self.clear()
        self.update(dt)
    
    def reset_required(self, props=()):
        self.clear_required()
        self.add_required(props=props)

    def add_required(self, props=()):
        if isinstance(props, str):
            self.__required_props.add(props)
            if props not in self:
                self[props] = None
        elif isinstance(props, Sequence):
            self.__required_props.update(props)
            for prop in props:
                if prop not in self:
                    self[prop] = None

    def del_required(self, props=()):
        if isinstance(props, str):
            self.__required_props.discard(props)
        elif isinstance(props, Sequence):
            for prop in props:
                self.__required_props.discard(prop)

    def clear_required(self):
        self.__required_props.clear()


class _Object(object):
    name = 'Object'
    modifiable_properties = ()
    
    def __init__(self, name='Object', **kwargs):
        self.property_set = PropertySet(_Object.modifiable_properties)
        self.name = name
    
    def filter_properties(self, kwargs):
        dt = {}
        for prop in self.modifiable_properties:
            if prop in kwargs:
                dt[prop] = kwargs[prop]
        return dt

    def change_params(self, _filter=True, **kwargs):
        if _filter:
            kwargs = self.filter_properties(kwargs)
        self.property_set.change_params(**kwargs)


class PrintInfoMixin(object):

    def _parse_property(self, p):
        if p.startswith('_'):
            return False
        elif callable(getattr(self, p)):
            return False
        else:
            return True

    def get_attrs(self):
        attrs = []
        for item in dir(self):
            if item == 'name':
                continue
            if self._parse_property(item):
                attrs.append(item)
        return attrs        

    def __str__(self):
        if getattr(self, 'name', None):
            info = "{}:\n".format(self.name)
        else:
            info = "{}:\n".format(self.__class__.__name__)
        for item in dir(self):
            if item == 'name':
                continue
            if self._parse_property(item):
                num = getattr(self, item)
                doc = getattr(self.__class__, item).__doc__
                if doc is None:
                    doc = ''
                # 格式化输出，中文对齐
                try:
                    info += "    {0:{3}<15}{1:<8} = {2:e}\n".format(str_half2full(doc), item, num, chr(12288))
                except:
                    info += "    {0:{3}<15}{1:<8} = {2:s}\n".format(str_half2full(doc), item, str(num), chr(12288))
        return info

    def __repr__(self):
        return "<class '{}'>".format(self.__class__.__name__)


class PrintableObject(_Object, PrintInfoMixin):
    """subclass of _Object + PrintInfoMixin"""


def str_half2full(ins):
    """把字符串半角转全角"""
    outs = ""
    for c in ins:
        code = ord(c)
        if code < 0x0020 or code > 0x007E:
            outs += c
        else:
            if code == 0x0020:
                code += 0x3000
            else:
                code += 0xFEE0
            outs += chr(code)
    
    return outs

