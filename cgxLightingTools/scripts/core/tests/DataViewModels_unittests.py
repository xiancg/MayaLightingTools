# -*- coding: utf-8 -*-
'''
unittests for DataViewModels library.

Created on Mar 22, 2016

@author: Chris Granados - Xian chris.granados@xiancg.com http://www.chrisgranados.com/
'''
##--------------------------------------------------------------------------------------------
##imports
##--------------------------------------------------------------------------------------------
from cgx.gui.Qt import QtCore
import unittest
import cgx.gui.DataViewModels as dvm


##--------------------------------------------------------------------------------------------
##Metadata
##--------------------------------------------------------------------------------------------
__author__ = "Chris Granados"
__copyright__ = "Copyright 2016, Chris Granados"
__credits__ = ["Chris Granados"]
__version__ = "1.0.0"
__email__ = "chris.granados@xiancg.com"


##--------------------------------------------------------------------------------------------
##Class: Objecs list Model tests
##--------------------------------------------------------------------------------------------
class TestObjectsListModel(unittest.TestCase):
	##--------------------------------------------------------------------------------------------
	##Setup/Teardown
	##--------------------------------------------------------------------------------------------
	def setUp(self):
		self.dataList = ["SEQ_01","SEQ_02","SEQ_03","SEQ_04"]
		self.listModel = dvm.ObjectsListModel(self.dataList)

	def tearDown(self):
		pass


	##--------------------------------------------------------------------------------------------
	##Methods
	##--------------------------------------------------------------------------------------------
	def test_rowCount(self):
		self.assertEqual(self.listModel.rowCount(),len(self.dataList))
		
	def test_rowCount_emptyInitialization(self):
		testModel = dvm.ObjectsListModel()
		self.assertEqual(testModel.rowCount(),0)
		
	def test_data_notValid(self):
		value = self.listModel.data(QtCore.QModelIndex())
		self.assertIsNone(value)
	
	def test_data_outOfRangeRow(self):
		index = self.listModel.createIndex(5,0)
		value = self.listModel.data(index)
		self.assertIsNone(value)
		
	def test_data_displayRole(self):
		index = self.listModel.index(3,0)
		value = self.listModel.data(index, role=QtCore.Qt.DisplayRole)
		self.assertEqual(value,"SEQ_04")
		
	def test_insertRows_passingValidData(self):
		rows = ["SEQ_05","SEQ_06"]
		returned = self.listModel.insertRows(1,rows)
		self.assertEqual(self.listModel.dataList,["SEQ_01","SEQ_05","SEQ_06","SEQ_02","SEQ_03","SEQ_04"])
		self.assertTrue(returned)
	
	def test_insertRows_passingEmptyList(self):
		rows = []
		returned = self.listModel.insertRows(1,rows)
		self.assertFalse(returned)
		
	def test_removeRows_passingValidData(self):
		rows = [0,2]
		returned = self.listModel.removeRows(rows,len(rows))
		self.assertTrue(returned)
		self.assertEqual(self.listModel.dataList, ["SEQ_02","SEQ_04"])
	
	def test_removeRows_passingNotExistingIndexes(self):
		rows = [0,6]
		returned = self.listModel.removeRows(rows,len(rows))
		self.assertFalse(returned)
		self.assertEquals(self.listModel.dataList,self.dataList)
		
	def test_removeRows_indexListAndCountDifferInSize(self):
		rows = [0,2]
		returned = self.listModel.removeRows(rows,3)
		self.assertFalse(returned)
		
	def test_index_existingItemIndex(self):
		returned = self.listModel.index(1)
		self.assertIsInstance(returned,QtCore.QModelIndex)


