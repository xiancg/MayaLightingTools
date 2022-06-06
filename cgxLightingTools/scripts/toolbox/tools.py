'''
Created on Jun 29, 2019
Python 3 refactor, Jun 6, 2022

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
TODO: Refactor harcoded naming in specularConstrain
'''


import contextlib
import logging
import sys
import os
import copy
import json
from datetime import date
import cgxLightingTools.scripts.core as core

import maya.cmds as mc

lightsOff = []
renderEngines = {}
lightNodesDict = {}
_cfgPath = os.path.join(os.path.dirname(os.path.abspath(core.__file__)), 'cfg')
_lightAttrsPath = os.path.join(_cfgPath, 'lightAttrs.json')
with open(_lightAttrsPath) as fp:
    config = json.load(fp)
lightAttrs = config
logger = logging.getLogger(name='lgtToolsLog')


def initLogger():
    logger.setLevel(logging.WARNING)
    # Formatter
    formatter = logging.Formatter(
        '[%(asctime)s:%(module)s:%(funcName)s:%(lineno)s:%(levelname)s] %(message)s')
    # STDOUT stream
    streamHandler = logging.StreamHandler(sys.stdout)
    streamHandler.setLevel(logging.WARNING)
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)


def initFileLogger():
    # Formatter
    formatter = logging.Formatter(
        '[%(asctime)s:%(module)s:%(funcName)s:%(lineno)s:%(levelname)s] %(message)s')
    # Log file stream
    userPath = os.path.expanduser("~")
    finalDir = os.path.join(userPath, ".CGXTools")
    with contextlib.suppress(Exception):
        if not os.path.exists(finalDir):
            os.mkdir(finalDir)
    today = date.today()
    date_string = today.strftime("%d-%m-%Y")
    log_file_path = os.path.join(finalDir, f'lgtTools_{date_string}.log')
    fileHandler = logging.FileHandler(log_file_path, mode='a')
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
    logger.debug(f"Found these render engines: {','.join(renderEngines.keys())}")
    return renderEngines


def getCurrentRenderPlugin():
    currentRenderer = mc.getAttr('defaultRenderGlobals.currentRenderer')
    for plugin, renderers in getRenderEngines().iteritems():
        for each in renderers:
            if currentRenderer.lower() == str(each).lower():
                return plugin


def getLightNodes():
    lightNodes = mc.listNodeTypes('drawdb/light')
    lightNodesDict.clear()
    for key in renderEngines.keys():
        dependNodes = mc.pluginInfo(key, query=True, dependNode=True)
        rendererLights = list(set(lightNodes).intersection(dependNodes))
        lightNodesDict[key] = rendererLights
    defaultLightNodes = []
    for lightsList in lightNodesDict.values():
        defaultLightNodes += list(set(lightsList) ^ set(lightNodes))
    lightNodesDict['default'] = defaultLightNodes

    return lightNodesDict


def getLightNodesList():
    lightNodes = []
    for each in lightNodesDict.values():
        lightNodes += each
    return lightNodes


def getDefaultLightNodes():
    return lightNodesDict['default']


def getRendererLightNodes(renderer='default'):
    if mc.pluginInfo(renderer, query=True, loaded=True) or renderer == 'default':
        return lightNodesDict[renderer]
    logger.warning(f"No renderer named '{renderer}' was found loaded.")
    return None


def getLightsInScene():
    lightNodes = getLightNodesList()
    # All scene lights
    allLightsShapes = mc.ls(lights=True, type=lightNodes, long=True)
    allLightsScene = []
    for i in allLightsShapes:
        iTrans = mc.listRelatives(i, parent=True, fullPath=True)
        allLightsScene.append(iTrans[0])

    return allLightsScene


def getSelectedLights():
    lightNodes = getLightNodesList()
    selObjs = mc.ls(sl=True, long=True)
    selLights = []
    for each in selObjs:
        node_type = mc.nodeType(each)
        if node_type == "transform":
            shape_node = mc.listRelatives(each, shapes=True,
                                          noIntermediate=True,
                                          fullPath=True)[0]
            node_type = mc.nodeType(shape_node)
            if node_type in lightNodes:
                selLights.append(each)
        else:
            transform = mc.listRelatives(each, parent=True,
                                         fullPath=True)[0]
            if node_type in lightNodes:
                selLights.append(transform)

    return selLights


