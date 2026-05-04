"""
Basic loading of the fast C library.
"""
from ctypes import (
    POINTER,
    byref,
    c_char_p,
    c_double,
    c_int,
    c_size_t,
    c_uint,
    c_void_p,
    cdll,
    create_string_buffer,
)
from glob import glob
import platform

from .. import environment

# Determine the appropriate library extension based on platform
if platform.system() == "Windows":
    lib_pattern = "cpygad*.pyd"  # Python extension on Windows
elif platform.system() == "Darwin":
    lib_pattern = "cpygad*.so"   # .so on macOS
else:
    lib_pattern = "cpygad*.so"   # .so on Linux/Unix

lib_path = None
_has_cpygad = False

try:
    lib_path = glob(environment.module_dir + "C/" + lib_pattern)[0]
except IndexError:
    try:
        lib_path = glob(environment.module_dir + lib_pattern)[0]
    except IndexError:
        lib_path = None

if lib_path is not None:
    cpygad = cdll.LoadLibrary(lib_path)
    _has_cpygad = True
else:
    class DummyLib:
        def __getattr__(self, name):
            raise AttributeError(name)
    cpygad = DummyLib()

if _has_cpygad:
    cpygad.cubic.restype = c_double
    cpygad.cubic.argtypes = [c_double, c_double]
    cpygad.quartic.restype = c_double
    cpygad.quartic.argtypes = [c_double, c_double]
    cpygad.quintic.restype = c_double
    cpygad.quintic.argtypes = [c_double, c_double]
    cpygad.Wendland_C2.restype = c_double
    cpygad.Wendland_C2.argtypes = [c_double, c_double]
    cpygad.Wendland_C4.restype = c_double
    cpygad.Wendland_C4.argtypes = [c_double, c_double]
    cpygad.Wendland_C6.restype = c_double
    cpygad.Wendland_C6.argtypes = [c_double, c_double]

    cpygad.Voigt.restype = c_double
    cpygad.Voigt.argtypes = [c_double, c_double, c_double]
