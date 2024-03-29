from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.PyQt.QtWidgets import QTableWidget, QTableWidgetItem, QToolButton, QLabel
from qgis.PyQt.QtGui import QIcon
from .grid_item_layout import GridItemLayout, GridColLayout, GridRowLayout
from typing import List
"""
The GridLayoutTable stores the gridItemLayouts that the user adds in the GridVariableLayoutField
and lists them in a table in the plugin interface.
This class is a child of QObject to be able to have a pyqtSignal attribute.
"""
class GridLayoutTable(QObject):
    """
    The filled attribute is a signal that emits a boolean value when the layout built from the
    added items becomes acceptable or not.
    If the layout is acceptable (has both columns and rows), true is emitted.
    If the layout is not acceptable, false is emitted.
    """
    filled = pyqtSignal(bool)

    """
    The constructor of the GridLayoutTable class receives:
        - a label saying "Layout", that is displayed next to the tablewidget
        - a tableWidget that lists the GridLayoutItems added by the user
    The constructor will initialize two empty lists, one for storing GridColLayouts and another for
    GridRowLayouts. When both lists have elements the layout is acceptable.
    """
    def __init__(self, layoutLabel: QLabel, tableWidget: QTableWidget):
        super().__init__()

        self.setTableWidget(tableWidget)
        self.setLayoutLabel(layoutLabel)
        self.setColLayouts([])
        self.setRowLayouts([])
    
    def setLayoutLabel(self, l: QLabel):
        self.__layoutLabel = l

    def getLayoutLabel(self) -> QLabel:
        return self.__layoutLabel

    """
    The tableWidget setter a QTableWidget object,
    creates 4 columns on the QTableWidget and sets "Quantity", "Type" and "Spacing" as header labels of the first 3 columns.
    """
    def setTableWidget(self, t: QTableWidget):
        labels = ["Quantity", "Type", "Spacing", ""]
        columnCount = len(labels)
        t.setColumnCount(columnCount)
        t.setHorizontalHeaderLabels(labels)
        self.__tableWidget = t

    def getTableWidget(self) -> QTableWidget:
        return self.__tableWidget

    def setColLayouts(self, l: List[GridColLayout]):
        self.__colLayouts = l
    
    def getColLayouts(self) ->List[GridColLayout]:
        return self.__colLayouts
    
    def setRowLayouts(self, l: List[GridRowLayout]):
        self.__rowLayouts = l
    
    def getRowLayouts(self) ->List[GridRowLayout]:
        return self.__rowLayouts

    """
    The addColLayout function receives the layout of a set of columns and adds it to the list of column layouts and to the tableWidget (1 row).
    It also checks if the layout is correctly defined (has both rows and columns) and emits the signal "filled" which has a boolean
    that is true when the layout is correctly defined and false when the layout is not correctly defined yet.
    """
    def addColLayout(self, l: GridColLayout):
        colLayouts = self.getColLayouts()
        colLayouts.append(l)
        self.addItemLayout(l)

        self.filled.emit(self.isFilled())
    
    """
    The addRowLayout function receives the layout of a set of rows and adds it to the list of row layouts and to the tableWidget (1 row).
    It also checks if the layout is correctly defined (has both rows and columns) and emits the signal "filled" which has a boolean
    that is true when the layout is correctly defined and false when the layout is not correctly defined yet.
    """
    def addRowLayout(self, l: GridRowLayout):
        rowLayouts = self.getRowLayouts()
        rowLayouts.append(l)
        self.addItemLayout(l)

        self.filled.emit(self.isFilled())


    """
    The addItemLayout function is used by the addColLayout and addRowLayout functions to display a item layout in a row of the tableWidget.
    """
    def addItemLayout(self, l: GridItemLayout):
        t = self.getTableWidget()
        rowCount = t.rowCount()
        
        t.insertRow(rowCount)
        items = l.getTableWidgetItems()

        for i in range(len(items)):
            t.setItem(rowCount, i, items[i])

        #b = QToolButton(t)
        #icon = QIcon(":images/themes/default/mActionRemove.svg")
        #b.setIcon(icon)
        #t.setCellWidget(rowCount, colCount - 1, b)
        #t.resizeColumnToContents(colCount - 1)


    """
    The isFilled function returns true if the layout is complete (has both rows and columns) and false otherwise.
    """
    def isFilled(self) -> bool:
        colLayouts = self.getColLayouts()
        rowLayouts = self.getRowLayouts()
        filled = bool(colLayouts) and bool(rowLayouts)
        return filled
    
    """
    The setVisible function displays the tableWidget and its label if the "v" argument is true and hides them
    if the "v" argument is false.
    This function is used when the user selects which type of layout to set.
    """
    def setVisible(self, v: bool):
        items = [self.getTableWidget(),
                 self.getLayoutLabel()]

        for item in items:
            item.setVisible(v)