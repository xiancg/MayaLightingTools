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
        self.assertItemsEqual(defaultLightNodes, lightNodes['default'])

    def test_getLightNodesList(self):
        lightNodes = tools.getLightNodesList()
        self.assertGreaterEqual(lightNodes, 6)

    def test_getDefaultLightNodes(self):
        lightNodes = tools.getDefaultLightNodes()
        defaultLightNodes = ['ambientLight', 'areaLight', 'directionalLight',
                             'pointLight', 'spotLight', 'volumeLight']
        self.assertItemsEqual(defaultLightNodes, lightNodes)

    def test_getLightNodesForRenderer(self):
        lightNodes = tools.getRendererLightNodes('mtoa')
        arnoldLightNodes = ['aiPhotometricLight', 'aiMeshLight', 'aiSkyDomeLight',
                            'aiSky', 'aiAreaLight']
        self.assertItemsEqual(lightNodes, arnoldLightNodes)


class FunctionsTest(unittest.TestCase):
    def setUp(self):
        light1 = mc.spotLight()
        light2 = mc.spotLight()
        light3 = mc.spotLight()
        light4 = mc.spotLight()
        light5 = mc.spotLight()

        self.light1Trans = mc.listRelatives(light1, parent=True, fullPath=True)[0]
        self.light2Trans = mc.listRelatives(light2, parent=True, fullPath=True)[0]
        self.light3Trans = mc.listRelatives(light3, parent=True, fullPath=True)[0]
        self.light4Trans = mc.listRelatives(light4, parent=True, fullPath=True)[0]
        self.light5Trans = mc.listRelatives(light5, parent=True, fullPath=True)[0]

        mc.setAttr(self.light4Trans + '.visibility', 0)
        mc.setAttr(self.light5Trans + '.visibility', 0)
        tools.storeLightsOffStatus()

    def test_simpleIsolateLights(self):
        mc.select(self.light1Trans,replace=True)
        tools.simpleIsolateLights()
        self.assertTrue(mc.getAttr(self.light1Trans + '.visibility'))
        self.assertFalse(mc.getAttr(self.light2Trans + '.visibility'))
        self.assertFalse(mc.getAttr(self.light4Trans + '.visibility'))

        tools.simpleIsolateLights()
        self.assertTrue(mc.getAttr(self.light1Trans + '.visibility'))
        self.assertTrue(mc.getAttr(self.light2Trans + '.visibility'))
        self.assertFalse(mc.getAttr(self.light4Trans + '.visibility'))


# --------------------------------------------------------
#  Main
# --------------------------------------------------------
if __name__ == "__main__" or 'eclipsePython' in __name__:
    unittest.main()
