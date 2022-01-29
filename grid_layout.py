from .point import Point, Origin
from .cell import Cell
from .angle import Angle
from .grid_item_layout import GridItemLayout
from typing import List
"""
The GridLayout class is used to build the grid.
It is in the layout that the number of rows and columns of the grid, as well as the spacing of
each row and column, are specified.
The GridLayout class is the parent class of 2 classes:
    - The GridRegularLayout, that defines the layout of a regular grid
    - The GridVariableLayout, that defines the layout of a variable spaced grid
"""
class GridLayout:
    def getNCols(self) -> int:
        pass

    def getNRows(self) -> int:
        pass

    """
    The toPoints function returns the points that define the corners of the grid cells.
    To call this function the GridLayout must already have the rows and columns defined
    (including their spacings) and only the origin point (bottom left point) and the
    angle of the grid have to be provided for the points of the grid to be calculated.
    The points are returned in a matrix where each point can be obtained from the row number
    and column number - points[row][column] .
    """
    def toPoints(self, origin: Origin, angle: Angle) -> List[List[Point]]:
        pass

    """
    The toCells function returns the cells of the grid.
    To call this function the GridLayout must already have the rows and columns defined
    (including their spacings) and only the origin point (bottom left point) and the
    angle of the grid have to be provided for the cells to be calculated.
    The cells are returned in a matrix where each cell can be obtained from the row number
    and column number - cells[row][column] .
    """
    def toCells(self, origin: Origin, angle: Angle) -> List[List[Cell]]:
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
    
    """
    The toString function is used to write the layout of the grid in MOHID format.
    The string is built according to the first argument of the function, which is
    the configuration provided in form of a dictionary.
    This configuration was previously read from the config.json file.
    """
    def toString(self, config: dict) -> str:
        pass

"""
The GridRegularLayout is used to build a regular grid: All columns have the same spacing
and all rows have the same spacing.
"""
class GridRegularLayout(GridLayout):
    """
    The constructor of the GridRegularLayout class receives:
        - the number of columns of the grid
        - the number of rows of the grid
        - the spacing of the columns
        - the spacing of the rows
    """
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

    """
    The toPoints function returns the points that define the corners of the grid cells.
    To call this function the GridLayout must already have the rows and columns defined
    (including their spacings) and only the origin point (bottom left point) and the
    angle of the grid have to be provided for the points of the grid to be calculated.
    The points are returned in a matrix where each point can be obtained from the row number
    and column number - points[row][column] .
    """
    def toPoints(self, origin: Origin, angle: Angle) -> List[List[Point]]:
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
    
    """
    The toString function is used to write the layout of the grid in MOHID format.
    The string is built according to the first argument of the function, which is
    the configuration provided in form of a dictionary.
    This configuration was previously read from the config.json file.
    """
    #TODO: complete this function
    def toString(self, config: dict) -> str:
        return ""

"""
The GridVariableLayout is used to build a variable spaced grid: The columns may have different
spacings and the rows may also have different spacings.
"""
class GridVariableLayout(GridLayout):
    """
    The constructor of the GridVariableLayout receives:
        - the layouts of the columns
        - the layouts of the rows
    """
    def __init__(self, colLayouts: List[GridItemLayout], rowLayouts: List[GridItemLayout]):
        self.setColLayouts(colLayouts)
        self.setRowLayouts(rowLayouts)

    def setColLayouts(self, l: List[GridItemLayout]):
        if l:
            self.__colLayouts = l
        else:
            raise Exception("Column layout list is empty")

    def getColLayouts(self) -> List[GridItemLayout]:
        return self.__colLayouts

    def setRowLayouts(self, l: List[GridItemLayout]):
        if l:
            self.__rowLayouts = l
        else:
            raise Exception("Row layout list is empty")

    def getRowLayouts(self) -> List[GridItemLayout]:
        return self.__rowLayouts

    def getNCols(self) -> int:
        l = self.getColLayouts()
        n = sum([i.getN() for i in l])
        return n

    def getNRows(self) -> int:
        l = self.getRowLayouts()
        n = sum([i.getN() for i in l])
        return n

    """
    The toPoints function returns the points that define the corners of the grid cells.
    To call this function the GridLayout must already have the rows and columns defined
    (including their spacings) and only the origin point (bottom left point) and the
    angle of the grid have to be provided for the points of the grid to be calculated.
    The points are returned in a matrix where each point can be obtained from the row number
    and column number - points[row][column] .
    """
    def toPoints(self, origin: Origin, angle: Angle) -> List[List[Point]]:
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

    """
    The toString function is used to write the layout of the grid in MOHID format.
    The string is built according to the first argument of the function, which is
    the configuration provided in form of a dictionary.
    This configuration was previously read from the config.json file.
    """
    #TODO: complete this function
    def toString(self, config: dict) -> str:
        return ""