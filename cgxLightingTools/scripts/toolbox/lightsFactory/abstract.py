'''
Created on July 3, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
TODO: Implement naming
TODO: Implement attributes. This will require a lot of work to do
it automatically, use config file preset for now.
TODO: Implement arnold lights creation. 
TODO: Split renderers implementations to different modules
'''
import abc
import cgxLightingTools.scripts.toolbox.tools as tools


class LightsFactory(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self):
        self.lightNodeTypes = tools.getLightNodesList()
    
    @abc.abstractmethod
    def createLight(self, _lightNodeType):
        pass
    
    def setDefaultAttributes(self, lightNode):
        pass
    
    def buildName(self, lightNode):
        pass
