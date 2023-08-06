from itertools import product
import numpy
from lyncs_cppyy import ll, cppdef, include, gbl, lib
from lyncs_cppyy.numpy import array_to_pointers


def test_to_pointer():
    arr = numpy.arange(10)
    ptr = ll.to_pointer(arr.__array_interface__["data"][0], "long*", size=10)
    assert (arr == list(ptr)).all()


def test_casting():
    class Double(ll.CppType("double")):
        def __init__(self, value):
            super().__init__()
            self.value = value

        def __cppyy__(self):
            return self.value

    val = Double(1234.5678)
    assert ll.cast["double"](val) == 1234.5678
