from qgis.PyQt.QtWidgets import QTableWidget, QTableWidgetItem
from .item_layout import ItemLayout

class Layout:
    def __init__(self, table: QTableWidget):
        labels = ["Quantity", "Type", "Spacing"]
        columnCount = len(labels)
        table.setColumnCount(columnCount)
        table.setHorizontalHeaderLabels(labels)
        self.setTableWidget(table)
        self.setRows([])
        self.setCols([])

    def setTableWidget(self,  tableWidget: QTableWidget):
        self.__tableWidget = tableWidget

    def getTableWidget(self) -> QTableWidget:
        return self.__tableWidget
    
    def getRows(self) -> list[ItemLayout]:
        return self.__rows
    
    def setRows(self, rows: list[ItemLayout]):
        self.__rows = rows
    
    def getCols(self) -> list[ItemLayout]:
        return self.__cols
    
    def setCols(self, cols: list[ItemLayout]):
        self.__cols = cols

    def addCols(self, n: int, spacingStart: float, spacingEnd: float):
        if n < 1 :
            raise Exception("Number of columns lower than 1")
        elif spacingStart <= 0 :
            raise Exception("Column spacing start not greater than 0")
        elif spacingEnd <= 0 :
            raise Exception("Column spacing end not greater than 0")
        
        self.addItems(n, "Column", spacingStart, spacingEnd)
        colLayout = ItemLayout(n, spacingStart, spacingEnd)
        col = self.getCols()
        col.append(colLayout)

    def addRows(self, n: int, spacingStart: float, spacingEnd: float):
        if n < 1 :
            raise Exception("Number of rows lower than 1")
        elif spacingStart <= 0 :
            raise Exception("Row spacing start not greater than 0")
        elif spacingEnd <= 0 :
            raise Exception("Row spacing end not greater than 0")

        self.addItems(n, "Row", spacingStart, spacingEnd)
        rowLayout = ItemLayout(n, spacingStart, spacingEnd)
        rows = self.getRows()
        rows.append(rowLayout)
        
    def addItems(self, n: int, type: str, spacingStart: float, spacingEnd: float):
        if n < 1 :
            raise Exception("Number of items lower than 1")
        elif spacingStart <= 0 :
            raise Exception("Item spacing start not greater than 0")
        elif spacingEnd <= 0 :
            raise Exception("Item spacing end not greater than 0")

        table = self.getTableWidget()
        rowCount = table.rowCount()
        colCount = table.columnCount()

        items = [QTableWidgetItem(str(n)),
                 QTableWidgetItem(type),
                 QTableWidgetItem(str(spacingStart) + " to " + str(spacingEnd))]

        table.insertRow(rowCount)
        for col in range(colCount):
            item = items[col]
            table.setItem(rowCount, col, item)
    
    def isValid(self) -> bool:
        rows = self.getRows()
        cols = self.getCols()
        return bool(rows) and bool(cols)