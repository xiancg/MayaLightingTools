'''
Created on July 4, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
'''
import maya.cmds as mc
import mtoa.utils as mutils
from cgxLightingTools.scripts.toolbox.lightsFactory.default_factory import LightsFactory
import cgxLightingTools.scripts.toolbox.tools as tools


class ArnoldFactory(LightsFactory):
    def __init__(self):
        super(ArnoldFactory, self).__init__()
        self.lightNodeTypes = tools.getRendererLightNodes('mtoa')
        
    def createLight(self, lightNodeType, lightName):
        if lightNodeType in self.lightNodeTypes and lightNodeType == 'aiMeshLight':
            shapeNode = self._createMeshLight(lightName)
        elif lightNodeType in self.lightNodeTypes and lightNodeType == 'aiSky':
            skydome = mutils.createLocatorWithName('aiSkyDomeLight', lightName, asLight=True)
            shapeNode = mc.createNode('aiPhysicalSky', name= lightName + '_aiPS')
            mc.connectAttr(shapeNode + ".outColor", skydome[0] + ".color")
        elif lightNodeType in self.lightNodeTypes and lightNodeType == 'aiLightPortal' and len(mc.ls(type='aiSkyDome')) >= 1:
            shapeNode, transform = mutils.createLocatorWithName(lightNodeType, lightName, asLight=True)
        elif lightNodeType in self.lightNodeTypes and lightNodeType != 'aiLightPortal':
            shapeNode, transform = mutils.createLocatorWithName(lightNodeType, lightName, asLight=True)
        else:
            return False
        if shapeNode:
            self.setDefaultAttrs(shapeNode)
            return True
        else: 
            return False
    
    def _createMeshLight(self, lightName, legacy=False, centerPivot=True):
        '''Copied from mtoa.utils. Modified to return transform and shapeNode and receive name input'''
        sls = mc.ls(sl=True, et='transform')
        if len(sls) == 0:
            mc.confirmDialog(title='Error', message='No transform is selected!', button='Ok')
            return
        meshTransform = sls[0]
        shs = mc.listRelatives(meshTransform, fullPath=True, type='mesh')
        if shs is None or len(shs) == 0:
            mc.confirmDialog(title='Error', message='The selected transform has no meshes', button='Ok')
            return
        meshShape = shs[0]
        if legacy:
            mc.setAttr('%s.aiTranslator' % meshShape, 'mesh_light', type='string')
        else:
            # Make sure the shape has not been converted already
            existing = mc.listConnections('%s.outMesh' % meshShape, shapes=True, type='aiMeshLight')
            if existing and len(existing) > 0:
                mc.confirmDialog(title='Error', message='Mesh light already created!', button='Ok')
                return

            # Make sure the shape has only a single parent
            # Multiple light instances are not supported
            allPaths = mc.listRelatives(meshShape, allParents=True, fullPath=True) or []
            if len(allPaths) != 1:
                mc.confirmDialog(title='Error', message='The mesh has multiple instances. Light instances are not supported!', button='Ok')
                return

            (lightShape,lightTransform) = mutils.createLocatorWithName('aiMeshLight', nodeName=lightName, asLight=True)

            mc.connectAttr('%s.outMesh' % meshShape, '%s.inMesh' % lightShape)

            p = mc.parent(lightTransform, meshTransform, relative=True)
            lightShape = mc.listRelatives(p[0], shapes=True, fullPath=True)[0]
            # Hide the original mesh using the visibility attribute
            # We previously used lodVisibility to keep the dirtiness propagation enabled,
            # but I can't manage to find a situation that fails. So we're now using visibility

            #mc.connectAttr('%s.showOriginalMesh' % lightShape, '%s.lodVisibility' % meshShape)
            mc.connectAttr('%s.showOriginalMesh' % lightShape, '%s.visibility' % meshShape)

            # FIXME : we shouldn't have to do this, but otherwise it takes a couple of tweaks on
            # showOriginalMesh before seeing its effect
            mc.setAttr('%s.showOriginalMesh' % lightShape, 1)
            mc.setAttr('%s.showOriginalMesh' % lightShape, 0)

            return lightShape


# --------------------------------------------------------
#  Main
# --------------------------------------------------------
def main():
    pass

if __name__ == '__main__' or 'eclipsePython' in __name__:
    main()