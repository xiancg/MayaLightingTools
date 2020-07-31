# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'M:\CGXLightingTools\cgxLightingTools\scripts\gui\uiSketch\LightCreator.ui'
#
# Created: Wed Jul 17 17:56:01 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(562, 91)
        Dialog.setMinimumSize(QtCore.QSize(562, 91))
        Dialog.setMaximumSize(QtCore.QSize(562, 91))
        self.whatAffects_LINEEDIT = QtGui.QLineEdit(Dialog)
        self.whatAffects_LINEEDIT.setGeometry(QtCore.QRect(250, 30, 113, 20))
        self.whatAffects_LINEEDIT.setObjectName("whatAffects_LINEEDIT")
        self.number_SPINBOX = QtGui.QSpinBox(Dialog)
        self.number_SPINBOX.setGeometry(QtCore.QRect(370, 30, 61, 21))
        self.number_SPINBOX.setObjectName("number_SPINBOX")
        self.function_COMBOBOX = QtGui.QComboBox(Dialog)
        self.function_COMBOBOX.setGeometry(QtCore.QRect(130, 30, 111, 22))
        self.function_COMBOBOX.setObjectName("function_COMBOBOX")
        self.type_COMBOBOX = QtGui.QComboBox(Dialog)
        self.type_COMBOBOX.setGeometry(QtCore.QRect(440, 30, 111, 22))
        self.type_COMBOBOX.setObjectName("type_COMBOBOX")
        self.category_LABEL = QtGui.QLabel(Dialog)
        self.category_LABEL.setGeometry(QtCore.QRect(10, 10, 47, 13))
        self.category_LABEL.setObjectName("category_LABEL")
        self.function_LABEL = QtGui.QLabel(Dialog)
        self.function_LABEL.setGeometry(QtCore.QRect(130, 10, 47, 13))
        self.function_LABEL.setObjectName("function_LABEL")
        self.whatAffects_LABEL = QtGui.QLabel(Dialog)
        self.whatAffects_LABEL.setGeometry(QtCore.QRect(250, 10, 81, 16))
        self.whatAffects_LABEL.setObjectName("whatAffects_LABEL")
        self.number_LABEL = QtGui.QLabel(Dialog)
        self.number_LABEL.setGeometry(QtCore.QRect(370, 10, 47, 13))
        self.number_LABEL.setObjectName("number_LABEL")
        self.type_LABEL = QtGui.QLabel(Dialog)
        self.type_LABEL.setGeometry(QtCore.QRect(440, 10, 47, 13))
        self.type_LABEL.setObjectName("type_LABEL")
        self.create_BTN = QtGui.QPushButton(Dialog)
        self.create_BTN.setGeometry(QtCore.QRect(210, 60, 71, 23))
        self.create_BTN.setObjectName("create_BTN")
        self.cancel_BTN = QtGui.QPushButton(Dialog)
        self.cancel_BTN.setGeometry(QtCore.QRect(290, 60, 71, 23))
        self.cancel_BTN.setObjectName("cancel_BTN")
        self.category_COMBOBOX = QtGui.QComboBox(Dialog)
        self.category_COMBOBOX.setGeometry(QtCore.QRect(10, 30, 111, 22))
        self.category_COMBOBOX.setObjectName("category_COMBOBOX")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.category_LABEL.setText(QtGui.QApplication.translate("Dialog", "Category", None, QtGui.QApplication.UnicodeUTF8))
        self.function_LABEL.setText(QtGui.QApplication.translate("Dialog", "Function", None, QtGui.QApplication.UnicodeUTF8))
        self.whatAffects_LABEL.setText(QtGui.QApplication.translate("Dialog", "What Affects", None, QtGui.QApplication.UnicodeUTF8))
        self.number_LABEL.setText(QtGui.QApplication.translate("Dialog", "Number", None, QtGui.QApplication.UnicodeUTF8))
        self.type_LABEL.setText(QtGui.QApplication.translate("Dialog", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.create_BTN.setText(QtGui.QApplication.translate("Dialog", "Create", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_BTN.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

