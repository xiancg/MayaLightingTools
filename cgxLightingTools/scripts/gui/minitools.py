'''
Created on July 10, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
TODO: Set width and height sizing properties on show depending on preferences
'''
from __future__ import absolute_import
import os

from PySide2 import QtWidgets, QtCore
import maya.cmds as mc
import cgxLightingTools.scripts.gui.mayaWindow as mWin
from cgxLightingTools.scripts.toolbox import tools
import cgxLightingTools.scripts.toolbox.lightsFactory as lightsFactory


class MiniToolsDialog(QtWidgets.QDialog):
    def __init__(self, parent=mWin.getMayaWindow()):
        super(MiniToolsDialog, self).__init__(parent=parent)
        self._prefOrientation = 'horizontal'
        self.initFactories()
        self.setupUi()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
    
    def initFactories(self):
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
    
    def setupUi(self):
        self.setObjectName('miniTools_DIALOG')
        self.setWindowTitle('Mini Tools')
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        if self._prefOrientation == 'horizontal':
            self.resize(392, 90)
            self.setMinimumSize(QtCore.QSize(392,90))
            self.setMaximumSize(QtCore.QSize(10000, 90))
            mainLayout = self.loadHorizontal()
        else:
            self.resize(90, 347)
            self.setMinimumSize(QtCore.QSize(90,347))
            self.setMaximumSize(QtCore.QSize(90, 10000))
            mainLayout = self.loadVertical()
        tools_GRIDLAY = QtWidgets.QGridLayout()
        tools_GRIDLAY.setObjectName("tools_GRIDLAY")
        lgtVis_GRIDLAY = QtWidgets.QGridLayout()
        lgtVis_GRIDLAY.setObjectName("lgtVis_GRIDLAY")
        defaultLights_GRIDLAY = QtWidgets.QGridLayout()
        defaultLights_GRIDLAY.setObjectName("defaultLights_GRIDLAY")
        rendererLights_GRIDLAY = QtWidgets.QGridLayout()
        rendererLights_GRIDLAY.setObjectName("rendererLights_GRIDLAY")
        self.createButtons()
        if mainLayout.objectName() == 'horizontalLayout':
            tools_GRIDLAY.addWidget(self.simpleIsolate_BTN, 0, 0, 1, 1)
            tools_GRIDLAY.addWidget(self.lookThru_BTN, 0, 1, 1, 1)
            tools_GRIDLAY.addWidget(self.aimLight_BTN, 0, 2, 1, 1)
            tools_GRIDLAY.addWidget(self.specularConstrain_BTN, 0, 3, 2, 1)
            tools_GRIDLAY.addWidget(self.cleanUpCams_BTN, 1, 0, 1, 1)
            tools_GRIDLAY.addWidget(self.lightsManager_BTN, 1, 1, 1, 1)
            tools_GRIDLAY.addWidget(self.alignLight_BTN, 1, 2, 1, 1)
            mainLayout.addLayout(tools_GRIDLAY)
            spacerWidth = 8
            spacerHeight = 20
            spacerItem1 = QtWidgets.QSpacerItem(spacerWidth, spacerHeight, 
                                QtWidgets.QSizePolicy.Expanding,
                                QtWidgets.QSizePolicy.Minimum)
            mainLayout.addItem(spacerItem1)
            lgtVis_GRIDLAY.addWidget(self.visSnapshot01_BTN, 0, 0, 1, 1)
            lgtVis_GRIDLAY.addWidget(self.visSnapshot02_BTN, 0, 1, 1, 1)
            lgtVis_GRIDLAY.addWidget(self.visSnapshot03_BTN, 2, 1, 1, 1)
            lgtVis_GRIDLAY.addWidget(self.visSnapshot04_BTN, 1, 0, 1, 1)
            lgtVis_GRIDLAY.addWidget(self.visSnapshot05_BTN, 1, 1, 1, 1)
            lgtVis_GRIDLAY.addWidget(self.visSnapshot06_BTN, 2, 0, 1, 1)
            mainLayout.addLayout(lgtVis_GRIDLAY)
            spacerItem2 = QtWidgets.QSpacerItem(spacerWidth, spacerHeight, 
                                        QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Minimum)
            mainLayout.addItem(spacerItem2)
            lights_VERTLAY = QtWidgets.QVBoxLayout()
            lights_VERTLAY.setObjectName("lights_VERTLAY")
            defaultLights_GRIDLAY.addWidget(self.spotLight_BTN, 0, 0, 1, 1)
            defaultLights_GRIDLAY.addWidget(self.pointLight_BTN, 0, 1, 1, 1)
            defaultLights_GRIDLAY.addWidget(self.areaLight_BTN, 0, 2, 1, 1)
            defaultLights_GRIDLAY.addWidget(self.directionalLight_BTN, 0, 3, 1, 1)
            defaultLights_GRIDLAY.addWidget(self.ambientLight_BTN, 0, 4, 1, 1)
            defaultLights_GRIDLAY.addWidget(self.volumeLight_BTN, 0, 5, 1, 1)
            lights_VERTLAY.addLayout(defaultLights_GRIDLAY)
            rendererLights_GRIDLAY.addWidget(self.aiAreaLight_BTN, 0, 0, 1, 1)
            rendererLights_GRIDLAY.addWidget(self.aiSkyDomeLight_BTN, 0, 1, 1, 1)
            rendererLights_GRIDLAY.addWidget(self.aiMeshLight_BTN, 0, 2, 1, 1)
            rendererLights_GRIDLAY.addWidget(self.aiPhotometricLight_BTN, 0, 3, 1, 1)
            rendererLights_GRIDLAY.addWidget(self.aiLightPortal_BTN, 0, 4, 1, 1)
            rendererLights_GRIDLAY.addWidget(self.aiPhysicalSky_BTN, 0, 5, 1, 1)
            lights_VERTLAY.addLayout(rendererLights_GRIDLAY)
            mainLayout.addLayout(lights_VERTLAY)
            spacerItem3 = QtWidgets.QSpacerItem(spacerWidth, spacerHeight, 
                                        QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Minimum)
            mainLayout.addItem(spacerItem3)
        else:
            tools_GRIDLAY.addWidget(self.simpleIsolate_BTN, 0, 0, 1, 1)
            tools_GRIDLAY.addWidget(self.lookThru_BTN, 0, 1, 1, 1)
            tools_GRIDLAY.addWidget(self.aimLight_BTN, 1, 0, 1, 1)
            tools_GRIDLAY.addWidget(self.specularConstrain_BTN, 2, 0, 1, 1)
            tools_GRIDLAY.addWidget(self.cleanUpCams_BTN, 2, 1, 1, 1)
            tools_GRIDLAY.addWidget(self.lightsManager_BTN, 3, 0, 1, 2)
            tools_GRIDLAY.addWidget(self.alignLight_BTN, 1, 1, 1, 1)
            mainLayout.addLayout(tools_GRIDLAY)
            spacerWidth = 20
            spacerHeight = 8
            spacerItem1 = QtWidgets.QSpacerItem(spacerWidth, spacerHeight,
                                QtWidgets.QSizePolicy.Minimum,
                                QtWidgets.QSizePolicy.Expanding)
            mainLayout.addItem(spacerItem1)
            lgtVis_GRIDLAY.addWidget(self.visSnapshot01_BTN, 0, 0, 1, 1)
            lgtVis_GRIDLAY.addWidget(self.visSnapshot02_BTN, 0, 1, 1, 1)
            lgtVis_GRIDLAY.addWidget(self.visSnapshot03_BTN, 0, 2, 1, 1)
            lgtVis_GRIDLAY.addWidget(self.visSnapshot04_BTN, 1, 0, 1, 1)
            lgtVis_GRIDLAY.addWidget(self.visSnapshot05_BTN, 1, 1, 1, 1)
            lgtVis_GRIDLAY.addWidget(self.visSnapshot06_BTN, 1, 2, 1, 1)
            mainLayout.addLayout(lgtVis_GRIDLAY)
            spacerItem2 = QtWidgets.QSpacerItem(spacerWidth, spacerHeight,
                                        QtWidgets.QSizePolicy.Minimum,
                                        QtWidgets.QSizePolicy.Expanding)
            mainLayout.addItem(spacerItem2)
            defaultLights_GRIDLAY.addWidget(self.spotLight_BTN, 0, 0, 1, 1)
            defaultLights_GRIDLAY.addWidget(self.pointLight_BTN, 0, 1, 1, 1)
            defaultLights_GRIDLAY.addWidget(self.areaLight_BTN, 0, 2, 1, 1)
            defaultLights_GRIDLAY.addWidget(self.directionalLight_BTN, 1, 0, 1, 1)
            defaultLights_GRIDLAY.addWidget(self.ambientLight_BTN, 1, 1, 1, 1)
            defaultLights_GRIDLAY.addWidget(self.volumeLight_BTN, 1, 2, 1, 1)
            rendererLights_GRIDLAY.addWidget(self.aiAreaLight_BTN, 0, 0, 1, 1)
            rendererLights_GRIDLAY.addWidget(self.aiSkyDomeLight_BTN, 0, 1, 1, 1)
            rendererLights_GRIDLAY.addWidget(self.aiMeshLight_BTN, 0, 2, 1, 1)
            rendererLights_GRIDLAY.addWidget(self.aiPhotometricLight_BTN, 1, 0, 1, 1)
            rendererLights_GRIDLAY.addWidget(self.aiLightPortal_BTN, 1, 1, 1, 1)
            rendererLights_GRIDLAY.addWidget(self.aiPhysicalSky_BTN, 1, 2, 1, 1)
            mainLayout.addLayout(defaultLights_GRIDLAY)
            mainLayout.addLayout(rendererLights_GRIDLAY)
            spacerItem3 = QtWidgets.QSpacerItem(spacerWidth, spacerHeight,
                                        QtWidgets.QSizePolicy.Minimum,
                                        QtWidgets.QSizePolicy.Expanding)
            mainLayout.addItem(spacerItem3)

        tools_GRIDLAY.setAlignment(self.lightsManager_BTN, QtCore.Qt.AlignCenter)
        mainLayout.addWidget(self.config_BTN)
        mainLayout.setAlignment(self.config_BTN, QtCore.Qt.AlignCenter)
        self.setLayout(mainLayout)
        
        QtCore.QMetaObject.connectSlotsByName(self)
    
    def createButtons(self):
        '''TODO: Should the light creation buttons be responsibility of factories?'''
        toolsBtnSize = QtCore.QSize(32, 32)
        visBtnSize = QtCore.QSize(14, 14)
        lightsBtnSize = QtCore.QSize(16, 16)
        configBtnSize = QtCore.QSize(20, 20)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                            QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        # TOOLS
        self.simpleIsolate_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.lookThru_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.aimLight_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.specularConstrain_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.cleanUpCams_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.lightsManager_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.alignLight_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.simpleIsolate_BTN.setSizePolicy(sizePolicy)
        self.simpleIsolate_BTN.setMinimumSize(toolsBtnSize)
        self.simpleIsolate_BTN.setMaximumSize(toolsBtnSize)
        self.simpleIsolate_BTN.setText("")
        self.simpleIsolate_BTN.setObjectName("simpleIsolate_BTN")
        self.lookThru_BTN.setSizePolicy(sizePolicy)
        self.lookThru_BTN.setMinimumSize(toolsBtnSize)
        self.lookThru_BTN.setMaximumSize(toolsBtnSize)
        self.lookThru_BTN.setText("")
        self.lookThru_BTN.setObjectName("lookThru_BTN")
        self.aimLight_BTN.setSizePolicy(sizePolicy)
        self.aimLight_BTN.setMinimumSize(toolsBtnSize)
        self.aimLight_BTN.setMaximumSize(toolsBtnSize)
        self.aimLight_BTN.setText("")
        self.aimLight_BTN.setObjectName("aimLight_BTN")
        self.specularConstrain_BTN.setSizePolicy(sizePolicy)
        self.specularConstrain_BTN.setMinimumSize(toolsBtnSize)
        self.specularConstrain_BTN.setMaximumSize(toolsBtnSize)
        self.specularConstrain_BTN.setText("")
        self.specularConstrain_BTN.setObjectName("specularConstrain_BTN")
        self.cleanUpCams_BTN.setSizePolicy(sizePolicy)
        self.cleanUpCams_BTN.setMinimumSize(toolsBtnSize)
        self.cleanUpCams_BTN.setMaximumSize(toolsBtnSize)
        self.cleanUpCams_BTN.setText("")
        self.cleanUpCams_BTN.setObjectName("cleanUpCams_BTN")
        self.alignLight_BTN.setSizePolicy(sizePolicy)
        self.alignLight_BTN.setMinimumSize(toolsBtnSize)
        self.alignLight_BTN.setMaximumSize(toolsBtnSize)
        self.alignLight_BTN.setText("")
        self.alignLight_BTN.setObjectName("alignLight_BTN")
        self.lightsManager_BTN.setSizePolicy(sizePolicy)
        self.lightsManager_BTN.setMinimumSize(toolsBtnSize)
        self.lightsManager_BTN.setMaximumSize(toolsBtnSize)
        self.lightsManager_BTN.setText("")
        self.lightsManager_BTN.setObjectName("lightsManager_BTN")

        # LIGHT VIS SNAPSHOTS
        self.visSnapshot01_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.visSnapshot02_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.visSnapshot03_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.visSnapshot04_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.visSnapshot05_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.visSnapshot06_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.visSnapshot02_BTN.setObjectName("visSnapshot01_BTN")
        self.visSnapshot01_BTN.setSizePolicy(sizePolicy)
        self.visSnapshot01_BTN.setMinimumSize(visBtnSize)
        self.visSnapshot01_BTN.setMaximumSize(visBtnSize)
        self.visSnapshot01_BTN.setText("")
        self.visSnapshot02_BTN.setObjectName("visSnapshot02_BTN")
        self.visSnapshot02_BTN.setSizePolicy(sizePolicy)
        self.visSnapshot02_BTN.setMinimumSize(visBtnSize)
        self.visSnapshot02_BTN.setMaximumSize(visBtnSize)
        self.visSnapshot02_BTN.setText("")
        self.visSnapshot03_BTN.setObjectName("visSnapshot03_BTN")
        self.visSnapshot03_BTN.setSizePolicy(sizePolicy)
        self.visSnapshot03_BTN.setMinimumSize(visBtnSize)
        self.visSnapshot03_BTN.setMaximumSize(visBtnSize)
        self.visSnapshot03_BTN.setText("")
        self.visSnapshot04_BTN.setObjectName("visSnapshot04_BTN")
        self.visSnapshot04_BTN.setSizePolicy(sizePolicy)
        self.visSnapshot04_BTN.setMinimumSize(visBtnSize)
        self.visSnapshot04_BTN.setMaximumSize(visBtnSize)
        self.visSnapshot04_BTN.setText("")
        self.visSnapshot05_BTN.setObjectName("visSnapshot05_BTN")
        self.visSnapshot05_BTN.setSizePolicy(sizePolicy)
        self.visSnapshot05_BTN.setMinimumSize(visBtnSize)
        self.visSnapshot05_BTN.setMaximumSize(visBtnSize)
        self.visSnapshot05_BTN.setText("")
        self.visSnapshot06_BTN.setObjectName("visSnapshot06_BTN")
        self.visSnapshot06_BTN.setSizePolicy(sizePolicy)
        self.visSnapshot06_BTN.setMinimumSize(visBtnSize)
        self.visSnapshot06_BTN.setMaximumSize(visBtnSize)
        self.visSnapshot06_BTN.setText("")

        # DEFAULT LIGHTS
        self.spotLight_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.pointLight_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.areaLight_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.directionalLight_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.ambientLight_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.volumeLight_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.spotLight_BTN.setSizePolicy(sizePolicy)
        self.spotLight_BTN.setMinimumSize(lightsBtnSize)
        self.spotLight_BTN.setMaximumSize(lightsBtnSize)
        self.spotLight_BTN.setText("")
        self.spotLight_BTN.setObjectName("spotLight_BTN")
        self.pointLight_BTN.setSizePolicy(sizePolicy)
        self.pointLight_BTN.setMinimumSize(lightsBtnSize)
        self.pointLight_BTN.setMaximumSize(lightsBtnSize)
        self.pointLight_BTN.setText("")
        self.pointLight_BTN.setObjectName("pointLight_BTN")
        self.areaLight_BTN.setSizePolicy(sizePolicy)
        self.areaLight_BTN.setMinimumSize(lightsBtnSize)
        self.areaLight_BTN.setMaximumSize(lightsBtnSize)
        self.areaLight_BTN.setText("")
        self.areaLight_BTN.setObjectName("areaLight_BTN")
        self.directionalLight_BTN.setSizePolicy(sizePolicy)
        self.directionalLight_BTN.setMinimumSize(lightsBtnSize)
        self.directionalLight_BTN.setMaximumSize(lightsBtnSize)
        self.directionalLight_BTN.setText("")
        self.directionalLight_BTN.setObjectName("directionalLight_BTN")
        self.ambientLight_BTN.setSizePolicy(sizePolicy)
        self.ambientLight_BTN.setMinimumSize(lightsBtnSize)
        self.ambientLight_BTN.setMaximumSize(lightsBtnSize)
        self.ambientLight_BTN.setText("")
        self.ambientLight_BTN.setObjectName("ambientLight_BTN")
        self.volumeLight_BTN.setSizePolicy(sizePolicy)
        self.volumeLight_BTN.setMinimumSize(QtCore.QSize(16, 16))
        self.volumeLight_BTN.setMaximumSize(QtCore.QSize(16, 16))
        self.volumeLight_BTN.setText("")
        self.volumeLight_BTN.setObjectName("volumeLight_BTN")

        # MTOA LIGHTS
        self.aiAreaLight_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.aiSkyDomeLight_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.aiMeshLight_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.aiPhotometricLight_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.aiLightPortal_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.aiPhysicalSky_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.aiAreaLight_BTN.setSizePolicy(sizePolicy)
        self.aiAreaLight_BTN.setMinimumSize(lightsBtnSize)
        self.aiAreaLight_BTN.setMaximumSize(lightsBtnSize)
        self.aiAreaLight_BTN.setText("")
        self.aiAreaLight_BTN.setObjectName("aiAreaLight_BTN")
        self.aiSkyDomeLight_BTN.setSizePolicy(sizePolicy)
        self.aiSkyDomeLight_BTN.setMinimumSize(lightsBtnSize)
        self.aiSkyDomeLight_BTN.setMaximumSize(lightsBtnSize)
        self.aiSkyDomeLight_BTN.setText("")
        self.aiSkyDomeLight_BTN.setObjectName("aiSkyDomeLight_BTN")
        self.aiMeshLight_BTN.setSizePolicy(sizePolicy)
        self.aiMeshLight_BTN.setMinimumSize(lightsBtnSize)
        self.aiMeshLight_BTN.setMaximumSize(lightsBtnSize)
        self.aiMeshLight_BTN.setText("")
        self.aiMeshLight_BTN.setObjectName("aiMeshLight_BTN")
        self.aiPhotometricLight_BTN.setSizePolicy(sizePolicy)
        self.aiPhotometricLight_BTN.setMinimumSize(lightsBtnSize)
        self.aiPhotometricLight_BTN.setMaximumSize(lightsBtnSize)
        self.aiPhotometricLight_BTN.setText("")
        self.aiPhotometricLight_BTN.setObjectName("aiPhotometricLight_BTN")
        self.aiLightPortal_BTN.setSizePolicy(sizePolicy)
        self.aiLightPortal_BTN.setMinimumSize(lightsBtnSize)
        self.aiLightPortal_BTN.setMaximumSize(lightsBtnSize)
        self.aiLightPortal_BTN.setText("")
        self.aiLightPortal_BTN.setObjectName("aiLightPortal_BTN")
        self.aiPhysicalSky_BTN.setSizePolicy(sizePolicy)
        self.aiPhysicalSky_BTN.setMinimumSize(lightsBtnSize)
        self.aiPhysicalSky_BTN.setMaximumSize(lightsBtnSize)
        self.aiPhysicalSky_BTN.setText("")
        self.aiPhysicalSky_BTN.setObjectName("aiPhysicalSky_BTN")

        #CONFIG
        self.config_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.config_BTN.setMaximumSize(configBtnSize)
        self.config_BTN.setText("")
        self.config_BTN.setObjectName("config_BTN")
        
    def loadHorizontal(self):
        horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        horizontalLayout.setObjectName("horizontalLayout")

        return horizontalLayout
        
    
    def loadVertical(self):
        verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        verticalLayout.setObjectName("verticalLayout")

        return verticalLayout


# --------------------------------------------------------
#  Main
# --------------------------------------------------------
def main():
    for qt in QtWidgets.QApplication.topLevelWidgets():
        try:
            qtname = qt.objectName()
            if qtname in ['miniTools_DIALOG']:
                qt.close()
                break
        except:
            pass

    test = MiniToolsDialog()
    test.show()


if __name__ == '__main__' or 'eclipsePython' in __name__:
    main()