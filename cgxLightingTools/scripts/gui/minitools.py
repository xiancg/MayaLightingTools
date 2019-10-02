'''
@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
TODO: Review code to show, hide and close
TODO: Move rename, duplicate and delete closer to the creation buttons.
TODO: Options to create lights aligned with selection with some default offset
TODO: Add separators to naming library
TODO: Create GUI for naming library
TODO: Change light attrs implementation
TODO: Create light attrs GUI
TODO: Implement new stylesheet
TODO: Shortcuts implementation pass for everything
TODO: Add option to set shortcuts for tools
TODO: All alerts should be changed to something without the need for confirmation
Check QGraphicsOpacityEffect and QPropertyAnimation
TODO: Rewrite lights manager and enable it here
'''
from __future__ import absolute_import
import os
import json
from functools import partial

from PySide2 import QtWidgets, QtCore, QtGui
import maya.cmds as mc
import cgxLightingTools.scripts.gui.mayaWindow as mWin
from cgxLightingTools.scripts.toolbox import tools
from cgxLightingTools.scripts.core import stats
from cgxLightingTools.scripts.gui import minitools_buttons as btns
from cgxLightingTools.scripts.gui.lightCreator import LightCreator_GUI
from cgxLightingTools.scripts.gui.lightCreator import LightRenamer_GUI
from cgxLightingTools.scripts.gui.lightDuplicator import LightDuplicator_GUI
from cgxLightingTools.scripts.gui.lookThruDefaults import LookThruDefaults_GUI
from cgxLightingTools.scripts.toolbox.initfactories import init_factories
from cgxLightingTools.scripts.gui import minitools_icons

