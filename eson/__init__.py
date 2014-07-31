r"""Python ESON <https://github.com/e-son/ESON> implementation.

:mod:`eson` is an edited copy of standard python module :mod:`json`.
Therefore, it coppies :mod:`json`'s API, which is similar to :mod:`pickle`.

Encoding basic Python object hierarchies::

    >>> import eson
    >>> eson.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
    '["foo", {"bar": ["baz", null, 1.0, 2]}]'
    >>> print eson.dumps("\"foo\bar")
    "\"foo\bar"
    >>> print eson.dumps(u'\u1234')
    "\u1234"
    >>> print eson.dumps('\\')
    "\\"
    >>> print eson.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True)
    {"a": 0, "b": 0, "c": 0}
    >>> from StringIO import StringIO
    >>> io = StringIO()
    >>> eson.dump(['streaming API'], io)
    >>> io.getvalue()
    '["streaming API"]'

Encoding tags::

    >>> import eson
    >>> from eson.tag import Tag
    >>> eson.dumps(Tag("hello","world"))
    '#hello "world"'
    >>> eson.dumps([ Tag("foo",[4, 2]), Tag("out",Tag("in",42))])
    '[#foo [4, 2], #out #in 42]'

Compact encoding::

    >>> import eson
    >>> eson.dumps([1,2,3,{'4': 5, '6': 7}], sort_keys=True, separators=(',',':'))
    '[1,2,3,{"4":5,"6":7}]'

Pretty printing::

    >>> import eson
    >>> print eson.dumps({'4': 5, '6': 7}, sort_keys=True,
    ...                  indent=4, separators=(',', ': '))
    {
        "4": 5,
        "6": 7
    }

Decoding JSON::

    >>> import eson
    >>> obj = [u'foo', {u'bar': [u'baz', None, 1.0, 2]}]
    >>> eson.loads('["foo", {"bar":["baz", null, 1.0, 2]}]') == obj
    True
    >>> eson.loads('"\\"foo\\bar"') == u'"foo\x08ar'
    True
    >>> from StringIO import StringIO
    >>> io = StringIO('["streaming API"]')
    >>> eson.load(io)[0] == 'streaming API'
    True

Decoding tags::

    >>> import eson
    >>> import eson.tag
    >>> def to_tuple(data):
    ...     print("Called handler on " + str(data))
    ...     return tuple(data)
    ... 
    >>> eson.tag.register("tuple",to_tuple)
    >>> eson.loads('#tuple [true, "two", 3]')
    Called handler on [True, 'two', 3]
    (True, 'two', 3)

Specializing ESON object decoding::

    >>> import eson
    >>> def as_complex(dct):
    ...     if '__complex__' in dct:
    ...         return complex(dct['real'], dct['imag'])
    ...     return dct
    ...
    >>> eson.loads('{"__complex__": true, "real": 1, "imag": 2}',
    ...     object_hook=as_complex)
    (1+2j)
    >>> from decimal import Decimal
    >>> eson.loads('1.1', parse_float=Decimal) == Decimal('1.1')
    True

Specializing tag decoding::

    >>> import eson
    >>> import eson.tag
    >>> eson.loads("#foo [4, #poo 5]", tag_strategy = eson.tag.ignore_strategy)
    [4, 5]
    >>> eson.loads("#foo 42", tag_strategy = eson.tag.struct_strategy)
    <eson.tag.Tag object, tag="foo", data=42>
    >>> def my_strategy(tag, data):
    ...     return (tag, data)
    ... 
    >>> eson.loads("#foo 42", tag_strategy = my_strategy)
    ('foo', 42)

Specializing ESON object encoding::

    >>> import eson
    >>> from eson.tag import Tag
    >>> def object_encode(o):         
    ...     return Tag(o.__class__.__name__, o.__dict__)
    ... 
    >>> class Foo:
    ...     def __init__(self, data):
    ...         self.data = data
    ... 
    >>> eson.dumps(Foo(42),default=object_encode)
    '#Foo {"data": 42}'
    >>> foo = Foo(47)
    >>> foo.toESON = lambda self: Tag("foo", self.data)
    >>> eson.dumps(foo)
    '#foo 47'

"""

__all__ = [
    'dump', 'dumps', 'load', 'loads',
    'ESONDecoder', 'ESONEncoder',
]

from .decoder import ESONDecoder
from .encoder import ESONEncoder

_default_encoder = ESONEncoder(
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    indent=None,
    separators=None,
    default=None,
)

