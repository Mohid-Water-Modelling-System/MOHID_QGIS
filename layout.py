from .item_layout import ItemLayout

class Layout:
    def __init__(self):
        self.setRows([])
        self.setCols([])

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

        rowLayout = ItemLayout(n, spacingStart, spacingEnd)
        rows = self.getRows()
        rows.append(rowLayout)
    
    def isValid(self) -> bool:
        rows = self.getRows()
        cols = self.getCols()
        return bool(rows) and bool(cols)