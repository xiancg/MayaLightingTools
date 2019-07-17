'''
Created on July 10, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
'''
from __future__ import absolute_import
from PySide2 import QtCore, QtWidgets
from cgxLightingTools.scripts.toolbox import tools
import cgxLightingTools.scripts.toolbox.lightsFactory as lightsFactory
from cgxLightingTools.scripts.gui import dataViewModels as dvm
import cgxLightingTools.scripts.gui.mayaWindow as mWin

class LightCreator_GUI(QtWidgets.QDialog):
    def __init__(self, parent= mWin.getMayaWindow()):
        super(LightCreator_GUI, self).__init__(parent)
        self._initFactories()
        self._setupUi()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
    
    def _initFactories(self):
        '''TODO: Traverse render engines and create factories accordingly.
        Also list factories, compare and use what is available'''
        renderers = tools.getRenderEngines()
        self.defaultFactory = lightsFactory.default_factory.LightsFactory()
        if renderers is not None:
            if 'mtoa' in renderers.keys():
                self.mtoaFactory = lightsFactory.mtoa_factory.ArnoldFactory()
        '''
        if renderers is not None:
            rendererNames = renderers.keys()
            rendererNames.append('default')
            factoryPath = os.path.dirname(lightsFactory.__file__)
            factories = [name for _, name, _ in pkgutil.iter_modules([factoryPath])]
            for factory in factories:
                if factory in rendererNames:
                    for name, obj in inspect.getmembers(foo):
                        if inspect.isclass(obj):
                            self.factories.append(obj.__init__())
        '''
    
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
        activeRule = self.defaultFactory.naming.getActiveRule()
        tokens = dict()
        i = 0
        if activeRule:
            for field in activeRule.fields:
                if self.defaultFactory.naming.hasToken(field):
                    token = self.defaultFactory.naming.getToken(field)
                    tokens[token.name] = {'obj':token, 'index':i}
                    i += 2
        self._setSize(112*len(tokens),91)
        for key, value in tokens.iteritems():
            tokenObj = tokens[key]['obj']
            labelSize = QtCore.QSize(60, 13)
            label = QtWidgets.QLabel(self)
            label.setSizePolicy(sizePolicy)
            label.setMinimumSize(labelSize)
            label.setMaximumSize(labelSize)
            label.setObjectName(tokenObj.name + '_LABEL')
            label.setText(tokenObj.name.capitalize())
            if isinstance(tokenObj, self.defaultFactory.naming.TokenNumber):
                #Create spinbox
                ctrlSpinSize = QtCore.QSize(61, 21)
                ctrlSpin = QtWidgets.QSpinBox(self)
                ctrlSpin.setSizePolicy(sizePolicy)
                ctrlSpin.setMinimumSize(ctrlSpinSize)
                ctrlSpin.setMaximumSize(ctrlSpinSize)
                ctrlSpin.setObjectName(tokenObj.name + '_SPINBOX')
                tokens[key]['ctrl'] = ctrlSpin
                tokens[key]['label'] = label
            else:
                if tokenObj.required:
                    #Create line edit
                    ctrlLineSize = QtCore.QSize(113, 20)
                    ctrlLine = QtWidgets.QLineEdit(self)
                    ctrlLine.setSizePolicy(sizePolicy)
                    ctrlLine.setMinimumSize(ctrlLineSize)
                    ctrlLine.setMaximumSize(ctrlLineSize)
                    ctrlLine.setObjectName(tokenObj.name + '_LINEEDIT')
                    tokens[key]['ctrl'] = ctrlLine
                    labelSize = QtCore.QSize(110, 13)
                    label.setMinimumSize(labelSize)
                    label.setMaximumSize(labelSize)
                    tokens[key]['label'] = label
                else:
                    #Create combobox with options
                    ctrlComboSize = QtCore.QSize(111, 22)
                    ctrlCombo = QtWidgets.QComboBox(self)
                    ctrlCombo.setSizePolicy(sizePolicy)
                    ctrlCombo.setMinimumSize(ctrlComboSize)
                    ctrlCombo.setMaximumSize(ctrlComboSize)
                    ctrlCombo.setObjectName(tokenObj.name + '_COMBOBOX')
                    model = dvm.ObjectsListModel(tokenObj.options.values(), ctrlCombo)
                    ctrlCombo.setModel(model)
                    if tokenObj.default:
                        dataList = ctrlCombo.model().dataList
                        for x in range(len(dataList)):
                            if dataList[x] == tokenObj.default:
                                ctrlCombo.setCurrentIndex(x)
                    tokens[key]['ctrl'] = ctrlCombo
                    labelSize = QtCore.QSize(110, 13)
                    label.setMinimumSize(labelSize)
                    label.setMaximumSize(labelSize)
                    tokens[key]['label'] = label
        for key, value in tokens.iteritems():
            for item in tokens[key].keys():
                tokenObj = tokens[key]['obj']
                tokenCtrl = tokens[key]['ctrl']
                tokenLabel = tokens[key]['label']
                tokenIndex = tokens[key]['index']
                if item == 'label':
                    main_GRIDLAY.addWidget(tokenLabel, 0, tokenIndex, 
                                            1, 1, QtCore.Qt.AlignLeft)
                elif item == 'ctrl':
                    main_GRIDLAY.addWidget(tokenCtrl, 1, tokenIndex,
                                            1, 1, QtCore.Qt.AlignCenter)
        for column in range(0, i, 2):
            main_GRIDLAY.setColumnMinimumWidth(column,1)
            main_GRIDLAY.setColumnStretch(column,1)
        vert_VERTLAY.addLayout(main_GRIDLAY)
        btns_GRIDLAY = QtWidgets.QGridLayout(self)
        btns_GRIDLAY.setObjectName('btns_GRIDLAY')
        btns_GRIDLAY.addWidget(self.create_BTN, 0, 1, 1, 1, QtCore.Qt.AlignCenter)
        btns_GRIDLAY.addWidget(self.cancel_BTN, 0, 2, 1, 1, QtCore.Qt.AlignCenter)
        spacing = 112*(i/2)
        btns_GRIDLAY.setColumnMinimumWidth(0,spacing)
        btns_GRIDLAY.setColumnStretch(0,spacing)
        btns_GRIDLAY.setColumnMinimumWidth(3,spacing)
        btns_GRIDLAY.setColumnStretch(3,spacing)
        vert_VERTLAY.addLayout(btns_GRIDLAY)
        self.setLayout(vert_VERTLAY)
        QtCore.QMetaObject.connectSlotsByName(self)

    
    def _setSize(self, x, y):
        self.resize(x, y)
        self.setMinimumSize(QtCore.QSize(x, y))
        self.setMaximumSize(QtCore.QSize(x, y))


# --------------------------------------------------------
#  Main
# --------------------------------------------------------
def main():
    temp = LightCreator_GUI()
    temp.show()


if __name__ == '__main__' or 'eclipsePython' in __name__:
    main()