'''
@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
'''
from __future__ import absolute_import

import maya.cmds as mc
import mtoa.aovs as aovs
from cgxLightingTools.scripts.toolbox.post_functions.default_post_functions import PostFunctions_default

class PostFunctions_mtoa(PostFunctions_default):
    def __init__(self):
        super(PostFunctions_mtoa, self).__init__()

    def postLightCreation(self, shapeNode, *args, **kwargs):
        '''Place here all custom stuff you want to do with the created light node'''
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
        transform = mc.listRelatives(shapeNode, parent=True)[0]
        oldLightGroup = mc.getAttr(shapeNode + '.aiAov')
        oldAOV = 'aiAOV_RGBA_' + oldLightGroup
        mc.setAttr(shapeNode + '.aiAov', 'LG_' + transform, type='string')
        if mc.objExists(oldAOV):
            aovNode = mc.rename(oldAOV, 'RGBA_LG_' + transform)
            mc.setAttr(aovNode + ".name", 'RGBA_LG_' + transform, type="string")
        mc.select(shapeNode, replace=True)