'''
Created on July 4, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
Based upon the work of Cesar Saez https://www.cesarsaez.me
'''

import unittest
from cgxLightingTools.scripts.core import namingConventions as n




class SolveCase(unittest.TestCase):
    def setUp(self):
        n.addToken('whatAffects')
        n.addToken('digits')
        n.addToken('category', natural='natural', 
                    practical='practical', dramatic='dramatic',
                    volumetric='volumetric', default='natural')
        n.addToken('function', key='key', 
                    fill='fill', ambient='ambient',
                    bounce='bounce', rim='rim',
                    kick='kick', default='custom')
        n.addToken('type', lighting='LGT', 
                    animation='ANI', default='LGT')
        return super(SolveCase, self).setUp()
    
    def tearDown(self):
        n.resetTokens()
        return super(SolveCase, self).tearDown()

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


class ParseCase(unittest.TestCase):
    def setUp(self):
        n.addToken('whatAffects')
        n.addToken('digits')
        n.addToken('category', natural='natural', 
                    practical='practical', dramatic='dramatic',
                    volumetric='volumetric', default='natural')
        n.addToken('function', key='key', 
                    fill='fill', ambient='ambient',
                    bounce='bounce', rim='rim',
                    kick='kick', default='custom')
        n.addToken('type', lighting='LGT', 
                    animation='ANI', default='LGT')
        return super(ParseCase, self).setUp()
    
    def tearDown(self):
        n.resetTokens()
        return super(ParseCase, self).tearDown()

    def test_parsing(self):
        name = 'dramatic_bounce_chars_001_LGT'
        parsed = n.parse(name)
        self.assertEqual(parsed['category'], 'dramatic')
        self.assertEqual(parsed['function'], 'bounce')
        self.assertEqual(parsed['whatAffects'], 'chars')
        self.assertEqual(parsed['digits'], '001')
        self.assertEqual(parsed['type'], 'lighting')


class TokenCase(unittest.TestCase):
    def test_add(self):
        result = n.addToken('whatAffects')
        self.assertTrue(result)

        result = n.addToken('category', natural='natural', 
                            practical='practical', dramatic='dramatic',
                            volumetric='volumetric', default='natural')
        self.assertTrue(result)
    
    def test_resetTokens(self):
        result = n.resetTokens()
        self.assertTrue(result)
    
    def test_removeToken(self):
        n.addToken('test')
        print n.tokens.get('test')
        result = n.removeToken('test')
        self.assertTrue(result)

        result = n.removeToken('test2')
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
