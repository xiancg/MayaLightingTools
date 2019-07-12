'''
Created on July 10, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
'''
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide2 import QtWidgets, QtCore
import cgxLightingTools.scripts.gui.mayaWindow as mWin


class DialogWidget(MayaQWidgetDockableMixin, QtWidgets.QDialog):
    def __init__(self, parent=mWin.getMayaWindow()):
        super(DialogWidget, self).__init__(parent=parent)
        self.setObjectName('MY_CUSTOM_UI')
        self.setWindowTitle('TEST')
        layout = QtWidgets.QGridLayout()
        button = QtWidgets.QPushButton("HELP")
        layout.addWidget(button)
        self.setLayout(layout)

# --------------------------------------------------------
#  Main
# --------------------------------------------------------
def main():
    test = DialogWidget()
    test.show(dockable=True)


if __name__ == '__main__' or 'eclipsePython' in __name__:
    main()