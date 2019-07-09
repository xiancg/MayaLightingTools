import os
import cgxLightingTools.scripts.core.namingConventions as n

repoPath = os.path.join(os.path.dirname(os.path.abspath(n.__file__)),'cfg')
os.environ['NAMING_REPO'] = repoPath

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

n.saveSession()