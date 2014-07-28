"""Python ESON implementation using json library
"""

import json
from functools import wraps
from .encoder import ESONEncoder
from .decoder import ESONDecoder


def default_cls(c):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwds):
            if "cls" not in kwds:
                kwds["cls"] = c
            return f(*args, **kwds)
        return wrapper
    return decorator


dump = default_cls(ESONEncoder)(json.dump)
dumps = default_cls(ESONEncoder)(json.dumps)

load = default_cls(ESONDecoder)(json.load)
loads = default_cls(ESONDecoder)(json.loads)
