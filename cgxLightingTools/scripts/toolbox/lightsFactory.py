'''
Created on July 3, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
TODO: Structure this as a package, with implementations inside
TODO: Implement naming
TODO: Implement attributes. This will require a lot of work to do
it automatically, use config file preset for now.
TODO: Implement arnold lights creation. 
TODO: Split renderers implementations to different modules
'''
import abc
import maya.cmds as mc
import cgxLightingTools.scripts.toolbox.tools as tools


class LightsFactory(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self):
        self.lightNodeTypes = list()
    
    @abc.abstractmethod
    def createLight(self, _lightNodeType):
        pass
    
    def setDefaultAttributes(self, lightNode):
        pass
    
    def buildName(self, lightNode):
        pass


class MayaDefaultFactory(LightsFactory):
    def __init__(self):
        super(MayaDefaultFactory).__init__()
        self.lightNodeTypes = tools.getDefaultLightNodes()
        
    def createLight(self, _lightNodeType):
        if _lightNodeType in self.lightNodeTypes():
            lightName = self.buildName()
            shapeNode = str()
            if _lightNodeType == "spotLight":
                shapeNode = mc.spotLight(name=lightName)
            elif _lightNodeType == "directionalLight":
                shapeNode = mc.directionalLight(name=lightName)
            elif _lightNodeType == "pointLight":
                shapeNode = mc.pointLight(name=lightName)
            elif _lightNodeType == "areaLight":
                shapeNode = mc.createNode("areaLight")
                transform = mc.listRelatives(shapeNode, parent=True)[0]
                mc.rename(transform, lightName)
            if mc.objExists(shapeNode):
                self.setDefaultAttributes(shapeNode)
        else:
            pass #Warning


class ArnoldFactory(LightsFactory):
    def __init__(self):
        super(ArnoldFactory).__init__()
        self.lightNodeTypes = tools.getRendererLightNodes('mtoa')
        
    def createLight(self, _lightNodeType):
        if _lightNodeType in self.lightNodeTypes():
            setName(lightNode)
            setDefaultAttributes(lightNode)
        else:
            pass #Warning