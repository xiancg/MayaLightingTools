'''
Created on July 4, 2019
Python 3 refactor, Jun 6, 2022

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
'''
import maya.cmds as mc
import mtoa.utils as mutils
import mtoa.core as mcore
from cgxLightingTools.scripts.toolbox.lightsFactory.default_factory import LightsFactory
import cgxLightingTools.scripts.toolbox.tools as tools


class ArnoldFactory(LightsFactory):
    def __init__(self):
        super(ArnoldFactory, self).__init__()
        self.lightNodeTypes = tools.getRendererLightNodes('mtoa')
        # Creates default mtoa nodes if they don't exist already
        mcore.createOptions()

    def createLight(self, lightNodeType, lightName, *args, **kwargs):
        preCreationSelection = mc.ls(sl=True, long=True)
        if len(preCreationSelection) < 1:
            preCreationSelection = None
        else:
            preCreationSelection = preCreationSelection[0]

        if lightNodeType in self.lightNodeTypes and \
           lightNodeType == 'aiMeshLight':
            shapeNode = self._createMeshLight(lightName)
        elif lightNodeType in self.lightNodeTypes and \
                lightNodeType == 'aiSky':
            skydome = mutils.createLocatorWithName('aiSkyDomeLight', lightName, asLight=True)
            shapeNode = mc.createNode('aiPhysicalSky', name=f'{lightName}_aiPS')
            mc.connectAttr(f"{shapeNode}.outColor", f"{skydome[0]}.color")
        elif lightNodeType in self.lightNodeTypes and \
                lightNodeType == 'aiLightPortal' and \
                len(mc.ls(type='aiSkyDome')) >= 1:
            shapeNode, transform = mutils.createLocatorWithName(
                lightNodeType, lightName, asLight=True)
        elif lightNodeType in self.lightNodeTypes and \
                lightNodeType != 'aiLightPortal':
            shapeNode, transform = mutils.createLocatorWithName(
                lightNodeType, lightName, asLight=True)
        else:
            return None
        if shapeNode:
            tools.setDefaultAttrs(shapeNode)
            transformNode = mc.listRelatives(shapeNode, parent=True)[0]

            if lightNodeType not in ['aiMeshLight', 'aiSkyDomeLight', 'aiPhysicalSky']:
                self.alignLight(transformNode, preCreationSelection)

            try:
                self.post_fn.postLightCreation(transformNode, shapeNode, *args, **kwargs)
            except Exception:
                tools.logger.exception(
                    "Post light creation function not executed due to exceptions")
            finally:
                return transformNode, shapeNode
        else:
            return None

    def _createMeshLight(self, lightName, legacy=False, centerPivot=True):
        '''Copied from mtoa.utils. Modified to return transform and shapeNode and receive name input'''
        sls = mc.ls(sl=True, et='transform')
        if len(sls) == 0:
            mc.confirmDialog(title='Error', message='No transform is selected!', button='Ok')
            return
        meshTransform = sls[0]
        shs = mc.listRelatives(meshTransform, fullPath=True, type='mesh')
        if shs is None or len(shs) == 0:
            mc.confirmDialog(
                title='Error', message='The selected transform has no meshes', button='Ok')
            return
        meshShape = shs[0]
        if legacy:
            mc.setAttr(f'{meshShape}.aiTranslator', 'mesh_light', type='string')
        else:
            # Make sure the shape has not been converted already
            existing = mc.listConnections(f'{meshShape}.outMesh', shapes=True, type='aiMeshLight')

            if existing and len(existing) > 0:
                mc.confirmDialog(title='Error', message='Mesh light already created!', button='Ok')
                return

            # Make sure the shape has only a single parent
            # Multiple light instances are not supported
            allPaths = mc.listRelatives(meshShape, allParents=True, fullPath=True) or []
            if len(allPaths) != 1:
                mc.confirmDialog(
                    title='Error', message='The mesh has multiple instances. Light instances are not supported!', button='Ok')
                return

            (lightShape, lightTransform) = mutils.createLocatorWithName(
                'aiMeshLight', nodeName=lightName, asLight=True)

            mc.connectAttr(f'{meshShape}.outMesh', f'{lightShape}.inMesh')

            p = mc.parent(lightTransform, meshTransform, relative=True)
            lightShape = mc.listRelatives(p[0], shapes=True, fullPath=True)[0]
            # Hide the original mesh using the visibility attribute
            # We previously used lodVisibility to keep the dirtiness propagation enabled,
            # but I can't manage to find a situation that fails. So we're now using visibility

            # mc.connectAttr('%s.showOriginalMesh' % lightShape, '%s.lodVisibility' % meshShape)
            mc.connectAttr(f'{lightShape}.showOriginalMesh', f'{meshShape}.visibility')

            # FIXME : we shouldn't have to do this, but otherwise it takes a couple of tweaks on
            # showOriginalMesh before seeing its effect
            mc.setAttr(f'{lightShape}.showOriginalMesh', 1)
            mc.setAttr(f'{lightShape}.showOriginalMesh', 0)

            return lightShape


# --------------------------------------------------------
#  Main
# --------------------------------------------------------
def main():
    pass


if __name__ == '__main__' or 'eclipsePython' in __name__:
    main()
