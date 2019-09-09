'''
@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
Button reimplementation to allow right click and stats collection
'''
from __future__ import absolute_import

from PySide2 import QtWidgets, QtCore, QtGui
from cgxLightingTools.scripts.core import stats

class MiniTools_BTN(QtWidgets.QPushButton):

    rightClick = QtCore.Signal(QtCore.QPoint, super)

    def __init__(self, parent=None):
        super(MiniTools_BTN, self).__init__(parent)
        self.snap = dict()
        self.hasSnap = False
        self.parent = parent
        
    def mousePressEvent(self, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.RightButton:
                cursor = QtGui.QCursor()
                self.rightClick.emit(self.mapFromGlobal(cursor.pos()), self)
                stats.collect(self.objectName())
            else:
                super(MiniTools_BTN, self).mousePressEvent(event)
                stats.collect(self.objectName())

# --------------------------------------------------------
#  Main
# --------------------------------------------------------
def main():
    pass

if __name__ == '__main__' or 'eclipsePython' in __name__:
    main()