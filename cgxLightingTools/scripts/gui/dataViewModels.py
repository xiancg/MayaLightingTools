# -*- coding: utf-8 -*-
'''
Data view models for data visualization.

Modified on Mar 22, 2016

NOTE: Remove rows for tables works by passing both a list of ints or QModelIndex, for trees by passing only a list of QModelIndex

@author: Chris Granados - Xian chris.granados@xiancg.com http://www.chrisgranados.com/
'''


# --------------------------------------------------------------------------------------------
# imports
# --------------------------------------------------------------------------------------------
from PySide2 import QtCore


# --------------------------------------------------------------------------------------------
# Metadata
# --------------------------------------------------------------------------------------------
__author__ = "Chris Granados"
__copyright__ = "Copyright 2016, Chris Granados"
__credits__ = ["Chris Granados"]
__version__ = "3.0.0"
__email__ = "chris.granados@xiancg.com"


# --------------------------------------------------------------------------------------------
# Class: Data Table Model
# --------------------------------------------------------------------------------------------
class DataTableModel(QtCore.QAbstractTableModel):
    # --------------------------------------------------------------------------------------------
    # Constructor
    # --------------------------------------------------------------------------------------------
    def __init__(self, dataList=[[]], headers=[], parent=None):
        '''
        DataTableModel for Model/View programming.
        :param dataList: List of lists of object to be displayed. Each list inside the main list is a row.
        :type list: List of lists
        :param headers: List of column names to be displayed in the table.
        :type headers: List of strings
        :param parent: QWidget that uses this model. Default=None
        :type parent: QWidget
        '''
        super(DataTableModel, self).__init__(parent)
        self.__dataList = dataList
        if dataList == None:
            self.__dataList = []

        self.__headers = headers
        if headers == None:
            self.__headers = []

    # --------------------------------------------------------------------------------------------
    # Methods
    # --------------------------------------------------------------------------------------------
    def rowCount(self, parent=QtCore.QModelIndex()):
        '''
        Rows number for the table
        :param parent: Default QModelIndex
        :type parent: QModelIndex
        :return: dataList len
        :rtype: int
        '''
        if len(self.dataList) == 1:
            if self.dataList[0] == []:
                return 0
            else:
                return len(self.dataList)
        else:
            return len(self.dataList)

    def columnCount(self, parent=QtCore.QModelIndex()):
        '''
        Columns number for the table
        :param parent: Default QModelIndex
        :type parent: QModelIndex
        :return: headers len
        :rtype: int
        '''
        return len(self.headers)

    def flags(self, index):
        '''
        Set flags for each table cell. Re-implement if different flags are needed and use conditional chains if per-cell flags are needed.
        :param index: Item to be filtered
        :type index: QModelIndex
        :return: Flags to be used
        :rtype: QtCore.Qt.Flags
        '''
        if not index.isValid():
            return QtCore.Qt.NoItemFlags
        else:
            # return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role):
        '''
        Query/Edit data for specified index, depending on role.
        :param index: Queried index
        :type index: QModelIndex
        :param role: Qt role requested for the item
        :type role: QtCore.Qt.Role
        :return: Item data to be returned or shown in the GUI. Might be None.
        :rtype: object
        '''
        row = index.row()
        column = index.column()

        if not index.isValid():
            return None
        elif row >= len(self.dataList) or row < 0:
            return None
        elif column >= len(self.headers) or column < 0:
            return None

        if role in [QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole, QtCore.Qt.EditRole]:
            value = self.dataList[row][column]
            return value
        else:
            return None

    def headerData(self, section, orientation, role):
        '''
        Names of colums.
        :param section: Queried header index
        :type section: int
        :param orientation: Horizontal by default. Re-implement if vertical is needed as well.
        :type orientation: QtCore.Qt.Orientation
        :param role: Qt role requested for the item
        :type role: QtCore.Qt.Role
        :return: Item data to be returned or shown in the GUI. Might be None.
        :rtype: object
        '''
        if orientation == QtCore.Qt.Horizontal:
            if role in [QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole, QtCore.Qt.EditRole]:
                if section > len(self.headers) - 1:
                    return None
                else:
                    value = self.headers[section]
                    return value
            else:
                return None
        else:
            return None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        '''
        Edits the data in the cells.
        :param section: Queried header index
        :type section: int
        :param orientation: Vertical or Horizontal
        :type orientation: QtCore.Qt.Orientation
        :param role: Qt role requested for the item
        :type role: QtCore.Qt.Role
        :return: If item was edited successfully return True. 
        :rtype: boolean
        '''
        row = index.row()
        column = index.column()
        if not index.isValid():
            return False
        elif row >= len(self.dataList) or row < 0:
            return False
        elif column >= len(self.headers) or column < 0:
            return False

        if role == QtCore.Qt.EditRole:
            if value != None:
                self.dataList[row][column] = value
                self.dataChanged.emit(index, index)
                return True
            else:
                return False
        else:
            return False

    def insertRows(self, position, count, data, parent=QtCore.QModelIndex()):
        '''
        Insert rows in the table.
        :param position: Inserting items from this index.
        :type position: int
        :param count: Number of rows to be added
        :type count: int
        :param data: List of values for a single row or a list of rows
        :type data: List or list of lists
        :param parent: Default QModelIndex
        :type parent: QModelIndex
        :return: True if insert was successful. False if a number of conditions are not matched.
        :rtype: boolean
        '''
        if position < 0:
            return False
        else:
            manyRows = all(isinstance(x, list) for x in data)
            if manyRows:
                rowsLen = all(len(x) == self.columnCount() for x in data)
                if rowsLen:
                    self.beginInsertRows(parent, position, position + (count - 1))
                    for row in data:
                        self.dataList.insert(position, row)
                    self.endInsertRows()
                    return True
                else:
                    return False
            else:
                if len(data) == self.columnCount():
                    self.beginInsertRows(parent, position, position + (count - 1))
                    self.dataList.insert(position, data)
                    self.endInsertRows()
                    return True
                else:
                    return False

    def insertColumns(self, position, columns, parent=QtCore.QModelIndex()):
        '''
        Insert columns in the table.
        :param position: Inserting items from this index.
        :type position: int
        :param count: Columns to be added
        :type count: list
        :param parent: Default QModelIndex
        :type parent: QModelIndex
        :return: True if insert was successful. False if a number of conditions are not matched.
        :rtype: boolean
        '''
        if position < 0:
            return False
        else:
            if type(columns) is list:
                self.beginInsertColumns(parent, position, position + len(columns) - 1)
                for i in columns[::-1]:
                    self.headers.insert(position, i)
                    for row in self.dataList:
                        row.insert(position, "Type here")
                self.endInsertColumns()
                return True
            else:
                return False

    def removeRows(self, indexList, count, parent=QtCore.QModelIndex()):
        '''
        Remove rows in the table
        :param indexList: Remove items in this list.
        :type indexList: int list or QModelIndex list
        :param count: Columns to be added
        :type count: list
        :param parent: Default QModelIndex
        :type parent: QModelIndex
        :return: True if remove was successful. False if a number of conditions are not matched.
        :rtype: boolean
        '''
        QMIndexList = all(isinstance(x, QtCore.QModelIndex) for x in indexList)
        if QMIndexList:
            intIndexList = sorted([index.row() for index in indexList])
            indexList = intIndexList

        for i in indexList:
            if i > len(self.dataList) - 1:
                return False
            elif i < 0:
                return False

        if len(indexList) != count:
            return False
        else:
            position = indexList[0]
            self.beginRemoveRows(parent, position, position + (count - 1))
            for i in sorted(indexList, reverse=True):
                del(self.dataList[i])
            self.endRemoveRows()
            return True

    def removeColumns(self, indexList, count, parent=QtCore.QModelIndex()):
        '''
        Remove columns in the table
        :param indexList: Remove items in this list.
        :type indexList: int list or QModelIndex list
        :param count: Columns to be added
        :type count: list
        :param parent: Default QModelIndex
        :type parent: QModelIndex
        :return: True if remove was successful. False if a number of conditions are not matched.
        :rtype: boolean
        '''
        QMIndexList = all(isinstance(x, QtCore.QModelIndex) for x in indexList)
        if QMIndexList:
            intIndexList = sorted([index.column() for index in indexList])
            indexList = intIndexList

        for i in indexList:
            if i > len(self.headers) - 1:
                return False
            elif i < 0:
                return False

        if len(indexList) != count:
            return False
        else:
            position = indexList[0]
            self.beginRemoveColumns(parent, position, position + (count - 1))
            for i in sorted(indexList, reverse=True):
                del(self.headers[i])
                for row in self.dataList:
                    del(row[i])
            self.endRemoveColumns()
            return True

    def index(self, row, column, parent=QtCore.QModelIndex()):
        '''
        Returns a QModelIndex according to given data.
        :param row: Returns a QModelIndex with this row index.
        :type row: int
        :param column: Returns a QModelIndex with this column index.
        :type column: int
        :param parent: Default QModelIndex
        :type parent: QModelIndex
        :return: QModelIndex if data corresponding to row and column was found. Empty QModelIndex if not.
        :rtype: QModelIndex
        '''
        if row > -1 and column > -1:
            if row < len(self.dataList) and column < len(self.headers):
                return self.createIndex(row, column, self.dataList[row][column])
            else:
                return QtCore.QModelIndex()
        else:
            return QtCore.QModelIndex()

    # --------------------------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------------------------

    @property
    def dataList(self):
        return self.__dataList

    @property
    def headers(self):
        return self.__headers


