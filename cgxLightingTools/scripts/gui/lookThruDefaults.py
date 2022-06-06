'''
Created on July 20, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
'''
from __future__ import absolute_import

import os
import json

from PySide2 import QtCore, QtWidgets
import cgxLightingTools.scripts.gui.mayaWindow as mWin


class LookThruDefaults_GUI(QtWidgets.QDialog):
    def __init__(self, parent=mWin.getMayaWindow()):
        super(LookThruDefaults_GUI, self).__init__(parent)
        self._setupUi()
        self._setConnections()
        self._initCtrls()
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
        mainLayout.setColumnMinimumWidth(2, 10)
        mainLayout.setColumnStretch(2, 10)
        mainLayout.setRowMinimumHeight(4, 6)
        mainLayout.setRowStretch(4, 6)

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
        self.winWidth_SPINBOX.setMaximum(2000)
        self.winWidth_SPINBOX.setMinimum(100)
        self.winHeight_SPINBOX.setSizePolicy(sizePolicy)
        self.winHeight_SPINBOX.setMinimumSize(spinBoxSize)
        self.winHeight_SPINBOX.setMaximumSize(spinBoxSize)
        self.winHeight_SPINBOX.setObjectName('winHeight_SPINBOX')
        self.winHeight_SPINBOX.setMaximum(2000)
        self.winHeight_SPINBOX.setMinimum(100)
        self.nearClip_DBLSPINBOX.setSizePolicy(sizePolicy)
        self.nearClip_DBLSPINBOX.setMinimumSize(spinBoxSize)
        self.nearClip_DBLSPINBOX.setMaximumSize(spinBoxSize)
        self.nearClip_DBLSPINBOX.setObjectName('nearClip_DBLSPINBOX')
        self.nearClip_DBLSPINBOX.setMinimum(0.00001)
        self.nearClip_DBLSPINBOX.setMaximum(100000000)
        self.farClip_DBLSPINBOX.setSizePolicy(sizePolicy)
        self.farClip_DBLSPINBOX.setMinimumSize(spinBoxSize)
        self.farClip_DBLSPINBOX.setMaximumSize(spinBoxSize)
        self.farClip_DBLSPINBOX.setObjectName('farClip_DBLSPINBOX')
        self.farClip_DBLSPINBOX.setMinimum(0.00001)
        self.farClip_DBLSPINBOX.setMaximum(100000000)

    def _setConnections(self):
        self.save_BTN.clicked.connect(self._save)
        self.cancel_BTN.clicked.connect(self._cancel)

    def _save(self):
        userPath = os.path.expanduser("~")
        finalDir = os.path.join(userPath, ".CGXTools")
        try:
            if not os.path.exists(finalDir):
                os.mkdir(finalDir)
        except:
            pass
        filepath = os.path.join(finalDir, "MiniTools.pref")
        config = dict()
        if os.path.exists(filepath):
            with open(filepath) as fp:
                config = json.load(fp)
                config['lookThru_nearClip'] = self.nearClip_DBLSPINBOX.value()
                config['lookThru_farClip'] = self.farClip_DBLSPINBOX.value()
                config['lookThru_winWidth'] = self.winWidth_SPINBOX.value()
                config['lookThru_winHeight'] = self.winHeight_SPINBOX.value()
            with open(filepath, 'w') as fp:
                json.dump(config, fp, indent=4)
        else:
            config = {'lookThru_nearClip': self.nearClip_DBLSPINBOX.value(),
                      'lookThru_farClip': self.farClip_DBLSPINBOX.value(),
                      'lookThru_winWidth': self.winWidth_SPINBOX.value(),
                      'lookThru_winHeight': self.winHeight_SPINBOX.value()}
            with open(filepath, 'w') as fp:
                json.dump(config, fp, indent=4)

        self.done(1)

    def _initCtrls(self):
        userPath = os.path.expanduser("~")
        finalDir = os.path.join(userPath, ".CGXTools")
        filepath = os.path.join(finalDir, "MiniTools.pref")
        config = dict()
        if os.path.exists(filepath):
            with open(filepath) as fp:
                config = json.load(fp)
        valuesList = [config.get('lookThru_nearClip'), config.get('lookThru_farClip'),
                      config.get('lookThru_winWidth'), config.get('lookThru_winHeight')]
        if None not in valuesList:
            self.nearClip_DBLSPINBOX.setValue(config.get('lookThru_nearClip'))
            self.farClip_DBLSPINBOX.setValue(config.get('lookThru_farClip'))
            self.winWidth_SPINBOX.setValue(config.get('lookThru_winWidth'))
            self.winHeight_SPINBOX.setValue(config.get('lookThru_winHeight'))
        else:
            self.nearClip_DBLSPINBOX.setValue(1.0)
            self.farClip_DBLSPINBOX.setValue(1000000)
            self.winWidth_SPINBOX.setValue(629)
            self.winHeight_SPINBOX.setValue(404)

    def _cancel(self):
        self.done(0)


# --------------------------------------------------------
#  Main
# --------------------------------------------------------
def main():
    temp = LookThruDefaults_GUI()
    temp.show()


if __name__ == '__main__' or 'eclipsePython' in __name__:
    main()
