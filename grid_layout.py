from .point import Point, Origin
from .cell import Cell
from .angle import Angle
from .grid_item_layout import GridItemLayout


class GridLayout:
    def getNCols(self) -> int:
        pass

    def getNRows(self) -> int:
        pass

    def toPoints(self, origin: Origin, angle: Angle) -> list[list[Point]]:
        pass

    def toCells(self, origin: Origin, angle: Angle) -> list[list[Cell]]:
        points = self.toPoints(origin, angle)
        nRows = self.getNRows()
        nCols = self.getNCols()

        cells = []
        for r in range(nRows):
            row = []
            for c in range(nCols):
                pA = points[r][c]
                pB = points[r][c + 1]
                pC = points[r + 1][c + 1]
                pD = points[r + 1][c]
                cell = Cell(pA, pB, pC, pD)
                row.append(cell)
            cells.append(row)
        return cells
    
    def toString(self, config: dict) -> str:
        pass


class GridRegularLayout(GridLayout):
    def __init__(self, nCols: int, nRows: int, colSpacing: float, rowSpacing: float):
        self.setNCols(nCols)
        self.setNRows(nRows)
        self.setColSpacing(colSpacing)
        self.setRowSpacing(rowSpacing)

    def setNCols(self, n: int):
        if n < 1:
            raise Exception("Number of columns lower than 1")
        self.__nCols = n

    def getNCols(self) -> int:
        return self.__nCols

    def setNRows(self, n: int):
        if n < 1:
            raise Exception("Number of rows lower than 1")
        self.__nRows = n

    def getNRows(self) -> int:
        return self.__nRows

    def setColSpacing(self, s: float):
        if s <= 0:
            raise Exception("Column spacing not greater than 0")
        self.__colSpacing = s

    def getColSpacing(self) -> float:
        return self.__colSpacing

    def setRowSpacing(self, s: float):
        if s <= 0:
            raise Exception("Row spacing not greater than 0")
        self.__rowSpacing = s

    def getRowSpacing(self) -> float:
        return self.__rowSpacing

    def toPoints(self, origin: Origin, angle: Angle) -> list[list[Point]]:
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
    
    def toString(self, config: dict) -> str:
        return ""


class GridVariableLayout(GridLayout):
    def __init__(self, colLayouts: list[GridItemLayout], rowLayouts: list[GridItemLayout]):
        self.setColLayouts(colLayouts)
        self.setRowLayouts(rowLayouts)

    def setColLayouts(self, l: list[GridItemLayout]):
        if l:
            self.__colLayouts = l
        else:
            raise Exception("Column layout list is empty")

    def getColLayouts(self) -> list[GridItemLayout]:
        return self.__colLayouts

    def setRowLayouts(self, l: list[GridItemLayout]):
        if l:
            self.__rowLayouts = l
        else:
            raise Exception("Row layout list is empty")

    def getRowLayouts(self) -> list[GridItemLayout]:
        return self.__rowLayouts

    def getNCols(self) -> int:
        l = self.getColLayouts()
        n = sum([i.getN() for i in l])
        return n

    def getNRows(self) -> int:
        l = self.getRowLayouts()
        n = sum([i.getN() for i in l])
        return n

    def toPoints(self, origin: Origin, angle: Angle) -> list[list[Point]]:
        cls = self.getColLayouts()
        rls = self.getRowLayouts()
        x = origin.x()
        y = origin.y()

        points = []
        yOffset = 0
        for rl in rls:
            yVariation = (rl.getSpacingEnd() -
                          rl.getSpacingStart()) / rl.getN()
            for r in range(rl.getN() + 1):
                row = []
                xOffset = 0
                for cl in cls:
                    xVariation = (cl.getSpacingEnd() -
                                  cl.getSpacingStart()) / cl.getN()
                    for c in range(cl.getN() + 1):
                        point = Point(x + xOffset, y + yOffset)
                        point.rotate(origin, angle)
                        row.append(point)
                        xOffset += cl.getSpacingStart() + (c * xVariation)
                points.append(row)
                yOffset += rl.getSpacingStart() + (r * yVariation)

        return points

    def toString(self, config: dict) -> str:
        return ""