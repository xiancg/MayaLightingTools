'''
Created on July 10, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
'''
import os
import maya.cmds as mc
from PySide2 import QtCore, QtWidgets

from cgxLightingTools.scripts.toolbox import tools
from cgxLightingTools.scripts.gui import dataViewModels as dvm
import cgxLightingTools.scripts.gui.mayaWindow as mWin


class LightCreator_GUI(QtWidgets.QDialog):
    def __init__(self, lightNodeType, factories, parent=mWin.getMayaWindow()):
        super(LightCreator_GUI, self).__init__(parent)
        self._lightNodeType = lightNodeType
        self.factories = factories
        self._setupUi()
        self._setConnections()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

    def _setupUi(self):
        self.setObjectName('LightCreator_DIALOG')
        self.setWindowTitle('Light Creator')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        vert_VERTLAY = QtWidgets.QVBoxLayout(self)
        vert_VERTLAY.setObjectName("vert_VERTLAY")
        main_GRIDLAY = QtWidgets.QGridLayout(self)
        main_GRIDLAY.setObjectName("main_GRIDLAY")
        btnSize = QtCore.QSize(71, 23)
        self.create_BTN = QtWidgets.QPushButton(self)
        self.create_BTN.setSizePolicy(sizePolicy)
        self.create_BTN.setMinimumSize(btnSize)
        self.create_BTN.setMaximumSize(btnSize)
        self.create_BTN.setText('Create')
        self.create_BTN.setObjectName("create_BTN")
        self.cancel_BTN = QtWidgets.QPushButton(self)
        self.cancel_BTN.setSizePolicy(sizePolicy)
        self.cancel_BTN.setMinimumSize(btnSize)
        self.cancel_BTN.setMaximumSize(btnSize)
        self.cancel_BTN.setText('Cancel')
        self.cancel_BTN.setObjectName("cancel_BTN")

        # Create controls for each token type and adjust window size accordingly
        defaultFactory = self.factories['default']
        activeRule = defaultFactory.naming.getActiveRule()
        self.tokens = dict()
        i = 0
        if activeRule:
            for field in activeRule.fields:
                if defaultFactory.naming.hasToken(field):
                    token = defaultFactory.naming.getToken(field)
                    self.tokens[token.name] = {'obj': token, 'index': i}
                    i += 1
        self._setSize(112 * len(self.tokens), 91)
        for key, value in self.tokens.iteritems():
            tokenObj = self.tokens[key]['obj']
            labelSize = QtCore.QSize(60, 13)
            label = QtWidgets.QLabel(self)
            label.setSizePolicy(sizePolicy)
            label.setMinimumSize(labelSize)
            label.setMaximumSize(labelSize)
            label.setObjectName(tokenObj.name + '_LABEL')
            label.setText(tokenObj.name.capitalize())
            if isinstance(tokenObj, defaultFactory.naming.TokenNumber):
                # Create spinbox
                ctrlSpinSize = QtCore.QSize(61, 21)
                ctrlSpin = QtWidgets.QSpinBox(self)
                ctrlSpin.setSizePolicy(sizePolicy)
                ctrlSpin.setMinimumSize(ctrlSpinSize)
                ctrlSpin.setMaximumSize(ctrlSpinSize)
                ctrlSpin.setObjectName(tokenObj.name + '_SPINBOX')
                ctrlSpin.setValue(tokenObj.default)
                ctrlSpin.setRange(0, 1000000)
                self.tokens[key]['ctrl'] = ctrlSpin
                self.tokens[key]['label'] = label
            else:
                if tokenObj.required:
                    # Create line edit
                    ctrlLineSize = QtCore.QSize(113, 20)
                    ctrlLine = QtWidgets.QLineEdit(self)
                    ctrlLine.setSizePolicy(sizePolicy)
                    ctrlLine.setMinimumSize(ctrlLineSize)
                    ctrlLine.setMaximumSize(ctrlLineSize)
                    ctrlLine.setObjectName(tokenObj.name + '_LINEEDIT')
                    ctrlLine.setFocus(QtCore.Qt.PopupFocusReason)
                    self.tokens[key]['ctrl'] = ctrlLine
                    labelSize = QtCore.QSize(110, 13)
                    label.setMinimumSize(labelSize)
                    label.setMaximumSize(labelSize)
                    self.tokens[key]['label'] = label
                else:
                    # Create combobox with options
                    ctrlComboSize = QtCore.QSize(111, 22)
                    ctrlCombo = QtWidgets.QComboBox(self)
                    ctrlCombo.setSizePolicy(sizePolicy)
                    ctrlCombo.setMinimumSize(ctrlComboSize)
                    ctrlCombo.setMaximumSize(ctrlComboSize)
                    ctrlCombo.setObjectName(tokenObj.name + '_COMBOBOX')
                    model = dvm.ObjectsListModel(tokenObj.options.keys(), ctrlCombo)
                    ctrlCombo.setModel(model)
                    if tokenObj.default:
                        dataList = ctrlCombo.model().dataList
                        for x in range(len(dataList)):
                            if dataList[x] == tokenObj.default:
                                ctrlCombo.setCurrentIndex(x)
                                break
                    self.tokens[key]['ctrl'] = ctrlCombo
                    labelSize = QtCore.QSize(110, 13)
                    label.setMinimumSize(labelSize)
                    label.setMaximumSize(labelSize)
                    self.tokens[key]['label'] = label
        for key, value in self.tokens.iteritems():
            for item in self.tokens[key].keys():
                tokenCtrl = self.tokens[key]['ctrl']
                tokenLabel = self.tokens[key]['label']
                tokenIndex = self.tokens[key]['index']
                if item == 'label':
                    main_GRIDLAY.addWidget(tokenLabel, 0, tokenIndex * 2,
                                           1, 1, QtCore.Qt.AlignLeft)
                elif item == 'ctrl':
                    main_GRIDLAY.addWidget(tokenCtrl, 1, tokenIndex * 2,
                                           1, 1, QtCore.Qt.AlignCenter)
        for column in range(0, i, 2):
            main_GRIDLAY.setColumnMinimumWidth(column, 1)
            main_GRIDLAY.setColumnStretch(column, 1)
        vert_VERTLAY.addLayout(main_GRIDLAY)
        btns_GRIDLAY = QtWidgets.QGridLayout(self)
        btns_GRIDLAY.setObjectName('btns_GRIDLAY')
        btns_GRIDLAY.addWidget(self.create_BTN, 0, 1, 1, 1, QtCore.Qt.AlignCenter)
        btns_GRIDLAY.addWidget(self.cancel_BTN, 0, 2, 1, 1, QtCore.Qt.AlignCenter)
        spacing = 112 * (i / 2)
        btns_GRIDLAY.setColumnMinimumWidth(0, spacing)
        btns_GRIDLAY.setColumnStretch(0, spacing)
        btns_GRIDLAY.setColumnMinimumWidth(3, spacing)
        btns_GRIDLAY.setColumnStretch(3, spacing)
        vert_VERTLAY.addLayout(btns_GRIDLAY)
        self.setLayout(vert_VERTLAY)

        QtCore.QMetaObject.connectSlotsByName(self)

    def _setSize(self, x, y):
        self.resize(x, y)
        self.setMinimumSize(QtCore.QSize(x, y))
        self.setMaximumSize(QtCore.QSize(x, y))

    def _setConnections(self):
        self.create_BTN.clicked.connect(self._create)
        self.cancel_BTN.clicked.connect(self._cancel)

        self.installEventFilter(self)

    def eventFilter(self, widget, event):
        if event.type() == QtCore.QEvent.KeyPress:
            key = event.key()
            if key == QtCore.Qt.Key_Escape:
                self._cancel()
                return True
            elif key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Enter:
                self._create()
                return True
        return QtWidgets.QWidget.eventFilter(self, widget, event)

    def _create(self):
        result = False
        for name, factory in self.factories.iteritems():
            if self._lightNodeType in factory.lightNodeTypes:
                kwargs = dict()
                for key, value in self.tokens.iteritems():
                    tokenObj = self.tokens[key]['obj']
                    tokenCtrl = self.tokens[key]['ctrl']
                    if tokenObj.isNumber:
                        kwargs[tokenObj.name] = tokenCtrl.value()
                    else:
                        if tokenObj.required:
                            kwargs[tokenObj.name] = tokenCtrl.text().replace(" ", "")
                        else:
                            kwargs[tokenObj.name] = tokenCtrl.currentText()
                lightName = factory.buildName(**kwargs)
                result = factory.createLight(self._lightNodeType, lightName)
                break
        if result:
            self.done(1)
        else:
            self.done(0)

    def _cancel(self):
        self.done(0)