def dump(obj, fp, skipkeys=False, ensure_ascii=True, check_circular=True,
        allow_nan=True, cls=None, indent=None, separators=None,
        default=None, sort_keys=False, **kw):
    """Serialize ``obj`` as a ESON formatted stream to ``fp`` (a
    ``.write()``-supporting file-like object).

    If ``skipkeys`` is true then ``dict`` keys that are not basic types
    (``str``, ``int``, ``float``, ``bool``, ``None``) will be skipped
    instead of raising a ``TypeError``.

    If ``ensure_ascii`` is false, then the strings written to ``fp`` can
    contain non-ASCII characters if they appear in strings contained in
    ``obj``. Otherwise, all such characters are escaped in ESON strings.

    If ``check_circular`` is false, then the circular reference check
    for container types will be skipped and a circular reference will
    result in an ``OverflowError`` (or worse).

    If ``allow_nan`` is false, then it will be a ``ValueError`` to
    serialize out of range ``float`` values (``nan``, ``inf``, ``-inf``)
    in strict compliance of the ESON specification, instead of using the
    JavaScript equivalents (``NaN``, ``Infinity``, ``-Infinity``).

    If ``indent`` is a non-negative integer, then ESON array elements and
    object members will be pretty-printed with that indent level. An indent
    level of 0 will only insert newlines. ``None`` is the most compact
    representation.

    If specified, ``separators`` should be an ``(item_separator, key_separator)``
    tuple.  The default is ``(', ', ': ')`` if *indent* is ``None`` and
    ``(',', ': ')`` otherwise.  To get the most compact ESON representation,
    you should specify ``(',', ':')`` to eliminate whitespace.

    ``default(obj)`` is a function that should return a serializable version
    of obj or raise TypeError. The default simply raises TypeError.

    If *sort_keys* is ``True`` (default: ``False``), then the output of
    dictionaries will be sorted by key.

    To use a custom ``ESONEncoder`` subclass (e.g. one that overrides the
    ``.default()`` method to serialize additional types), specify it with
    the ``cls`` kwarg; otherwise ``ESONEncoder`` is used.

    """
    # cached encoder
    if (not skipkeys and ensure_ascii and
        check_circular and allow_nan and
        cls is None and indent is None and separators is None and
        default is None and not sort_keys and not kw):
        iterable = _default_encoder.iterencode(obj)
    else:
        if cls is None:
            cls = ESONEncoder
        iterable = cls(skipkeys=skipkeys, ensure_ascii=ensure_ascii,
            check_circular=check_circular, allow_nan=allow_nan, indent=indent,
            separators=separators,
            default=default, sort_keys=sort_keys, **kw).iterencode(obj)
    # could accelerate with writelines in some versions of Python, at
    # a debuggability cost
    for chunk in iterable:
        fp.write(chunk)


def dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True,
        allow_nan=True, cls=None, indent=None, separators=None,
        default=None, sort_keys=False, **kw):
    """Serialize ``obj`` to a ESON formatted ``str``.

    If ``skipkeys`` is false then ``dict`` keys that are not basic types
    (``str``, ``int``, ``float``, ``bool``, ``None``) will be skipped
    instead of raising a ``TypeError``.

    If ``ensure_ascii`` is false, then the return value can contain non-ASCII
    characters if they appear in strings contained in ``obj``. Otherwise, all
    such characters are escaped in ESON strings.

    If ``check_circular`` is false, then the circular reference check
    for container types will be skipped and a circular reference will
    result in an ``OverflowError`` (or worse).

    If ``allow_nan`` is false, then it will be a ``ValueError`` to
    serialize out of range ``float`` values (``nan``, ``inf``, ``-inf``) in
    strict compliance of the ESON specification, instead of using the
    JavaScript equivalents (``NaN``, ``Infinity``, ``-Infinity``).

    If ``indent`` is a non-negative integer, then ESON array elements and
    object members will be pretty-printed with that indent level. An indent
    level of 0 will only insert newlines. ``None`` is the most compact
    representation.

    If specified, ``separators`` should be an ``(item_separator, key_separator)``
    tuple.  The default is ``(', ', ': ')`` if *indent* is ``None`` and
    ``(',', ': ')`` otherwise.  To get the most compact ESON representation,
    you should specify ``(',', ':')`` to eliminate whitespace.

    ``default(obj)`` is a function that should return a serializable version
    of obj or raise TypeError. The default simply raises TypeError.

    If *sort_keys* is ``True`` (default: ``False``), then the output of
    dictionaries will be sorted by key.

    To use a custom ``ESONEncoder`` subclass (e.g. one that overrides the
    ``.default()`` method to serialize additional types), specify it with
    the ``cls`` kwarg; otherwise ``ESONEncoder`` is used.

    """
    # cached encoder
    if (not skipkeys and ensure_ascii and
        check_circular and allow_nan and
        cls is None and indent is None and separators is None and
        default is None and not sort_keys and not kw):
        return _default_encoder.encode(obj)
    if cls is None:
        cls = ESONEncoder
    return cls(
        skipkeys=skipkeys, ensure_ascii=ensure_ascii,
        check_circular=check_circular, allow_nan=allow_nan, indent=indent,
        separators=separators, default=default, sort_keys=sort_keys,
        **kw).encode(obj)


