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
            transform = mc.listRelatives(initNode, parent=True)[0]
            result = mc.rename(transform, lightName)
            shapeNode = mc.listRelatives(result, shapes=True, 
                                        noIntermediate=True, type='light')[0]
        elif lightNodeType == 'areaLight':
            initNode = mc.createNode('areaLight')
            transform = mc.listRelatives(initNode, parent=True)[0]
            result = mc.rename(transform, lightName)
            shapeNode = mc.listRelatives(result, shapes=True,
                                        noIntermediate=True, type='light')[0]
        else:
            return False
        if shapeNode:
            self.setDefaultAttrs(shapeNode)
            return True
        else: 
            return False
    
    def createButtons(self):
        pass
    
    def setDefaultAttrs(self, lightNode):
        '''TODO: Old implementation. Need to change to programatic listing of attrs and attr types'''
        for key in tools.getLightNodes().keys():
            if self._lightAttrs.get(key):
                for attrName, attrDict in self._lightAttrs[key].iteritems():
                    value = attrDict["default"]
                    if attrName in mc.listAttr(lightNode):#Check if attribute exists in the object
                        if attrDict["uiControl"] == "floatslider" or attrDict["uiControl"] == "intslider":
                            mc.setAttr(lightNode + "." + attrName, value)
                        elif attrDict["uiControl"] == "combobox" or attrDict["uiControl"] == "booleancombobox":
                            valueIndex = attrDict["values"].index(value)
                            mc.setAttr(lightNode + "." + attrName, valueIndex)
                        elif attrDict["uiControl"] == "colorswatch":
                            mc.setAttr(lightNode + "." + attrName, 1, 1, 1, type= "double3")
    
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