##--------------------------------------------------------------------------------------------
##Class: Data Table Model tests
##--------------------------------------------------------------------------------------------
class TestDataTableModel(unittest.TestCase):
	##--------------------------------------------------------------------------------------------
	##Setup/Teardown
	##--------------------------------------------------------------------------------------------
	def setUp(self):
		self.dataList = [["LGT_sirena_01_Rim", 15.8, False, "areaLight",None],["LGT_pulpo_01_Key", 23.4, False, "spotLight",2.5]]
		self.headers = ["LightName","aiExposure","visibility","lightType","radius"]
		self.tableModel = dvm.DataTableModel(self.dataList, self.headers)

	def tearDown(self):
		pass


	##--------------------------------------------------------------------------------------------
	##Methods
	##--------------------------------------------------------------------------------------------
	def test_rowCount_emptyDataList(self):
		testdataList = []
		testHeaders = ["LightName","aiExposure","visibility","lightType","radius"]
		testModel = dvm.DataTableModel(testdataList, testHeaders)
		self.assertEqual(testModel.rowCount(),0)
	
	def test_rowCount_emptyFirstRow(self):
		testdataList = [[]]
		testHeaders = ["LightName","aiExposure","visibility","lightType","radius"]
		testModel = dvm.DataTableModel(testdataList, testHeaders)
		self.assertEqual(testModel.rowCount(),0)
	
	def test_rowCount_singleRow(self):
		testdataList = [["LGT_sirena_01_Rim", 15.8, False, "areaLight",None]]
		testHeaders = ["LightName","aiExposure","visibility","lightType","radius"]
		testModel = dvm.DataTableModel(testdataList, testHeaders)
		self.assertEqual(testModel.rowCount(),len(testdataList))
	
	def test_rowCount_multipleRows(self):
		self.assertEqual(self.tableModel.rowCount(),len(self.dataList))
		
	def test_columnCount(self):
		self.assertEqual(self.tableModel.columnCount(), len(self.headers))
		
	def test_data_invalidIndex(self):
		value = self.tableModel.data(QtCore.QModelIndex(),QtCore.Qt.DisplayRole)
		self.assertIsNone(value)
	
	def test_data_rowOutOfRange(self):
		index = self.tableModel.createIndex(5,0)
		value = self.tableModel.data(index,QtCore.Qt.DisplayRole)
		self.assertIsNone(value)
	
	def test_data_columnOutOfRange(self):
		index = self.tableModel.createIndex(0,7)
		value = self.tableModel.data(index,QtCore.Qt.DisplayRole)
		self.assertIsNone(value)
	
	def test_data_roles(self):
		index = self.tableModel.createIndex(0,0)
		value = self.tableModel.data(index,QtCore.Qt.DisplayRole)
		self.assertEqual(value,self.dataList[0][0])
	
	def test_data_notImplementedRole(self):
		index = self.tableModel.createIndex(0,0)
		value = self.tableModel.data(index,QtCore.Qt.WhatsThisRole)
		self.assertIsNone(value)
		
	def test_headerData_sectionOutOfRange(self):
		returned = self.tableModel.headerData(7,QtCore.Qt.Horizontal,QtCore.Qt.DisplayRole)
		self.assertIsNone(returned)
	
	def test_headerData_commonParams(self):
		returned = self.tableModel.headerData(3,QtCore.Qt.Horizontal,QtCore.Qt.DisplayRole)
		self.assertEqual(returned, "lightType")
	
	def test_setData_invalidIndex(self):
		value = self.tableModel.setData(QtCore.QModelIndex(),"thisValue",QtCore.Qt.EditRole)
		self.assertFalse(value)
	
	def test_setData_noneValue(self):
		value = self.tableModel.setData(QtCore.QModelIndex(),None,QtCore.Qt.EditRole)
		self.assertFalse(value)
	
	def test_setData_commonParams(self):
		index = self.tableModel.createIndex(0,1)
		value = self.tableModel.setData(index,"LGT_sirena_01_Custom",QtCore.Qt.EditRole)
		self.assertTrue(value)
		self.assertEqual(self.tableModel.dataList[0][1],"LGT_sirena_01_Custom")
		
	def test_insertRows_insertManyRows(self):
		rowA = ["LGT_medusa_03_Kick", 12.3, True, "spotLight",1]
		rowB = ["LGT_medusa_01_Key", 18, True, "spotLight",5]
		returned = self.tableModel.insertRows(self.tableModel.rowCount(),2,[rowA,rowB])
		self.assertTrue(returned)
	
	def test_insertRows_insertSingleRow(self):
		rowA = ["LGT_medusa_03_Kick", 12.3, True, "spotLight",1]
		returned = self.tableModel.insertRows(self.tableModel.rowCount(),1,rowA)
		self.assertTrue(returned)
		
	def test_insertRows_wrongItemsNumberInRow(self):
		rowA = ["LGT_medusa_03_Kick", 12.3, True, "spotLight"]
		returned = self.tableModel.insertRows(self.tableModel.rowCount(),1,rowA)
		self.assertFalse(returned)
		
	def test_insertColumn_appendColumns(self):
		columns = ["aiTemperature","aiSamples"]
		returned = self.tableModel.insertColumns(self.tableModel.columnCount(),columns)
		self.assertTrue(returned)
		self.assertEqual(self.tableModel.headers,['LightName', 'aiExposure', 'visibility', 'lightType', 'radius','aiTemperature','aiSamples'])
		
	def test_removeRows_usingIntList(self):
		returned = self.tableModel.removeRows([0],1)
		self.assertTrue(returned)
	
	def test_removeRows_usingQModelIndex(self):
		index = self.tableModel.createIndex(0,0)
		returned = self.tableModel.removeRows([index],1)
		self.assertTrue(returned)
		
	def test_removeColumns_usingIntList(self):
		returned = self.tableModel.removeColumns([0],1)
		self.assertTrue(returned)
		self.assertEqual(self.tableModel.headers,['aiExposure', 'visibility', 'lightType', 'radius'])
	
	def test_removeColumns_usingQModelIndex(self):
		indexA = self.tableModel.createIndex(0,1)
		indexB = self.tableModel.createIndex(0,3)
		returned = self.tableModel.removeColumns([indexA,indexB],2)
		self.assertTrue(returned)
		self.assertEqual(self.tableModel.headers,['LightName', 'visibility', 'radius'])
		
	def test_index_existingItemIndex(self):
		returned = self.tableModel.index(0,3)
		self.assertIsInstance(returned,QtCore.QModelIndex)