class LightRenamer_GUI(LightCreator_GUI):
    def __init__(self, lightNode, factories, parent=mWin.getMayaWindow()):
        super(LightRenamer_GUI, self).__init__(mc.nodeType(lightNode), factories, parent=parent)
        self._lightNode = lightNode
        self._initUi()
        self._setConnections()

    def _setConnections(self):
        try:
            self.create_BTN.clicked.disconnect()
        except:
            pass
        self.create_BTN.clicked.connect(self._rename)

        self.installEventFilter(self)

    def eventFilter(self, widget, event):
        if event.type() == QtCore.QEvent.KeyPress:
            key = event.key()
            if key == QtCore.Qt.Key_Escape:
                self._cancel()
                return True
            elif key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Enter:
                self._rename()
                return True
        return QtWidgets.QWidget.eventFilter(self, widget, event)

    def _initUi(self):
        self.create_BTN.setText('Rename')
        tokensParse = self.factories['default'].parseOldNameByTokens(self._lightNode)
        if tokensParse is not None:
            for key, value in self.tokens.iteritems():
                tokenObj = self.tokens[key]['obj']
                tokenCtrl = self.tokens[key]['ctrl']
                if tokenObj.name in tokensParse.keys():
                    if tokenObj.isNumber:
                        tokenCtrl.setValue(tokensParse[tokenObj.name])
                    else:
                        if tokenObj.required:
                            tokenCtrl.setText(tokensParse[tokenObj.name])
                        else:
                            dataList = tokenCtrl.model().dataList
                            for x in range(len(dataList)):
                                if dataList[x] == tokensParse[tokenObj.name]:
                                    tokenCtrl.setCurrentIndex(x)
                                    break
        else:
            oldNameStr, oldNameNum = self._parseOldNameParts(self._lightNode)
            kwargs = dict()
            for key, value in self.tokens.iteritems():
                tokenObj = self.tokens[key]['obj']
                tokenCtrl = self.tokens[key]['ctrl']
                if tokenObj.isNumber:
                    tokenCtrl.setValue(oldNameNum)
                elif tokenObj.required:
                    tokenCtrl.setText(oldNameStr)

    def _parseOldNameParts(self, lightNode):
        '''TODO: This could be moved to the factories so the tools enforce good naming when duplicating'''
        objTransform, objShape = tools.getTransformAndShape(lightNode)
        if mc.nodeType(objShape) in tools.getLightNodesList():
            if '_' in objTransform:
                nameSplit = objTransform.split('_')
                number = 1
                longestPart = str()
                for part in nameSplit:
                    if part.isdigit():
                        number = int(part)
                        continue
                    else:
                        if len(part) > len(longestPart):
                            longestPart = part
                else:
                    return longestPart, number
            else:
                return objTransform, 1

    def _rename(self):
        result = False
        for name, factory in self.factories.iteritems():
            if self._lightNodeType in factory.lightNodeTypes:
                kwargs = dict()
                for key, value in self.tokens.iteritems():
                    tokenObj = self.tokens[key]['obj']
                    tokenCtrl = self.tokens[key]['ctrl']
                    if tokenObj.isNumber:
                        kwargs[tokenObj.name] = tokenCtrl.value()
                    else:
                        if tokenObj.required:
                            kwargs[tokenObj.name] = tokenCtrl.text().replace(" ", "")
                        else:
                            kwargs[tokenObj.name] = tokenCtrl.currentText()
                lightName = factory.buildName(**kwargs)
                result = factory.renameLight(self._lightNode, lightName)
                break
        if result:
            self.done(1)
        else:
            self.done(0)

# --------------------------------------------------------
#  Main
# --------------------------------------------------------


def main():
    pass


if __name__ == '__main__' or 'eclipsePython' in __name__:
    main()
