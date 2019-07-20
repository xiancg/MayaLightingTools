# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'M:\CGXLightingTools\cgxLightingTools\scripts\gui\uiSketch\LookThruDefaults.ui'
#
# Created: Sat Jul 20 19:57:25 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_LookThruPrefs(object):
    def setupUi(self, LookThruPrefs):
        LookThruPrefs.setObjectName("LookThruPrefs")
        LookThruPrefs.resize(242, 152)
        LookThruPrefs.setMinimumSize(QtCore.QSize(242, 152))
        LookThruPrefs.setMaximumSize(QtCore.QSize(242, 152))
        self.save_BTN = QtGui.QPushButton(LookThruPrefs)
        self.save_BTN.setGeometry(QtCore.QRect(30, 120, 81, 23))
        self.save_BTN.setObjectName("save_BTN")
        self.cancel_BTN = QtGui.QPushButton(LookThruPrefs)
        self.cancel_BTN.setGeometry(QtCore.QRect(124, 120, 81, 23))
        self.cancel_BTN.setObjectName("cancel_BTN")
        self.winWidth_LABEL = QtGui.QLabel(LookThruPrefs)
        self.winWidth_LABEL.setGeometry(QtCore.QRect(10, 10, 111, 16))
        self.winWidth_LABEL.setObjectName("winWidth_LABEL")
        self.winHeight_LABEL = QtGui.QLabel(LookThruPrefs)
        self.winHeight_LABEL.setGeometry(QtCore.QRect(130, 10, 111, 16))
        self.winHeight_LABEL.setObjectName("winHeight_LABEL")
        self.nearClip_LABEL = QtGui.QLabel(LookThruPrefs)
        self.nearClip_LABEL.setGeometry(QtCore.QRect(10, 60, 111, 16))
        self.nearClip_LABEL.setObjectName("nearClip_LABEL")
        self.farClip_LABEL = QtGui.QLabel(LookThruPrefs)
        self.farClip_LABEL.setGeometry(QtCore.QRect(130, 60, 111, 16))
        self.farClip_LABEL.setObjectName("farClip_LABEL")
        self.winWidth_SPINBOX = QtGui.QSpinBox(LookThruPrefs)
        self.winWidth_SPINBOX.setGeometry(QtCore.QRect(10, 30, 101, 22))
        self.winWidth_SPINBOX.setObjectName("winWidth_SPINBOX")
        self.nearClip_DBLSPINBOX = QtGui.QDoubleSpinBox(LookThruPrefs)
        self.nearClip_DBLSPINBOX.setGeometry(QtCore.QRect(10, 80, 101, 22))
        self.nearClip_DBLSPINBOX.setObjectName("nearClip_DBLSPINBOX")
        self.winHeight_SPINBOX = QtGui.QSpinBox(LookThruPrefs)
        self.winHeight_SPINBOX.setGeometry(QtCore.QRect(130, 30, 101, 22))
        self.winHeight_SPINBOX.setObjectName("winHeight_SPINBOX")
        self.farClip_DBLSPINBOX = QtGui.QDoubleSpinBox(LookThruPrefs)
        self.farClip_DBLSPINBOX.setGeometry(QtCore.QRect(130, 80, 101, 22))
        self.farClip_DBLSPINBOX.setObjectName("farClip_DBLSPINBOX")

        self.retranslateUi(LookThruPrefs)
        QtCore.QMetaObject.connectSlotsByName(LookThruPrefs)

    def retranslateUi(self, LookThruPrefs):
        LookThruPrefs.setWindowTitle(QtGui.QApplication.translate("LookThruPrefs", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.save_BTN.setText(QtGui.QApplication.translate("LookThruPrefs", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_BTN.setText(QtGui.QApplication.translate("LookThruPrefs", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.winWidth_LABEL.setText(QtGui.QApplication.translate("LookThruPrefs", "Window Width", None, QtGui.QApplication.UnicodeUTF8))
        self.winHeight_LABEL.setText(QtGui.QApplication.translate("LookThruPrefs", "Window Height", None, QtGui.QApplication.UnicodeUTF8))
        self.nearClip_LABEL.setText(QtGui.QApplication.translate("LookThruPrefs", "Near Clipping Plane", None, QtGui.QApplication.UnicodeUTF8))
        self.farClip_LABEL.setText(QtGui.QApplication.translate("LookThruPrefs", "Far Clipping Plane", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    LookThruPrefs = QtGui.QDialog()
    ui = Ui_LookThruPrefs()
    ui.setupUi(LookThruPrefs)
    LookThruPrefs.show()
    sys.exit(app.exec_())

