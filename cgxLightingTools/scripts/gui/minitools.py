'''
Created on July 10, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
TODO: Set width and height sizing properties on show depending on preferences
'''
from __future__ import absolute_import
import os
import json
from functools import partial

from PySide2 import QtWidgets, QtCore
import maya.cmds as mc
import cgxLightingTools.scripts.gui.mayaWindow as mWin
from cgxLightingTools.scripts.toolbox import tools
import cgxLightingTools.scripts.toolbox.lightsFactory as lightsFactory


class MiniToolsDialog(QtWidgets.QDialog):
    def __init__(self, parent=mWin.getMayaWindow()):
        super(MiniToolsDialog, self).__init__(parent=parent)
        self._prefOrientation = self._loadPrefOrientation()
        self._initFactories()
        self._setupUi()
        self._setConnections()
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
        self.setObjectName('miniTools_DIALOG')
        self.setWindowTitle('Mini Tools')
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        if self._prefOrientation == 'horizontal':
            self.resize(412, 90)
            self.setMinimumSize(QtCore.QSize(412,90))
            self.setMaximumSize(QtCore.QSize(10000, 90))
            mainLayout = self._loadHorizontal()
        else:
            self.resize(90, 360)
            self.setMinimumSize(QtCore.QSize(90,360))
            self.setMaximumSize(QtCore.QSize(90, 10000))
            mainLayout = self._loadVertical()
        tools_GRIDLAY = QtWidgets.QGridLayout()
        tools_GRIDLAY.setObjectName("tools_GRIDLAY")
        lgtVis_GRIDLAY = QtWidgets.QGridLayout()
        lgtVis_GRIDLAY.setObjectName("lgtVis_GRIDLAY")
        lgtVis_GRIDLAY.setHorizontalSpacing(3)
        lgtVis_GRIDLAY.setVerticalSpacing(3)
        lgtCreate_GRIDLAY = QtWidgets.QGridLayout()
        lgtCreate_GRIDLAY.setObjectName("lgtCreate_GRIDLAY")
        self._createButtons()
        if mainLayout.objectName() == 'horizontalLayout':
            tools_GRIDLAY.addWidget(self.simpleIsolate_BTN, 0, 0, 1, 1, QtCore.Qt.AlignCenter)
            tools_GRIDLAY.addWidget(self.lookThru_BTN, 0, 1, 1, 1, QtCore.Qt.AlignCenter)
            tools_GRIDLAY.addWidget(self.aimLight_BTN, 0, 2, 1, 1, QtCore.Qt.AlignCenter)
            tools_GRIDLAY.addWidget(self.lightsManager_BTN, 0, 3, 2, 1, QtCore.Qt.AlignCenter)
            tools_GRIDLAY.addWidget(self.specularConstrain_BTN, 1, 0, 1, 1, QtCore.Qt.AlignCenter)
            tools_GRIDLAY.addWidget(self.cleanUpCams_BTN, 1, 1, 1, 1, QtCore.Qt.AlignCenter)
            tools_GRIDLAY.addWidget(self.alignLight_BTN, 1, 2, 1, 1, QtCore.Qt.AlignCenter)
            mainLayout.addLayout(tools_GRIDLAY)
            spacerWidth = 16
            spacerHeight = 20
            spacerItem1 = QtWidgets.QSpacerItem(spacerWidth, spacerHeight, 
                                QtWidgets.QSizePolicy.Expanding,
                                QtWidgets.QSizePolicy.Minimum)
            mainLayout.addItem(spacerItem1)
            lgtVis_GRIDLAY.addWidget(self.visSnapshot01_BTN, 1, 0, 1, 1)
            lgtVis_GRIDLAY.addWidget(self.visSnapshot02_BTN, 1, 1, 1, 1)
            lgtVis_GRIDLAY.addWidget(self.visSnapshot03_BTN, 1, 2, 1, 1)
            lgtVis_GRIDLAY.addWidget(self.visSnapshot04_BTN, 2, 0, 1, 1)
            lgtVis_GRIDLAY.addWidget(self.visSnapshot05_BTN, 2, 1, 1, 1)
            lgtVis_GRIDLAY.addWidget(self.visSnapshot06_BTN, 2, 2, 1, 1)
            lgtVis_GRIDLAY.setRowMinimumHeight(0,10)
            lgtVis_GRIDLAY.setRowStretch(0,10)
            lgtVis_GRIDLAY.setRowMinimumHeight(3,10)
            lgtVis_GRIDLAY.setRowStretch(3,10)
            mainLayout.addLayout(lgtVis_GRIDLAY)
            spacerItem2 = QtWidgets.QSpacerItem(spacerWidth, spacerHeight, 
                                        QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Minimum)
            mainLayout.addItem(spacerItem2)
            lgtCreate_GRIDLAY.addWidget(self.spotLight_BTN, 1, 0, 1, 1)
            lgtCreate_GRIDLAY.addWidget(self.pointLight_BTN, 1, 1, 1, 1)
            lgtCreate_GRIDLAY.addWidget(self.areaLight_BTN, 1, 2, 1, 1)
            lgtCreate_GRIDLAY.addWidget(self.directionalLight_BTN, 1, 3, 1, 1)
            lgtCreate_GRIDLAY.addWidget(self.ambientLight_BTN, 1, 4, 1, 1)
            lgtCreate_GRIDLAY.addWidget(self.volumeLight_BTN, 1, 5, 1, 1)
            lgtCreate_GRIDLAY.addWidget(self.aiAreaLight_BTN, 3, 0, 1, 1)
            lgtCreate_GRIDLAY.addWidget(self.aiSkyDomeLight_BTN, 3, 1, 1, 1)
            lgtCreate_GRIDLAY.addWidget(self.aiMeshLight_BTN, 3, 2, 1, 1)
            lgtCreate_GRIDLAY.addWidget(self.aiPhotometricLight_BTN, 3, 3, 1, 1)
            lgtCreate_GRIDLAY.addWidget(self.aiLightPortal_BTN, 3, 4, 1, 1)
            lgtCreate_GRIDLAY.addWidget(self.aiPhysicalSky_BTN, 3, 5, 1, 1)
            lgtCreate_GRIDLAY.setRowMinimumHeight(0,1)
            lgtCreate_GRIDLAY.setRowStretch(0,1)
            lgtCreate_GRIDLAY.setRowMinimumHeight(2,1)
            lgtCreate_GRIDLAY.setRowStretch(2,1)
            lgtCreate_GRIDLAY.setRowMinimumHeight(4,1)
            lgtCreate_GRIDLAY.setRowStretch(4,1)
            mainLayout.addLayout(lgtCreate_GRIDLAY)
            spacerItem3 = QtWidgets.QSpacerItem(spacerWidth, spacerHeight, 
                                        QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Minimum)
            mainLayout.addItem(spacerItem3)
        else:
            tools_GRIDLAY.addWidget(self.simpleIsolate_BTN, 0, 0, 1, 1, QtCore.Qt.AlignCenter)
            tools_GRIDLAY.addWidget(self.lookThru_BTN, 0, 1, 1, 1, QtCore.Qt.AlignCenter)
            tools_GRIDLAY.addWidget(self.aimLight_BTN, 1, 0, 1, 1, QtCore.Qt.AlignCenter)
            tools_GRIDLAY.addWidget(self.specularConstrain_BTN, 1, 1, 1, 1, QtCore.Qt.AlignCenter)
            tools_GRIDLAY.addWidget(self.cleanUpCams_BTN, 2, 0, 1, 1, QtCore.Qt.AlignCenter)
            tools_GRIDLAY.addWidget(self.alignLight_BTN, 2, 1, 1, 1, QtCore.Qt.AlignCenter)
            tools_GRIDLAY.addWidget(self.lightsManager_BTN, 3, 0, 1, 2, QtCore.Qt.AlignCenter)
            mainLayout.addLayout(tools_GRIDLAY)
            spacerWidth = 20
            spacerHeight = 16
            spacerItem1 = QtWidgets.QSpacerItem(spacerWidth, spacerHeight,
                                QtWidgets.QSizePolicy.Minimum,
                                QtWidgets.QSizePolicy.Expanding)
            mainLayout.addItem(spacerItem1)
            lgtVis_GRIDLAY.addWidget(self.visSnapshot01_BTN, 0, 1, 1, 1)
            lgtVis_GRIDLAY.addWidget(self.visSnapshot02_BTN, 0, 2, 1, 1)
            lgtVis_GRIDLAY.addWidget(self.visSnapshot03_BTN, 1, 1, 1, 1)
            lgtVis_GRIDLAY.addWidget(self.visSnapshot04_BTN, 1, 2, 1, 1)
            lgtVis_GRIDLAY.addWidget(self.visSnapshot05_BTN, 2, 1, 1, 1)
            lgtVis_GRIDLAY.addWidget(self.visSnapshot06_BTN, 2, 2, 1, 1)
            lgtVis_GRIDLAY.setColumnMinimumWidth(0,10)
            lgtVis_GRIDLAY.setColumnStretch(0,10)
            lgtVis_GRIDLAY.setColumnMinimumWidth(3,10)
            lgtVis_GRIDLAY.setColumnStretch(3,10)
            mainLayout.addLayout(lgtVis_GRIDLAY)
            spacerItem2 = QtWidgets.QSpacerItem(spacerWidth, spacerHeight,
                                        QtWidgets.QSizePolicy.Minimum,
                                        QtWidgets.QSizePolicy.Expanding)
            mainLayout.addItem(spacerItem2)
            lgtCreate_GRIDLAY.addWidget(self.spotLight_BTN, 0, 0, 1, 1)
            lgtCreate_GRIDLAY.addWidget(self.pointLight_BTN, 0, 1, 1, 1)
            lgtCreate_GRIDLAY.addWidget(self.areaLight_BTN, 0, 2, 1, 1)
            lgtCreate_GRIDLAY.addWidget(self.directionalLight_BTN, 1, 0, 1, 1)
            lgtCreate_GRIDLAY.addWidget(self.ambientLight_BTN, 1, 1, 1, 1)
            lgtCreate_GRIDLAY.addWidget(self.volumeLight_BTN, 1, 2, 1, 1)
            lgtCreate_GRIDLAY.addWidget(self.aiAreaLight_BTN, 3, 0, 1, 1)
            lgtCreate_GRIDLAY.addWidget(self.aiSkyDomeLight_BTN, 3, 1, 1, 1)
            lgtCreate_GRIDLAY.addWidget(self.aiMeshLight_BTN, 3, 2, 1, 1)
            lgtCreate_GRIDLAY.addWidget(self.aiPhotometricLight_BTN, 4, 0, 1, 1)
            lgtCreate_GRIDLAY.addWidget(self.aiLightPortal_BTN, 4, 1, 1, 1)
            lgtCreate_GRIDLAY.addWidget(self.aiPhysicalSky_BTN, 4, 2, 1, 1)
            lgtCreate_GRIDLAY.setRowMinimumHeight(2,3)
            lgtCreate_GRIDLAY.setRowStretch(2,3)
            mainLayout.addLayout(lgtCreate_GRIDLAY)
            spacerItem3 = QtWidgets.QSpacerItem(spacerWidth, spacerHeight,
                                        QtWidgets.QSizePolicy.Minimum,
                                        QtWidgets.QSizePolicy.Expanding)
            mainLayout.addItem(spacerItem3)

        mainLayout.addWidget(self.config_BTN)
        mainLayout.setAlignment(self.config_BTN, QtCore.Qt.AlignCenter)
        self.setLayout(mainLayout)
        
        QtCore.QMetaObject.connectSlotsByName(self)
    
    def _createButtons(self):
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
        self.simpleIsolate_BTN.setObjectName("simpleIsolate_BTN")
        self.simpleIsolate_BTN.setToolTip('Toggle Isolate Lights')
        self.lookThru_BTN.setSizePolicy(sizePolicy)
        self.lookThru_BTN.setMinimumSize(toolsBtnSize)
        self.lookThru_BTN.setMaximumSize(toolsBtnSize)
        self.lookThru_BTN.setObjectName("lookThru_BTN")
        self.lookThru_BTN.setToolTip('Look thru lights')
        self.aimLight_BTN.setSizePolicy(sizePolicy)
        self.aimLight_BTN.setMinimumSize(toolsBtnSize)
        self.aimLight_BTN.setMaximumSize(toolsBtnSize)
        self.aimLight_BTN.setObjectName("aimLight_BTN")
        self.aimLight_BTN.setToolTip('Aim: Select lights first, target last')
        self.specularConstrain_BTN.setSizePolicy(sizePolicy)
        self.specularConstrain_BTN.setMinimumSize(toolsBtnSize)
        self.specularConstrain_BTN.setMaximumSize(toolsBtnSize)
        self.specularConstrain_BTN.setObjectName("specularConstrain_BTN")
        self.specularConstrain_BTN.setToolTip('Specular: Select vertex')
        self.cleanUpCams_BTN.setSizePolicy(sizePolicy)
        self.cleanUpCams_BTN.setMinimumSize(toolsBtnSize)
        self.cleanUpCams_BTN.setMaximumSize(toolsBtnSize)
        self.cleanUpCams_BTN.setObjectName("cleanUpCams_BTN")
        self.cleanUpCams_BTN.setToolTip('Clean up light cams')
        self.alignLight_BTN.setSizePolicy(sizePolicy)
        self.alignLight_BTN.setMinimumSize(toolsBtnSize)
        self.alignLight_BTN.setMaximumSize(toolsBtnSize)
        self.alignLight_BTN.setObjectName("alignLight_BTN")
        self.alignLight_BTN.setToolTip('Align: Select lights first, target last')
        self.lightsManager_BTN.setSizePolicy(sizePolicy)
        self.lightsManager_BTN.setMinimumSize(toolsBtnSize)
        self.lightsManager_BTN.setMaximumSize(toolsBtnSize)
        self.lightsManager_BTN.setObjectName("lightsManager_BTN")
        self.lightsManager_BTN.setToolTip('Lights Manager')

        # LIGHT VIS SNAPSHOTS
        self.visSnapshot01_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.visSnapshot02_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.visSnapshot03_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.visSnapshot04_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.visSnapshot05_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.visSnapshot06_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.visSnapshot01_BTN.setObjectName("visSnapshot01_BTN")
        self.visSnapshot01_BTN.setSizePolicy(sizePolicy)
        self.visSnapshot01_BTN.setMinimumSize(visBtnSize)
        self.visSnapshot01_BTN.setMaximumSize(visBtnSize)
        self.visSnapshot01_BTN.setText("1")
        self.visSnapshot02_BTN.setObjectName("visSnapshot02_BTN")
        self.visSnapshot02_BTN.setSizePolicy(sizePolicy)
        self.visSnapshot02_BTN.setMinimumSize(visBtnSize)
        self.visSnapshot02_BTN.setMaximumSize(visBtnSize)
        self.visSnapshot02_BTN.setText("2")
        self.visSnapshot03_BTN.setObjectName("visSnapshot03_BTN")
        self.visSnapshot03_BTN.setSizePolicy(sizePolicy)
        self.visSnapshot03_BTN.setMinimumSize(visBtnSize)
        self.visSnapshot03_BTN.setMaximumSize(visBtnSize)
        self.visSnapshot03_BTN.setText("3")
        self.visSnapshot04_BTN.setObjectName("visSnapshot04_BTN")
        self.visSnapshot04_BTN.setSizePolicy(sizePolicy)
        self.visSnapshot04_BTN.setMinimumSize(visBtnSize)
        self.visSnapshot04_BTN.setMaximumSize(visBtnSize)
        self.visSnapshot04_BTN.setText("4")
        self.visSnapshot05_BTN.setObjectName("visSnapshot05_BTN")
        self.visSnapshot05_BTN.setSizePolicy(sizePolicy)
        self.visSnapshot05_BTN.setMinimumSize(visBtnSize)
        self.visSnapshot05_BTN.setMaximumSize(visBtnSize)
        self.visSnapshot05_BTN.setText("5")
        self.visSnapshot06_BTN.setObjectName("visSnapshot06_BTN")
        self.visSnapshot06_BTN.setSizePolicy(sizePolicy)
        self.visSnapshot06_BTN.setMinimumSize(visBtnSize)
        self.visSnapshot06_BTN.setMaximumSize(visBtnSize)
        self.visSnapshot06_BTN.setText("6")

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
        self.spotLight_BTN.setObjectName("spotLight_BTN")
        self.spotLight_BTN.setToolTip('Spot light')
        self.pointLight_BTN.setSizePolicy(sizePolicy)
        self.pointLight_BTN.setMinimumSize(lightsBtnSize)
        self.pointLight_BTN.setMaximumSize(lightsBtnSize)
        self.pointLight_BTN.setObjectName("pointLight_BTN")
        self.pointLight_BTN.setToolTip('Point light')
        self.areaLight_BTN.setSizePolicy(sizePolicy)
        self.areaLight_BTN.setMinimumSize(lightsBtnSize)
        self.areaLight_BTN.setMaximumSize(lightsBtnSize)
        self.areaLight_BTN.setObjectName("areaLight_BTN")
        self.areaLight_BTN.setToolTip('Area light')
        self.directionalLight_BTN.setSizePolicy(sizePolicy)
        self.directionalLight_BTN.setMinimumSize(lightsBtnSize)
        self.directionalLight_BTN.setMaximumSize(lightsBtnSize)
        self.directionalLight_BTN.setObjectName("directionalLight_BTN")
        self.directionalLight_BTN.setToolTip('Directional light')
        self.ambientLight_BTN.setSizePolicy(sizePolicy)
        self.ambientLight_BTN.setMinimumSize(lightsBtnSize)
        self.ambientLight_BTN.setMaximumSize(lightsBtnSize)
        self.ambientLight_BTN.setObjectName("ambientLight_BTN")
        self.ambientLight_BTN.setToolTip('Ambient light')
        self.volumeLight_BTN.setSizePolicy(sizePolicy)
        self.volumeLight_BTN.setMinimumSize(QtCore.QSize(16, 16))
        self.volumeLight_BTN.setMaximumSize(QtCore.QSize(16, 16))
        self.volumeLight_BTN.setObjectName("volumeLight_BTN")
        self.volumeLight_BTN.setToolTip('Volume light')

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
        self.aiAreaLight_BTN.setObjectName("aiAreaLight_BTN")
        self.aiAreaLight_BTN.setToolTip('aiAreaLight')
        self.aiSkyDomeLight_BTN.setSizePolicy(sizePolicy)
        self.aiSkyDomeLight_BTN.setMinimumSize(lightsBtnSize)
        self.aiSkyDomeLight_BTN.setMaximumSize(lightsBtnSize)
        self.aiSkyDomeLight_BTN.setObjectName("aiSkyDomeLight_BTN")
        self.aiSkyDomeLight_BTN.setToolTip('aiSkyDomeLight')
        self.aiMeshLight_BTN.setSizePolicy(sizePolicy)
        self.aiMeshLight_BTN.setMinimumSize(lightsBtnSize)
        self.aiMeshLight_BTN.setMaximumSize(lightsBtnSize)
        self.aiMeshLight_BTN.setObjectName("aiMeshLight_BTN")
        self.aiMeshLight_BTN.setToolTip('aiMeshLight')
        self.aiPhotometricLight_BTN.setSizePolicy(sizePolicy)
        self.aiPhotometricLight_BTN.setMinimumSize(lightsBtnSize)
        self.aiPhotometricLight_BTN.setMaximumSize(lightsBtnSize)
        self.aiPhotometricLight_BTN.setObjectName("aiPhotometricLight_BTN")
        self.aiPhotometricLight_BTN.setToolTip('aiPhotometricLight')
        self.aiLightPortal_BTN.setSizePolicy(sizePolicy)
        self.aiLightPortal_BTN.setMinimumSize(lightsBtnSize)
        self.aiLightPortal_BTN.setMaximumSize(lightsBtnSize)
        self.aiLightPortal_BTN.setObjectName("aiLightPortal_BTN")
        self.aiLightPortal_BTN.setToolTip('aiLightPortal')
        self.aiPhysicalSky_BTN.setSizePolicy(sizePolicy)
        self.aiPhysicalSky_BTN.setMinimumSize(lightsBtnSize)
        self.aiPhysicalSky_BTN.setMaximumSize(lightsBtnSize)
        self.aiPhysicalSky_BTN.setObjectName("aiPhysicalSky_BTN")
        self.aiPhysicalSky_BTN.setToolTip('aiPhysicalSky')

        #CONFIG
        self.config_BTN = QtWidgets.QPushButton(self.centralwidget)
        self.config_BTN.setMaximumSize(configBtnSize)
        self.config_BTN.setObjectName("config_BTN")
        self.config_BTN.setToolTip('Config Options')
        
    def _loadHorizontal(self):
        horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        horizontalLayout.setObjectName("horizontalLayout")

        return horizontalLayout
    
    def _loadVertical(self):
        verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        verticalLayout.setObjectName("verticalLayout")

        return verticalLayout
    
    def _setConnections(self):
        #CONTEXT MENUS
        self.config_BTN.clicked.connect(partial(self.configOptions, self.config_BTN.pos()))

    def _savePrefOrientation(self, prefOrientation):
        userPath = os.path.expanduser("~")
        finalDir = os.path.join(userPath, ".CGXTools")
        try:
            if not os.path.exists(finalDir):
                os.mkdir(finalDir)
        except:
            pass
        config = {'orientation': prefOrientation}
        filepath = os.path.join(finalDir, "MiniTools_orientation.pref")
        with open(filepath, "w") as fp:
            json.dump(config, fp, indent = 4)
    
    def _loadPrefOrientation(self):
        userPath = os.path.expanduser("~")
        finalDir = os.path.join(userPath, ".CGXTools")
        filepath = os.path.join(finalDir, "MiniTools_orientation.pref")
        config = dict()
        if os.path.exists(filepath):
            with open(filepath) as fp:
                config = json.load(fp)
        if config.get('orientation') is not None and config.get('orientation') in ['horizontal','vertical']:
            return config.get('orientation')
        else:
            self._savePrefOrientation('horizontal')
            return 'horizontal'
    
    # --------------------------------------------------------------------------------------------
	# Methods for config button
	# --------------------------------------------------------------------------------------------
    def configOptions (self,pos):
        """Method that creates the popupmenu"""
        menu = QtWidgets.QMenu(self.config_BTN)
        prefOrientationQ = menu.addAction("Toggle tools orientation")
        prefOrientationQ.setToolTip('Please restart MiniTools to see changes.')
        menu.popup(self.config_BTN.mapToGlobal(pos))

        if self._prefOrientation == 'horizontal':
            self._prefOrientation = 'vertical'
        else:
            self._prefOrientation = 'horizontal'
        prefOrientationQ.triggered.connect(partial(self._savePrefOrientation, self._prefOrientation))


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