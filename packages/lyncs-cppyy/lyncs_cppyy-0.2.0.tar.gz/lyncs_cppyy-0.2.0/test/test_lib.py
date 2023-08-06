import os
import pytest
import tempfile
from lyncs_cppyy import Lib, cppdef, gbl, loaded_libraries


def build_meson(sourcedir):
    from mesonbuild import mesonmain

    builddir = tempfile.mkdtemp()
    assert (
        mesonmain.run(
            [
                "setup",
                "--prefix",
                builddir,
                "--libdir",
                builddir + "/lib",
                builddir,
                sourcedir,
            ],
            "meson",
        )
        == 0
    )
    assert mesonmain.run(["compile", "-C", builddir], "meson") == 0
    assert mesonmain.run(["install", "-C", builddir], "meson") == 0
    return builddir


try:
    path = build_meson("test/cnumbers")
    skip = False
except ImportError:
    skip = True

skip = pytest.mark.skipif(skip, reason="Meson not available")


@skip
def test_cnumbers():
    cnumbers = Lib(
        header="numbers.h",
        library="libnumbers.so",
        c_include=True,
        path=path,
    )
    assert cnumbers.zero() == 0
    assert cnumbers.one() == 1
    assert cnumbers.ZERO == 0
    assert cnumbers.ONE == 1

    # Cppyy cannot access macros.
    with pytest.raises(AttributeError):
        gbl.ZERO

    with pytest.raises(AttributeError):
        cnumbers.TWO

    with pytest.raises(RuntimeError):
        cnumbers.load()

    cnumbers.GLOBAL = 5
    assert cnumbers.GLOBAL == 5
    assert getattr(cnumbers, "global")() == 5

    cppnumbers = Lib(
        header="numbers.hpp",
        path=path,
        namespace="numbers",
        include=path + "/include",  # Not needed
        library=Lib(),  # Not needed
        defined={"uno": "one", "GBL": "gbl"},
    )

    assert cppnumbers.zero["int"]() == 0
    assert cppnumbers.one["long"]() == 1
    assert cppnumbers.uno["long"]() == 1

    assert cppnumbers.ONE == 1

    cppnumbers.GBL = 1
    assert getattr(cppnumbers, "global")["int"]() == 1

    cppnumbers.GLOBAL = 1
    assert getattr(cnumbers, "global")() == 1


@skip
def test_symlink():
    os.symlink("libnumbers.so", path + "/lib/libnumbers2.so")
    cnumbers = Lib(
        header="numbers.h",
        library="libnumbers2.so",
        c_include=True,
        path=path,
    )
    assert cnumbers.zero() == 0


@skip
def test_errors():
    with pytest.raises(TypeError):
        Lib(header=[10])

    with pytest.raises(ValueError):
        Lib().get_macro("FOO")


@skip
def test_loaded_libraries():
    assert path + "/libnumbers.so" in loaded_libraries()
    assert "libnumbers" in loaded_libraries(short=True)
