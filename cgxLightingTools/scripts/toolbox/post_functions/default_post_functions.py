'''
@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
'''
from __future__ import absolute_import

import maya.cmds as mc

class PostFunctions_default(object):
    def __init__(self):
        super(PostFunctions_default, self).__init__()

    def postLightCreation(self, transformNode, shapeNode, *args, **kwargs):
        '''Place here all custom stuff you want to do with the created light node'''
        mc.select(shapeNode, replace=True)

    def postLightDuplicate(self, transformNode, shapeNode, *args, **kwargs):
        '''Place here all custom stuff you want to do with the duplicated light node'''
        mc.select(shapeNode, replace=True)

    def postLightRename(self, transformNode, shapeNode, *args, **kwargs):
        '''Place here all custom stuff you want to do with the renamed light node'''
        mc.select(shapeNode, replace=True)

    def postLightDelete(self, transformNode, shapeNode, *args, **kwargs):
        '''Place here all custom stuff you want to do with the deleted light node'''
        pass

# --------------------------------------------------------
#  Main
# --------------------------------------------------------
def main():
    pass

if __name__ == '__main__' or 'eclipsePython' in __name__:
    main()