""" ESON Tag features

Provides:

# Tag representation. #
Used for encoding tags from or, optionally, decoding tags to.


# Tag registration tools. #
To decode tag, you need have registered it with
handler function which transforms decoded data to final object.
Tags can be organized in namespace tree. Tag identifiers are paths in this tree
using slash ( '/' ) as a separator. Namespace is represented by dict object
where values can be other namespaces or handlers.
"""


class Tag:
    """ Class representing ESON tag. The only way to encode tags.
    """

    def __init__(self, tag, data):
        """ Constructs new Tag object using tag string and data object.
        """
        self.data = data
        self.tag = tag

    def __str__(self):
        return '#%s %s' % (self.tag, str(self.data))

    def __repr__(self):
        return '<%s.%s object, tag="%s", data=%s>' % (
            self.__module__,
            self.__class__.__name__,
            self.tag,
            repr(self.data)
        )


""" Tag namespace root
"""
_root = {}


def resolve(path):
    """ Returns object at given path in namespace tree.
    Returns None if path does not exist.
    """
    tokens = path.split('/')
    act = _root
    for t in tokens:
        if act == None:
            return None
        act = act.get(t)
    return act


def register(path, o):
    """ Registers object to given path.
    Parent namespace have to exist but path itself not.
    """
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
    """ Deletes whole subtree of given path if exists
    """
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
        f = resolve(tag)
        if not hasattr(f, '__call__'):
            return default(tag, data)
        return f(data)
    return handler


