
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
            if item is 'name':
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
            if item is 'name':
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

