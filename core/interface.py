# core/interface.py
# Loads the C library and defines all function prototypes.

import ctypes, os, platform, sys

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

system = platform.system()
lib_name = "calc_functions.dll" if system == "Windows" else "libcalc_functions.so"
lib_path = resource_path(lib_name)

try:
    lib = ctypes.CDLL(lib_path)
    def setup(name, arg_types, restype=ctypes.c_double):
        func = getattr(lib, name)
        func.argtypes = arg_types
        func.restype = restype

    # Setup all C functions
    setup('add', [ctypes.c_double, ctypes.c_double])
    setup('sub', [ctypes.c_double, ctypes.c_double])
    setup('mul', [ctypes.c_double, ctypes.c_double])
    setup('divide', [ctypes.c_double, ctypes.c_double])
    setup('power', [ctypes.c_double, ctypes.c_double])
    setup('root', [ctypes.c_double])
    setup('modulo', [ctypes.c_double, ctypes.c_double])
    setup('power_of_two', [ctypes.c_double])
    setup('inverse', [ctypes.c_double])
    setup('sine', [ctypes.c_double, ctypes.c_int])
    setup('cosine', [ctypes.c_double, ctypes.c_int])
    setup('tangent', [ctypes.c_double, ctypes.c_int])
    setup('arcsin', [ctypes.c_double, ctypes.c_int])
    setup('arccos', [ctypes.c_double, ctypes.c_int])
    setup('arctan', [ctypes.c_double, ctypes.c_int])
    setup('sinh_', [ctypes.c_double])
    setup('cosh_', [ctypes.c_double])
    setup('tanh_', [ctypes.c_double])
    setup('asinh_', [ctypes.c_double])
    setup('acosh_', [ctypes.c_double])
    setup('atanh_', [ctypes.c_double])
    setup('natural_log', [ctypes.c_double])
    setup('base10_log', [ctypes.c_double])
    setup('exp_func', [ctypes.c_double])
    setup('factorial', [ctypes.c_double])

except (OSError, AttributeError) as e:
    print(f"--- WARNING: C library not found or invalid. Using Python fallback. Error: {e} ---")
    lib = None