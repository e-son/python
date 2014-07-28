""" ESON Tag class
"""

class Tag:

    def __init__(self, tag, data):
        self.data = data
        self.tag = tag

    def _self_iterencode(self, _current_indent_level, _iterencode):
        yield '#%s ' % self.tag
        yield from _iterencode(self.data, _current_indent_level)