# --------------------------------------------------------------------------------------------
# Class: Objects lists model
# --------------------------------------------------------------------------------------------
class ObjectsListModel(QtCore.QAbstractListModel):
    # --------------------------------------------------------------------------------------------
    # Constructor
    # --------------------------------------------------------------------------------------------
    def __init__(self, dataList=[], parent=None):
        '''
        ObjectsListModel for Model/View programming.
        :param dataList: List of objects to be displayed.
        :type dataList: list
        :param parent: QWidget that uses this model. Default=None
        :type parent: QWidget
        '''
        super(ObjectsListModel, self).__init__(parent)
        self.__dataList = dataList
        if dataList == None:
            self.__dataList = []

    # --------------------------------------------------------------------------------------------
    # Methods
    # --------------------------------------------------------------------------------------------

    def rowCount(self, parent=QtCore.QModelIndex()):
        '''
        Rows number for the list
        :param parent: Default QModelIndex
        :type parent: QModelIndex
        :return: dataList len
        :rtype: CameraExporter
        '''
        return len(self.dataList)

    def flags(self, index):
        '''
        Set flags of each item.  Re-implement if different flags are needed and use conditional chains if per-item flags are needed.
        :param index: Item to be filtered
        :type index: QModelIndex
        :return: Flags to be used
        :rtype: QtCore.Qt.Flags
        '''
        if not index.isValid():
            return QtCore.Qt.NoItemFlags
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role=QtCore.Qt.DisplayRole):
        '''
        Query data for specified index and display it.
        :param index: Queried index
        :type index: QModelIndex
        :param role: Display role as default. Reimplement with elif chain for another role.
        :type role: QtCore.Qt.Role
        :return: Item data to be shown in the GUI. Might be None.
        :rtype: object
        '''
        row = index.row()
        if not index.isValid():
            return None
        elif row >= len(self.dataList) or row < 0:
            return None
        elif role in [QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole, QtCore.Qt.EditRole]:
            return self.dataList[row]
        else:
            return None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        '''
        Edits the data in the cells.
        :param section: Queried header index
        :type section: int
        :param orientation: Vertical or Horizontal
        :type orientation: QtCore.Qt.Orientation
        :param role: Qt role requested for the item
        :type role: QtCore.Qt.Role
        :return: If item was edited successfully return True. 
        :rtype: boolean
        '''
        row = index.row()
        if not index.isValid():
            return False
        elif row >= len(self.dataList) or row < 0:
            return False

        if role == QtCore.Qt.EditRole:
            if value != None:
                self.dataList[row] = value
                self.dataChanged.emit(index, index)
                return True
            else:
                return False
        else:
            return False

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        '''
        Insert rows in the list.
        :param position: Inserting items from this index.
        :type position: int
        :param rows: List of items to be added to the list.
        :type rows: Objects list
        :param parent: Default QModelIndex
        :type parent: QModelIndex
        :return: True if insert was successful. False if a number of conditions are not matched.
        :rtype: boolean
        '''
        if len(rows) <= 0:
            return False
        elif position > len(self.dataList):
            return False
        elif position < 0:
            return False
        else:
            self.beginInsertRows(parent, position, position + len(rows) - 1)
            for item in rows[::-1]:
                self.dataList.insert(position, item)

            self.endInsertRows()

            return True

    def removeRows(self, indexList, count, parent=QtCore.QModelIndex()):
        '''
        Remove rows from the list.
        :param indexList: Remove the items corresponding to this indexList
        :type indexList: int list or QModelIndex list
        :param count: Number of items to be removed
        :type count: int
        :param parent: Default QModelIndex
        :type parent: QModelIndex
        :return: True if remove was successful. False if a number of conditions are not matched.
        :rtype: boolean
        '''

        QMIndexList = all(isinstance(x, QtCore.QModelIndex) for x in indexList)
        if QMIndexList:
            intIndexList = sorted([index.row() for index in indexList])
            indexList = intIndexList

        for i in indexList:
            if i > len(self.dataList) - 1:
                return False
            elif i < 0:
                return False

        if len(indexList) != count:
            return False
        else:
            position = indexList[0]
            self.beginRemoveRows(parent, position, position + (count - 1))
            for i in sorted(indexList, reverse=True):
                del(self.dataList[i])
            self.endRemoveRows()
            return True

    def index(self, row, column=0, parent=QtCore.QModelIndex()):
        '''
        Returns a QModelIndex according to given data.
        :param row: Returns a QModelIndex with this row index.
        :type row: int
        :param column: Returns a QModelIndex with this column index.
        :type column: int
        :param parent: Default QModelIndex
        :type parent: QModelIndex
        :return: QModelIndex if data corresponding to row and column was found. Empty QModelIndex if not.
        :rtype: QModelIndex
        '''
        if row < len(self.dataList) and row > -1:
            return self.createIndex(row, 0, self.dataList[row])
        else:
            return QtCore.QModelIndex()

    # --------------------------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------------------------

    @property
    def dataList(self):
        return self.__dataList