##--------------------------------------------------------------------------------------------
##Class: Tree Node
##--------------------------------------------------------------------------------------------
class TestTreeNode(unittest.TestCase):
	##--------------------------------------------------------------------------------------------
	##Setup/Teardown
	##--------------------------------------------------------------------------------------------
	def setUp(self):
		self.rootNode = dvm.TreeNode(["root","geoName","instanceName"],["root","geoName","instanceName"])
		
	def tearDown(self):
		pass


	##--------------------------------------------------------------------------------------------
	##Methods
	##--------------------------------------------------------------------------------------------
	def test_insertChildren_passingSingleChild(self):
		childNodeA = self.rootNode.insertChildren(self.rootNode.childCount(),["C_geo_01_MSH","pSphere1","ChildA_C_geo_01_MSH_bkd"],self.rootNode.headers)
		self.assertEqual(self.rootNode.child(0),childNodeA)
		
	def test_insertChildren_passingMultipleChildren(self):
		childNodeA = self.rootNode.insertChildren(self.rootNode.childCount(),["C_geo_01_MSH","pSphere1","ChildA_C_geo_01_MSH_bkd"],self.rootNode.headers)
		childNodeB = self.rootNode.insertChildren(self.rootNode.childCount(),["C_geo_02_MSH","pCube1","ChildA_C_geo_02_MSH_bkd"],self.rootNode.headers)
		self.assertEqual(self.rootNode.children,[childNodeA,childNodeB])
		
	def test_insertChildren_deepChild(self):
		childNodeA = self.rootNode.insertChildren(self.rootNode.childCount(),["C_geo_01_MSH","pSphere1","ChildA_C_geo_01_MSH_bkd"],self.rootNode.headers)
		self.rootNode.insertChildren(self.rootNode.childCount(),["C_geo_02_MSH","pCube1","ChildA_C_geo_02_MSH_bkd"],self.rootNode.headers)
		deepChild = childNodeA.insertChildren(childNodeA.childCount(),["C_geo_03_MSH","pCone1",None],self.rootNode.headers)
		self.assertEqual(self.rootNode.child(0).child(0),deepChild)

	def test_child_outOfRangeRow(self):
		returned = self.rootNode.child(3)
		self.assertIsNone(returned)
		
	def test_child_validRow(self):
		self.rootNode.insertChildren(self.rootNode.childCount(),["C_geo_01_MSH","pSphere1","ChildA_C_geo_01_MSH_bkd"],self.rootNode.headers)
		childNodeB = self.rootNode.insertChildren(self.rootNode.childCount(),["C_geo_02_MSH","pCube1","ChildA_C_geo_02_MSH_bkd"],self.rootNode.headers)
		returned = self.rootNode.child(1)
		self.assertEqual(returned,childNodeB)
		
	def test_childNumber_childrenNode(self):
		self.rootNode.insertChildren(self.rootNode.childCount(),["C_geo_01_MSH","pSphere1","ChildA_C_geo_01_MSH_bkd"],self.rootNode.headers)
		childNode = self.rootNode.insertChildren(self.rootNode.childCount(),["C_geo_02_MSH","pCube1","ChildA_C_geo_02_MSH_bkd"],self.rootNode.headers)
		returned = childNode.childNumber()
		self.assertEqual(1,returned)
	
	def test_childNumber_rootNode(self):
		returned = self.rootNode.childNumber()
		self.assertEqual(0,returned)
	
	def test_insertColumns_fromRoot(self):
		returned = self.rootNode.insertColumns(self.rootNode.columnCount(),["newColummA","newColummB"])
		self.assertTrue(returned)
		
	def test_removeChildren(self):
		childNodeA = self.rootNode.insertChildren(self.rootNode.childCount(),["C_geo_01_MSH","pSphere1","ChildA_C_geo_01_MSH_bkd"],self.rootNode.headers)
		self.rootNode.insertChildren(self.rootNode.childCount(),["C_geo_02_MSH","pCube1","ChildA_C_geo_02_MSH_bkd"],self.rootNode.headers)
		self.rootNode.insertChildren(self.rootNode.childCount(),["C_geo_03_MSH","pCube2","ChildA_C_geo_03_MSH_bkd"],self.rootNode.headers)
		childNodeA.insertChildren(childNodeA.childCount(),["C_geo_04_MSH","pCone1",None],self.rootNode.headers)
		returned = self.rootNode.removeChildren([0,1])
		self.assertTrue(returned)
		
	def test_removeColumns_deleteFromChildren(self):
		childNodeA = self.rootNode.insertChildren(self.rootNode.childCount(),["C_geo_01_MSH","pSphere1","ChildA_C_geo_01_MSH_bkd"],self.rootNode.headers)
		self.rootNode.insertChildren(self.rootNode.childCount(),["C_geo_02_MSH","pCube1","ChildA_C_geo_02_MSH_bkd"],self.rootNode.headers)
		self.rootNode.insertChildren(self.rootNode.childCount(),["C_geo_03_MSH","pCube2","ChildA_C_geo_03_MSH_bkd"],self.rootNode.headers)
		childNodeA.insertChildren(childNodeA.childCount(),["C_geo_04_MSH","pCone1",None],self.rootNode.headers)
		returned = childNodeA.removeColumns([0,1])
		self.assertFalse(returned)
	
	def test_removeColumns_deleteFromRoot(self):
		childNodeA = self.rootNode.insertChildren(self.rootNode.childCount(),["C_geo_01_MSH","pSphere1","ChildA_C_geo_01_MSH_bkd"],self.rootNode.headers)
		self.rootNode.insertChildren(self.rootNode.childCount(),["C_geo_02_MSH","pCube1","ChildA_C_geo_02_MSH_bkd"],self.rootNode.headers)
		self.rootNode.insertChildren(self.rootNode.childCount(),["C_geo_03_MSH","pCube2","ChildA_C_geo_03_MSH_bkd"],self.rootNode.headers)
		childNodeA.insertChildren(childNodeA.childCount(),["C_geo_04_MSH","pCone1",None],self.rootNode.headers)
		returned = self.rootNode.removeColumns([0,1])
		self.assertTrue(returned)
	
	def test_log(self):
		pass
		'''
		childNodeA = self.rootNode.insertChildren(self.rootNode.childCount(),["C_geo_01_MSH","pSphere1","ChildA_C_geo_01_MSH_bkd"],self.rootNode.headers)
		self.rootNode.insertChildren(self.rootNode.childCount(),["C_geo_02_MSH","pCube1","ChildA_C_geo_02_MSH_bkd"],self.rootNode.headers)
		self.rootNode.insertChildren(self.rootNode.childCount(),["C_geo_03_MSH","pCube2","ChildA_C_geo_03_MSH_bkd"],self.rootNode.headers)
		childNodeA.insertChildren(childNodeA.childCount(),["C_geo_04_MSH","pCone1",None],self.rootNode.headers)
		print self.rootNode
		'''
		

