'''
Created on July 4, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
Based upon the work of Cesar Saez https://www.cesarsaez.me
'''
import string

rule = '{category}_{function}_{whatAffects}_{digits}_{type}'
tokens = dict()


def addToken(name,**kwargs):
    if len(kwargs) == 0:
        tokens[name] = None
        return True
    if kwargs.get('default'):
        kwargs['_default'] = kwargs['default']
        del kwargs['default']
    tokens[name] = kwargs
    return True


def removeToken(name):
    if name in tokens.keys():
        del tokens[name]
        return True
    return False


def resetTokens():
    tokens.clear()
    return True


def parse(name):
    retval = dict()
    fields = [x[1] for x in string.Formatter().parse(rule)]
    splitName = name.split('_')
    for i, f in enumerate(fields):
        namePart = splitName[i]
        lookup = tokens[f]
        if lookup is None: #required
            retval[f] = namePart
            continue
        for key, value in lookup.iteritems():
            if namePart == value and key != '_default':
                retval[f] = key
                break
    return retval


def solve(*args, **kwargs):
    values = dict()
    fields = [x[1] for x in string.Formatter().parse(rule)]
    i = 0
    for f in fields:
        lookup = tokens[f]
        if lookup is None: #required
            if kwargs.get(f) is not None:
                values[f] = kwargs[f]
                continue
            values[f] = args[i]
            i += 1
            continue
        if kwargs.get(f) in lookup.keys():
            values[f] = lookup[kwargs.get(f, '_default')]
        else:
            values[f] = lookup['_default']

    return rule.format(**values)