# --------------------------------------------------------------------------------------------
# Class: Tree Node
# --------------------------------------------------------------------------------------------
class TreeNode(object):
    # --------------------------------------------------------------------------------------------
    # Constructor
    # --------------------------------------------------------------------------------------------
    def __init__(self, dataList, headers, parent=None):
        '''
        TreeNode to be used by DataTreeModel.
        :param dataList: List of objects to be displayed by DataTreeModel for this node. IT'S MANDATORY TO HAVE THE NAME AS THE FIRST ITEM IN THIS LIST.
        :type dataList: list
        :param parent: TreeNode to be the parent of this node. None only if node is root of tree structure.
        :type parent: TreeNode or None
        '''
        self.__parent = parent
        self.__data = dataList  # Example: [name,itemType,internalName]
        self.__headers = headers
        self.__children = []
        self.__depth = 0
        self.initDepth()

    # --------------------------------------------------------------------------------------------
    # Methods
    # --------------------------------------------------------------------------------------------

    def child(self, row):
        '''
        Child in a specific row index of this TreeNode.
        :param row: index
        :type row: int
        :return: TreeNode. None if a number of conditions are not matched.
        :rtype: TreeNode or None
        '''
        if row > len(self.children) - 1:
            return None
        return self.children[row]

    def childCount(self):
        '''
        Children number for this TreeNode.
        :return: Children number for this TreeNode.
        :rtype: int
        '''
        return len(self.children)

    def childNumber(self):
        '''
        Child index according to parent node for this TreeNode.
        :return: Child index
        :rtype: int
        '''
        if self.parent != None:
            return self.parent.children.index(self)
        else:
            return 0

    def columnCount(self):
        '''
        Number of items in data
        :return: Number of items in data
        :rtype: int
        '''
        return len(self.headers)

    def insertChildren(self, position, data, _headers, count=1):
        '''
        Insert a TreeNode with given data and with self node as parent
        :param position: Inserting items from this index.
        :type position: int
        :param data: List of data lists or single list to be added as children.
        :type data: List or list of lists
        :param count: How many children
        :type count: int
        :return: TreeNode with given data or list of TreeNodes. None if a number of conditions are not matched.
        :rtype: TreeNode, list of TreeNodes or None
        '''
        headers = _headers[:]  # Copy headers list to avoid recursive errors
        if position < 0 or position > len(self.children):
            return None
        else:
            manyRows = all(isinstance(x, list) for x in data)
            if manyRows:
                if len(data) != count:
                    return None
                else:
                    rowsLen = all(len(childData) == self.columnCount() for childData in data)
                    if rowsLen:
                        insertedChildren = []
                        for childData in data:
                            node = TreeNode(childData, headers, self)
                            self.children.insert(position, node)
                            insertedChildren.append(node)
                        return insertedChildren
                    else:
                        return None
            else:
                node = TreeNode(data, headers, self)
                self.children.insert(position, node)
                return node

    def insertColumns(self, position, columns):
        '''
        Insert columns to this node.
        :param position: Inserting items from this index.
        :type position: int
        :param columns: List of items to be added to the list.
        :type columns: Objects list
        :return: True if successful
        :rtype: Boolean
        '''
        if position < 0 or position > self.columnCount():
            return False
        else:
            for column in sorted(columns):
                self.data.insert(position, column)
                self.headers.insert(position, column)
            return True

    def removeChildren(self, indexList):
        '''
        Remove children from this node.
        :param indexList: Remove items included in this list.
        :type indexList: int list
        :return: True if successful
        :rtype: Boolean
        '''
        for i in indexList:
            if i > len(self.children) - 1:
                return False
            elif i < 0:
                return False

        for i in sorted(indexList, reverse=True):
            del(self.children[i])

        return True

    def removeColumns(self, indexList):
        '''
        Remove data items from this node, requested by DataTreeModel.
        :param indexList: Remove items included in this list.
        :type indexList: int list
        :return: True if successful
        :rtype: Boolean
        '''
        for i in indexList:
            if i > len(self.data) - 1:
                return False
            elif i < 0:
                return False

        if self.parent != None:
            if self.parent.columnCount() == self.columnCount() - len(indexList):
                for i in sorted(indexList, reverse=True):
                    del(self.data[i])
                    del(self.headers[i])
                return True
            else:
                return False
        else:
            for i in sorted(indexList, reverse=True):
                del(self.data[i])
                del(self.headers[i])
            return True

    def dataValue(self, column):
        '''
        Get data for specific column index
        :param column: index int for requested item in data list
        :type column: int
        :return: data value
        :rtype: object
        '''
        if column >= len(self.data):
            return None
        else:
            return self.data[column]

    def setData(self, column, value):
        '''
        Set data for specific column index
        :param column: index int for item in data list to be replaced
        :type column: int
        :param value: Value to use
        :type value: object
        :return: True if successful.
        :rtype: boolean
        '''
        if column < 0 or column >= len(self.data):
            return False
        else:
            self.data[column] = value
            return True

    def asDict(self):
        '''
        Assembles headers and data from this node as header:value pairs.
        :return: Dict with header:value pairs
        :rtype: dict
        '''
        newDict = {}
        i = 0
        for each in self.headers:
            newDict[each] = self.data[i]
            i += 1
        return newDict

    def log(self, tabLevel=-1):
        '''
        Print output with this tree representation when requested.
        :return: String with tree form.
        :rtype: string
        '''

        output = ""
        tabLevel += 1

        for i in range(tabLevel):
            output += "\t"
        output += "|------" + ", ".join(str(x) for x in self.headers) + "\n"

        for i in range(tabLevel):
            output += "\t"
        output += "|------" + ", ".join(str(x) for x in self.data) + "\n"

        for child in self.children:
            output += child.log(tabLevel)

        tabLevel -= 1
        output += "\n"

        return output

    def initDepth(self):
        '''
        Initialize tree depth for this node. If root, depth is 0
        '''
        if self.parent == None:
            self.depth = 0
        else:
            parentDepth = self.parent.depth
            self.depth = parentDepth + 1

    def __repr__(self):
        return self.log()

    # --------------------------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------------------------

    @property
    def depth(self):
        return self.__depth

    @depth.setter
    def depth(self, d):
        self.__depth = d

    @property
    def name(self):
        return self.__data[0]

    @name.setter
    def name(self, n):
        self.__data[0] = n

    @property
    def parent(self):
        return self.__parent

    @property
    def data(self):
        return self.__data

    @property
    def children(self):
        return self.__children

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, d):
        self.__headers = d


