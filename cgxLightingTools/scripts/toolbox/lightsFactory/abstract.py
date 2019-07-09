'''
Created on July 3, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
TODO: Implement arnold lights creation.
TODO: Implement attributes. This will require a lot of work to do
it automatically, use config file preset for now.
'''
import os
import maya.cmds as mc
from cgxLightingTools.scripts.toolbox import tools
import cgxLightingTools.scripts.core.namingConventions as naming


class LightsFactory(object):
    def __init__(self):
        self.lightNodeTypes = tools.getLightNodesList()
        repoPath = os.path.join(os.path.dirname(os.path.abspath(naming.__file__)),'cfg')
        os.environ['NAMING_REPO'] = repoPath
        naming.loadSession()
        self.naming = naming
    
    def createLight(self, lightNodeType, lightName):
        if lightNodeType == 'spotLight':
            shapeNode = mc.spotLight(name=lightName)
        elif lightNodeType == 'directionalLight':
            shapeNode = mc.directionalLight(name=lightName)
        elif lightNodeType == 'pointLight':
            shapeNode = mc.pointLight(name=lightName)
        elif lightNodeType == 'areaLight':
            shapeNode = mc.createNode('areaLight')
            transform = mc.listRelatives(shapeNode, parent=True)[0]
            mc.rename(transform, lightName)
        else:
            return False
        if shapeNode:
            self.setDefaultAttrs(shapeNode)
        return True
    
    def setDefaultAttrs(self, lightNode):
        pass
    
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


def main():
    pass

if __name__ == '__main__' or 'eclipsePython' in __name__:
    main()