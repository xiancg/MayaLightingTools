'''
Python 3 refactor, Jun 6, 2022

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
'''

import os
import json

_stats = {}


def collect(tool):
    if tool in _stats.keys():
        currentValue = _stats.get(tool)
        if currentValue:
            _stats[tool] = currentValue + 1
    else:
        _stats[tool] = 1


def save():
    repo = os.path.join(os.path.expanduser("~"), ".CGXTools")
    filepath = os.path.join(repo, "lightingTools.stats")
    with open(filepath, "w") as fp:
        json.dump(_stats, fp, indent=4)


def load():
    repo = os.path.join(os.path.expanduser("~"), ".CGXTools")
    filepath = os.path.join(repo, "lightingTools.stats")
    if os.path.exists(filepath):
        with open(filepath) as fp:
            return json.load(fp)
        return dict()

# --------------------------------------------------------
#  Main
# --------------------------------------------------------


def main():
    pass


if __name__ == '__main__' or 'eclipsePython' in __name__:
    main()
