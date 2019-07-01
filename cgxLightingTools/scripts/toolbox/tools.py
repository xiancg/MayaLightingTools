'''
Created on Jun 29, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
TODO: Reimplement isolate methods and all methods that rely on gettingLightNodes
TODO: Build attributes dict from light nodes for lightsManager
'''
import maya.cmds as mc

lightsOff = list()

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
    lightNodes = mc.listNodeTypes('drawdb/light')
    renderEngines = getRenderEngines()
    result = dict()
    for key, value in renderEngines.iteritems():
        dependNodes = mc.pluginInfo(key, query=True, dependNode=True)
        rendererLights = list(set(lightNodes).intersection(dependNodes))
        result[key] = rendererLights
    defaultLightNodes = list()
    for lightsList in result.itervalues():
        defaultLightNodes += list(set(lightsList) ^ set(lightNodes))
    result['default'] = defaultLightNodes

    return result


def getLightNodesList():
    lightNodesDict = getLightNodes()
    lightNodes = list()
    for each in lightNodesDict.itervalues():
        lightNodes += each
    return lightNodes


def getDefaultLightNodes():
    return getLightNodes()['default']


def getRendererLightNodes(renderer='default'):
    if mc.pluginInfo(renderer, query=True, loaded=True) or renderer == 'default':
        return getLightNodes()[renderer]
    else:
        raise ValueError(
            "No renderer named '{}' was found loaded.".format(renderer))
        return None


def simpleIsolateLights():
    lightNodes = getLightNodesList()
    # All scene lights
    allLightsShapes = mc.ls(lights=True, type=lightNodes, long=True)
    allLightsScene = []
    for i in allLightsShapes:
        iTrans = mc.listRelatives(i, parent=True, fullPath=True)
        allLightsScene.append(iTrans[0])

    # Selected scene lights
    selObjs = mc.ls(sl=True, long=True)
    selLights = []
    for e in selObjs:
        eShape = mc.listRelatives(
            e, shapes=True, noIntermediate=True, fullPath=True)
        eNodeType = mc.nodeType(eShape[0])
        if eNodeType in lightNodes:
            selLights.append(e)

    # Toggle visibilities
    for light in allLightsScene:
        # If light is ON but not selected, switch it OFF
        if mc.getAttr(light + ".visibility") == True and light not in selLights:
            mc.setAttr((light + ".visibility"), False)
        #Else, if light is OFF and was not OFF before this command, switch it ON
        elif mc.getAttr(light + ".visibility") == False and light not in lightsOff:
            mc.setAttr((light + ".visibility"), True)


def storeLightsOffStatus():
    allLightsScene = list()
    del lightsOff[:]
    lightNodes = getLightNodesList()
    allLightsShapes = mc.ls(lights=True, type=lightNodes, long=True)
    for i in allLightsShapes:
        iTrans = mc.listRelatives(i, parent=True, fullPath=True)[0]
        allLightsScene.append(iTrans)
    for light in allLightsScene:
        if mc.getAttr(light + ".visibility") == False:
            lightsOff.append(light)

storeLightsOffStatus()

def main():
    print getRenderEngines()
    print getLightNodes()


if __name__ == '__main__' or 'eclipsePython' in __name__:
    main()
