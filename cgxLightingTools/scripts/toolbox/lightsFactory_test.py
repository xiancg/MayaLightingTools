'''
Created on July 9, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
TODO: Implement padding in naming library
'''
import maya.standalone
maya.standalone.initialize()
import maya.cmds as mc
mc.loadPlugin('mtoa')

import unittest
from cgxLightingTools.scripts.toolbox.lightsFactory.abstract import LightsFactory


class FactoryTest(unittest.TestCase):
    def test_createLight(self):
        factory = LightsFactory()
        lightName = factory.buildName('chars', 16, category='dramatic', function='bounce')
        lightCreated = factory.createLight('spotLight', lightName)
        self.assertTrue(lightCreated)
        name = 'dramatic_bounce_chars_016_LGT'
        self.assertEqual(lightName, name)
    
    def test_createLight_existing(self):
        factory = LightsFactory()
        mc.spotLight(name='dramatic_bounce_chars_016_LGT')
        mc.spotLight(name='dramatic_bounce_chars_017_LGT')
        lightName = factory.buildName('chars', 16, category='dramatic', function='bounce')
        lightCreated = factory.createLight('spotLight', lightName)
        self.assertTrue(lightCreated)
        name = 'dramatic_bounce_chars_018_LGT'
        self.assertEqual(lightName, name)


if __name__ == '__main__':
    unittest.main()