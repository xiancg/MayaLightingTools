# -*- coding: utf-8 -*-
'''
Test the use of DataViewModels with PySide.

Created on Mar 22, 2016

@author: Chris Granados - Xian chris.granados@xiancg.com http://www.chrisgranados.com/
'''


##--------------------------------------------------------------------------------------------
##imports
##--------------------------------------------------------------------------------------------
from cgx.gui.Qt import QtWidgets, QtCore
import cgx.gui.DataViewModels as dvm
import sys, os
from cgx.core.JSONManager import JSONManager


##--------------------------------------------------------------------------------------------
##Metadata
##--------------------------------------------------------------------------------------------
__author__ = "Chris Granados"
__copyright__ = "Copyright 2016, Chris Granados"
__credits__ = ["Chris Granados"]
__version__ = "1.0.0"
__email__ = "chris.granados@xiancg.com"


##--------------------------------------------------------------------------------------------
##Main
##-------------------------------------------------------------------------------------------- 
def main():
    app = QtWidgets.QApplication(sys.argv)
    
    #LIST VIEW
    '''
    dataList = ["SEQ_01","SEQ_02","SEQ_03","SEQ_04"]
    listModel = dvm.ObjectsListModel(dataList)
    listView = QtWidgets.QListView()  
    listView.setModel(listModel)  
    listView.show()
    combobox = QtWidgets.QComboBox()
    combobox.setModel(listModel)
    combobox.show()
    listView2 = QtWidgets.QListView()
    listView2.show()
    listView2.setModel(listModel)
    '''
    
    #TABLE VIEW
    '''
    dataListTable = [["LGT_sirena_01_Rim", 15.8, False, "areaLight",None],["LGT_pulpo_01_Key", 23.4, False, "spotLight",2.5]]
    headersTable = ["LightName","aiExposure","visibility","lightType","radius"]
    tableView = QtWidgets.QTableView() 
    tableModel = dvm.DataTableModel(dataListTable, headersTable, tableView)
    tableView.setModel(tableModel)  
    tableView.show()
    '''
    '''
    #TREE VIEW
    treeHeaders = ["root","geoName","instanceName"]
    rootNode = dvm.TreeNode(treeHeaders, ["root","geoName","instanceName"])
    childNodeA = rootNode.insertChildren(rootNode.childCount(),["C_geo_01_MSH","pSphere1","ChildA_C_geo_01_MSH_bkd"], ["root","geoName","instanceName"])
    rootNode.insertChildren(rootNode.childCount(),["C_geo_02_MSH","pCube1","ChildA_C_geo_02_MSH_bkd"],["root","geoName","instanceName"])
    childNodeA.insertChildren(childNodeA.childCount(),["C_geo_03_MSH","pCone1",None],["root","geoName","instanceName"])
    treeView = QtWidgets.QTreeView()
    treeModel = dvm.DataTreeModel(rootNode,treeHeaders,treeView)
    treeView.setModel(treeModel)
    treeView.show()
    '''
    #TREE VIEW
    
    appRootFolder = os.path.dirname(__file__)
    lightAttrs_json = appRootFolder + "/resources/" + "LightsManager_lightAttrs.json"
    json_file = JSONManager(lightAttrs_json)
    headers=["name","display","uiControl","default","minValue","maxValue","values","lightTypes"]
    treeView = QtWidgets.QTreeView()
    treeModel = dvm.DataTreeModel(json_file.rootNode,headers,treeView)
    treeView.setModel(treeModel)
    treeView.show()
    
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()