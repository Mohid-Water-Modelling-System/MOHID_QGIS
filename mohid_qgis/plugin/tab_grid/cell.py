from qgis.core import QgsPolygon, QgsLineString, QgsPoint
from .point import Point
from typing import List

"""
The Cell class implements a cell of the grid.
A Cell is set of 4 points.
This class can return a rectangular Qgis polygon built from its points 
"""
class Cell:
    """
    The Cell constructor receives for points (a,b,c,d) which are the corners of the cell.
    """
    def __init__(self, a: Point, b: Point, c: Point, d: Point):
        self.setPoints([a, b, c, d])

    def getPoints(self) -> List[Point]:
        return self.__points

    def setPoints(self, points: List[Point]):
        self.__points = points

    """
    The toQgsPolygon function return a rectangular Qgis polygon to visualize the cell.
    It is build from a line that unites the 4 corners of the cell.
    """
    def toQgsPolygon(self) -> QgsPolygon:
        points = self.getPoints()
        
        newPoints = []
        for point in points:
            newPoints.append(QgsPoint(point))
        
        # Polygon needs to be closed, add last point equal to the first to close the ring
        newPoints.append(newPoints[0])
        line = QgsLineString(newPoints)
        try:
            polygon = QgsPolygon(line, rings=[])
        except Exception as e:
            pass
        return polygon
