'''
Created on July 3, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
TODO: Implement attributes on default and arnold. This will require 
a lot of work to do it automatically, use config file preset for now.
'''
import os
import json
import maya.cmds as mc
from cgxLightingTools.scripts.toolbox import tools
import cgxLightingTools.scripts.core.namingConventions as naming


class LightsFactory(object):
    def __init__(self):
        super(LightsFactory, self).__init__()
        self.lightNodeTypes = tools.getDefaultLightNodes()
        repoPath = os.path.join(os.path.dirname(os.path.abspath(naming.__file__)),'cfg')
        os.environ['NAMING_REPO'] = repoPath
        naming.loadSession()
        self.naming = naming
        lightAttrsPath = os.path.join(repoPath, 'lightAttrs.json')
        with open(lightAttrsPath) as fp:
            config = json.load(fp)
        self._lightAttrs = config
    
    def createLight(self, lightNodeType, lightName):
        if lightNodeType == 'spotLight':
            shapeNode = mc.spotLight(name=lightName)
        elif lightNodeType == 'directionalLight':
            shapeNode = mc.directionalLight(name=lightName)
        elif lightNodeType == 'pointLight':
            shapeNode = mc.pointLight(name=lightName)
        elif lightNodeType == 'ambientLight':
            shapeNode = mc.ambientLight(name=lightName)
        elif lightNodeType == 'volumeLight':
            initNode = mc.createNode('volumeLight')
            transform = mc.listRelatives(initNode, parent=True, fullPath=True)[0]
            result = mc.rename(transform, lightName)
            shapeNode = mc.listRelatives(result, shapes=True, 
                                        noIntermediate=True, type='light')[0]
        elif lightNodeType == 'areaLight':
            initNode = mc.createNode('areaLight')
            transform = mc.listRelatives(initNode, parent=True, fullPath=True)[0]
            result = mc.rename(transform, lightName)
            shapeNode = mc.listRelatives(result, shapes=True,
                                        noIntermediate=True, type='light')[0]
        else:
            return None
        if shapeNode:
            tools.setDefaultAttrs(shapeNode)
            self.postLightCreation(shapeNode)
            transformNode = mc.listRelatives(shapeNode, parent=True)[0]
            return transformNode, shapeNode
        else: 
            return None
    
    def duplicateLight(self, lightNode, withInputs=False):
        if mc.nodeType(lightNode) == 'transform':
            objShape = mc.listRelatives(lightNode, shapes=True, noIntermediate=True, fullPath=True)[0]
            objTransform = lightNode
        else:
            objShape = lightNode
            objTransform = mc.listRelatives(lightNode, parent=True)[0]
        transformNode = str()
        shapeNode = str()
        if mc.nodeType(objShape) in tools.getLightNodesList():
            parsedName = self.naming.parse(objTransform)
            print parsedName
            lightName = self.buildName(**parsedName)
            if withInputs:
                transformNode = mc.duplicate(objTransform, name= lightName, ic= True)[0]
            else:
                transformNode = mc.duplicate(objTransform, name= lightName)[0]
            shapeNode = mc.listRelatives(transformNode, shapes=True, noIntermediate=True, fullPath=True)[0]
        else:
            tools.logger.info('Only lights accepted. {} is {}'.format(lightNode, mc.nodeType(lightNode)))
            return None
        
        self.postLightCreation(shapeNode)

        return transformNode, shapeNode

    def postLightCreation(self, shapeNode):
        '''Place here all custom stuff you want to do with the created light node'''
        transform = mc.listRelatives(shapeNode, parent=True)[0]
        mc.setAttr(shapeNode + '.aiAov', 'LG_' + transform, type='string')
        aovNode = mc.createNode("aiAOV", name='RGBA_' + transform)
        mc.setAttr(aovNode + ".name", 'RGBA_' + transform, type="string")
        mc.setAttr(aovNode + ".type", 6)
        mc.setAttr(aovNode + ".enabled", True)
        try:
            mc.connectAttr("defaultArnoldFilter.message", aovNode + ".outputs[0].filter", force=True)
            mc.connectAttr("defaultArnoldDriver.message", aovNode + ".outputs[0].driver", force=True)
            mc.connectAttr(aovNode + ".message", "defaultArnoldRenderOptions.aovList",
                            nextAvailable=True, force=True)
        except RuntimeError:
            raise RuntimeError('Could not make connections from AOV to default filter, driver and aovList')
        finally:
            mc.select(shapeNode, replace=True)
    
    def buildName(self, *args, **kwargs):
        '''Recursive method to check if the light name
        is already in use and modify it accordingly if it is'''
        lightName = self.naming.solve(*args, **kwargs)
        if not mc.objExists(lightName):
			return lightName
        else:
            #Number might be passed as arg or kwarg
            argsList= list(args)
            for i, arg in enumerate(argsList):
                if isinstance(arg, int):
                    argsList[i] += 1
            args = tuple(argsList)
            for k, v in kwargs.iteritems():
                if isinstance(v, int):
                    kwargs[k] = v + 1

            lightName = self.buildName(*args, **kwargs)
            return lightName

# --------------------------------------------------------
#  Main
# --------------------------------------------------------
def main():
    pass

if __name__ == '__main__' or 'eclipsePython' in __name__:
    main()
