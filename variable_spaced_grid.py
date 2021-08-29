from qgis.core import QgsCoordinateReferenceSystem
from .point import Point
from .cell import Cell
from .grid import Grid
from .layout import Layout


class VariableSpacedGrid(Grid):
    def __init__(self, crs: QgsCoordinateReferenceSystem, origin: Point, angle: float, layout: Layout):
        
        if not layout.isValid():
            raise Exception("Variable Spaced Grid Layout is not valid")
        
        xO = origin.x()
        yO = origin.y()

        colLayout = layout.getCols()
        rowLayout = layout.getRows()

        nRows = 0
        for rl in rowLayout:
            nRows += rl.getN()

        nCols = 0
        for cl in colLayout:
            nCols += cl.getN()

        points = []
        yOffset = 0
        for rl in rowLayout:
            yVariation = (rl.getSpacingEnd() - rl.getSpacingStart()) / rl.getN()
            for r in range(rl.getN() + 1):
                row = []
                xOffset = 0
                for cl in colLayout:
                    xVariation = (cl.getSpacingEnd() - cl.getSpacingStart()) / cl.getN()
                    for c in range(cl.getN() + 1):
                        point = Point(xO + xOffset, yO + yOffset)
                        point.rotate(origin, angle)
                        row.append(point)
                        xOffset += cl.getSpacingStart() + (c * xVariation)
                points.append(row)
                yOffset += rl.getSpacingStart() + (r * yVariation)

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
