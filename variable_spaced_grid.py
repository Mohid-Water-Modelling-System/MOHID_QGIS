from qgis.core import QgsCoordinateReferenceSystem
from .point import Point
from .cell import Cell
from .grid import Grid


class VariableSpacedGrid(Grid):
    def __init__(self, crs: QgsCoordinateReferenceSystem, origin: Point, nCols: int, nRows: int,
                 colSpacingStart: float, colSpacingEnd: float,
                 rowSpacingStart: float, rowSpacingEnd: float, angle: float):

        xO = origin.x()
        yO = origin.y()
        xVariation = (colSpacingEnd - colSpacingStart) / nCols
        yVariation = (rowSpacingEnd - rowSpacingStart) / nRows

        points = []
        yOffset = 0
        for r in range(nRows + 1):
            row = []
            xOffset = 0
            for c in range(nCols + 1):
                point = Point(xO + xOffset, yO + yOffset)
                point.rotate(origin, angle)
                row.append(point)
                xOffset += colSpacingStart + (c * xVariation)
            points.append(row)
            yOffset += rowSpacingStart + (r * yVariation)

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
