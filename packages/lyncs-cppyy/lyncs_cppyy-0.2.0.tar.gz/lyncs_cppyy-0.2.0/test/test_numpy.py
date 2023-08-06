import numpy
from lyncs_cppyy import ll, cppdef, include, gbl, lib
from lyncs_cppyy.numpy import array_to_pointers


def test_flatten_array_to_pointers():
    for shape in [(10,), (10, 10), (10, 10, 10), (10, 10, 10, 10)]:  #
        arr = numpy.random.rand(*shape)
        ptrs = array_to_pointers(arr)
        vec = lib.flatten(ptrs, *shape)

        assert vec.size() == arr.size
        assert numpy.allclose(arr.flatten(), numpy.array(vec))
