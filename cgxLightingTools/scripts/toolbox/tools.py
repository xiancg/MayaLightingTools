'''
Created on Jun 29, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
TODO: Write light creation library
TODO: Build attributes dict from light nodes for lightsManager
TODO: Refactor harcoded naming in specularConstrain
'''
import maya.cmds as mc
import logging
import sys
import os

lightsOff = list()
renderEngines = dict()
lightNodesDict = dict()

def initLogger(fileLog=False):
    global logger
    logger = logging.getLogger(name='lgtToolsLog')
    logger.setLevel(logging.DEBUG)
    #Formatter
    formatter = logging.Formatter(
                '[%(asctime)s:%(module)s:%(funcName)s:%(lineno)s:%(levelname)s] %(message)s')
    #STDOUT stream
    streamHandler = logging.StreamHandler(sys.stdout)
    streamHandler.setLevel(logging.WARNING)
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)
    #Log file stream
    if fileLog:
        userPath = os.path.expanduser("~")
        finalDir = userPath + "/.CGXTools"
        if not os.path.exists(finalDir):
            os.mkdir(finalDir)
        fileHandler = logging.FileHandler(finalDir + '/lgtTools.log', mode='w')
        fileHandler.setLevel(logging.DEBUG)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)


def getRenderEngines():
    allPlugins = mc.pluginInfo(query=True, listPlugins=True)
    for each in allPlugins:
        registeredRenderers = mc.pluginInfo(each, query=True, renderer=True)
        if registeredRenderers is not None:
            renderEngines[each] = registeredRenderers

    if len(renderEngines.keys()) == 0:
        logger.critical('No render engines found.')
        return None
    logger.info('Found these render engines: {}'.format(','.join(renderEngines.keys())))
    return renderEngines


def getLightNodes():
    lightNodes = mc.listNodeTypes('drawdb/light')
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
    lightNodes = list()
    for each in lightNodesDict.itervalues():
        lightNodes += each
    return lightNodes


def getDefaultLightNodes():
    return lightNodesDict['default']


def getRendererLightNodes(renderer='default'):
    if mc.pluginInfo(renderer, query=True, loaded=True) or renderer == 'default':
        return lightNodesDict[renderer]
    else:
        logger.warning("No renderer named '{}' was found loaded.".format(renderer))
        return None


def getLightsInScene():
    lightNodes = getLightNodesList()
    # All scene lights
    allLightsShapes = mc.ls(lights=True, type=lightNodes, long=True)
    allLightsScene = list()
    for i in allLightsShapes:
        iTrans = mc.listRelatives(i, parent=True, fullPath=True)
        allLightsScene.append(iTrans[0])

    return allLightsScene


def getSelectedLights():
    lightNodes = getLightNodesList()
    selObjs = mc.ls(sl=True, long=True)
    selLights = list()
    for e in selObjs:
        eShape = mc.listRelatives(
            e, shapes=True, noIntermediate=True, fullPath=True)
        eNodeType = mc.nodeType(eShape[0])
        if eNodeType in lightNodes:
            selLights.append(e)
    
    return selLights


def simpleIsolateLights():
    allLightsScene = getLightsInScene()
    # Selected scene lights
    selLights = getSelectedLights()
    if len(selLights) < 1:
        logger.warning('Please select at least one light to isolate.')
    else:
        logger.info('{} lights selected for isolation.'.format(len(selLights)))
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
    allLightsScene = getLightsInScene()
    for light in allLightsScene:
        if mc.getAttr(light + ".visibility") == False:
            lightsOff.append(light)
    logger.debug('Lights off status stored. {} lights off found.'.format(len(lightsOff)))


def cleanUpCams ():
    allLightsScene = getLightsInScene()
    #Selected scene lights
    for each in allLightsScene:
        shapes = mc.listRelatives(each, shapes=True, noIntermediate = True, fullPath=True)
        i = 0
        for each in shapes:
            if mc.nodeType(each) == "camera":
                i += 1
                mc.delete(each)
    logger.info('Deleted {} cameras from lights.'.format(i))


