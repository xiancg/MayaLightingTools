from __future__ import absolute_import
import os
import cgxLightingTools.scripts.core.namingConventions as n

repoPath = os.path.join(os.path.dirname(os.path.abspath(n.__file__)),'cfg')
os.environ['NAMING_REPO'] = repoPath

n.addToken('whatAffects')
n.addTokenNumber('number')
n.addToken('category', natural='nat', 
            practical='pra', dramatic='dra',
            volumetric='vol', default='nat')
n.addToken('function', key='key', 
            fill='fil', ambient='amb',
            bounce='bnc', rim='rim',
            kick='kik', custom='cst', default='cst')
n.addToken('type', lighting='LGT', default='LGT')
n.addRule('lights', 'category', 'function', 'whatAffects', 'number', 'type')

n.saveSession()