def getTransformAndShape(lightNode):
    if mc.nodeType(lightNode) == 'transform':
        objShape = mc.listRelatives(lightNode, shapes=True, noIntermediate=True, fullPath=True)[0]
        objTransform = lightNode
    else:
        objShape = lightNode
        objTransform = mc.listRelatives(lightNode, parent=True)[0]

    return objTransform, objShape


def simpleIsolateLights():
    allLightsScene = getLightsInScene()
    # Selected scene lights
    selLights = getSelectedLights()
    if len(selLights) < 1:
        logger.warning('Please select at least one light to isolate.')
    else:
        logger.info(f'{len(selLights)} lights selected for isolation.')
        # Toggle visibilities
        for light in allLightsScene:
            # If light is ON but not selected, switch it OFF
            if mc.getAttr(f"{light}.visibility") is True and light not in selLights:
                mc.setAttr(f"{light}.visibility", False)
            elif mc.getAttr(f"{light}.visibility") is False and light not in lightsOff:
                mc.setAttr(f"{light}.visibility", True)


def lightsVisibilitySnapshot():
    del lightsOff[:]
    allLightsScene = getLightsInScene()
    for light in allLightsScene:
        if mc.getAttr(f"{light}.visibility") is False:
            lightsOff.append(light)
    logger.debug(f'Lights visibility snapshot taken. {len(lightsOff)} lights off found.')

    return copy.deepcopy(lightsOff)


def lightsAttrsSnapshot():
    allLightsScene = getLightsInScene()
    lightNodes = getLightNodesList()
    snapshot = {}
    for light in allLightsScene:
        finalAttrsDict = {}
        shapeNode = mc.listRelatives(light, shapes=True, noIntermediate=True,
                                     fullPath=True, type=lightNodes)[0]
        for key in getLightNodes().keys():
            if lightAttrs.get(key):
                for attrName, attrDict in lightAttrs[key].iteritems():
                    objAttr = f"{shapeNode}.{attrName}"
                    if attrName in mc.listAttr(shapeNode) and not mc.connectionInfo(objAttr, isDestination=True):
                        if attrDict["uiControl"] in ['floatslider', 'intslider', 'combobox', 'booleancombobox']:
                            value = mc.getAttr(objAttr)
                            finalAttrsDict[attrName] = {'value': value,
                                                        'uiControl': attrDict["uiControl"]}
                        elif attrDict["uiControl"] == "colorswatch":
                            value = list(mc.getAttr(objAttr)[0])
                            finalAttrsDict[attrName] = {'value': value,
                                                        'uiControl': attrDict["uiControl"]}
        snapshot[light] = finalAttrsDict
    return snapshot


def loadLightsAttrsSnapshot(snapshot):
    try:
        lightNodes = getLightNodesList()
        for light, finalAttrsDict in snapshot.iteritems():
            if mc.objExists(light):
                shapeNode = mc.listRelatives(light, shapes=True, noIntermediate=True,
                                             fullPath=True, type=lightNodes)[0]
                for attrName, attrDict in finalAttrsDict.iteritems():
                    objAttr = f"{shapeNode}.{attrName}"
                    if attrName in mc.listAttr(shapeNode) and not mc.connectionInfo(objAttr, isDestination=True):
                        if attrDict["uiControl"] in ["floatslider", "intslider"]:
                            mc.setAttr(objAttr, attrDict['value'])
                        elif attrDict["uiControl"] in ["combobox", "booleancombobox"]:
                            mc.setAttr(objAttr, int(attrDict['value']))
                        elif attrDict["uiControl"] == "colorswatch":
                            mc.setAttr(objAttr, attrDict['value'][0],
                                       attrDict['value'][1], attrDict['value'][2],
                                       type="double3")
    except Exception:
        logger.warning('Attributes snapshot could not be loaded.')
        return False
    return True


