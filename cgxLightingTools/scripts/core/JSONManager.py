# -*- coding: utf-8 -*-
'''
Library to parse and read JSON files.

Created on Mar 28, 2016

@author: Chris Granados - Xian chris.granados@xiancg.com http://www.chrisgranados.com/
'''
##--------------------------------------------------------------------------------------------
##imports
##--------------------------------------------------------------------------------------------
import json, os
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
##Class: JSON Manager (Reads and writes json files using TreeNode as interface)
##--------------------------------------------------------------------------------------------
class JSONManager():
    ##--------------------------------------------------------------------------------------------
    ##Constructor
    ##--------------------------------------------------------------------------------------------
    def __init__(self, _fileName = None, _parentUI=None):
        '''
        Reads and writes json files conforming to a concrete predefined structure template (all dicts, shared property naming).
        :param _parentUI: QWidget where an instance of this object is being used.
        :type _parentUI: PySide.QWidget
        :param _fileName: Absolute path to a json file.
        :type _fileName: string
        
        Simple json example:
        {
            "uvAA": true, 
            "uvEntireRange": false, 
            "uvMod": true, 
            "uvRange": true, 
            "uvSize": "4096"
        }
        
        Tree json example:
        {
            "BaseFolder_3D":
            {
            "concreteFolderType":"productionStep_rootfolder",
            "abstractFolderType":"rootFolder",
            "folderFunction":"grouping",
            "placeholder":true,
            "ANIMATION":
                {
                "concreteFolderType":"pipelineStep_mainfolder",
                "abstractFolderType":"mainFolder",
                "folderFunction":"grouping",
                "placeholder":false,
                "SEQ_##":
                    {
                    "abstractFolderType":"subfolder",
                    "concreteFolderType":"sequence_subfolder",
                    "folderFunction":"grouping",
                    "placeholder":true,
                    "s_###":
                        {
                        "abstractFolderType":"subfolder",
                        "concreteFolderType":"shot_subfolder",
                        "folderFunction":"grouping",
                        "placeholder":true,
                        "Audio":{"abstractFolderType":"branchfolder","concreteFolderType":"wip_branchfolder","folderFunction":"work_content","placeholder":false},
                        "Camera":{"abstractFolderType":"leaffolder","concreteFolderType":"published_leaffolder", "folderFunction":"published_content","placeholder":false},
                        "Kickoff":{"abstractFolderType":"branchfolder","concreteFolderType":"wip_branchfolder", "folderFunction":"work_content","placeholder":false},
                        "Plate":{"abstractFolderType":"branchfolder","concreteFolderType":"wip_branchfolder", "folderFunction":"work_content","placeholder":false},
                        "Previews":{"abstractFolderType":"branchfolder","concreteFolderType":"wip_branchfolder", "folderFunction":"work_content","placeholder":false},
                        "Published":{"abstractFolderType":"leaffolder","concreteFolderType":"published_leaffolder", "folderFunction":"published_content","placeholder":false}
                        }
                    }
                }
            }
        }
        '''
        self.__parentUI = _parentUI
        if _fileName != None:
            self.__fileName = _fileName
            self.__jsonObj = self.parseJsonObj(self.__fileName)
            self.__rootNode = dvm.TreeNode(['dictRoot'],['dictRoot'])
            self.jsonToTree()
    
    ##--------------------------------------------------------------------------------------------
    ##Methods
    ##--------------------------------------------------------------------------------------------        
    def jsonToTree(self):
        '''
        Converts a json object to a hierarchical structure using TreeNode.
        :return: Root TreeNode for resulting tree.
        :rtype: TreeNode
        '''
        self.__rootNode = dvm.TreeNode(['dictRoot'],['dictRoot'])
        #Test if all values aren't dict (meaning it doesn't have children, it's pure properties)
        propertiesOnly = all(type(value) != dict for value in self.jsonObj.values())
        #If they aren't, create TreeNode with all key:value pairs
        if propertiesOnly:
            data = self.jsonObj.values()#name,properties
            self.rootNode.insertChildren(self.rootNode.childCount(), data, self.jsonObj.keys(), 1)
        else:
            #Loop through to explore children
            for key, value in self.jsonObj.iteritems():
                if type(value) == dict:
                    self.__jsonToTree_recursive(key, value, self.rootNode)
        
        return self.rootNode
        
        
    def __jsonToTree_recursive(self, name, _dict, _parentNode):
        '''
        Recursive function for self.jsonToTree().
        :param name: name for node to be created
        :type name: string
        :param _dict: Data to be writen to TreeNode
        :type _dict: dict
        :param _parentNode: Insert node under this parent.
        :type _parentNode: TreeNode
        '''
        propertiesOnly = all(type(value) != dict for value in _dict.values())
        if propertiesOnly:
            data = [name]
            keys = ['name']
            for key in sorted(_dict.keys()):
                data.append(_dict[key])
                keys.append(key)
            _parentNode.insertChildren(_parentNode.childCount(), data, keys, 1)
        else:
            #Filter properties and create node for first item
            data = [name]
            keys = ['name']
            for key in sorted(_dict.keys()):
                if type(_dict[key]) != dict:
                    data.append(_dict[key])
                    keys.append(key)
            newNode = _parentNode.insertChildren(_parentNode.childCount(), data, keys, 1)
            
            #Loop through again to explore children
            for key, value in _dict.iteritems():
                if type(value) == dict:
                    self.__jsonToTree_recursive(key, value, newNode)
    
    
    def treeToJson(self):
        '''
        Converts a TreeNode object to a hierarchical structure using a dict
        :return: Root dict for the resulting tree
        :rtype: dict
        '''
        finalDict = {}
        for child in self.rootNode.children:
            childDict = child.asDict()
            cleanDict={i:childDict[i] for i in childDict if i!='name'}
            newDict = {}
            if child.childCount() > 0:
                newDict = self.__treeToJson_recursive(child,cleanDict)
                finalDict[child.name] = newDict
            elif 'name' not in childDict.keys():
                finalDict = childDict
            else:
                finalDict[child.name] = cleanDict

        return finalDict

    
    def __treeToJson_recursive(self, _node, _dict):
        '''
        Recursive function for self.treeToJson().
        :param _node: TreeNode to be explored
        :type _node: TreeNode
        :param _dict: Dict on which children will be added
        :type _dict: dict
        :return: dict for the resulting tree
        :rtype: dict
        '''
        for child in _node.children:
            childDict = child.asDict()
            cleanDict = {i:childDict[i] for i in childDict if i!='name'}
            if child.childCount() > 0:
                newDict = self.__treeToJson_recursive(child,cleanDict)
                _dict[child.name] = newDict
            else:
                _dict[child.name] = cleanDict
        return _dict
    

    def getName(self, _findName, _exactMatch):
        '''
        Retrieves nodes whose name matches with given parameters.
        :param _findName: Look for this name.
        :type _findName: string
        :param _exactMatch: Instead of looking only for the exact given string, look for this as well: _findName.lower(), _findName.upper(), _findName.swapcase(), _findName.capitalize()
        :type _exactMatch: boolean
        :return: List of matching TreeNode
        :rtype: list of TreeNode
        '''
        matchList = [_findName]
        if not _exactMatch:
            matchList += self.__matchingVariables(matchList)
        finalList = []
        for child in self.rootNode.children:
            if child.name in matchList:
                finalList.append(child)
            if child.childCount() > 0:
                finalList += self.__getName_recursive(child, matchList)
        
        return finalList
    
    
    def __getName_recursive(self, _node, _matchList):
        '''
        Recursive function for self.getName().
        :param _node: Explore this TreeNode recursively
        :type _node: TreeNode
        :param _matchList: Look for this variations
        :type _matchList: strings list
        :return: List of matching TreeNode
        :rtype: list of TreeNode
        '''
        tempList = []
        for child in _node.children:
            if child.name in _matchList:
                tempList.append(child)
            if child.childCount() > 0:
                tempList += self.__getName_recursive(child, _matchList)
        
        return tempList
    
    
    def getProperty(self, _findProperty, _exactMatch):
        '''
        Retrieves nodes with this property.
        :param _findProperty: Look for this property.
        :type _findProperty: string
        :param _exactMatch: Instead of looking only for the exact given string, look for this as well: _findProperty.lower(), _findProperty.upper(), _findProperty.swapcase(), _findProperty.capitalize()
        :type _exactMatch: boolean
        :return: List of matching TreeNode
        :rtype: list of TreeNode
        '''
        matchList = [_findProperty]
        if not _exactMatch:
            matchList += self.__matchingVariables(matchList)
        finalList = []
        for child in self.rootNode.children:
            if bool(set(child.headers) & set(matchList)):
                finalList.append(child)
            if child.childCount() > 0:
                finalList += self.__getProperty_recursive(child, matchList)
        
        return finalList
    
    
    def __getProperty_recursive(self, _node, _matchList):
        '''
        Recursive function for self.getProperty().
        :param _node: Explore this TreeNode recursively
        :type _node: TreeNode
        :param _matchList: Look for this variations
        :type _matchList: strings list
        :return: List of matching TreeNode
        :rtype: list of TreeNode
        '''
        tempList = []
        for child in _node.children:
            if bool(set(child.headers) & set(_matchList)):
                tempList.append(child)
            if child.childCount() > 0:
                tempList += self.__getProperty_recursive(child, _matchList)

        return tempList
    
    
    def getPropertiesAndValues(self, _dict):
        '''
        Retrieves nodes with this property:value pairs.
        :param _dict: Look for nodes with this exact properties and values. {"property":"value"}
        :type _dict: dict
        :return: List of matching TreeNode
        :rtype: list of TreeNode
        '''
        finalList = []
        for child in self.rootNode.children:
            if bool( set(child.headers) & set(_dict.keys()) ):#Properties names match
                filteredNodeDict = {}
                nodeAsDict = child.asDict()
                for each in _dict.keys():
                    if each in nodeAsDict.keys():
                        filteredNodeDict[each] = nodeAsDict[each]
                if filteredNodeDict == _dict:#Properties values match
                    finalList.append(child)
            if child.childCount() > 0:
                finalList += self.__getPropertiesAndValues_recursive(child, _dict)
        return finalList
    
    
    def __getPropertiesAndValues_recursive(self, node, _dict):
        '''
        Recursive function for self.getPropertiesAndValues().
        :param _dict: Look for nodes with this exact properties and values. {"property":"value"}
        :type _dict: dict
        :param _node: Explore this TreeNode recursively
        :type _node: TreeNode
        :return: List of matching TreeNode
        :rtype: list of TreeNode
        '''
        tempList = []
        for child in node.children:
            if bool( set(child.headers) & set(_dict.keys()) ):#Properties names match
                filteredNodeDict = {}
                nodeAsDict = child.asDict()
                for each in _dict.keys():
                    if each in nodeAsDict.keys():
                        filteredNodeDict[each] = nodeAsDict[each]
                if filteredNodeDict == _dict:#Properties values match
                    tempList.append(child)
            if child.childCount() > 0:
                tempList += self.__getPropertiesAndValues_recursive(child, _dict)
        return tempList
    
    
    def getValueByProperty(self, _property, _exactMatch):
        '''
        :param _property: Look for this property value.
        :type _property: string
        :param _exactMatch: Instead of looking only for the exact given string, look for this as well: _findProperty.lower(), _findProperty.upper(), _findProperty.swapcase(), _findProperty.capitalize()
        :type _exactMatch: boolean
        :return: Property value
        :rtype: object
        '''
        matchList = [_property]
        if not _exactMatch:
            matchList += self.__matchingVariables(matchList)
        propertiesOnly = all(type(value) != dict for value in self.jsonObj.values())
        if propertiesOnly:
            if _property in self.jsonObj.keys():
                return self.jsonObj[_property]
            else:
                return None
        else:
            return None
        
    
    def __matchingVariables(self, _varsList):
        '''
        Returns a list with the given strings converted to different variations.
        :param _varsList: list of strings to be processed.
        :type _varsList: strings list
        :return: List with string variations.
        :rtype: strings list
        '''
        allVars = []
        for each in _varsList:
            if type(each) == str:
                allVars += [each.lower(), each.upper(), each.swapcase(), each.capitalize()]
            else:
                allVars += [each]
        return allVars
    
    
    def parseJsonObj(self, _fileName):
        '''
        Parse json file and convert it to Python object. Accepts json starting with a dict only. --> YES:{}, NO:[]
        :param _fileName: Absolute path to a json file.
        :type _fileName: string
        :return: Python object (dict) with all data from json file. None if passed json doesn't start as dict --> YES:{}, NO:[]
        :rtype: object
        '''
        self.__fileName = _fileName
        fIn = open(self.__fileName, 'r')
        jsonObj = json.load(fIn)
        fIn.close()
        
        if type(jsonObj) == dict:
            self.jsonObj = jsonObj
            self.jsonToTree()
            return self.jsonObj
        else:
            return None
    

    def writeJson(self, _data, _filename):
        '''
        Writes a json file with the given _data to the given path
        :param _fileName: Absolute path for the json file to be created. 'C:/tree.json'
        :type _fileName: string
        :return: True if write operation succeeded
        :rtype: boolean
        '''
        fOut = open(_filename, 'w')
        json.dump(_data, fOut, indent = 4)
        fOut.close()
        if os.path.exists(_filename):
            return True
        else:
            return False
   
    
    ##--------------------------------------------------------------------------------------------
    ##Properties
    ##--------------------------------------------------------------------------------------------
    @property
    def rootNode(self):
        return self.__rootNode
    @rootNode.setter
    def rootNode(self, r):
        self.__rootNode = r
        
    @property
    def jsonObj(self):
        return self.__jsonObj
    @jsonObj.setter
    def jsonObj(self, f):
        self.__jsonObj = f
    
    @property
    def fileName(self):
        return self.__fileName
    


##--------------------------------------------------------------------------------------------
##Main
##-------------------------------------------------------------------------------------------- 
def main():
    pass


if __name__=="__main__":
    main()