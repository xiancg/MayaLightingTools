'''
Created on July 3, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
TODO: Implement attributes on default and arnold. This will require 
a lot of work to do it automatically, use config file preset for now.
TODO: Remove post methods from here and move them to a separate library
'''
import os
import json
import maya.cmds as mc
from cgxLightingTools.scripts.toolbox import tools
import cgxLightingTools.scripts.core.namingConventions as naming
from cgxLightingTools.scripts.toolbox.lightsFactory import post_functions


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
    
    def createLight(self, lightNodeType, lightName, *args, **kwargs):
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
            post_functions.postLightCreation(shapeNode, *args, **kwargs)
            transformNode = mc.listRelatives(shapeNode, parent=True)[0]
            return transformNode, shapeNode
        else: 
            return None
    
    def duplicateLight(self, lightNode, withInputs=False, withNodes=False, *args, **kwargs):
        if mc.nodeType(lightNode) == 'transform':
            objShape = mc.listRelatives(lightNode, shapes=True, noIntermediate=True, fullPath=True)[0]
            objTransform = lightNode
        else:
            objShape = lightNode
            objTransform = mc.listRelatives(lightNode, parent=True)[0]
        transformNode = str()
        shapeNode = str()
        if mc.nodeType(objShape) in tools.getLightNodesList():
            parsedName = self.parseOldNameByTokens(objTransform)
            if parsedName is not None:
                lightName = self.buildName(**parsedName)
                if withInputs and not withNodes:
                    transformNode = mc.duplicate(objTransform, name= lightName, ic= True)[0]
                elif withInputs and withNodes:
                    transformNode = mc.duplicate(objTransform, name= lightName, ic= True, un=True)[0]
                else:
                    transformNode = mc.duplicate(objTransform, name= lightName)[0]
            else:
                if withInputs and not withNodes:
                    transformNode = mc.duplicate(objTransform, ic= True)[0]
                elif withInputs and withNodes:
                    transformNode = mc.duplicate(objTransform, ic= True, un=True)[0]
                else:
                    transformNode = mc.duplicate(objTransform)[0]
            shapeNode = mc.listRelatives(transformNode, shapes=True, noIntermediate=True, fullPath=True)[0]
        else:
            tools.logger.info('Only lights accepted. {} is {}'.format(lightNode, mc.nodeType(lightNode)))
            return None
        
        post_functions.postLightDuplicate(shapeNode, *args, **kwargs)

        return transformNode, shapeNode
    
    def renameLight(self, lightNode, lightName, *args, **kwargs):
        if mc.nodeType(lightNode) == 'transform':
            objShape = mc.listRelatives(lightNode, shapes=True, noIntermediate=True, fullPath=True)[0]
            objTransform = lightNode
        else:
            objShape = lightNode
            objTransform = mc.listRelatives(lightNode, parent=True)[0]
        parsedName = self.naming.parse(lightName)
        finalLightName = self.buildName(**parsedName)
        result = mc.rename(objTransform, finalLightName)
        shapeNode = mc.listRelatives(result, shapes=True, noIntermediate=True, fullPath=True)[0]

        post_functions.postLightRename(shapeNode, *args, **kwargs)
        
        return result
    
    def parseOldNameByTokens(self, lightNode):
        if mc.nodeType(lightNode) == 'transform':
            objShape = mc.listRelatives(lightNode, shapes=True, noIntermediate=True, fullPath=True)[0]
            objTransform = lightNode
        else:
            objShape = lightNode
            objTransform = mc.listRelatives(lightNode, parent=True)[0]
        nameSplit = objTransform.split('_')
        result = None
        if len(nameSplit) == len(self.naming.getActiveRule().fields):
            if mc.nodeType(objShape) in self.lightNodeTypes:
                result = self.naming.parse(objTransform)

        return result
    
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