_default_decoder = ESONDecoder(object_hook=None, object_pairs_hook=None)


def load(fp, cls=None, object_hook=None, parse_float=None,
        parse_int=None, parse_constant=None, object_pairs_hook=None, 
        tag_strategy = None, **kw):
    """Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
    a ESON document) to a Python object.

    ``object_hook`` is an optional function that will be called with the
    result of any object literal decode (a ``dict``). The return value of
    ``object_hook`` will be used instead of the ``dict``. This feature
    can be used to implement custom decoders (e.g. ESON-RPC class hinting).

    ``object_pairs_hook`` is an optional function that will be called with the
    result of any object literal decoded with an ordered list of pairs.  The
    return value of ``object_pairs_hook`` will be used instead of the ``dict``.
    This feature can be used to implement custom decoders that rely on the
    order that the key and value pairs are decoded (for example,
    collections.OrderedDict will remember the order of insertion). If
    ``object_hook`` is also defined, the ``object_pairs_hook`` takes priority.

    ``tag_strategy``, if specified, it is used to handle tag instead of
    classic strategy. Strategy is a function from (tag, data) to parsed
    value. See eson.tag module for some default strategies.

    To use a custom ``ESONDecoder`` subclass, specify it with the ``cls``
    kwarg; otherwise ``ESONDecoder`` is used.

    """
    return loads(fp.read(),
        cls=cls, object_hook=object_hook,
        parse_float=parse_float, parse_int=parse_int,
        parse_constant=parse_constant, object_pairs_hook=object_pairs_hook,
        tag_strategy = tag_strategy, **kw)


def loads(s, encoding=None, cls=None, object_hook=None, parse_float=None,
        parse_int=None, parse_constant=None, object_pairs_hook=None,
        tag_strategy = None, **kw):
    """Deserialize ``s`` (a ``str`` instance containing a ESON
    document) to a Python object.

    ``object_hook`` is an optional function that will be called with the
    result of any object literal decode (a ``dict``). The return value of
    ``object_hook`` will be used instead of the ``dict``. This feature
    can be used to implement custom decoders (e.g. ESON-RPC class hinting).

    ``object_pairs_hook`` is an optional function that will be called with the
    result of any object literal decoded with an ordered list of pairs.  The
    return value of ``object_pairs_hook`` will be used instead of the ``dict``.
    This feature can be used to implement custom decoders that rely on the
    order that the key and value pairs are decoded (for example,
    collections.OrderedDict will remember the order of insertion). If
    ``object_hook`` is also defined, the ``object_pairs_hook`` takes priority.

    ``parse_float``, if specified, will be called with the string
    of every ESON float to be decoded. By default this is equivalent to
    float(num_str). This can be used to use another datatype or parser
    for ESON floats (e.g. decimal.Decimal).

    ``parse_int``, if specified, will be called with the string
    of every ESON int to be decoded. By default this is equivalent to
    int(num_str). This can be used to use another datatype or parser
    for ESON integers (e.g. float).

    ``parse_constant``, if specified, will be called with one of the
    following strings: -Infinity, Infinity, NaN, null, true, false.
    This can be used to raise an exception if invalid ESON numbers
    are encountered.

    ``tag_strategy``, if specified, it is used to handle tag instead of
    classic strategy. Strategy is a function from (tag, data) to parsed
    value. See eson.tag module for some default strategies.

    To use a custom ``ESONDecoder`` subclass, specify it with the ``cls``
    kwarg; otherwise ``ESONDecoder`` is used.

    The ``encoding`` argument is ignored and deprecated.

    """
    if not isinstance(s, str):
        raise TypeError('the ESON object must be str, not {!r}'.format(
                            s.__class__.__name__))
    if s.startswith(u'\ufeff'):
        raise ValueError("Unexpected UTF-8 BOM (decode using utf-8-sig)")
    if (cls is None and object_hook is None and
            parse_int is None and parse_float is None and
            parse_constant is None and object_pairs_hook is None and
            tag_strategy is None and not kw):
        return _default_decoder.decode(s)
    if cls is None:
        cls = ESONDecoder
    if object_hook is not None:
        kw['object_hook'] = object_hook
    if object_pairs_hook is not None:
        kw['object_pairs_hook'] = object_pairs_hook
    if parse_float is not None:
        kw['parse_float'] = parse_float
    if parse_int is not None:
        kw['parse_int'] = parse_int
    if parse_constant is not None:
        kw['parse_constant'] = parse_constant
    if tag_strategy is not None:
        kw['tag_strategy'] = tag_strategy
    return cls(**kw).decode(s)

