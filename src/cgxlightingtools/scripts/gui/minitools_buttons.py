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
        self.parent = parent
        self.collect_stats = False
        
    def mousePressEvent(self, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.RightButton:
                cursor = QtGui.QCursor()
                self.rightClick.emit(self.mapFromGlobal(cursor.pos()), self)
                if self.collect_stats:
                    stats.collect(self.objectName())
            else:
                super(MiniTools_BTN, self).mousePressEvent(event)
                if self.collect_stats:
                    stats.collect(self.objectName())


class VisSnapshot_BTN(MiniTools_BTN):
    def __init__(self, parent=None):
        super(VisSnapshot_BTN, self).__init__(parent)
        self._snap = dict()
        self._is_active = False
        self.update_status_style()

    def update_status_style(self):
        if self.snap and self.is_active:
            self.setStyleSheet("background-color: green")
        elif self.snap and not self.is_active:
            self.setStyleSheet("background-color: orange")
        else:
            self.setStyleSheet("background-color: grey")
    
    @property
    def is_active(self):
        return self._is_active
    
    @is_active.setter
    def is_active(self, a):
        self._is_active = a
        self.update_status_style()

    @property
    def snap(self):
        return self._snap

    @snap.setter
    def snap(self, d):
        self._snap = d
        self.update_status_style()

# --------------------------------------------------------
#  Main
# --------------------------------------------------------
def main():
    pass

if __name__ == '__main__' or 'eclipsePython' in __name__:
    main()