##--------------------------------------------------------------------------------------------
##Class: Data Tree Model tests
##--------------------------------------------------------------------------------------------
class TestDataTreeModel(unittest.TestCase):
	##--------------------------------------------------------------------------------------------
	##Setup/Teardown
	##--------------------------------------------------------------------------------------------
	def setUp(self):
		self.headers = ["root","geoName","instanceName"]
		self.rootNode = dvm.TreeNode(["root","geoName","instanceName"],["root","geoName","instanceName"])
		self.childNodeA = self.rootNode.insertChildren(self.rootNode.childCount(),["C_geo_01_MSH","pSphere1","ChildA_C_geo_01_MSH_bkd"],self.rootNode.headers)
		self.childNodeB = self.rootNode.insertChildren(self.rootNode.childCount(),["C_geo_02_MSH","pCube1","ChildA_C_geo_02_MSH_bkd"],self.rootNode.headers)
		self.deepChild = self.childNodeA.insertChildren(self.childNodeA.childCount(),["C_geo_03_MSH","pCone1",None],self.rootNode.headers)
		self.treeModel = dvm.DataTreeModel(self.rootNode,["root","geoName","instanceName"])

	def tearDown(self):
		pass


	##--------------------------------------------------------------------------------------------
	##Methods
	##--------------------------------------------------------------------------------------------
	def test_rowCount_passingRoot(self):
		
		returned = self.treeModel.rowCount(self.treeModel.indexFromNode(self.rootNode))
		self.assertEqual(returned,2)
		
	def test_rowCount_passingChild(self):
		returned = self.treeModel.rowCount(self.treeModel.indexFromNode(self.childNodeA))
		self.assertEqual(returned,1)
	
	def test_data_requestIndex(self):
		returned = self.treeModel.data(self.treeModel.indexFromNode(self.childNodeA))
		self.assertEqual(returned,"C_geo_01_MSH")
		
	def test_setData_editChildData(self):
		returned = self.treeModel.setData((self.treeModel.indexFromNode(self.childNodeA,1)), "pSphere152")
		self.assertEqual(self.childNodeA.data, ["C_geo_01_MSH","pSphere152","ChildA_C_geo_01_MSH_bkd"])
		self.assertTrue(returned)
		
	def test_getNode(self):
		returned = self.treeModel.getNode(self.treeModel.indexFromNode(self.childNodeA,1))
		self.assertEqual(returned,self.childNodeA)
		
	def test_headerData_sectionOutOfRange(self):
		returned = self.treeModel.headerData(7,QtCore.Qt.Horizontal,QtCore.Qt.DisplayRole)
		self.assertIsNone(returned)
	
	def test_headerData_commonParams(self):
		returned = self.treeModel.headerData(2,QtCore.Qt.Horizontal)
		self.assertEqual(returned, "instanceName")
		
	def test_index_existingItemIndex(self):
		index = self.treeModel.indexFromNode(self.childNodeA,1)
		returned = self.treeModel.index(0,0,index)
		self.assertIsInstance(returned,QtCore.QModelIndex)
		self.assertEqual(self.treeModel.getNode(returned),self.childNodeA.children[0])
	
	def test_insertColumns_recursiveAddColumns(self):
		columns = ["aiTemperature","aiSamples"]
		returned = self.treeModel.insertColumns(self.treeModel.columnCount(),columns)
		self.assertTrue(returned)
		self.assertEqual(self.treeModel.headers,["root","geoName","instanceName","aiTemperature","aiSamples"])
		self.assertEqual(self.treeModel.columnCount(),self.childNodeA.columnCount())
	
	def test_insertRows_passingSingleRow(self):
		rows = ["C_geo_07_MSH","pSphere325","ChildA_C_geo_07_MSH_bkd"]
		returned = self.treeModel.insertRows(self.childNodeA.childCount(),len(rows),rows,self.treeModel.indexFromNode(self.childNodeA))
		self.assertTrue(returned)
		self.assertEqual(self.childNodeA.children[1].data,rows)
		
	def test_insertRows_passingMultipleRows(self):
		rows = [["C_geo_07_MSH","pSphere325","ChildA_C_geo_07_MSH_bkd"],["C_geo_11_MSH","pCube123","ChildA_C_geo_11_MSH_bkd"]]
		returned = self.treeModel.insertRows(self.childNodeA.childCount(),len(rows),rows,self.treeModel.indexFromNode(self.childNodeA))
		self.assertTrue(returned)
		self.assertEqual(self.childNodeA.children[1].data,rows[0])
		
	def test_parent_commonParams(self):
		returned = self.treeModel.parent(self.treeModel.indexFromNode(self.childNodeA))
		self.assertIsInstance(returned, QtCore.QModelIndex)
		
	def test_indexFromNode(self):
		returned = self.treeModel.indexFromNode(self.childNodeA,1)
		self.assertIsInstance(returned, QtCore.QModelIndex)
		
	def test_removeColumns(self):
		columns = [1,2]
		returned = self.treeModel.removeColumns(columns, len(columns))
		self.assertTrue(returned)
		self.assertEqual(self.treeModel.headers, ["root"])
		self.assertEqual(self.treeModel.columnCount(),self.childNodeA.columnCount())

	def test_removeRows(self):
		indexList = [self.treeModel.indexFromNode(self.deepChild),self.treeModel.indexFromNode(self.childNodeB)]
		returned = self.treeModel.removeRows(indexList)
		self.assertTrue(returned)

##--------------------------------------------------------------------------------------------
##Main
##-------------------------------------------------------------------------------------------- 
if __name__ == '__main__':
	unittest.main()