'''
Created on July 3, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
TODO: Implement naming
TODO: Implement arnold lights creation.
TODO: Implement attributes. This will require a lot of work to do
it automatically, use config file preset for now.
'''
import abc
import os
from cgxLightingTools.scripts.toolbox import tools
import cgxLightingTools.scripts.core.namingConventions as naming
repoPath = os.path.join(os.path.dirname(os.path.abspath(naming.__file__)),'cfg')
os.environ['NAMING_REPO'] = repoPath
naming.loadSession()
print naming.getActiveRule().name
'''
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
'''

def main():
    pass

if __name__ == '__main__' or 'eclipsePython' in __name__:
    main()