def lookThruLight (winWidth=629, winHeight=404, nearClip=1.0, farClip= 1000000):
    selLight = getSelectedLights()
    if len(selLight) >= 1:
        for e in selLight:
            window = mc.window(width= winWidth, height= winHeight, title= e)
            mc.paneLayout()
            thisPanel = mc.modelPanel()
            mc.showWindow( window )
            
            selLightShape = mc.listRelatives(e, shapes = True, noIntermediate = True, fullPath=True)
            mc.lookThru(thisPanel, selLightShape[0], nc=nearClip, fc= farClip)
    elif len(selLight) == 0:
        logger.warning('Please select at least one light to look thru.')
    

def alignLightToObject ():
    selection = mc.ls(sl=True, long=True)
    if len(selection) >= 2:
        mc.align(alignToLead=True, xAxis='mid', yAxis='mid', zAxis='mid')
    elif len(selection) <= 1:
       logger.warning('Select at least one light and one object to align the light to.')


def aimLightToObject ():
    selection = mc.ls(sl=True, long=True)
    if len(selection) >= 2:
        target = selection[-1]
        for each in selection[:-1]:
            mc.aimConstraint(target, each, aimVector=(0,0,-1))
    elif len(selection) <= 1:
        logger.warning('Select at least one light and one target to aim the light to.')


def specularConstrain (_fixed=True):
    selection = mc.ls(sl=True)
    i = 0
    for vertex in selection:
        if '.vtx' in vertex:
            #Create locator
            locator = mc.spaceLocator(name= 'LGT_' +  vertex.rsplit('.vtx')[0] + '_LOC')[0]
            mc.setAttr(locator + '.visibility', 0)
            #Create point light
            pntLightShape = mc.pointLight(name= 'LGT_' + vertex.rsplit('.vtx')[0] + '_01_Specular')
            #Group point light
            pntLight = mc.listRelatives(pntLightShape, parent=True, fullPath=True)[0]
            pntGrp = mc.group(pntLight, name= pntLight + '_GRP')
            #Create point on poly constrain
            vtxUVMap = mc.polyListComponentConversion(vertex, fv=True,tuv=True)
            vtxUVs = mc.polyEditUV(vtxUVMap, query=True)
            thisPopC = mc.pointOnPolyConstraint(vertex, locator, offset=(0,0,0), weight=1)
            thisPopCAttrs = mc.listAttr(thisPopC, ud=True)
            mc.setAttr(thisPopC[0] + "." + thisPopCAttrs[1], vtxUVs[0])
            mc.setAttr(thisPopC[0] + "." + thisPopCAttrs[2], vtxUVs[1])
            locWorld = mc.xform(locator, query=True, rotatePivot = True, ws= True)
            mc.setAttr(pntGrp + '.tx', locWorld[0])
            mc.setAttr(pntGrp + '.ty', locWorld[1])
            mc.setAttr(pntGrp + '.tz', locWorld[2])
            #Create parent constrain
            mc.setAttr(pntGrp + '.tz', locWorld[2] + 5)
            mc.parentConstraint(locator, pntGrp, maintainOffset=True)
            #Create organize group
            organizeGroup = mc.group(pntGrp, locator, name= 'LGT_' +  vertex.rsplit('.vtx')[0] + '_GRP')
            mc.setAttr(organizeGroup + '.tx', lock=True)
            mc.setAttr(organizeGroup + '.ty', lock=True)
            mc.setAttr(organizeGroup + '.tz', lock=True)
            mc.setAttr(organizeGroup + '.rx', lock=True)
            mc.setAttr(organizeGroup + '.ry', lock=True)
            mc.setAttr(organizeGroup + '.rz', lock=True)
            mc.setAttr(organizeGroup + '.sx', lock=True)
            mc.setAttr(organizeGroup + '.sy', lock=True)
            mc.setAttr(organizeGroup + '.sz', lock=True)
            if not _fixed:
                mc.disconnectAttr(thisPopC[0] + '.constraintRotateX', locator + '.rx')
                mc.disconnectAttr(thisPopC[0] + '.constraintRotateY', locator + '.ry')
                mc.disconnectAttr(thisPopC[0] + '.constraintRotateZ', locator + '.rz')
            i += 1
    logger.info('{} specular constrain setups created.'.format(i))


def resetGlobals():
    storeLightsOffStatus()
    getRenderEngines()
    getLightNodes()
        

initLogger(fileLog=True)
storeLightsOffStatus()
getRenderEngines()
getLightNodes()


def main():
    print getRenderEngines()
    print getLightNodes()


if __name__ == '__main__' or 'eclipsePython' in __name__:
    main()
