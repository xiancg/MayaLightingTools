# coding=utf-8
from __future__ import absolute_import, print_function


import maya.cmds as mc
import mtoa.aovs as aovs
from cgxlightingtools.scripts.toolbox.post_functions.default_post_functions import PostFunctions_default


class PostFunctions_mtoa(PostFunctions_default):
    def __init__(self):
        super(PostFunctions_mtoa, self).__init__()

    def postLightCreation(self, transformNode, shapeNode, *args, **kwargs):
        '''Place here all custom stuff you want to do with the created light node'''
        mc.setAttr(shapeNode + '.aiAov', 'LG_' + transformNode, type='string')
        newAOVName = 'RGBA_LG_' + transformNode
        aovNode = aovs.AOVInterface().addAOV(newAOVName).node
        mc.setAttr(aovNode + ".name", 'RGBA_LG_' + transformNode, type="string")
        mc.setAttr(aovNode + ".type", 6)
        mc.setAttr(aovNode + ".enabled", True)
        mc.select(shapeNode, replace=True)

    def postLightDuplicate(self, transformNode, shapeNode, *args, **kwargs):
        '''Place here all custom stuff you want to do with the duplicated light node'''
        if not kwargs.get('keepAOVSetup'):
            mc.setAttr(shapeNode + '.aiAov', 'LG_' + transformNode, type='string')
            newAOVName = 'RGBA_LG_' + transformNode
            aovNode = aovs.AOVInterface().addAOV(newAOVName).node
            mc.setAttr(aovNode + ".name", 'RGBA_LG_' + transformNode, type="string")
            mc.setAttr(aovNode + ".type", 6)
            mc.setAttr(aovNode + ".enabled", True)
            mc.select(shapeNode, replace=True)

    def postLightRename(self, transformNode, shapeNode, *args, **kwargs):
        '''Place here all custom stuff you want to do with the renamed light node'''
        oldLightGroup = mc.getAttr(shapeNode + '.aiAov')
        oldAOV = 'aiAOV_RGBA_' + oldLightGroup
        mc.setAttr(shapeNode + '.aiAov', 'LG_' + transformNode, type='string')
        if mc.objExists(oldAOV):
            aovNode = mc.rename(oldAOV, 'RGBA_LG_' + transformNode)
            mc.setAttr(aovNode + ".name", 'RGBA_LG_' + transformNode, type="string")
        mc.select(shapeNode, replace=True)

    def postLightDelete(self, transformNode, shapeNode, *args, **kwargs):
        '''Place here all custom stuff you want to do with the deleted light node.
           Keep in mind the node doesn't exist anymore, you're just operating
           with the name.
        '''
        oldAOV = 'aiAOV_RGBA_LG_' + transformNode
        if mc.objExists(oldAOV):
            try:
                mc.delete(oldAOV)
            except:
                pass
