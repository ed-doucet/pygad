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

try:
    cpygad = cdll.LoadLibrary(glob(environment.module_dir + "C/" + lib_pattern)[0])
except IndexError:
    # Try alternative locations
    try:
        cpygad = cdll.LoadLibrary(glob(environment.module_dir + lib_pattern)[0])
    except IndexError:
        # If no library found, create a dummy object to avoid import errors
        # The Python fallbacks will be used
        class DummyLib:
            def __getattr__(self, name):
                def dummy_func(*args, **kwargs):
                    raise NotImplementedError(f"C extension function {name} not available")
                return dummy_func
        cpygad = DummyLib()

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
