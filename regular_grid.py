from qgis.core import QgsCoordinateReferenceSystem
from .point import Point
from .cell import Cell
from .grid import Grid


class RegularGrid(Grid):
    def __init__(self, crs: QgsCoordinateReferenceSystem, origin: Point, nCols: int, nRows: int,
                 colSpacing: float, rowSpacing: float, angle: float):

        xO = origin.x()
        yO = origin.y()

        points = []
        for r in range(nRows + 1):
            row = []
            for c in range(nCols + 1):
                xOffset = c * colSpacing
                yOffset = r * rowSpacing
                point = Point(xO + xOffset, yO + yOffset)
                point.rotate(origin, angle)
                row.append(point)
            points.append(row)

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

        super().__init__(crs, cells)