# --------------------------------------------------------------------------------------------
# Class: Tree Data Model
# --------------------------------------------------------------------------------------------
class DataTreeModel(QtCore.QAbstractItemModel):
    # --------------------------------------------------------------------------------------------
    # Constructor
    # --------------------------------------------------------------------------------------------
    def __init__(self, root=TreeNode(['name', 'itemType', 'internalName'], ['name', 'itemType', 'internalName']), headers=[], parent=None):
        '''
        DataTreeModel for Model/View programming.
        :param root: root TreeNode for this model.
        :type root: TreeNode
        :param headers: list of headers to be displayed in the table. Must be same len as data passed to rootnode
        :type headers: list
        :param parent: QWidget that uses this model. Default=None
        :type parent: QWidget
        '''
        super(DataTreeModel, self).__init__(parent)
        self.__rootNode = root
        self.__headers = headers
        if headers == None:
            self.__headers = []

    # --------------------------------------------------------------------------------------------
    # Methods
    # --------------------------------------------------------------------------------------------
    def columnCount(self, parent=QtCore.QModelIndex()):
        '''
        Number of columns
        :return: Number of items in headers
        :rtype: int
        '''
        return len(self.headers)

    def rowCount(self, index):
        '''
        Rows number for the given QModelIndex
        :param index: Pass a QModelIndex to find the correspoding node and count
        :type index: QModelIndex
        :return: Child count for the corresponding node
        :rtype: int
        '''
        node = self.dataList
        if index.isValid():
            node = index.internalPointer()

        return node.childCount()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        '''
        Query data for specified index and display it.
        :param index: Queried index
        :type index: QModelIndex
        :param role: Display role as default. Reimplement with elif chain for another role.
        :type role: QtCore.Qt.Role
        :return: Item data to be shown in the GUI. Might be None.
        :rtype: object
        '''
        if not index.isValid():
            return None
        else:
            if role != QtCore.Qt.DisplayRole and role != QtCore.Qt.EditRole:
                return None
            else:
                node = self.getNode(index)
                return node.dataValue(index.column())

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        '''
        Set data for specified index and display it.
        :param index: Index to be edited
        :type index: QModelIndex
        :param role: Edit role as default. Reimplement with elif chain for another role.
        :type role: QtCore.Qt.Role
        :return: Item data to be shown in the GUI. Might be None.
        :rtype: object
        '''
        if role != QtCore.Qt.EditRole:
            return False
        else:
            node = self.getNode(index)
            result = node.setData(index.column(), value)

            if result:
                self.dataChanged.emit(index, index)

            return result

    def flags(self, index):
        '''
        Set flags for each item.  Re-implement if different flags are needed and use conditional chains if per-item flags are needed.
        :param index: Item to be filtered
        :type index: QModelIndex
        :return: Flags to be used
        :rtype: QtCore.Qt.Flags
        '''
        if not index.isValid():
            return QtCore.Qt.NoItemFlags
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def getNode(self, index):
        '''
        Get TreeNode corresponding to given QModelIndex.
        :param index: Item for which the TreeNode is needed.
        :type index: QModelIndex
        :return: TreeNode. None if no node is found.
        :rtype: Treenode
        '''
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
            else:
                return None
        else:
            return self.dataList

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        '''
        Names of colums.
        :param section: Queried header index
        :type section: int
        :param orientation: Horizontal by default. Re-implement if vertical is needed as well.
        :type orientation: QtCore.Qt.Orientation
        :param role: Qt role requested for the item
        :type role: QtCore.Qt.Role
        :return: Item data to be returned or shown in the GUI. Might be None.
        :rtype: object
        '''
        if orientation == QtCore.Qt.Horizontal:
            if role in [QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole, QtCore.Qt.EditRole]:
                if section > len(self.headers) - 1:
                    return None
                else:
                    value = self.headers[section]
                    return value
            else:
                return None
        else:
            return None

    def index(self, row, column, parent=QtCore.QModelIndex()):
        '''
        Returns a QModelIndex according to given data.
        :param row: Returns a QModelIndex with this row index.
        :type row: int
        :param column: Returns a QModelIndex with this column index.
        :type column: int
        :param parent: Default QModelIndex
        :type parent: QModelIndex
        :return: QModelIndex if data corresponding to row and column was found. Empty QModelIndex if not.
        :rtype: QModelIndex
        '''
        if row > -1 and column > -1:
            if parent.isValid() and parent.column() != 0:
                return QtCore.QModelIndex()
            parentNode = self.getNode(parent)
            childNode = parentNode.child(row)

            if childNode:
                return self.createIndex(row, column, childNode)
            else:
                return QtCore.QModelIndex()
        else:
            return QtCore.QModelIndex()

    def insertColumns(self, position, columns, parent=QtCore.QModelIndex()):
        '''
        Insert columns in the table.
        :param position: Inserting items from this index.
        :type position: int
        :param columns: Columns to be added
        :type columns: list
        :param parent: Default QModelIndex
        :type parent: QModelIndex
        :return: True if insert was successful. False if a number of conditions are not matched.
        :rtype: boolean
        '''
        if position < 0:
            return False
        else:
            if type(columns) is list:
                self.beginInsertColumns(parent, position, position + len(columns) - 1)
                for i in columns[::-1]:
                    self.headers.insert(position, i)
                if self.dataList.childCount() > 0:
                    for child in self.dataList.children:
                        success = self.insertColumns_recursive(child, position, columns)
                self.endInsertColumns()
                return success
            else:
                return False

    def insertColumns_recursive(self, node, position, columns):
        '''
        Insert columns recursively in the TreeNodes. Not meant to be used directly.
        :param node: TreeNode where to insert columns
        :type node: TreeNode
        :param position: Inserting items from this index.
        :type position: int
        :param columns: Columns to be added
        :type columns: list
        '''
        success = node.insertColumns(position, columns)
        if node.childCount() > 0:
            for child in node.children:
                self.insertColumns_recursive(child, position, columns)
        return success

    def insertRows(self, position, count, data, parent=QtCore.QModelIndex()):
        '''
        Insert rows in the table.
        :param position: Inserting items from this index.
        :type position: int
        :param count: Number of rows to be added
        :type count: int
        :param data: List of values for a single row or a list of rows
        :type data: List or list of lists
        :param parent: Parent QModelIndex
        :type parent: QModelIndex
        :return: True if insert was successful. False if a number of conditions are not matched.
        :rtype: boolean
        '''
        if position < 0:
            return False
        else:
            parentNode = self.getNode(parent)
            if not parent.isValid():
                parentNode = self.dataList
            manyRows = all(isinstance(x, list) for x in data)
            if manyRows:
                rowsLen = all(len(x) == self.columnCount() for x in data)
                if rowsLen:
                    self.beginInsertRows(parent, position, position + (count - 1))
                    for each in sorted(data, reverse=True):
                        success = parentNode.insertChildren(position, each, self.headers[:])
                    self.endInsertRows()
                    return success
                else:
                    return False
            else:
                if len(data) == self.columnCount():
                    self.beginInsertRows(parent, position, position + (count - 1))
                    success = parentNode.insertChildren(position, data, self.headers[:])
                    self.endInsertRows()
                    return success
                else:
                    return False

    def parent(self, index):
        '''
        Given an index return its parent index.
        :param index: Found the parent for this index
        :type index: int
        :return: QModelIndex for the parent of given index
        :rtype: QModelIndex
        '''
        childNode = self.getNode(index)
        parentNode = childNode.parent
        if not index.isValid():
            return QtCore.QModelIndex()
        elif parentNode == self.dataList:
            return QtCore.QModelIndex()
        else:
            return self.createIndex(parentNode.childNumber(), 0, parentNode)

    def indexFromNode(self, node, column=0):
        '''
        Given a node and column return a QModelIndex.
        :param node: Get a QModelIndex for this node.
        :type node: TreeNode
        :param column: Column number for createIndex. Default = 0
        :type column: int
        :return: QModelIndex for the given node
        :rtype: QModelIndex
        '''
        return self.createIndex(node.childNumber(), column, node)

    def removeColumns(self, indexList, count, parent=QtCore.QModelIndex()):
        '''
        Remove columns in the tree structure
        :param indexList: Remove items in this list.
        :type indexList: int list or QModelIndex list
        :param count: Columns to be added
        :type count: list
        :param parent: Default QModelIndex
        :type parent: QModelIndex
        :return: True if remove was successful. False if a number of conditions are not matched.
        :rtype: boolean
        '''
        QMIndexList = all(isinstance(x, QtCore.QModelIndex) for x in indexList)
        if QMIndexList:
            intIndexList = sorted([index.column() for index in indexList])
            indexList = intIndexList

        for i in indexList:
            if i > len(self.headers) - 1:
                return False
            elif i < 0:
                return False

        if len(indexList) != count:
            return False
        else:
            if not parent.isValid():
                position = indexList[0]
                self.beginRemoveColumns(parent, position, position + (count - 1))
                for i in sorted(indexList, reverse=True):
                    del(self.headers[i])
                self.removeColumns_recursive(self.dataList, indexList)
                self.endRemoveColumns()
                return True
            else:
                return False

            if self.dataList.columnCount() == 0:
                self.removeRows([0], self.rowCount())

    def removeColumns_recursive(self, node, indexList):
        '''
        Remove columns recursively in the TreeNodes. Not meant to be used directly.
        :param node: TreeNode from where to remove columns
        :type node: TreeNode
        :param indexList: list with indexes to be removed
        :type indexList: int lsit
        :param columns: Columns to be added
        :type columns: list
        '''
        node.removeColumns(indexList)
        if node.childCount() > 0:
            for child in node.children:
                self.removeColumns_recursive(child, indexList)

    def removeRows(self, modelIndexList):
        '''
        Remove rows in the tree structure
        :param modelIndexList: Remove items in this list.
        :type modelIndexList: QModelIndex list
        :return: True if remove was successful. False if a number of conditions are not matched.
        :rtype: boolean
        '''
        QMIndexList = all(isinstance(x, QtCore.QModelIndex) for x in modelIndexList)
        if QMIndexList:
            # Group selected items by tree depth
            depthDict = {}
            for index in modelIndexList:
                if self.getNode(index).depth in depthDict.keys():
                    depthDict[self.getNode(index).depth].append(index)
                else:
                    depthDict[self.getNode(index).depth] = [index]

            # Loop through each depth level
            for depthLevel in sorted(depthDict.keys(), reverse=True):
                # Group by index level
                indexesDict = {}
                for item in depthDict[depthLevel]:
                    if item.row() in indexesDict.keys():
                        indexesDict[item.row()].append(item)
                    else:
                        indexesDict[item.row()] = [item]
                # Delete items from highest index and backwards
                for listIndex in sorted(indexesDict.keys(), reverse=True):
                    for index in indexesDict[listIndex]:
                        parentNode = self.getNode(index).parent
                        parentIndex = self.parent(index)
                        position = index.row()
                        count = 1
                        self.beginRemoveRows(parentIndex, position, position + count - 1)
                        parentNode.removeChildren([index.row()])
                        self.endRemoveRows()
            return True
        else:
            return False

    # --------------------------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------------------------

    @property
    def dataList(self):
        return self.__rootNode

    @property
    def headers(self):
        return self.__headers


# --------------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------------
def main():
    pass


if __name__ == "__main__":
    main()
