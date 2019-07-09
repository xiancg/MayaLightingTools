'''
Created on July 4, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
Heavily based upon the work of Cesar Saez https://www.cesarsaez.me
'''

import unittest
from cgxLightingTools.scripts.core import namingConventions as n
import tempfile

class SolveCase(unittest.TestCase):
    def setUp(self):
        n.resetTokens()
        n.addToken('whatAffects')
        n.addTokenNumber('digits')
        n.addToken('category', natural='natural', 
                    practical='practical', dramatic='dramatic',
                    volumetric='volumetric', default='natural')
        n.addToken('function', key='key', 
                    fill='fill', ambient='ambient',
                    bounce='bounce', rim='rim',
                    kick='kick', default='custom')
        n.addToken('type', lighting='LGT', 
                    animation='ANI', default='LGT')

        n.resetRules()
        n.addRule('lights', 'category', 'function', 'whatAffects', 'digits', 'type')
        return super(SolveCase, self).setUp()

    def test_explicit(self):
        name = 'natural_ambient_chars_001_LGT'
        solved = n.solve(category='natural', function='ambient',
                         whatAffects='chars', digits=1, type='lighting')
        self.assertEqual(solved, name)

    def test_noMatchForToken(self):
        name = 'natural_ambient_chars_001_LGT'
        solved = n.solve(category='natural', function='sarasa',
                         whatAffects='chars', digits=1, type='lighting')
        self.assertNotEqual(name, solved)

    def test_defaults(self):
        name = 'natural_custom_chars_001_LGT'
        solved = n.solve(category='natural', whatAffects='chars',
                         digits=1, type='lighting')
        self.assertEqual(solved, name)

        name = 'natural_custom_chars_001_LGT'
        solved = n.solve(whatAffects='chars',digits=1)
        self.assertEqual(solved, name)
    
    def test_implicit(self):
        name = 'natural_custom_chars_001_ANI'
        solved = n.solve('chars',1,type='animation')
        self.assertEqual(solved, name)

        name = 'natural_custom_chars_001_LGT'
        solved = n.solve('chars',1)
        self.assertEqual(solved, name)


class ParseCase(unittest.TestCase):
    def setUp(self):
        n.resetTokens()
        n.addToken('whatAffects')
        n.addTokenNumber('digits')
        n.addToken('category', natural='natural', 
                    practical='practical', dramatic='dramatic',
                    volumetric='volumetric', default='natural')
        n.addToken('function', key='key', 
                    fill='fill', ambient='ambient',
                    bounce='bounce', rim='rim',
                    kick='kick', default='custom')
        n.addToken('type', lighting='LGT', 
                    animation='ANI', default='LGT')
        
        n.resetRules()
        n.addRule('lights', 'category', 'function', 'whatAffects', 'digits', 'type')
        return super(ParseCase, self).setUp()

    def test_parsing(self):
        name = 'dramatic_bounce_chars_001_LGT'
        parsed = n.parse(name)
        self.assertEqual(parsed['category'], 'dramatic')
        self.assertEqual(parsed['function'], 'bounce')
        self.assertEqual(parsed['whatAffects'], 'chars')
        self.assertEqual(parsed['digits'], 1)
        self.assertEqual(parsed['type'], 'lighting')


class TokenCase(unittest.TestCase):
    def setUp(self):
        n.resetTokens()
        return super(TokenCase, self).setUp()
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
        result = n.removeToken('test')
        self.assertTrue(result)

        result = n.removeToken('test2')
        self.assertFalse(result)


class RuleCase(unittest.TestCase):
    def setUp(self):
        n.resetRules()
        return super(RuleCase, self).setUp()

    def test_add(self):
        result = n.addRule('lights', 'category', 'function', 'whatAffects', 'digits', 'type')
        self.assertTrue(result)
    
    def test_resetRules(self):
        result = n.resetRules()
        self.assertTrue(result)
    
    def test_removeRule(self):
        n.addRule('test', 'category', 'function', 'digits', 'type')
        result = n.removeRule('test')
        self.assertTrue(result)

        result = n.removeRule('test2')
        self.assertFalse(result)
    
    def test_active(self):
        pattern = '{category}_{function}_{digits}_{type}'
        n.addRule('lights', 'category', 'function', 'whatAffects', 'digits', 'type')
        n.addRule('test', 'category', 'function', 'digits', 'type')
        n.setActiveRule('test')
        result = n.getActiveRule()
        self.assertIsNotNone(result)


