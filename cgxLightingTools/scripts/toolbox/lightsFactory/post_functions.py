'''
Created on July 30, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
'''

from __future__ import absolute_import
import maya.cmds as mc


def postLightCreation(shapeNode, *args, **kwargs):
    '''Place here all custom stuff you want to do with the created light node'''
    transform = mc.listRelatives(shapeNode, parent=True)[0]
    mc.setAttr(shapeNode + '.aiAov', 'LG_' + transform, type='string')
    aovNode = mc.createNode("aiAOV", name='RGBA_LG_' + transform)
    mc.setAttr(aovNode + ".name", 'RGBA_LG_' + transform, type="string")
    mc.setAttr(aovNode + ".type", 6)
    mc.setAttr(aovNode + ".enabled", True)
    try:
        mc.connectAttr("defaultArnoldFilter.message", aovNode + ".outputs[0].filter", force=True)
        mc.connectAttr("defaultArnoldDriver.message", aovNode + ".outputs[0].driver", force=True)
        mc.connectAttr(aovNode + ".message", "defaultArnoldRenderOptions.aovList",
                        nextAvailable=True, force=True)
    except RuntimeError:
        raise RuntimeError('Could not make connections from AOV to default filter, driver and aovList for {}'.format(aovNode))
    finally:
        mc.select(shapeNode, replace=True)

def postLightDuplicate(shapeNode, *args, **kwargs):
    '''Place here all custom stuff you want to do with the duplicated light node'''
    if not kwargs.get('keepAOVSetup'):
        transform = mc.listRelatives(shapeNode, parent=True)[0]
        mc.setAttr(shapeNode + '.aiAov', 'LG_' + transform, type='string')
        aovNode = mc.createNode("aiAOV", name='RGBA_LG_' + transform)
        mc.setAttr(aovNode + ".name", 'RGBA_LG_' + transform, type="string")
        mc.setAttr(aovNode + ".type", 6)
        mc.setAttr(aovNode + ".enabled", True)
        try:
            mc.connectAttr("defaultArnoldFilter.message", aovNode + ".outputs[0].filter", force=True)
            mc.connectAttr("defaultArnoldDriver.message", aovNode + ".outputs[0].driver", force=True)
            mc.connectAttr(aovNode + ".message", "defaultArnoldRenderOptions.aovList",
                            nextAvailable=True, force=True)
        except RuntimeError:
            raise RuntimeError('Could not make connections from AOV to default filter, driver and aovList for {}'.format(aovNode))
        finally:
            mc.select(shapeNode, replace=True)

def postLightRename(shapeNode, *args, **kwargs):
    '''Place here all custom stuff you want to do with the renamed light node'''
    pass

def postLightDelete(shapeNode, *args, **kwargs):
    '''Place here all custom stuff you want to do with the deleted light node'''
    pass