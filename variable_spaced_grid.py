from qgis.core import QgsCoordinateReferenceSystem
from .point import Point
from .cell import Cell
from .grid import Grid


class VariableSpacedGrid(Grid):
    def __init__(self, crs: QgsCoordinateReferenceSystem, origin: Point, nCols: int, nRows: int,
                 colSpacingStart: float, colSpacingEnd: float,
                 rowSpacingStart: float, rowSpacingEnd: float, angle: float):
        
        if nCols < 1 :
            raise Exception("Number of columns lower than 1")
        elif nRows < 1 :
            raise Exception("Number of rows lower than 1")
        elif colSpacingStart <= 0 :
            raise Exception("Column spacing start not greater than 0")
        elif colSpacingEnd <= 0 :
            raise Exception("Column spacing end not greater than 0")
        elif rowSpacingStart <= 0 :
            raise Exception("Row spacing start not greater than 0")
        elif rowSpacingEnd <= 0 :
            raise Exception("Row spacing end not greater than 0")

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
