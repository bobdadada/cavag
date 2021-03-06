from copy import copy
import textwrap
from collections import UserDict
from collections.abc import Sequence
import abc

class PropertyLost(Exception):
    """Exception raised when necessary property are lost."""


class PropertySet(UserDict):
    
    def __init__(self, required_props=(), *args, **kwargs):
        self.__required_props = set(required_props)
        super().__init__(*args, **kwargs)
        for prop in self.__required_props:
            if prop not in self:
                self[prop] = None
    
    def get_strictly(self, key, default=None):
        value = self.get(key, default=default)
        if (key in self.__required_props) and (value is None):
            raise PropertyLost("property '%s' lost!"%key)
        return value
    
    def change_params(self, **kwargs):
        """
        This function will firstly clear all other keys except the necessary keys.
        And Then change the value in the input parameters **kwargs.
        """
        dt = {}
        for prop in self.__required_props:
            dt[prop] = self[prop]
        dt.update(kwargs)

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


class Object(object):
    name = 'Object'
    modifiable_properties = ()
    
    def __init__(self, name='Object', **kwargs):
        self.property_set = PropertySet(Object.modifiable_properties)
        self.name = name
        
        for prop in Object.modifiable_properties:
            self.property_set[prop] = kwargs.get(prop, None)

    def get_property(self, k, v_f=None):
        if (k not in self.property_set) or (self.property_set[k] is None):
            if v_f is None:
                raise PropertyLost("cannot calculate property '%s'"%k)
            else:
                self.property_set[k] = v_f()
        return self.property_set.get_strictly(k)

    def preprocess_properties(self, **propdict):
        return propdict
    
    @classmethod
    def filter_properties(cls, **propdict):
        dt = {k:v for k, v in propdict.items() if k.startswith('_')}
        for prop in cls.modifiable_properties:
            if prop in propdict:
                dt[prop] = propdict[prop]
        return dt
    
    def postprocess_properties(self, **propdict):
        return propdict
    
    def __filter_params(self, dp):
        dt = {}
        for k, v in dp.items():
            if not k.startswith('_'):
                dt[k] = v
        return dt

    def update_propset(self, **propdict):
        self.property_set.change_params(**self.__filter_params(propdict))
    
    def change_params(self, _filter=True, **kwargs):
        if _filter:
            kwargs = self.filter_properties(**kwargs)
        kwargs = self.preprocess_properties(**kwargs)
        self.update_propset(**kwargs)
        self.postprocess_properties(**kwargs)
    
    def __parse_property(self, p):
        try:
            if isinstance(getattr(self.__class__, p), property):
                return True
            else:
                return False
        except:
            return False

    def get_proplist(self):
        props = []
        for item in dir(self):
            if self.__parse_property(item):
                props.append(item)
        return props    


class PrintInfoMixin(object):

    @abc.abstractmethod    
    def get_proplist(self):
        pass

    def __str__(self):
        # 名称
        if getattr(self, 'name', None):
            info = "{}:\n".format(self.name)
        else:
            info = "{}:\n".format(self.__class__.__name__)
        
        # 属性
        for prop in self.get_proplist():
            try:
                val = getattr(self, prop)
                doc = getattr(self.__class__, prop).__doc__
                if doc is None:
                    doc = ''
                # 格式化输出，中文对齐
                info += "    {0:{3}<15}{1:<11}=\n{2:s}\n".format(str_half2full(textwrap.dedent(doc)),
                                                        prop,
                                                        textwrap.indent(str(val), ' '*8),
                                                        chr(12288))
            except:
                pass
            
        return info


class PrintableObject(Object, PrintInfoMixin):
    """subclass of Object + PrintInfoMixin"""


def str_half2full(ins):
    """把字符串半角转全角"""
    outs = ""
    for c in ins:
        code = ord(c)
        if code < 0x0020 or code > 0x007E:
            outs += c
        else:
            if code == 0x0020:
                code == 0x3000
            else:
                code += 0xFEE0
            outs += chr(code)
    
    return outs

