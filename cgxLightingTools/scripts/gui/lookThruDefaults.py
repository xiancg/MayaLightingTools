'''
Created on July 20, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
'''
from __future__ import absolute_import
from PySide2 import QtCore, QtWidgets
import cgxLightingTools.scripts.gui.mayaWindow as mWin

class LookThruDefaults_GUI(QtWidgets.QDialog):
    def __init__(self, parent= mWin.getMayaWindow()):
        super(LookThruDefaults_GUI, self).__init__(parent)
        self._setupUi()
        self._setConnections()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

    def _setupUi(self):
        self.setObjectName('LookThruDefaults_DIALOG')
        self.setWindowTitle('Look Thru Defaults')
        winSize = QtCore.QSize(242, 152)
        self.resize(winSize.width(), winSize.height())
        self.setMinimumSize(winSize)
        self.setMaximumSize(winSize)
        self._createButtons()
        mainLayout = QtWidgets.QGridLayout(self)
        mainLayout.setObjectName("tools_GRIDLAY")

        mainLayout.addWidget(self.winWidth_LABEL, 0, 1, 1, 1, QtCore.Qt.AlignCenter)
        mainLayout.addWidget(self.winHeight_LABEL, 0, 3, 1, 1, QtCore.Qt.AlignCenter)
        mainLayout.addWidget(self.winWidth_SPINBOX, 1, 1, 1, 1, QtCore.Qt.AlignCenter)
        mainLayout.addWidget(self.winHeight_SPINBOX, 1, 3, 1, 1, QtCore.Qt.AlignCenter)
        mainLayout.addWidget(self.nearClip_LABEL, 2, 1, 1, 1, QtCore.Qt.AlignCenter)
        mainLayout.addWidget(self.farClip_LABEL, 2, 3, 1, 1, QtCore.Qt.AlignCenter)
        mainLayout.addWidget(self.nearClip_DBLSPINBOX, 3, 1, 1, 1, QtCore.Qt.AlignCenter)
        mainLayout.addWidget(self.farClip_DBLSPINBOX, 3, 3, 1, 1, QtCore.Qt.AlignCenter)
        mainLayout.addWidget(self.save_BTN, 5, 1, 1, 2, QtCore.Qt.AlignCenter)
        mainLayout.addWidget(self.cancel_BTN, 5, 3, 1, 2, QtCore.Qt.AlignCenter)
        mainLayout.setColumnMinimumWidth(2,10)
        mainLayout.setColumnStretch(2,10)
        mainLayout.setRowMinimumHeight(4,6)
        mainLayout.setRowStretch(4,6)

        self.setLayout(mainLayout)

        QtCore.QMetaObject.connectSlotsByName(self)
        
    
    def _createButtons(self):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                            QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        btnSize = QtCore.QSize(81, 23)
        self.save_BTN = QtWidgets.QPushButton(self)
        self.cancel_BTN = QtWidgets.QPushButton(self)
        self.save_BTN.setSizePolicy(sizePolicy)
        self.save_BTN.setMinimumSize(btnSize)
        self.save_BTN.setMaximumSize(btnSize)
        self.save_BTN.setObjectName('save_BTN')
        self.save_BTN.setText('Save')
        self.cancel_BTN.setSizePolicy(sizePolicy)
        self.cancel_BTN.setMinimumSize(btnSize)
        self.cancel_BTN.setMaximumSize(btnSize)
        self.cancel_BTN.setObjectName('save_BTN')
        self.cancel_BTN.setText('Cancel')
        labelSize = QtCore.QSize(111, 16)
        self.winWidth_LABEL = QtWidgets.QLabel(self)
        self.winHeight_LABEL = QtWidgets.QLabel(self)
        self.nearClip_LABEL = QtWidgets.QLabel(self)
        self.farClip_LABEL = QtWidgets.QLabel(self)
        self.winWidth_LABEL.setSizePolicy(sizePolicy)
        self.winWidth_LABEL.setMinimumSize(labelSize)
        self.winWidth_LABEL.setMaximumSize(labelSize)
        self.winWidth_LABEL.setObjectName('winWidth_LABEL')
        self.winWidth_LABEL.setText('Window Width')
        self.winHeight_LABEL.setSizePolicy(sizePolicy)
        self.winHeight_LABEL.setMinimumSize(labelSize)
        self.winHeight_LABEL.setMaximumSize(labelSize)
        self.winHeight_LABEL.setObjectName('winHeight_LABEL')
        self.winHeight_LABEL.setText('Window Height')
        self.nearClip_LABEL.setSizePolicy(sizePolicy)
        self.nearClip_LABEL.setMinimumSize(labelSize)
        self.nearClip_LABEL.setMaximumSize(labelSize)
        self.nearClip_LABEL.setObjectName('nearClip_LABEL')
        self.nearClip_LABEL.setText('Near Clipping Plane')
        self.farClip_LABEL.setSizePolicy(sizePolicy)
        self.farClip_LABEL.setMinimumSize(labelSize)
        self.farClip_LABEL.setMaximumSize(labelSize)
        self.farClip_LABEL.setObjectName('farClip_LABEL')
        self.farClip_LABEL.setText('Far Clipping Plane')
        spinBoxSize = QtCore.QSize(101, 22)
        self.winWidth_SPINBOX = QtWidgets.QSpinBox(self)
        self.winHeight_SPINBOX = QtWidgets.QSpinBox(self)
        self.nearClip_DBLSPINBOX = QtWidgets.QDoubleSpinBox(self)
        self.farClip_DBLSPINBOX = QtWidgets.QDoubleSpinBox(self)
        self.winWidth_SPINBOX.setSizePolicy(sizePolicy)
        self.winWidth_SPINBOX.setMinimumSize(spinBoxSize)
        self.winWidth_SPINBOX.setMaximumSize(spinBoxSize)
        self.winWidth_SPINBOX.setObjectName('winWidth_SPINBOX')
        self.winHeight_SPINBOX.setSizePolicy(sizePolicy)
        self.winHeight_SPINBOX.setMinimumSize(spinBoxSize)
        self.winHeight_SPINBOX.setMaximumSize(spinBoxSize)
        self.winHeight_SPINBOX.setObjectName('winHeight_SPINBOX')
        self.nearClip_DBLSPINBOX.setSizePolicy(sizePolicy)
        self.nearClip_DBLSPINBOX.setMinimumSize(spinBoxSize)
        self.nearClip_DBLSPINBOX.setMaximumSize(spinBoxSize)
        self.nearClip_DBLSPINBOX.setObjectName('nearClip_DBLSPINBOX')
        self.farClip_DBLSPINBOX.setSizePolicy(sizePolicy)
        self.farClip_DBLSPINBOX.setMinimumSize(spinBoxSize)
        self.farClip_DBLSPINBOX.setMaximumSize(spinBoxSize)
        self.farClip_DBLSPINBOX.setObjectName('farClip_DBLSPINBOX')

       


    def _setConnections(self):
        pass


# --------------------------------------------------------
#  Main
# --------------------------------------------------------
def main():
    temp = LookThruDefaults_GUI()
    temp.show()


if __name__ == '__main__' or 'eclipsePython' in __name__:
    main()