def setDefaultAttrs(lightNode):
    '''TODO: Old implementation. Need to change to programatic listing of attrs and attr types'''
    for key in getLightNodes().keys():
        if lightAttrs.get(key):
            for attrName, attrDict in lightAttrs[key].iteritems():
                if attrName in mc.listAttr(lightNode):  # Check if attribute exists in the object
                    value = attrDict["default"]
                    if attrDict["uiControl"] in ["floatslider", "intslider"]:
                        mc.setAttr(f"{lightNode}.{attrName}", value)
                    elif attrDict["uiControl"] in ["combobox", "booleancombobox"]:
                        valueIndex = attrDict["values"].index(value)
                        mc.setAttr(f"{lightNode}.{attrName}", valueIndex)
                    elif attrDict["uiControl"] == "colorswatch":
                        mc.setAttr(f"{lightNode}.{attrName}", 1, 1, 1, type="double3")


def cleanUpCams():
    allLightsScene = getLightsInScene()
    # Selected scene lights
    i = 0
    for each in allLightsScene:
        shapes = mc.listRelatives(each, shapes=True, noIntermediate=True, fullPath=True)
        for each in shapes:
            if mc.nodeType(each) == "camera":
                i += 1
                mc.delete(each)
    logger.warning(f'Deleted {i} cameras from lights.')


def lookThruLight(winWidth=629, winHeight=404, nearClip=1.0, farClip=1000000):
    selLight = getSelectedLights()
    if len(selLight) >= 1:
        for e in selLight:
            window = mc.window(width=winWidth, height=winHeight, title=e)
            mc.paneLayout()
            thisPanel = mc.modelPanel()
            mc.showWindow(window)

            selLightShape = mc.listRelatives(e, shapes=True, noIntermediate=True, fullPath=True)
            mc.lookThru(thisPanel, selLightShape[0], nc=nearClip, fc=farClip)
    elif len(selLight) == 0:
        logger.warning('Please select at least one light to look thru.')


def alignLightToObject(selList=mc.ls(sl=True, long=True)):
    '''Select lights first, target last'''
    mc.select(selList, replace=True)
    if len(selList) >= 2:
        mc.align(alignToLead=True, xAxis='mid', yAxis='mid', zAxis='mid')
    elif len(selList) <= 1:
        logger.warning('Select at least one light and one object to align the light to.')


def aimLightToObject():
    selection = mc.ls(sl=True, long=True)
    if len(selection) >= 2:
        target = selection[-1]
        for each in selection[:-1]:
            mc.aimConstraint(target, each, aimVector=(0, 0, -1))
    elif len(selection) <= 1:
        logger.warning('Select at least one light and one target to aim the light to.')


def specularConstrain(_fixed=True):
    selection = mc.ls(sl=True)
    i = 0
    for vertex in selection:
        if '.vtx' in vertex:
            # Create locator
            locator = mc.spaceLocator(name='LGT_' + vertex.rsplit('.vtx')[0] + '_LOC')[0]
            mc.setAttr(f'{locator}.visibility', 0)
            # Create point light
            pntLightShape = mc.pointLight(name='LGT_' + vertex.rsplit('.vtx')[0] + '_01_Specular')
            # Group point light
            pntLight = mc.listRelatives(pntLightShape, parent=True, fullPath=True)[0]
            pntGrp = mc.group(pntLight, name=f'{pntLight}_GRP')
            # Create point on poly constrain
            vtxUVMap = mc.polyListComponentConversion(vertex, fv=True, tuv=True)
            vtxUVs = mc.polyEditUV(vtxUVMap, query=True)
            thisPopC = mc.pointOnPolyConstraint(vertex, locator, offset=(0, 0, 0), weight=1)
            thisPopCAttrs = mc.listAttr(thisPopC, ud=True)
            mc.setAttr(f"{thisPopC[0]}.{thisPopCAttrs[1]}", vtxUVs[0])
            mc.setAttr(f"{thisPopC[0]}.{thisPopCAttrs[2]}", vtxUVs[1])
            locWorld = mc.xform(locator, query=True, rotatePivot=True, ws=True)
            mc.setAttr(f'{pntGrp}.tx', locWorld[0])
            mc.setAttr(f'{pntGrp}.ty', locWorld[1])
            mc.setAttr(f'{pntGrp}.tz', locWorld[2])
            # Create parent constrain
            mc.setAttr(f'{pntGrp}.tz', locWorld[2] + 5)
            mc.parentConstraint(locator, pntGrp, maintainOffset=True)
            # Create organize group
            organizeGroup = mc.group(pntGrp,
                                     locator,
                                     name='LGT_' + vertex.rsplit('.vtx')[0] + '_GRP'
                                     )
            mc.setAttr(f'{organizeGroup}.tx', lock=True)
            mc.setAttr(f'{organizeGroup}.ty', lock=True)
            mc.setAttr(f'{organizeGroup}.tz', lock=True)
            mc.setAttr(f'{organizeGroup}.rx', lock=True)
            mc.setAttr(f'{organizeGroup}.ry', lock=True)
            mc.setAttr(f'{organizeGroup}.rz', lock=True)
            mc.setAttr(f'{organizeGroup}.sx', lock=True)
            mc.setAttr(f'{organizeGroup}.sy', lock=True)
            mc.setAttr(f'{organizeGroup}.sz', lock=True)
            if not _fixed:
                mc.disconnectAttr(f'{thisPopC[0]}.constraintRotateX', f'{locator}.rx')
                mc.disconnectAttr(f'{thisPopC[0]}.constraintRotateY', f'{locator}.ry')
                mc.disconnectAttr(f'{thisPopC[0]}.constraintRotateZ', f'{locator}.rz')
            i += 1
    logger.info(f'{i} specular constrain setups created.')


