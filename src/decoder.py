""" ESONDecoder - extended JSONDeccoder
"""

from json.decoder import JSONDecoder
from .scanner import py_make_eson_scanner


__all__ = ['ESONDecoder']


class ESONDecoder (JSONDecoder):

    def __init__(self, *args, **kwargs):
        super(ESONDecoder, self).__init__(*args, **kwargs)
        self.scan_once = py_make_eson_scanner(self)

