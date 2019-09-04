'''
@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
Imports all post_functions from this package to the package namespace,
so they can be used as for example: import post_functions.default_post_functions
'''

def _import_post_functions():
    import os.path
    import pkgutil
    postFuncPath = os.path.dirname(__file__)
    return [name for _, name, _ in pkgutil.iter_modules([postFuncPath])]
__all__ = _import_post_functions()
from . import *