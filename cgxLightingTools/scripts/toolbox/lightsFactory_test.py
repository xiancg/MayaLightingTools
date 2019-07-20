'''
Created on July 9, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
'''
from __future__ import absolute_import
'''
import maya.standalone
maya.standalone.initialize()'''
import maya.cmds as mc
# mc.loadPlugin('mtoa')

import unittest
from cgxLightingTools.scripts.toolbox.lightsFactory.default_factory import LightsFactory
from cgxLightingTools.scripts.toolbox.lightsFactory.mtoa_factory import ArnoldFactory

class FactoryTest(unittest.TestCase):
    def test_createLight(self):
        factory = LightsFactory()
        lightName = factory.buildName('chars', 16, category='dramatic', function='bounce')
        lightCreated = factory.createLight('spotLight', lightName)
        name = 'dramatic_bounce_chars_016_LGT'
        self.assertEqual(lightCreated[0], name)
    
    def test_createLight_existing(self):
        factory = LightsFactory()
        mc.spotLight(name='dramatic_bounce_chars_016_LGT')
        mc.spotLight(name='dramatic_bounce_chars_017_LGT')
        lightName = factory.buildName('chars', 16, category='dramatic', function='bounce')
        lightCreated = factory.createLight('spotLight', lightName)
        name = 'dramatic_bounce_chars_018_LGT'
        self.assertEqual(lightCreated[0], name)
    
    def test_createArnoldLight(self):
        factory = ArnoldFactory()
        lightName = factory.buildName('chars', number=125)
        lightCreated = factory.createLight('aiAreaLight', lightName)
        name = 'natural_custom_chars_125_LGT'
        self.assertEqual(lightCreated[0], name)
    
    def test_createMeshLight(self):
        factory = ArnoldFactory()
        cube = mc.polyCube()
        mc.select(cube, replace=True)
        lightName = factory.buildName('chars', number=7)
        lightCreated = factory.createLight('aiMeshLight', lightName)
        name = 'natural_custom_chars_007_LGT'
        self.assertEqual(lightCreated[0], name)
    
    def test_duplicateLight(self):
        factory = LightsFactory()
        lightName = factory.buildName('chars', 16, category='dramatic', function='bounce')
        lightCreated = factory.createLight('spotLight', lightName)
        duplicatedLight = factory.duplicateLight(lightCreated[0])
        name = 'dramatic_bounce_chars_017_LGT'
        self.assertEqual(duplicatedLight[0], name)

# --------------------------------------------------------
#  Main
# --------------------------------------------------------
if __name__ == '__main__':
    unittest.main()