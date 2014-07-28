""" ESON Tag class
"""

class Tag:

    def __init__(self, tag, data):
        self.data = data
        self.tag = tag

    def _self_iterencode(self, _current_indent_level, _iterencode):
        yield '#%s ' % self.tag
        yield from _iterencode(self.data, _current_indent_level)


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
    if tokens[-1] in act:
        del act[tokens[-1]]
