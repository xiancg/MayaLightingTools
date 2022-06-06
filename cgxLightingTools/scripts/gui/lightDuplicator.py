'''
Created on July 30, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
'''

import maya.cmds as mc
from PySide2 import QtCore, QtWidgets

from cgxLightingTools.scripts.toolbox import tools
import cgxLightingTools.scripts.gui.mayaWindow as mWin


class LightDuplicator_GUI(QtWidgets.QDialog):
    def __init__(self, withInputs, withNodes, factories, parent=mWin.getMayaWindow()):
        super(LightDuplicator_GUI, self).__init__(parent)
        self.withInputs = withInputs
        self.withNodes = withNodes
        self.factories = factories
        self._setupUi()
        self._setConnections()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

    def _setupUi(self):
        self.setObjectName('LightDuplicator_DIALOG')
        self.setWindowTitle('Light Duplicator')
        dialogSize = QtCore.QSize(225, 111)
        self.resize(dialogSize.width(), dialogSize.height())
        self.setMinimumSize(dialogSize)
        self.setMaximumSize(dialogSize)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        vert_VERTLAY = QtWidgets.QVBoxLayout(self)
        vert_VERTLAY.setObjectName("vert_VERTLAY")
        htal_HTALLAY = QtWidgets.QHBoxLayout(self)
        htal_HTALLAY.setObjectName("htal_HTALLAY")
        btnSize = QtCore.QSize(71, 23)
        labelSize = QtCore.QSize(200, 13)
        ctrlSpinSize = QtCore.QSize(200, 21)
        chkBoxSize = QtCore.QSize(200, 21)
        self.howMany_LABEL = QtWidgets.QLabel(self)
        self.howMany_LABEL.setSizePolicy(sizePolicy)
        self.howMany_LABEL.setMinimumSize(labelSize)
        self.howMany_LABEL.setMaximumSize(labelSize)
        self.howMany_LABEL.setObjectName('howMany_LABEL')
        self.howMany_LABEL.setText('How many copies?')
        self.howMany_SPINBOX = QtWidgets.QSpinBox(self)
        self.howMany_SPINBOX.setSizePolicy(sizePolicy)
        self.howMany_SPINBOX.setMinimumSize(ctrlSpinSize)
        self.howMany_SPINBOX.setMaximumSize(ctrlSpinSize)
        self.howMany_SPINBOX.setObjectName('howMany_SPINBOX')
        self.howMany_SPINBOX.setValue(1)
        self.howMany_SPINBOX.setRange(1, 10000)
        self.howMany_SPINBOX.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.keepSetup_CHKBOX = QtWidgets.QCheckBox(self)
        self.keepSetup_CHKBOX.setSizePolicy(sizePolicy)
        self.keepSetup_CHKBOX.setMinimumSize(chkBoxSize)
        self.keepSetup_CHKBOX.setMaximumSize(chkBoxSize)
        self.keepSetup_CHKBOX.setObjectName('howMany_SPINBOX')
        self.keepSetup_CHKBOX.setText('Keep Light Group and AOV setup')
        self.keepSetup_CHKBOX.setChecked(True)
        self.duplicate_BTN = QtWidgets.QPushButton(self)
        self.duplicate_BTN.setSizePolicy(sizePolicy)
        self.duplicate_BTN.setMinimumSize(btnSize)
        self.duplicate_BTN.setMaximumSize(btnSize)
        self.duplicate_BTN.setText('Duplicate')
        self.duplicate_BTN.setObjectName("duplicate_BTN")
        self.cancel_BTN = QtWidgets.QPushButton(self)
        self.cancel_BTN.setSizePolicy(sizePolicy)
        self.cancel_BTN.setMinimumSize(btnSize)
        self.cancel_BTN.setMaximumSize(btnSize)
        self.cancel_BTN.setText('Cancel')
        self.cancel_BTN.setObjectName("cancel_BTN")

        vert_VERTLAY.addWidget(self.howMany_LABEL)
        vert_VERTLAY.addWidget(self.howMany_SPINBOX)
        vert_VERTLAY.addWidget(self.keepSetup_CHKBOX)
        htal_HTALLAY.addWidget(self.duplicate_BTN)
        htal_HTALLAY.addWidget(self.cancel_BTN)
        vert_VERTLAY.addLayout(htal_HTALLAY)
        self.setLayout(vert_VERTLAY)

    def _setConnections(self):
        self.duplicate_BTN.clicked.connect(self._duplicate)
        self.cancel_BTN.clicked.connect(self._cancel)

        self.installEventFilter(self)

    def eventFilter(self, widget, event):
        if event.type() == QtCore.QEvent.KeyPress:
            key = event.key()
            if key == QtCore.Qt.Key_Escape:
                self._cancel()
                return True
            elif key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Enter:
                self._duplicate()
                return True
        return QtWidgets.QWidget.eventFilter(self, widget, event)

    def _duplicate(self):
        allSel = mc.ls(sl=True)
        if len(allSel) < 1:
            msgBox = QtWidgets.QMessageBox(self)
            msgBox.setWindowTitle("Warning!")
            msgBox.setText("Please select at least one light to duplicate.")
            msgBox.exec_()
            tools.logger.info('Please select at least one light to duplicate.')
        else:
            for each in allSel:
                objTransform, objShape = tools.getTransformAndShape(each)
                for name, factory in self.factories.iteritems():
                    if mc.nodeType(objShape) in factory.lightNodeTypes:
                        for i in range(self.howMany_SPINBOX.value()):
                            factory.duplicateLight(objTransform, self.withInputs, self.withNodes,
                                                   keepAOVSetup=self.keepSetup_CHKBOX.isChecked())

            self.done(1)

    def _cancel(self):
        self.done(0)


# --------------------------------------------------------
#  Main
# --------------------------------------------------------
def main():
    pass


if __name__ == '__main__' or 'eclipsePython' in __name__:
    main()
