from .point import Point
from .cell import Cell


class GridLayout:
    def getNCols(self) -> int:
        pass
    
    def getNRows(self) -> int:
        pass

    def toPoints(self, origin: Point, angle: float) -> list[list[Point]]:
        pass

    def toCells(self, origin: Point, angle: float) -> list[list[Cell]]:
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