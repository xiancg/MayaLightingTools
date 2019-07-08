'''
Created on July 4, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
Based upon the work of Cesar Saez https://www.cesarsaez.me
'''

import unittest
from cgxLightingTools.scripts.core import namingConventions as n
import maya.cmds as mc

# Digits deberian pasar como # o como el numero en si?


class SolveCase(unittest.TestCase):
    def test_explicit(self):
        name = 'natural_ambient_chars_001_LGT'
        solved = n.solve(category='natural', function='ambient',
                         whatAffects='chars', digits='001', type='lighting')
        self.assertEqual(solved, name)

    def test_noMatchForToken(self):
        name = 'natural_ambient_chars_001_LGT'
        solved = n.solve(category='natural', function='sarasa',
                         whatAffects='chars', digits='001', type='lighting')
        self.assertNotEqual(name, solved)

    def test_defaults(self):
        name = 'natural_custom_chars_001_LGT'
        solved = n.solve(category='natural', whatAffects='chars',
                         digits='001', type='lighting')
        self.assertEqual(solved, name)

        name = 'natural_custom_chars_001_LGT'
        solved = n.solve(whatAffects='chars',digits='001')
        self.assertEqual(solved, name)
    
    def test_implicit(self):
        name = 'natural_custom_chars_001_ANI'
        solved = n.solve('chars','001',type='animation')
        self.assertEqual(solved, name)

        name = 'natural_custom_chars_001_LGT'
        solved = n.solve('chars','001')
        self.assertEqual(solved, name)


def ParseCase(unittest.TestCase):
    def test_parsing(self):
        pass



if __name__ == '__main__':
    unittest.main()
