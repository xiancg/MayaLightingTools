# -*- coding: utf-8 -*-
'''
Interpret and wrap ui files.

Created on Mar 25, 2016

@author: Chris Granados - Xian chris.granados@xiancg.com http://www.chrisgranados.com/
'''


##--------------------------------------------------------------------------------------------
##imports
##--------------------------------------------------------------------------------------------
from cgx.gui.Qt import QtCore, QtWidgets
from cgx.gui.Qt import __binding__

if __binding__ in ('PySide2', 'PyQt5'):
    import pyside2uic
    import shiboken2
elif __binding__ in ('PySide', 'PyQt4'):
    import pysideuic
    import shiboken
else:
    print('No Qt binding available.')

import xml.etree.ElementTree as xml
from cStringIO import StringIO


##--------------------------------------------------------------------------------------------
##Metadata
##--------------------------------------------------------------------------------------------
__author__ = "Chris Granados"
__copyright__ = "Copyright 2016, Chris Granados"
__credits__ = ["Jason Parks","Nathan Horne","Chris Granados", "Max Rocamora"]
__version__ = "2.0.0"
__email__ = "chris.granados@xiancg.com"


##--------------------------------------------------------------------------------------------
##PySide defs- by Jason Parks and Nathan Horne
##--------------------------------------------------------------------------------------------
def loadUiType(uiFile):
    """
    Pyside lacks the "loadUiType" command, so we have to convert the ui file to py code in-memory first
    and then execute it in a special frame to retrieve the form_class.
    """
    parsed = xml.parse(uiFile)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(uiFile, 'r') as f:
        o = StringIO()
        frame = {}
        if __binding__ in ('PySide', 'PyQt4'):
            pysideuic.compileUi(f, o, indent=0)
        elif __binding__ in ('PySide2', 'PyQt5'):
            pyside2uic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame
        
        #Fetch the base_class and form class based on their type in the xml from designer
        form_class = frame['Ui_%s'%form_class]
        
        base_class = eval('QtWidgets.%s'%widget_class)
    return form_class, base_class


def wrapinstance(ptr, base=None):
    """
    Utility to convert a pointer to a Qt class instance (PySide/PyQt compatible)

    :param ptr: Pointer to QObject in memory
    :type ptr: long or Swig instance
    :param base: (Optional) Base class to wrap with (Defaults to QObject, which should handle anything)
    :type base: QtWidgets.QWidget
    :return: QWidget or subclass instance
    :rtype: QtWidgets.QWidget
    """
    if ptr is None:
        return None
    ptr = long(ptr) #Ensure type
    if __binding__ in ('PySide', 'PyQt4'):
        if globals().has_key('shiboken'):
            if base is None:
                qObj = shiboken.wrapInstance(long(ptr), QtCore.QObject)
                metaObj = qObj.metaObject()
                cls = metaObj.className()
                superCls = metaObj.superClass().className()
                if hasattr(QtWidgets, cls):
                    base = getattr(QtWidgets, cls)
                elif hasattr(QtWidgets, superCls):
                    base = getattr(QtWidgets, superCls)
                else:
                    base = QtWidgets.QWidget
            return shiboken.wrapInstance(long(ptr), base)
        else:
            return None
    elif __binding__ in ('PySide2', 'PyQt5'):
        if globals().has_key('shiboken2'):
            if base is None:
                qObj = shiboken2.wrapInstance(long(ptr), QtCore.QObject)
                metaObj = qObj.metaObject()
                cls = metaObj.className()
                superCls = metaObj.superClass().className()
                if hasattr(QtWidgets, cls):
                    base = getattr(QtWidgets, cls)
                elif hasattr(QtWidgets, superCls):
                    base = getattr(QtWidgets, superCls)
                else:
                    base = QtWidgets.QWidget
            return shiboken2.wrapInstance(long(ptr), base)
        else:
            return None
    else:
        return None


##--------------------------------------------------------------------------------------------
## Main
##--------------------------------------------------------------------------------------------
def main():
    pass


if __name__=="__main__":
    main()