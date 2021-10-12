from .grid_layout import GridLayout
from .point import Point

class GridRegularLayout(GridLayout):
    def __init__(self, nCols: int, nRows: int, colSpacing: float, rowSpacing: float):
        self.setNCols(nCols)
        self.setNRows(nRows)
        self.setColSpacing(colSpacing)
        self.setRowSpacing(rowSpacing)
    
    def setNCols(self, n: int):
        if n < 1 :
            raise Exception("Number of columns lower than 1")
        self.__nCols = n
    
    def getNCols(self) -> int:
        return self.__nCols

    def setNRows(self, n: int):
        if n < 1 :
            raise Exception("Number of rows lower than 1")
        self.__nRows = n
    
    def getNRows(self) -> int:
        return self.__nRows
    
    def setColSpacing(self, s: float):
        if s <= 0 :
            raise Exception("Column spacing not greater than 0")
        self.__colSpacing = s
    
    def getColSpacing(self) -> float:
        return self.__colSpacing
    
    def setRowSpacing(self, s: float):
        if s <= 0 :
            raise Exception("Row spacing not greater than 0")
        self.__rowSpacing = s
    
    def getRowSpacing(self) -> float:
        return self.__rowSpacing
    
    def toPoints(self, origin: Point, angle: float) -> list[list[Point]]:
        nCols = self.getNCols()
        nRows = self.getNRows()
        colSpacing = self.getColSpacing()
        rowSpacing = self.getRowSpacing()
        x = origin.x()
        y = origin.y()

        points = []
        for r in range(nRows + 1):
            row = []
            yOffset = r * rowSpacing
            for c in range(nCols + 1):
                xOffset = c * colSpacing
                point = Point(x + xOffset, y + yOffset)
                point.rotate(origin, angle)
                row.append(point)
            points.append(row)

        return points