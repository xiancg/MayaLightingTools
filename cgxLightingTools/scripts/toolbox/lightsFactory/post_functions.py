'''
Created on July 30, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
NOTE: DO NOT delete any method, even if you're not using it.
'''
from __future__ import absolute_import

import maya.cmds as mc

class PostFunctions_default(object):
    def __init__(self):
        super(PostFunctions_default, self).__init__()

    def postLightCreation(self, shapeNode, *args, **kwargs):
        '''Place here all custom stuff you want to do with the created light node'''
        mc.select(shapeNode, replace=True)

    def postLightDuplicate(self, shapeNode, *args, **kwargs):
        '''Place here all custom stuff you want to do with the duplicated light node'''
        mc.select(shapeNode, replace=True)

    def postLightRename(self, shapeNode, *args, **kwargs):
        '''Place here all custom stuff you want to do with the renamed light node'''
        mc.select(shapeNode, replace=True)

    def postLightDelete(self, shapeNode, *args, **kwargs):
        '''Place here all custom stuff you want to do with the deleted light node'''
        pass

class PostFunctions_mtoa(object):
    def __init__(self):
        super(PostFunctions_mtoa, self).__init__()

    def postLightCreation(self, shapeNode, *args, **kwargs):
        '''Place here all custom stuff you want to do with the created light node'''
        import mtoa.aovs as aovs # ! This is wrong, need to isolate to another module (a new package inside lightsFactory?)
        transform = mc.listRelatives(shapeNode, parent=True)[0]
        mc.setAttr(shapeNode + '.aiAov', 'LG_' + transform, type='string')
        newAOVName = 'RGBA_LG_' + transform
        aovNode = aovs.AOVInterface().addAOV(newAOVName).node
        mc.setAttr(aovNode + ".name", 'RGBA_LG_' + transform, type="string")
        mc.setAttr(aovNode + ".type", 6)
        mc.setAttr(aovNode + ".enabled", True)
        mc.select(shapeNode, replace=True)

    def postLightDuplicate(self, shapeNode, *args, **kwargs):
        '''Place here all custom stuff you want to do with the duplicated light node'''
        import mtoa.aovs as aovs
        if not kwargs.get('keepAOVSetup'):
            transform = mc.listRelatives(shapeNode, parent=True)[0]
            mc.setAttr(shapeNode + '.aiAov', 'LG_' + transform, type='string')
            newAOVName = 'RGBA_LG_' + transform
            aovNode = aovs.AOVInterface().addAOV(newAOVName).node
            mc.setAttr(aovNode + ".name", 'RGBA_LG_' + transform, type="string")
            mc.setAttr(aovNode + ".type", 6)
            mc.setAttr(aovNode + ".enabled", True)
            mc.select(shapeNode, replace=True)

    def postLightRename(self, shapeNode, *args, **kwargs):
        '''Place here all custom stuff you want to do with the renamed light node'''
        import mtoa.aovs as aovs
        transform = mc.listRelatives(shapeNode, parent=True)[0]
        oldLightGroup = mc.getAttr(shapeNode + '.aiAov')
        oldAOV = 'aiAOV_RGBA_' + oldLightGroup
        mc.setAttr(shapeNode + '.aiAov', 'LG_' + transform, type='string')
        if mc.objExists(oldAOV):
            aovNode = mc.rename(oldAOV, 'RGBA_LG_' + transform)
            mc.setAttr(aovNode + ".name", 'RGBA_LG_' + transform, type="string")
        mc.select(shapeNode, replace=True)

    def postLightDelete(self, shapeNode, *args, **kwargs):
        '''Place here all custom stuff you want to do with the deleted light node'''
        pass