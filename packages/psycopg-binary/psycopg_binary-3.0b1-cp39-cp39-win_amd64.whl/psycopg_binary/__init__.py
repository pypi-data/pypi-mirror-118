"""
psycopg -- PostgreSQL database adapter for Python -- C optimization package
"""


""""""  # start delvewheel patch
def _delvewheel_init_patch_0_0_14():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'psycopg_binary.libs'))
    if sys.version_info[:2] >= (3, 8):
        if os.path.exists(os.path.join(sys.base_prefix, 'conda-meta')):
            os.environ['CONDA_DLL_SEARCH_MODIFICATION_ENABLE']='1'
        os.add_dll_directory(libs_dir)
    else:
        from ctypes import WinDLL
        with open(os.path.join(libs_dir, '.load-order-psycopg_binary-3.0b1')) as file:
            load_order = file.read().split()
        for lib in load_order:
            WinDLL(os.path.join(libs_dir, lib))


_delvewheel_init_patch_0_0_14()
del _delvewheel_init_patch_0_0_14
# end delvewheel patch



# Copyright (C) 2020-2021 The Psycopg Team

import sys

# This package shouldn't be imported before psycopg itself, or weird things
# will happen
if "psycopg" not in sys.modules:
    raise ImportError(
        "the psycopg package should be imported before psycopg_binary"
    )

from .version import __version__  # noqa