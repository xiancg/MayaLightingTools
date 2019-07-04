'''
Created on July 4, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
'''
from cgxLightingTools.scripts.toolbox.lightsFactory.abstract import LightsFactory
import cgxLightingTools.scripts.toolbox.tools as tools


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