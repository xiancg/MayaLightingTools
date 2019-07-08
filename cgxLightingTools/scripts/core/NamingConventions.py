'''
Created on July 4, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
Based upon the work of Cesar Saez https://www.cesarsaez.me
'''
import string

_rules = {'_active': None}
_tokens = dict()

class Token(object):
    def __init__(self, name):
        super(Token, self).__init__()
        self._name = name
        self._default = None
        self._options = dict()
    
    def addOption(self, key, value):
        self._options[key] = value

    def solve(self, name=None):
        '''Solve for abbreviation given a certain name. Ex: center could return C'''
        if name is None:
            return self.default
        return self._options.get(name)
    
    def parse(self, value):
        '''Get metatada (origin) for given value in name. Ex: L could return left'''
        for k, v in self._options.iteritems():
            if v == value:
                return k
    
    @property
    def required(self):
        return self.default is None
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, n):
        self._name = n
    
    @property
    def default(self):
        if self._default is None and len(self._options):
            self._default = self._options.values()[0]
        return self._default
    
    @default.setter
    def default(self, d):
        self._default = d


class Rule(object):
    def __init__(self, name, fields):
        super(Rule, self).__init__()
        self.name = name
        self._fields = list()
        self.addFields(fields)
    
    def addFields(self, tokenNames):
        self._fields.extend(tokenNames)
        return True
    
    def solve(self, **values):
        '''Build the name string with given values and return it'''
        return self._pattern.format(**values)
    
    def parse(self, name):
        '''Build and return dictionary with keys as tokens and values as given names'''
        retval = dict()
        splitName = name.split('_')
        for i, f in enumerate(self.fields):
            namePart = splitName[i]
            token = _tokens[f]
            if token.required:
                retval[f] = namePart
                continue
            retval[f] = token.parse(namePart)
        return retval

    @property
    def _pattern(self):
        return '{' + '}_{'.join(self.fields) + '}'

    @property
    def fields(self):
        return tuple(self._fields)

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, n):
        self._name = n


def addRule(name, *fields):
    rule = Rule(name, fields)
    _rules[name] = rule
    if getActiveRule() is None:
        setActiveRule(name)
    return True


def removeRule(name):
    if hasRule(name):
        del _rules[name]
        return True
    return False


def hasRule(name):
    return name in _rules.keys()


def resetRules():
    _rules.clear()
    _rules['_active'] = None
    return True


def getActiveRule():
    name = _rules['_active']
    return _rules.get(name)


def setActiveRule(name):
    if hasRule(name):
        _rules['_active'] = name
        return True
    return False


def addToken(name,**kwargs):
    token = Token(name)
    for k, v in kwargs.iteritems():
        if k == "default":
            token.default = v
            continue
        token.addOption(k, v)
    _tokens[name] = token
    return token


def removeToken(name):
    if hasToken(name):
        del _tokens[name]
        return True
    return False


def hasToken(name):
    return name in _tokens.keys()


def resetTokens():
    _tokens.clear()
    return True


def parse(name):
    rule = getActiveRule()
    return rule.parse(name)
    

def solve(*args, **kwargs):
    values = dict()
    rule = getActiveRule()
    i = 0
    for f in rule.fields:
        token = _tokens[f]
        if token.required:
            if kwargs.get(f) is not None:
                values[f] = kwargs[f]
                continue
            values[f] = args[i]
            i += 1
            continue
        values[f] = token.solve(kwargs.get(f))

    return rule.solve(**values)
