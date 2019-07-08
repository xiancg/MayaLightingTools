'''
Created on July 4, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
'''
from cgxLightingTools.scripts.toolbox.lightsFactory.abstract import LightsFactory
import cgxLightingTools.scripts.toolbox.tools as tools


class MayaDefaultFactory(LightsFactory):
    def __init__(self):
        super(MayaDefaultFactory, self).__init__()
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