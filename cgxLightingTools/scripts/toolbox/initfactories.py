'''
Created on Aug 30, 2019
Python 3 refactor, Jun 6, 2022

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
'''

import os
import pkgutil
import inspect

from cgxLightingTools.scripts.toolbox import tools
import cgxLightingTools.scripts.toolbox.lightsFactory as lightsFactory


def init_factories():
    defaultFactory = lightsFactory.default_factory.LightsFactory()
    result = {'default': defaultFactory}
    renderers = tools.getRenderEngines()
    if renderers is not None:
        rendererNames = renderers.keys()
        factoryPath = os.path.dirname(lightsFactory.__file__)
        factories = [name for _, name, _ in pkgutil.iter_modules([factoryPath])
                     if name.endswith('factory')]
        for factory in factories:
            if factory.rsplit('_')[0] in rendererNames:
                for name, obj in inspect.getmembers(eval(f'lightsFactory.{factory}')):
                    if inspect.isclass(obj) and name != 'LightsFactory':
                        factoryObj = eval(f'lightsFactory.{factory}.{name}()')
                        result[factory.split('_')[0]] = factoryObj
                        break
    return result
