"""
Additional low-level functions to the one provided by cppyy
"""
# pylint: disable=C0303

from cppyy.ll import __all__
from cppyy.ll import *
from .lib import lib

__all__ = list(__all__) + [
    "make_shared",
    "to_pointer",
    "CppType",
]

make_shared = lib.make_shared


def CppType(dtype):
    """
    Returns a base class that allows for automatic type conversion calling
    the look-up method `__cppyy__` to be implemented in the child class.

    ```
    class Double(CppType("double")):

        def __init__(self, value):
                super().__init__()
                self.value=value

        def __cppyy__(self):
                return self.value
    ```
    """
    return lib.CppType[dtype]


def to_pointer(ptr: int, ctype: str = "void *", size: int = None):
    "Casts integer to void pointer"
    ptr = cast[ctype](ptr)
    if size is not None:
        ptr.reshape((size,))
    return ptr
