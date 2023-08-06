from collections import OrderedDict
from contextlib import suppress

from .native import NativePackageCompiler

__all__ = [
    'COMPILATOR_MAP',
]


COMPILATOR_MAP = OrderedDict((
    ('py_compile', NativePackageCompiler),
))


with suppress(ImportError):
    from .cython import CythonPackageCompiler

    COMPILATOR_MAP['cython'] = CythonPackageCompiler
