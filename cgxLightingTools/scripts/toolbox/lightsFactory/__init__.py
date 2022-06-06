'''
Created on July 15, 2019
Python 3 refactor, Jun 6, 2022

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
Imports all factories from this package to the package namespace,
so they can be used as for example: import lightsFactory.default_factory
'''


def _import_factories():
    import os.path
    import pkgutil
    factoryPath = os.path.dirname(__file__)
    return [name for _, name, _ in pkgutil.iter_modules([factoryPath])]


__all__ = _import_factories()
from . import *
