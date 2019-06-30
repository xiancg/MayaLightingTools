# -*- coding: utf-8 -*-
'''
unitests for JSONManager

Created on Mar 28, 2016

@author: Chris Granados - Xian chris.granados@xiancg.com http://www.chrisgranados.com/
'''
##--------------------------------------------------------------------------------------------
##imports
##--------------------------------------------------------------------------------------------
import unittest, os
import cgx.core.JSONManager as reader
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
##Class: Test JSON Reader
##--------------------------------------------------------------------------------------------
class Test_JSONManager(unittest.TestCase):
    ##--------------------------------------------------------------------------------------------
    ##Setup/Teardown
    ##--------------------------------------------------------------------------------------------
    def setUp(self):
        self.appRootFolder = os.path.dirname(__file__)
        self.configCacheTools = "cgx_cacheTools_config.json"
        self.configSubstance = "substance_config.json"
        self.configFolderStructure = "gzmo_3DFullCG_structure.json"
        self.fileName = self.appRootFolder + "/resources/" + self.configFolderStructure
        self.JSONManager = reader.JSONManager(None,self.fileName)

    def tearDown(self):
        pass


    ##--------------------------------------------------------------------------------------------
    ##Methods
    ##--------------------------------------------------------------------------------------------
    def test_parseJsonObj_isDict(self):
        returned = self.JSONManager.parseJsonObj(self.fileName)
        self.assertIsInstance(returned, dict)
    #@unittest.SkipTest
    def test_getKey_exactMatchSimpleJson(self):
        fileName = self.appRootFolder + "/resources/" + self.configSubstance
        self.JSONManager.jsonObj = self.JSONManager.parseJsonObj(fileName)
        returned = self.JSONManager.jsonToTree()
        self.assertEqual(returned.children[0].data,[False, str(4096), True, True, True])
    
    def test_jsonToTree(self):
        fileName = self.appRootFolder + "/resources/" + self.configFolderStructure
        self.JSONManager.jsonObj = self.JSONManager.parseJsonObj(fileName)
        returned = self.JSONManager.jsonToTree()
        self.assertIsInstance(returned, dvm.TreeNode)
        
    def test_getName_fuzzyMatch(self):
        fileName = self.appRootFolder + "/resources/" + self.configFolderStructure
        self.JSONManager.jsonObj = self.JSONManager.parseJsonObj(fileName)
        returned = self.JSONManager.getName('Published', False)
        #for x in returned: print x
        self.assertTrue(len(returned) > 0)
        
    def test_getName_SimpleJsonShouldReturnZero(self):
        fileName = self.appRootFolder + "/resources/" + self.configSubstance
        self.JSONManager.jsonObj = self.JSONManager.parseJsonObj(fileName)
        returned = self.JSONManager.getName('uvSize', False)
        #for x in returned: print x
        self.assertTrue(len(returned) == 0)
        
    def test_getProperty_fuzzyMatchSimpleJson(self):
        fileName = self.appRootFolder + "/resources/" + self.configSubstance
        self.JSONManager.jsonObj = self.JSONManager.parseJsonObj(fileName)
        returned = self.JSONManager.getProperty('uvSize', False)
        #for x in returned: print x
        self.assertTrue(len(returned) == 1)

    def test_getProperty_fuzzyMatchTree(self):
        fileName = self.appRootFolder + "/resources/" + self.configFolderStructure
        self.JSONManager.jsonObj = self.JSONManager.parseJsonObj(fileName)
        returned = self.JSONManager.getProperty('folderFunction', False)
        #for x in returned: print x
        self.assertTrue(len(returned) == 40)
        
    def test_getPropertiesAndValues_published(self):
        fileName = self.appRootFolder + "/resources/" + self.configFolderStructure
        self.JSONManager.jsonObj = self.JSONManager.parseJsonObj(fileName)
        propertiesDict = {"concreteFolderType":"published_leaffolder","folderFunction":"published_content"}
        returned = self.JSONManager.getPropertiesAndValues(propertiesDict)
        #for x in returned: print x
        self.assertTrue(len(returned) == 10)
        
    def test_getPropertiesAndValues_placeHolderProperty(self):
        fileName = self.appRootFolder + "/resources/" + self.configFolderStructure
        self.JSONManager.jsonObj = self.JSONManager.parseJsonObj(fileName)
        propertiesDict = {"placeholder":True,"concreteFolderType":"asset_subfolder"}
        returned = self.JSONManager.getPropertiesAndValues(propertiesDict)
        #for x in returned: print x
        self.assertTrue(len(returned) == 2)

    def test_treeToJson_treeStrcutre(self):
        fileName = self.appRootFolder + "/resources/" + self.configFolderStructure
        self.JSONManager.jsonObj = self.JSONManager.parseJsonObj(fileName)
        returned= self.JSONManager.treeToJson()
        self.assertIsInstance(returned,dict)
    
    def test_treeToJson_simpleJSON(self):
        fileName = self.appRootFolder + "/resources/" + self.configSubstance
        self.JSONManager.jsonObj = self.JSONManager.parseJsonObj(fileName)
        returned = self.JSONManager.treeToJson()
        self.assertIsInstance(returned,dict)
    
    def test_writeJson_simpleJSON(self):
        fileName = self.appRootFolder + "/resources/" + self.configSubstance
        self.JSONManager.jsonObj = self.JSONManager.parseJsonObj(fileName)
        jsonDict = self.JSONManager.treeToJson()
        returned = self.JSONManager.writeJson(jsonDict, 'C:/simple.json')
        self.assertTrue(returned)
    
    def test_writeJson_treeJSON(self):
        fileName = self.appRootFolder + "/resources/" + self.configFolderStructure
        self.JSONManager.jsonObj = self.JSONManager.parseJsonObj(fileName)
        jsonDict = self.JSONManager.treeToJson()
        returned = self.JSONManager.writeJson(jsonDict, 'C:/tree.json')
        self.assertTrue(returned)
        

##--------------------------------------------------------------------------------------------
##Main
##--------------------------------------------------------------------------------------------
if __name__=="__main__":
    unittest.main()