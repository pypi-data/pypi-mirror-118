"""
Cppyy interface for Lyncs

In this package we provide some additional tools for the usage of
[cppyy](https://cppyy.readthedocs.io/en/latest/) in the Lyncs API.
"""

__version__ = "0.2.0"

from cppyy import nullptr, cppdef, gbl, include, c_include, set_debug
from .lib import *
from .numpy import *
from .ll import *
