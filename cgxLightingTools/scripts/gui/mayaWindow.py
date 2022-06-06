'''
Created on July 12, 2019
Python 3 refactor, Jun 6, 2022

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
PySide defs- by Jason Parks and Nathan Horne
'''
import maya.OpenMayaUI as mui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance


def getMayaWindow():
    '''Get the Maya main window as a QMainWindow instance'''
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QtWidgets.QWidget)
