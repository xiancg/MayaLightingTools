'''
Python 3 refactor, Jun 6, 2022

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
'''


import contextlib
import maya.cmds as mc
import mtoa.aovs as aovs
from cgxLightingTools.scripts.toolbox.post_functions.default_post_functions import PostFunctions_default


class PostFunctions_mtoa(PostFunctions_default):
    def __init__(self):
        super(PostFunctions_mtoa, self).__init__()

    def postLightCreation(self, transformNode, shapeNode, *args, **kwargs):
        '''Place here all custom stuff you want to do with the created light node'''
        mc.setAttr(f'{shapeNode}.aiAov', f'LG_{transformNode}', type='string')
        newAOVName = f'RGBA_LG_{transformNode}'
        aovNode = aovs.AOVInterface().addAOV(newAOVName).node
        mc.setAttr(f"{aovNode}.name", f'RGBA_LG_{transformNode}', type="string")
        mc.setAttr(f"{aovNode}.type", 6)
        mc.setAttr(f"{aovNode}.enabled", True)
        mc.select(shapeNode, replace=True)

    def postLightDuplicate(self, transformNode, shapeNode, *args, **kwargs):
        '''Place here all custom stuff you want to do with the duplicated light node'''
        if not kwargs.get('keepAOVSetup'):
            mc.setAttr(f'{shapeNode}.aiAov', f'LG_{transformNode}', type='string')
            newAOVName = f'RGBA_LG_{transformNode}'
            aovNode = aovs.AOVInterface().addAOV(newAOVName).node
            mc.setAttr(f"{aovNode}.name", f'RGBA_LG_{transformNode}', type="string")
            mc.setAttr(f"{aovNode}.type", 6)
            mc.setAttr(f"{aovNode}.enabled", True)
            mc.select(shapeNode, replace=True)

    def postLightRename(self, transformNode, shapeNode, *args, **kwargs):
        '''Place here all custom stuff you want to do with the renamed light node'''
        oldLightGroup = mc.getAttr(f'{shapeNode}.aiAov')
        oldAOV = f'aiAOV_RGBA_{oldLightGroup}'
        mc.setAttr(f'{shapeNode}.aiAov', f'LG_{transformNode}', type='string')
        if mc.objExists(oldAOV):
            aovNode = mc.rename(oldAOV, f'RGBA_LG_{transformNode}')
            mc.setAttr(f"{aovNode}.name", f'RGBA_LG_{transformNode}', type="string")
        mc.select(shapeNode, replace=True)

    def postLightDelete(self, transformNode, shapeNode, *args, **kwargs):
        '''Place here all custom stuff you want to do with the deleted light node.
           Keep in mind the node doesn't exist anymore, you're just operating
           with the name.
        '''
        oldAOV = f'aiAOV_RGBA_LG_{transformNode}'
        if mc.objExists(oldAOV):
            with contextlib.suppress(Exception):
                mc.delete(oldAOV)
