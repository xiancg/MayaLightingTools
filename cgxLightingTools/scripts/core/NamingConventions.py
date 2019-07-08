'''
Created on July 4, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
Based upon the work of Cesar Saez https://www.cesarsaez.me
'''
import string

rule = '{category}_{function}_{whatAffects}_{digits}_{type}'
tokens = {
    'category': {'natural': 'natural',
                 'practical': 'practical',
                 'dramatic': 'dramatic',
                 'volumetric': 'volumetric',
                 '_default': 'natural'
                 },
    'function': {'key': 'key',
                 'fill': 'fill',
                 'ambient': 'ambient',
                 'bounce': 'bounce',
                 'rim': 'rim',
                 'kick': 'kick',
                 '_default': 'custom'
                 },
    'whatAffects': None,
    'digits': None,
    'type': {
        'lighting': 'LGT',
        'animation': 'ANI',
        '_default': 'LGT'
    }
}


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