def transformBake(items, sampleBy=1):
    for item in items:
        if ".vtx" in item:
            vtxExp = mc.filterExpand(item, selectionMask=31, expand=True)
            for vtx in vtxExp:
                # THIS DOESN'T WORK IF UVS ARE OVERLAPED
                cleanObjName = vtx[:vtx.index(".vtx")]
                thisLoc = mc.spaceLocator(name=f"{vtx}__LOC_bkd", p=(0, 0, 0))
                # Make constrain
                vtxUVMap = mc.polyListComponentConversion(vtx, fv=True, tuv=True)
                vtxUVs = mc.polyEditUV(vtxUVMap, query=True)
                thisPopC = mc.pointOnPolyConstraint(vtx, thisLoc, offset=(0, 0, 0), weight=1)
                thisPopCAttrs = mc.listAttr(thisPopC, ud=True)
                mc.setAttr(f"{thisPopC[0]}.{thisPopCAttrs[1]}", vtxUVs[0])
                mc.setAttr(f"{thisPopC[0]}.{thisPopCAttrs[2]}", vtxUVs[1])
                # Bake animation
                start = mc.playbackOptions(query=True, minTime=True)
                end = mc.playbackOptions(query=True, maxTime=True)
                mc.bakeResults(thisLoc,
                               simulation=True,
                               t=(int(start), int(end)),
                               sampleBy=sampleBy,
                               preserveOutsideKeys=True,
                               sparseAnimCurveBake=False,
                               removeBakedAttributeFromLayer=False,
                               bakeOnOverrideLayer=False,
                               minimizeRotation=True,
                               at=("tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz")
                               )
                # Delete constrain
                mc.delete(thisPopC[0])
        elif mc.nodeType(item) == "transform":
            thisLoc = mc.spaceLocator(name=f"{item}__LOC_bkd", p=(0, 0, 0))
            # Make constrains
            pConstrain = mc.parentConstraint(item, thisLoc, maintainOffset=False)
            sConstrain = mc.scaleConstraint(item, thisLoc, maintainOffset=False)
            # Bake animation
            start = mc.playbackOptions(query=True, minTime=True)
            end = mc.playbackOptions(query=True, maxTime=True)
            mc.bakeResults(thisLoc,
                           simulation=True,
                           t=(int(start), int(end)),
                           sampleBy=sampleBy,
                           preserveOutsideKeys=True,
                           sparseAnimCurveBake=False,
                           removeBakedAttributeFromLayer=False,
                           bakeOnOverrideLayer=False,
                           minimizeRotation=True,
                           at=("tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz")
                           )
            # Delete constrain
            mc.delete(pConstrain, sConstrain)
        else:
            logger.info(f'Only Vertex or Transforms accepted. Found {item}')
    # Done Alert!!
    logger.info('Done baking transforms.')


def resetGlobals():
    lightsVisibilitySnapshot()
    getRenderEngines()
    getLightNodes()


initLogger()
lightsVisibilitySnapshot()
getRenderEngines()
getLightNodes()


# --------------------------------------------------------
#  Main
# --------------------------------------------------------
def main():
    # print getLightsInScene()
    pass


if __name__ == '__main__' or 'eclipsePython' in __name__:
    main()
