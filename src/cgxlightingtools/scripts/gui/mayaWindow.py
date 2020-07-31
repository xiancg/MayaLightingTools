'''
Created on July 12, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
PySide defs- by Jason Parks and Nathan Horne
'''
from __future__ import absolute_import
import maya.OpenMayaUI as mui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance


def getMayaWindow():
    '''Get the Maya main window as a QMainWindow instance'''
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtWidgets.QWidget)


# --------------------------------------------------------
#  Main
# --------------------------------------------------------
def main():
    pass


if __name__=="__main__":
    main()