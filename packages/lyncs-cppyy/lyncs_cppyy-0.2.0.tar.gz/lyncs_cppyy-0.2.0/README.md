# cppyy wrapper for Lyncs

[![python](https://img.shields.io/pypi/pyversions/lyncs_cppyy.svg?logo=python&logoColor=white)](https://pypi.org/project/lyncs_cppyy/)
[![pypi](https://img.shields.io/pypi/v/lyncs_cppyy.svg?logo=python&logoColor=white)](https://pypi.org/project/lyncs_cppyy/)
[![license](https://img.shields.io/github/license/Lyncs-API/lyncs.cppyy?logo=github&logoColor=white)](https://github.com/Lyncs-API/lyncs.cppyy/blob/master/LICENSE)
[![build & test](https://img.shields.io/github/workflow/status/Lyncs-API/lyncs.cppyy/build%20&%20test?logo=github&logoColor=white)](https://github.com/Lyncs-API/lyncs.cppyy/actions)
[![codecov](https://img.shields.io/codecov/c/github/Lyncs-API/lyncs.cppyy?logo=codecov&logoColor=white)](https://codecov.io/gh/Lyncs-API/lyncs.cppyy)
[![pylint](https://img.shields.io/badge/pylint%20score-9.4%2F10-green?logo=python&logoColor=white)](http://pylint.pycqa.org/)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg?logo=codefactor&logoColor=white)](https://github.com/ambv/black)


In this package we provide some additional features to [cppyy].

[cppyy]: https://cppyy.readthedocs.io/en/latest/

## Installation

The package can be installed via `pip`:

```
pip install [--user] lyncs_cppyy
```

## Documentation

The main documentation of [cppyy] is available at https://cppyy.readthedocs.io/en/latest/.

> cppyy is an automatic, run-time, Python-C++ bindings generator, for calling C++ from Python [...]

Lyncs_cppyy is an additional layer between cppyy and the interfaces to libraries provided by Lyncs.
In the following we give an overview of the additional functionalities.

### Lib class

In cppyy, libraries are loaded and used as follow:

```python
>>> import cppyy
>>> cppyy.include('zlib.h')        # bring in C++ definitions
>>> cppyy.load_library('libz')     # load linker symbols
>>> cppyy.gbl.zlibVersion()        # use a zlib API
'1.2.11'
>>>
```

In lyncs_cppyy we have define the class Lib for holding the information on a library. It is used as follow

```python
>>> from lyncs_cppyy import Lib
>>> zlib = Lib(header = 'zlib.h', library = 'libz')
>>> zlib.zlibVersion()
'1.2.11'
>>>
```

Lib returns a variable that represents the library.
The library is loaded at the first usage of the variable.
In most of the cases, accessing attributes of the variable is like accessing attributed of `cppyy.gbl`.
Exceptions are made for

- macros defined in the headers, e.g. `zlib.ZLIB_VERSION -> '1.2.11'`
- functions defined under a namespace which can be directly accessed specifying a namespace
- and the following attributes of Lib, e.g. `zlib.header -> ['zlib.h']`.

The list of attributes and initialization options of `Lib` are:

- `header`: string(or list) of the header(s) to be included.

- `library`: string(or list) of the shared library(ies) to be loaded.
  A library can also be an instance of the `Lib` class.

- `c_include`: if the library is a c library (`True`) or a c++ library (`False`, default)

- `namespace`: in case of a c++ library, a string(or list) of the namespace(s) to be used.
  Equivalent to `using namespace ...` in c++. Without, symbols should be access as `lib.namespace.*`.

- `path`: string(or list) of the path(s) to the base directory of the library.
  Headers will be searched in `PATH/include` and libraries in `PATH/lib`.

- `include`: string(or list) of the directory(ies) to include. Equivalent to `-I` used at compile time.

- `defined`: dictionary of aliases that act as defined macros.

### Other functions

- `loaded_libraries()`: Returns the list of loaded libraries
- `to_pointer(ptr, ctype="void *")`: Converts an integer (ptr) to cppyy pointer
- `CppType(ctype)`: Generates a base class that allows for automatic type conversion calling
  the look-up method `__cppyy__`. See its doc for more details.
- `array_to_pointers(arr)`: Creates a c-style array of pointers to be used for accessing the elements
  of a numpy-like array.