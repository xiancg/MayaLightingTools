# coding=utf-8


def _import_factories():
    """
    Imports all factories from this package to the package namespace,
    so they can be used as for example: import lightsFactory.default_factory
    """
    import os.path
    import pkgutil
    factoryPath = os.path.dirname(__file__)
    return [name for _, name, _ in pkgutil.iter_modules([factoryPath])]


__all__ = _import_factories()

from . import *  # noqa:F403, F401, E402
