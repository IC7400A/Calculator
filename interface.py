import platform
import os
import sys
from ctypes import CDLL, c_double

def resource_path(relative_path):
    """Used by PyInstaller to get the resource path"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Choose the appropriate library file
if platform.system() == "Windows":
    lib_name = "libcalc.dll"
else:
    lib_name = "libcalc.so"

lib_path = resource_path(lib_name)
lib = CDLL(lib_path)

# Define function signatures
lib.add.argtypes = [c_double, c_double]
lib.add.restype = c_double

lib.sub.argtypes = [c_double, c_double]
lib.sub.restype = c_double

lib.mul.argtypes = [c_double, c_double]
lib.mul.restype = c_double

lib.divide.argtypes = [c_double, c_double]
lib.divide.restype = c_double
