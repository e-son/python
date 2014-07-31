""" Module containing ESON built-in tags implementations
"""

from ..encoder import _ESONable_classes
from ..tag import register


# Registers core namespace
register('core', {})


def decoder(identifier):
    """ Creates decorator that registers function
    as a decoder for a given identifier
    """
    def decorator(f):
        register(identifier, f)
        return f
    return decorator


def encoder(cls):
    """ Creates decorator that registers function
    as an encoder for a given class
    """
    def decorator(f):
        _ESONable_classes[cls] = f
        return f
    return decorator


### IMPORT ALL SUBMODULES ###

from . import dt


