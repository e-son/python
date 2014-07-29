""" ESON Tag class
"""

class Tag:

    def __init__(self, tag, data):
        self.data = data
        self.tag = tag

    def _self_iterencode(self, _current_indent_level, _iterencode):
        yield '#%s ' % self.tag
        for chunk in _iterencode(self.data, _current_indent_level):
            yield chunk

    def __str__(self):
        return '#%s %s' % (self.tag, str(self.data))

    def __repr__(self):
        return '<%s.%s object, tag="%s", data=%s>' % (
            self.__module__,
            self.__class__.__name__,
            self.tag,
            repr(self.data)
        )



_root = {}


def resolve(path):
    tokens = path.split('/')
    act = _root
    for t in tokens:
        if act == None:
            return None
        act = act.get(t)
    return act


def register(path, o):
    tokens = path.split('/')
    act = _root
    for t in tokens[:-1]:
        if act == None:
            raise ValueError("Parent namespace not registered")
        act = act.get(t)
    if act == None:
        raise ValueError("Parent namespace not registered")
    if tokens[-1] in act:
        raise ValueError("Path already in use")
    act[tokens[-1]] = o

 
def delete(path):
    tokens = path.split('/')
    act = _root
    for t in tokens[:-1]:
        if act == None:
            return
        act = act.get(t)
    if act and tokens[-1] in act:
        del act[tokens[-1]]


def error_handler(tag, data):
    raise KeyError("Tag %s not registered" % tag)

def ignore_handler(tag, data):
    return data

def struct_handler(tag, data):
    return Tag(tag, data)

def make_standard_handler(default = error_handler):
    def handler(tag, data):
        f = resolve(tag) or default
        return f(tag, data)
    return handler


