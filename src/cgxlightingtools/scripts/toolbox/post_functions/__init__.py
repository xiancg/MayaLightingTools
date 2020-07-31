# coding=utf-8
from __future__ import absolute_import, print_function


def _import_post_functions():
    """
    Imports all post_functions from this package to the package namespace,
    so they can be used as for example: import post_functions.default_post_functions
    """
    import os.path
    import pkgutil
    postFuncPath = os.path.dirname(__file__)
    return [name for _, name, _ in pkgutil.iter_modules([postFuncPath])]


__all__ = _import_post_functions()

from . import *  # noqa:F403, F401, E402