# --------------------------------------------------------
# Mini Tools window
# --------------------------------------------------------
class MiniTools_GUI(QtWidgets.QMainWindow):
    def __init__(self, parent=mWin.getMayaWindow()):
        super(MiniTools_GUI, self).__init__(parent)
        self._prefOrientation = self._loadOrientationPref()
        self.factories = init_factories()
        self._setupUi()
        self._setConnections()
        self._loadStatsPrefs()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
    
    def _setupUi(self):
        self.setObjectName('miniTools_MW')
        self.setWindowTitle('Mini Tools')
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        if self._prefOrientation == 'horizontal':
            self.resize(462, 90)
            self.setMinimumSize(QtCore.QSize(462,90))
            self.setMaximumSize(QtCore.QSize(10000, 90))
            mainLayout = self._loadHorizontal()
        else:
            self.resize(100, 406)
            self.setMinimumSize(QtCore.QSize(100, 406))
            self.setMaximumSize(QtCore.QSize(100, 10000))
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
            tools_GRIDLAY.addWidget(self.lightsManager_BTN, 0, 3, 1, 1, QtCore.Qt.AlignCenter)
            tools_GRIDLAY.addWidget(self.duplicateLight_BTN, 0, 4, 1, 1, QtCore.Qt.AlignCenter)
            tools_GRIDLAY.addWidget(self.deleteLight_BTN, 0, 5, 2, 1, QtCore.Qt.AlignCenter)
            tools_GRIDLAY.addWidget(self.specularConstrain_BTN, 1, 0, 1, 1, QtCore.Qt.AlignCenter)
            tools_GRIDLAY.addWidget(self.cleanUpCams_BTN, 1, 1, 1, 1, QtCore.Qt.AlignCenter)
            tools_GRIDLAY.addWidget(self.alignLight_BTN, 1, 2, 1, 1, QtCore.Qt.AlignCenter)
            tools_GRIDLAY.addWidget(self.transformBake_BTN, 1, 3, 1, 1, QtCore.Qt.AlignCenter)
            tools_GRIDLAY.addWidget(self.renameLight_BTN, 1, 4, 1, 1, QtCore.Qt.AlignCenter)

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
            tools_GRIDLAY.addWidget(self.transformBake_BTN, 3, 0, 1, 1, QtCore.Qt.AlignCenter)
            tools_GRIDLAY.addWidget(self.lightsManager_BTN, 3, 1, 1, 1, QtCore.Qt.AlignCenter)
            tools_GRIDLAY.addWidget(self.duplicateLight_BTN, 4, 0, 1, 1, QtCore.Qt.AlignCenter)
            tools_GRIDLAY.addWidget(self.renameLight_BTN, 4, 1, 1, 1, QtCore.Qt.AlignCenter)
            tools_GRIDLAY.addWidget(self.deleteLight_BTN, 5, 0, 1, 2, QtCore.Qt.AlignCenter)
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
        self.setCentralWidget(self.centralwidget)
        
        QtCore.QMetaObject.connectSlotsByName(self)
    
    def _createButtons(self):
        toolsBtnSize = QtCore.QSize(32, 32)
        visBtnSize = QtCore.QSize(14, 14)
        lightsBtnSize = QtCore.QSize(16, 16)
        configBtnSize = QtCore.QSize(20, 20)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        # TOOLS
        self.simpleIsolate_BTN = btns.MiniTools_BTN(self.centralwidget)
        self.lookThru_BTN = btns.MiniTools_BTN(self.centralwidget)
        self.aimLight_BTN = btns.MiniTools_BTN(self.centralwidget)
        self.specularConstrain_BTN = btns.MiniTools_BTN(self.centralwidget)
        self.cleanUpCams_BTN = btns.MiniTools_BTN(self.centralwidget)
        self.lightsManager_BTN = btns.MiniTools_BTN(self.centralwidget)
        self.alignLight_BTN = btns.MiniTools_BTN(self.centralwidget)
        self.transformBake_BTN = btns.MiniTools_BTN(self.centralwidget)
        self.duplicateLight_BTN = btns.MiniTools_BTN(self.centralwidget)
        self.renameLight_BTN = btns.MiniTools_BTN(self.centralwidget)
        self.deleteLight_BTN = btns.MiniTools_BTN(self.centralwidget)
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
        self.specularConstrain_BTN.setToolTip('Specular: Select vertex. Right click for more options.')
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
        self.transformBake_BTN.setSizePolicy(sizePolicy)
        self.transformBake_BTN.setMinimumSize(toolsBtnSize)
        self.transformBake_BTN.setMaximumSize(toolsBtnSize)
        self.transformBake_BTN.setObjectName("transformBake_BTN")
        self.transformBake_BTN.setToolTip('Transform bake. Objects or vertex.')
        self.duplicateLight_BTN.setSizePolicy(sizePolicy)
        self.duplicateLight_BTN.setMinimumSize(toolsBtnSize)
        self.duplicateLight_BTN.setMaximumSize(toolsBtnSize)
        self.duplicateLight_BTN.setObjectName("duplicateLight_BTN")
        self.duplicateLight_BTN.setToolTip('Duplicate lights. Right click for more options.')
        self.duplicateLight_BTN.setText('Dupli\ncate')
        self.duplicateLight_BTN.setStyleSheet("font-size: 10px;")
        self.renameLight_BTN.setSizePolicy(sizePolicy)
        self.renameLight_BTN.setMinimumSize(toolsBtnSize)
        self.renameLight_BTN.setMaximumSize(toolsBtnSize)
        self.renameLight_BTN.setObjectName("renameLight_BTN")
        self.renameLight_BTN.setToolTip('Rename selected light.')
        self.renameLight_BTN.setText('Re\nname')
        self.renameLight_BTN.setStyleSheet("font-size: 10px;")
        self.deleteLight_BTN.setSizePolicy(sizePolicy)
        self.deleteLight_BTN.setMinimumSize(toolsBtnSize)
        self.deleteLight_BTN.setMaximumSize(toolsBtnSize)
        self.deleteLight_BTN.setObjectName("deleteLight_BTN")
        self.deleteLight_BTN.setToolTip('Delete selected lights (Ctrl+Del)')
        self.deleteLight_BTN.setText('Del')
        self.deleteLight_BTN.setStyleSheet("font-size: 10px;")
        delLight = QtWidgets.QAction("Delete Light", self.deleteLight_BTN,
                                     shortcut=QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Delete),
                                     triggered=self._deleteLight)
        self.deleteLight_BTN.addAction(delLight)
        self.toolsBtns = [self.simpleIsolate_BTN, self.lookThru_BTN,
                          self.aimLight_BTN, self.aimLight_BTN,
                          self.specularConstrain_BTN, self.cleanUpCams_BTN,
                          self.lightsManager_BTN, self.alignLight_BTN,
                          self.transformBake_BTN, self.duplicateLight_BTN,
                          self.renameLight_BTN, self.deleteLight_BTN]

        # LIGHT VIS SNAPSHOTS
        self.visSnapshot01_BTN = btns.VisSnapshot_BTN(self.centralwidget)
        self.visSnapshot02_BTN = btns.VisSnapshot_BTN(self.centralwidget)
        self.visSnapshot03_BTN = btns.VisSnapshot_BTN(self.centralwidget)
        self.visSnapshot04_BTN = btns.VisSnapshot_BTN(self.centralwidget)
        self.visSnapshot05_BTN = btns.VisSnapshot_BTN(self.centralwidget)
        self.visSnapshot06_BTN = btns.VisSnapshot_BTN(self.centralwidget)
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
        self.visSnapBtns = [self.visSnapshot01_BTN, self.visSnapshot02_BTN, 
                            self.visSnapshot03_BTN, self.visSnapshot04_BTN,
                            self.visSnapshot05_BTN, self.visSnapshot06_BTN]

        # DEFAULT LIGHTS
        self.spotLight_BTN = btns.MiniTools_BTN(self.centralwidget)
        self.pointLight_BTN = btns.MiniTools_BTN(self.centralwidget)
        self.areaLight_BTN = btns.MiniTools_BTN(self.centralwidget)
        self.directionalLight_BTN = btns.MiniTools_BTN(self.centralwidget)
        self.ambientLight_BTN = btns.MiniTools_BTN(self.centralwidget)
        self.volumeLight_BTN = btns.MiniTools_BTN(self.centralwidget)
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
        self.aiAreaLight_BTN = btns.MiniTools_BTN(self.centralwidget)
        self.aiSkyDomeLight_BTN = btns.MiniTools_BTN(self.centralwidget)
        self.aiMeshLight_BTN = btns.MiniTools_BTN(self.centralwidget)
        self.aiPhotometricLight_BTN = btns.MiniTools_BTN(self.centralwidget)
        self.aiLightPortal_BTN = btns.MiniTools_BTN(self.centralwidget)
        self.aiPhysicalSky_BTN = btns.MiniTools_BTN(self.centralwidget)
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
        self.lightBtns = [self.spotLight_BTN, self.pointLight_BTN,
                          self.areaLight_BTN, self.directionalLight_BTN,
                          self.ambientLight_BTN, self.volumeLight_BTN,
                          self.aiAreaLight_BTN, self.aiSkyDomeLight_BTN,
                          self.aiMeshLight_BTN, self.aiPhotometricLight_BTN,
                          self.aiLightPortal_BTN, self.aiPhysicalSky_BTN]

        #CONFIG
        self.config_BTN = btns.MiniTools_BTN(self.centralwidget)
        self.config_BTN.setSizePolicy(sizePolicy)
        self.config_BTN.setMaximumSize(configBtnSize)
        self.config_BTN.setMinimumSize(configBtnSize)
        self.config_BTN.setObjectName("config_BTN")
        self.config_BTN.setToolTip('Config Options')
        
        # * Enable this when lights manager gets reworked
        self.lightsManager_BTN.setEnabled(False)
        
    def _loadHorizontal(self):
        horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        horizontalLayout.setObjectName("horizontalLayout")

        return horizontalLayout
    
    def _loadVertical(self):
        verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        verticalLayout.setObjectName("verticalLayout")

        return verticalLayout
    
    def _setConnections(self):
        # BUTTONS
        self.lookThru_BTN.clicked.connect(self._lookThruLight)
        self.cleanUpCams_BTN.clicked.connect(tools.cleanUpCams)
        self.alignLight_BTN.clicked.connect(tools.alignLightToObject)
        self.aimLight_BTN.clicked.connect(tools.aimLightToObject)
        self.simpleIsolate_BTN.clicked.connect(tools.simpleIsolateLights)
        self.specularConstrain_BTN.clicked.connect(tools.specularConstrain)
        self.transformBake_BTN.clicked.connect(self._transformBake)
        self.duplicateLight_BTN.clicked.connect(self._duplicateLight)
        self.renameLight_BTN.clicked.connect(self._renameLight)
        self.deleteLight_BTN.clicked.connect(self._deleteLight)
        self.visSnapshot01_BTN.clicked.connect(partial(self._lightAttrsSnapshotOpt,self.visSnapshot01_BTN))
        self.visSnapshot02_BTN.clicked.connect(partial(self._lightAttrsSnapshotOpt,self.visSnapshot02_BTN))
        self.visSnapshot03_BTN.clicked.connect(partial(self._lightAttrsSnapshotOpt,self.visSnapshot03_BTN))
        self.visSnapshot04_BTN.clicked.connect(partial(self._lightAttrsSnapshotOpt,self.visSnapshot04_BTN))
        self.visSnapshot05_BTN.clicked.connect(partial(self._lightAttrsSnapshotOpt,self.visSnapshot05_BTN))
        self.visSnapshot06_BTN.clicked.connect(partial(self._lightAttrsSnapshotOpt,self.visSnapshot06_BTN))
        # LIGHTS
        self.spotLight_BTN.clicked.connect(partial(self._createLight,'spotLight'))
        self.pointLight_BTN.clicked.connect(partial(self._createLight,'pointLight'))
        self.areaLight_BTN.clicked.connect(partial(self._createLight,'areaLight'))
        self.directionalLight_BTN.clicked.connect(partial(self._createLight,'directionalLight'))
        self.ambientLight_BTN.clicked.connect(partial(self._createLight,'ambientLight'))
        self.volumeLight_BTN.clicked.connect(partial(self._createLight,'volumeLight'))
        self.aiAreaLight_BTN.clicked.connect(partial(self._createLight,'aiAreaLight'))
        self.aiSkyDomeLight_BTN.clicked.connect(partial(self._createLight,'aiSkyDomeLight'))
        self.aiMeshLight_BTN.clicked.connect(partial(self._createLight,'aiMeshLight'))
        self.aiPhotometricLight_BTN.clicked.connect(partial(self._createLight,'aiPhotometricLight'))
        self.aiLightPortal_BTN.clicked.connect(partial(self._createLight,'aiLightPortal'))
        self.aiPhysicalSky_BTN.clicked.connect(partial(self._createLight,'aiSky'))
        # ICONS TOOLS
        toolsIconSize = QtCore.QSize(32,32)
        self.lookThru_BTN.setIcon(QtGui.QIcon(":/lookThru.png"))
        self.lookThru_BTN.setIconSize(toolsIconSize)
        self.cleanUpCams_BTN.setIcon(QtGui.QIcon(":/cleanUpCams.png"))
        self.cleanUpCams_BTN.setIconSize(toolsIconSize)
        self.aimLight_BTN.setIcon(QtGui.QIcon(":/aimLight.png"))
        self.aimLight_BTN.setIconSize(toolsIconSize)
        self.alignLight_BTN.setIcon(QtGui.QIcon(":/alignLight.png"))
        self.alignLight_BTN.setIconSize(toolsIconSize)
        self.simpleIsolate_BTN.setIcon(QtGui.QIcon(":/simpleIsolate.png"))
        self.simpleIsolate_BTN.setIconSize(toolsIconSize)
        self.specularConstrain_BTN.setIcon(QtGui.QIcon(":/specularConstrain.png"))
        self.specularConstrain_BTN.setIconSize(toolsIconSize)
        self.lightsManager_BTN.setIcon(QtGui.QIcon(":/lightsManager.png"))
        self.lightsManager_BTN.setIconSize(toolsIconSize)
        self.transformBake_BTN.setIcon(QtGui.QIcon(":/transformBake.png"))
        self.transformBake_BTN.setIconSize(toolsIconSize)
        # ICONS LIGHTS
        lightsIconSize = QtCore.QSize(16,16)
        self.spotLight_BTN.setIcon(QtGui.QIcon(":/create_spotLight.png"))
        self.spotLight_BTN.setIconSize(lightsIconSize)
        self.pointLight_BTN.setIcon(QtGui.QIcon(":/create_pointLight.png"))
        self.pointLight_BTN.setIconSize(lightsIconSize)
        self.areaLight_BTN.setIcon(QtGui.QIcon(":/create_areaLight.png"))
        self.areaLight_BTN.setIconSize(lightsIconSize)
        self.directionalLight_BTN.setIcon(QtGui.QIcon(":/create_directionalLight.png"))
        self.directionalLight_BTN.setIconSize(lightsIconSize)
        self.ambientLight_BTN.setIcon(QtGui.QIcon(":/create_ambientLight.png"))
        self.ambientLight_BTN.setIconSize(lightsIconSize)
        self.volumeLight_BTN.setIcon(QtGui.QIcon(":/create_volumeLight.png"))
        self.volumeLight_BTN.setIconSize(lightsIconSize)
        self.aiAreaLight_BTN.setIcon(QtGui.QIcon(":/create_aiAreaLight.png"))
        self.aiAreaLight_BTN.setIconSize(lightsIconSize)
        self.aiSkyDomeLight_BTN.setIcon(QtGui.QIcon(":/create_aiSkyDomeLight.png"))
        self.aiSkyDomeLight_BTN.setIconSize(lightsIconSize)
        self.aiMeshLight_BTN.setIcon(QtGui.QIcon(":/create_aiMeshLight.png"))
        self.aiMeshLight_BTN.setIconSize(lightsIconSize)
        self.aiPhotometricLight_BTN.setIcon(QtGui.QIcon(":/create_aiPhotometricLight.png"))
        self.aiPhotometricLight_BTN.setIconSize(lightsIconSize)
        self.aiLightPortal_BTN.setIcon(QtGui.QIcon(":/create_aiLightPortal.png"))
        self.aiLightPortal_BTN.setIconSize(lightsIconSize)
        self.aiPhysicalSky_BTN.setIcon(QtGui.QIcon(":/create_aiPhysicalSky.png"))
        self.aiPhysicalSky_BTN.setIconSize(lightsIconSize)

        # CONFIG ICON
        configIconSize = QtCore.QSize(20,20)
        self.config_BTN.setIcon(QtGui.QIcon(":/config.png"))
        self.config_BTN.setIconSize(configIconSize)

        # CONTEXT MENUS
        self.specularConstrain_BTN.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.specularConstrain_BTN.rightClick.connect(self.specConstrainOptions)
        self.simpleIsolate_BTN.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.simpleIsolate_BTN.rightClick.connect(self.isolateOptions)
        self.duplicateLight_BTN.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.duplicateLight_BTN.rightClick.connect(self.duplicateLightOptions)
        self.config_BTN.clicked.connect(self.configOptions)
        self.visSnapshot01_BTN.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.visSnapshot01_BTN.rightClick.connect(self.lightAttrsSnapshotOptions)
        self.visSnapshot02_BTN.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.visSnapshot02_BTN.rightClick.connect(self.lightAttrsSnapshotOptions)
        self.visSnapshot03_BTN.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.visSnapshot03_BTN.rightClick.connect(self.lightAttrsSnapshotOptions)
        self.visSnapshot04_BTN.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.visSnapshot04_BTN.rightClick.connect(self.lightAttrsSnapshotOptions)
        self.visSnapshot05_BTN.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.visSnapshot05_BTN.rightClick.connect(self.lightAttrsSnapshotOptions)
        self.visSnapshot06_BTN.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.visSnapshot06_BTN.rightClick.connect(self.lightAttrsSnapshotOptions)
    
    def _prefs_path(self):
        userPath = os.path.expanduser("~")
        finalDir = os.path.join(userPath, ".CGXTools")
        try:
            if not os.path.exists(finalDir):
                os.mkdir(finalDir)
        except:
            pass
        filepath = os.path.join(finalDir, "MiniTools.pref")
        return filepath

    def _saveOrientationPref(self, prefOrientation):
        filepath = self._prefs_path()
        config = dict()
        if os.path.exists(filepath):
            with open(filepath) as fp:
                config = json.load(fp)
                config['orientation'] = prefOrientation
            with open(filepath, 'w') as fp:
                json.dump(config, fp, indent = 4)
        else:
            config = {'orientation': prefOrientation}
            with open(filepath, "w") as fp:
                json.dump(config, fp, indent = 4)
        # Open a new instance with the new orientation
        load()
        self.close()
    
    def _loadOrientationPref(self):
        filepath = self._prefs_path()
        config = dict()
        if os.path.exists(filepath):
            with open(filepath) as fp:
                config = json.load(fp)
        if config.get('orientation') is not None and \
           config.get('orientation') in ['horizontal','vertical']:
            return config.get('orientation')
        else:
            config = {'orientation': 'horizontal'}
            with open(filepath, "w") as fp:
                json.dump(config, fp, indent = 4)
            return 'horizontal'
    
    def _saveLookThruPrefs(self, winWidth, winHeight, nearClip, farClip):
        filepath = self._prefs_path()
        config = dict()
        if os.path.exists(filepath):
            with open(filepath) as fp:
                config = json.load(fp)
                config['lookThru_nearClip'] = nearClip
                config['lookThru_farClip'] = farClip
                config['lookThru_winWidth'] = winWidth
                config['lookThru_winHeight'] = winHeight
            with open(filepath, 'w') as fp:
                json.dump(config, fp, indent = 4)
        else:
            config = {'lookThru_nearClip':nearClip,'lookThru_farClip':farClip,
                      'lookThru_winWidth':winWidth,'lookThru_winHeight':winHeight}
            with open(filepath, 'w') as fp:
                json.dump(config, fp, indent = 4)
    
    def _loadLookThruPrefs(self):
        filepath = self._prefs_path()
        config = dict()
        if os.path.exists(filepath):
            with open(filepath) as fp:
                config = json.load(fp)
        valuesList = [config.get('lookThru_nearClip'),config.get('lookThru_farClip'),
                    config.get('lookThru_winWidth'),config.get('lookThru_winHeight')]
        if None not in valuesList:
            return config
        else:
            self._saveLookThruPrefs(629, 404, 1.0, 1000000)
            config = {'lookThru_nearClip':1.0, 'lookThru_farClip':1000000,
                      'lookThru_winWidth': 629, 'lookThru_winHeight':404}
            return config

    def _saveStatsPrefs(self, statsBool):
        filepath = self._prefs_path()
        config = dict()
        if os.path.exists(filepath):
            with open(filepath) as fp:
                config = json.load(fp)
                config['stats'] = statsBool
            with open(filepath, 'w') as fp:
                json.dump(config, fp, indent = 4)
        else:
            config = {'stats':statsBool}
            with open(filepath, 'w') as fp:
                json.dump(config, fp, indent = 4)
        if statsBool:
            for btn in self.toolsBtns:
                btn.collect_stats = True
        
    def _loadStatsPrefs(self):
        filepath = self._prefs_path()
        config = dict()
        if os.path.exists(filepath):
            with open(filepath) as fp:
                config = json.load(fp)
        if config.get('stats'):
            stats.load()
            for btn in self.toolsBtns:
                btn.collect_stats = True
            return config.get('stats')
        else:
            self._saveStatsPrefs(False)
            return False
    
    def _saveDebugPrefs(self, debugBool):
        filepath = self._prefs_path()
        config = dict()
        if os.path.exists(filepath):
            with open(filepath) as fp:
                config = json.load(fp)
                config['debug'] = debugBool
            with open(filepath, 'w') as fp:
                json.dump(config, fp, indent = 4)
        else:
            config = {'debug':debugBool}
            with open(filepath, 'w') as fp:
                json.dump(config, fp, indent = 4)
        if debugBool:
            tools.initFileLogger()
    
    def _loadDebugPrefs(self):
        filepath = self._prefs_path()
        config = dict()
        if os.path.exists(filepath):
            with open(filepath) as fp:
                config = json.load(fp)
        if config.get('debug'):
            tools.initFileLogger()
            return config.get('debug')
        else:
            self._saveStatsPrefs(False)
            return False
    
    def _transformBake(self):
        allSel = mc.ls(sl=True)
        if len(allSel) < 1:
            msgBox = QtWidgets.QMessageBox(self)
            msgBox.setWindowTitle("Warning!")
            msgBox.setText("Please select at least one vertex or transform to bake.")
            msgBox.exec_()
            tools.logger.info('Please select at least one vertex or transform to bake.')
        else:
            inputDialog = QtWidgets.QInputDialog()
            inputDialog.setInputMode(QtWidgets.QInputDialog.DoubleInput)
            inputDialog.setDoubleDecimals(2)
            inputDialog.setDoubleMinimum(0.01)
            value, ok = inputDialog.getDouble(self, 'Sample By', 'Each ### frames:', 1.0)
            if ok:
                try:
                    mc.refresh(suspend=True)
                    tools.transformBake(allSel,value)
                except:
                    pass
                finally:
                    mc.refresh(suspend=False)
        #Done!
        msgBox = QtWidgets.QMessageBox(self)
        msgBox.setWindowTitle("Done!")
        msgBox.setText("Done baking transforms.")
        msgBox.exec_()
    
    def _lookThruLight(self):
        config = self._loadLookThruPrefs()
        tools.lookThruLight(config['lookThru_winWidth'],
                            config['lookThru_winHeight'],
                            config['lookThru_nearClip'],
                            config['lookThru_farClip'])
    
    def _createLight(self, lightNodeType):
        dialog = LightCreator_GUI(lightNodeType, self.factories, self)
        dialog.show()
        if dialog == 1:
            tools.resetGlobals()
    
    def _renameLight(self):
        allSel = mc.ls(sl=True)
        if len(allSel) > 1:
            msgBox = QtWidgets.QMessageBox(self)
            msgBox.setWindowTitle("Warning!")
            msgBox.setText("Please select one light only.")
            msgBox.exec_()
            tools.logger.info('Please select one light only.')
        else:
            lightNode = allSel[0]
            objTransform, objShape= tools.getTransformAndShape(lightNode)
            dialog = LightRenamer_GUI(objShape, self.factories, self)
            dialog.show()
            if dialog == 1:
                tools.resetGlobals()
    
    def _duplicateLight(self, withInputs=False, withNodes= False):
        dialog = LightDuplicator_GUI(withInputs, withNodes, self.factories, self)
        dialog.exec_()
        if dialog == 1:
            tools.resetGlobals()
    
    def _deleteLight(self):
        allSel = mc.ls(sl=True)
        success = False
        for each in allSel:
            objTransform, objShape= tools.getTransformAndShape(each)
            for name, factory in self.factories.iteritems():
                if mc.nodeType(objShape) in factory.lightNodeTypes:
                    factory.deleteLight(objTransform, objShape)
                    success = True
                    break
        if success:
            tools.resetGlobals()

    def _lookThruDefaults(self):
        dialog = LookThruDefaults_GUI(self)
        dialog.exec_()
        if dialog == 1:
            tools.resetGlobals()
    
    def closeEvent(self, event):
        if self._loadStatsPrefs():
            stats.save()
        QtWidgets.QMainWindow.closeEvent(self, event)

    # --------------------------------------------------------
	# Method for right-click menus
	# --------------------------------------------------------
    def configOptions (self):
        """Method that creates the popupmenu"""
        menu = QtWidgets.QMenu(self.config_BTN)
        prefOrientationQ = menu.addAction("Toggle tools orientation")
        prefLookThruQ = menu.addAction("Look thru preferences")
        menu.addSeparator()

        usageStatsQ = menu.addAction("Help collecting usage statistics")
        usageStatsQ.setCheckable(True)
        usageStatsQ.setObjectName("config_stats")
        if self._loadStatsPrefs():
            usageStatsQ.setChecked(True)

        debugModeQ = menu.addAction("Debug Mode")
        debugModeQ.setCheckable(True)
        debugModeQ.setObjectName("config_debugMode")
        if self._loadDebugPrefs():
            debugModeQ.setChecked(True)

        self.config_BTN.setMenu(menu)
        if self._prefOrientation == 'horizontal':
            self._prefOrientation = 'vertical'
        else:
            self._prefOrientation = 'horizontal'

        prefOrientationQ.triggered.connect(partial(self._saveOrientationPref, self._prefOrientation))
        prefLookThruQ.triggered.connect(self._lookThruDefaults)
        usageStatsQ.triggered[bool].connect(self._saveStatsPrefs)
        debugModeQ.triggered[bool].connect(self._saveDebugPrefs)

        self.config_BTN.showMenu()

    def specConstrainOptions (self, pos):
        """Method that creates the popupmenu"""
        menu = QtWidgets.QMenu(self.specularConstrain_BTN)
        notFixedQ = menu.addAction("Not fixed specular (no rotation)")
        menu.popup(self.specularConstrain_BTN.mapToGlobal(pos))

        notFixedQ.triggered.connect(partial(tools.specularConstrain, False))

    def isolateOptions (self, pos):
        """Method that creates the popupmenu"""
        menu = QtWidgets.QMenu(self.simpleIsolate_BTN)
        resetVisSnapshotQ = menu.addAction("Reset visibility snapshot for this tool")
        menu.popup(self.simpleIsolate_BTN.mapToGlobal(pos))

        resetVisSnapshotQ.triggered.connect(partial(tools.lightsVisibilitySnapshot))
    
    def duplicateLightOptions (self, pos):
        """Method that creates the popupmenu"""
        menu = QtWidgets.QMenu(self.duplicateLight_BTN)
        duplicateWithInputsQ = menu.addAction("Duplicate with inputs")
        duplicateWithAllQ = menu.addAction("Duplicate with inputs and nodes")
        menu.popup(self.duplicateLight_BTN.mapToGlobal(pos))

        duplicateWithInputsQ.triggered.connect(partial(self._duplicateLight, True))
        duplicateWithAllQ.triggered.connect(partial(self._duplicateLight, True, True))

    def lightAttrsSnapshotOptions (self, pos, btn):
        """Method that creates the popupmenu"""
        menu = QtWidgets.QMenu(btn)
        menu.setStyleSheet("background-color: grey")
        clearSnapshotQ = menu.addAction("Clear snapshot")
        clearAllSnapshotQ = menu.addAction("Clear all snapshots")
        menu.popup(btn.mapToGlobal(pos))

        clearSnapshotQ.triggered.connect(partial(self._clearAttrsSnapshotOpt, btn))
        clearAllSnapshotQ.triggered.connect(self._clearAllSnapshotsOpt)
    
    def _lightAttrsSnapshotOpt(self, btn):
        if not btn.snap:
            btn.snap = tools.lightsAttrsSnapshot()
            btn.is_active = False
        else:
            tools.loadLightsAttrsSnapshot(btn.snap)
            btn.is_active = True
            for each in self.visSnapBtns:
                if each is not btn:
                    each.is_active = False

    def _clearAttrsSnapshotOpt(self, btn):
        btn.snap.clear()
        btn.is_active = False
    
    def _clearAllSnapshotsOpt(self):
        msgBox = QtWidgets.QMessageBox()
        result = msgBox.question(self, "Warning!",
                 "Are you sure you want to clear all attribute snapshots?")
        if result == msgBox.StandardButton.Yes:
            for btn in self.visSnapBtns:
                self._clearAttrsSnapshotOpt(btn)


# --------------------------------------------------------
#  Main
# --------------------------------------------------------
def load():
    for qt in QtWidgets.QApplication.topLevelWidgets():
        try:
            qtname = qt.objectName()
            if qtname in ['miniTools_MW']:
                qt.close()
                break
        except:
            pass
    tools.resetGlobals()
    miniTools = MiniTools_GUI()
    miniTools.show()


if __name__ == '__main__' or 'eclipsePython' in __name__:
    load()