class SerializationCase(unittest.TestCase):
    def setUp(self):
        n.resetRules()
        n.resetTokens()

    def test_tokens(self):
        token1 = n.addToken('function', key='key', 
                    fill='fill', ambient='ambient',
                    bounce='bounce', rim='rim',
                    kick='kick', default='custom')
        token2 = n.Token.fromData(token1.data())
        self.assertEqual(token1.data(),token2.data())
    
    def test_rules(self):
        rule1 = n.addRule('lights', 'category', 'function', 'whatAffects', 'digits', 'type')
        rule2 = n.Rule.fromData(rule1.data())
        self.assertEqual(rule1.data(),rule2.data())
    
    def test_validation(self):
        token = n.addToken('function', key='key', 
                    fill='fill', ambient='ambient',
                    bounce='bounce', rim='rim',
                    kick='kick', default='custom')
        rule = n.addRule('lights', 'category', 'function', 'whatAffects', 'digits', 'type')
        self.assertIsNone(n.Rule.fromData(token.data()))
        self.assertIsNone(n.Token.fromData(rule.data()))
    
    def test_save_load_rule(self):
        n.addRule('test', 'category', 'function', 'whatAffects', 'digits', 'type')
        filepath = tempfile.mktemp()
        n.saveRule('test', filepath)

        n.resetRules()
        n.loadRule(filepath)
        self.assertTrue(n.hasRule('test'))

    def test_save_load_token(self):
        n.addToken('test', key='key', 
                    fill='fill', ambient='ambient',
                    bounce='bounce', rim='rim',
                    kick='kick', default='custom')
        filepath = tempfile.mktemp()
        n.saveToken('test', filepath)

        n.resetTokens()
        n.loadToken(filepath)
        self.assertTrue(n.hasToken('test'))
    
    def test_save_load_session(self):
        n.addToken('whatAffects')
        n.addTokenNumber('digits')
        n.addToken('category', natural='natural', 
                    practical='practical', dramatic='dramatic',
                    volumetric='volumetric', default='natural')
        n.addToken('function', key='key', 
                    fill='fill', ambient='ambient',
                    bounce='bounce', rim='rim',
                    kick='kick', default='custom')
        n.addToken('type', lighting='LGT', 
                    animation='ANI', default='LGT')
        n.addRule('lights', 'category', 'function', 'whatAffects', 'digits', 'type')
        n.addRule('test', 'category', 'function')
        n.setActiveRule('lights')

        repo = tempfile.mkdtemp()
        n.saveSession(repo)

        n.resetRules()
        n.resetTokens()

        n.loadSession(repo)
        self.assertTrue(n.hasToken('whatAffects'))
        self.assertTrue(n.hasToken('digits'))
        self.assertTrue(n.hasToken('category'))
        self.assertTrue(n.hasToken('function'))
        self.assertTrue(n.hasToken('type'))
        self.assertTrue(n.hasRule('lights'))
        self.assertTrue(n.hasRule('test'))
        self.assertEqual(n.getActiveRule().name, 'lights')


class NumberTokenCase(unittest.TestCase):
    def setUp(self):
        n.resetTokens()
        n.addToken('whatAffects')
        n.addTokenNumber('number') 
        n.addToken('category', natural='natural', 
                    practical='practical', dramatic='dramatic',
                    volumetric='volumetric', default='natural')
        n.addToken('function', key='key', 
                    fill='fill', ambient='ambient',
                    bounce='bounce', rim='rim',
                    kick='kick', default='custom')
        n.addToken('type', lighting='LGT', default='LGT')
        n.addRule('lights', 'category', 'function', 'whatAffects', 'number', 'type')
        return super(NumberTokenCase, self).setUp()

    def test_explicitSolve(self):
        name = 'natural_ambient_chars_024_LGT'
        solved = n.solve(category='natural', function='ambient',
                        whatAffects='chars', number=24, type='lighting')
        self.assertEqual(solved, name)
    
    def test_implicitSolve(self):
        name = 'natural_custom_chars_032_LGT'
        solved = n.solve('chars',32)
        self.assertEqual(solved, name)


if __name__ == '__main__':
    unittest.main()
