'''
Created on Jun 29, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
TODO: Reimplement isolate methods and all methods that rely on gettingLightNodes
TODO: Build attributes dict from light nodes for lightsManager
'''
import maya.cmds as mc


def getRenderEngines():
    allPlugins = mc.pluginInfo(query=True, listPlugins=True)
    renderEngines = dict()
    for each in allPlugins:
        registeredRenderers = mc.pluginInfo(each, query=True, renderer=True)
        if registeredRenderers is not None:
            renderEngines[each] = registeredRenderers

    if len(renderEngines.keys()) == 0:
        return None
    return renderEngines

def getLightNodes():
    lightNodes = mc.listNodeTypes( 'drawdb/light' )
    renderEngines = getRenderEngines()
    result = dict()
    for key,value in renderEngines.iteritems():
        dependNodes = mc.pluginInfo(key, query=True, dependNode=True)
        rendererLights = list(set(lightNodes).intersection(dependNodes))
        result[key] = rendererLights
    defaultLightNodes = list()
    for lightsList in result.itervalues():
        defaultLightNodes += list(set(lightsList) ^ set(lightNodes))
    result['default'] = defaultLightNodes

    return result

def getDefaultLightNodes():
    return getLightNodes()['default']

def getRendererLightNodes(renderer='default'):
    if mc.pluginInfo(renderer, query=True, loaded=True) or renderer == 'default':
        return getLightNodes()[renderer]
    else:
        raise ValueError("No renderer named '{}' was found loaded.".format(renderer))
        return None

def main():
    print getRenderEngines()
    print getLightNodes()


if __name__ == '__main__' or 'eclipsePython' in __name__:
    main()
