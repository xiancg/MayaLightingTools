'''
Created on Jun 29, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
'''
import maya.standalone
maya.standalone.initialize()
import maya.cmds as mc
mc.loadPlugin('mtoa')

import unittest
from cgxLightingTools.scripts.toolbox import tools


class NodesTest(unittest.TestCase):

    def test_getRenderEngines(self):
        engines = tools.getRenderEngines()
        self.assertIsNotNone(engines)

    def test_getLightNodes(self):
        lightNodes = tools.getLightNodes()
        defaultLightNodes = ['ambientLight', 'areaLight', 'directionalLight', 
                            'pointLight', 'spotLight', 'volumeLight']
        self.assertItemsEqual
    
    def test_getDefaultLightNodes(self):
        lightNodes = tools.getDefaultLightNodes()
        defaultLightNodes = ['ambientLight', 'areaLight', 'directionalLight', 
                            'pointLight', 'spotLight', 'volumeLight']
        self.assertItemsEqual(defaultLightNodes, lightNodes)

    def test_getLightNodesForRenderer(self):
        lightNodes = tools.getRendererLightNodes('mtoa')
        arnoldLightNodes = ['aiPhotometricLight','aiMeshLight','aiSkyDomeLight',
                            'aiSky','aiAreaLight']
        self.assertItemsEqual(lightNodes, arnoldLightNodes)


if __name__ == "__main__" or 'eclipsePython' in __name__:
    unittest.main()
