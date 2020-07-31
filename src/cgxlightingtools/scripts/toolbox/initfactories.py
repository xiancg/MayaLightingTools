# coding=utf-8
from __future__ import absolute_import, print_function

import os
import pkgutil
import inspect

from cgxlightinglools.scripts.toolbox import tools
import cgxlightinglools.scripts.toolbox.lightsFactory as lightsFactory


def init_factories():
    defaultFactory = lightsFactory.default_factory.LightsFactory()
    result = {'default': defaultFactory}
    renderers = tools.getRenderEngines()
    if renderers is not None:
        rendererNames = renderers.keys()
        factoryPath = os.path.dirname(lightsFactory.__file__)
        factories = [
            name for _, name, _ in pkgutil.iter_modules([factoryPath])
            if name.endswith('factory')
        ]
        for factory in factories:
            if factory.rsplit('_')[0] in rendererNames:
                for name, obj in inspect.getmembers(eval('lightsFactory.{}'.format(factory))):
                    if inspect.isclass(obj) and name != 'LightsFactory':
                        factoryObj = eval('lightsFactory.{}.{}()'.format(factory, name))
                        result[factory.split('_')[0]] = factoryObj
                        break
    return result


# --------------------------------------------------------
#  Main
# --------------------------------------------------------
def main():
    pass


if __name__ == '__main__' or 'eclipsePython' in __name__:
    main()
