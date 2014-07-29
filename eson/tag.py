""" ESON Tag features

Provides:

# Tag representation. #
Used for encoding tags from or, optionally, decoding tags to.

# Tag startegies #
Tag startegy is a fuction, which takes tags identifier and decoded data turns
it into represented object. Several strategies are provided in this module.

# Tag registration tools. #
In standart strategy, handler has to be registred to decode tag.
Handler is a strategy without tag argument - tag is specified during
registration. Handlers can be organized in namespace tree. Namespace is
represented as a dictionary of other namespaces or handlers.
Tag identifiers are paths in the tree. Slash ( '/' ) is the separator. 
"""


class Tag:
    """ Class representing ESON tag. The only way to encode tags.
    """

    def __init__(self, tag, data):
        """ Constructs new Tag object using tag identifier and data object.
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
    """ Registers namespace or handler to given path.
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


def error_strategy(tag, data):
    """ Tag strategy that just throws error
    """
    raise KeyError("Tag %s not registered" % tag)

def ignore_strategy(tag, data):
    """ Tag strategy that ignores tag
    """
    return data

def struct_strategy(tag, data):
    """ Tag strategy decodes tag into Tag object
    """
    return Tag(tag, data)

def make_standard_strategy(default_strategy = error_strategy):
    """ Creates tag strategy which tries to find handler in registered tags.
    If default_strategy is specified it is used when tag is not registered.
    """
    def strategy(tag, data):
        f = resolve(tag)
        if not hasattr(f, '__call__'):
            return default_strategy(tag, data)
        return f(data)
    return strategy


