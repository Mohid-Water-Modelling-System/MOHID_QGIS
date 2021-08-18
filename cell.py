from qgis.core import QgsPolygon, QgsLineString
from .point import Point


class Cell:
    def __init__(self, a: Point, b: Point, c: Point, d: Point):
        self.setPoints([a, b, c, d])

    def getPoints(self) -> list[Point]:
        return self.__points

    def setPoints(self, points: list[Point]):
        self.__points = points

    def toQgsPolygon(self) -> QgsPolygon:
        points = self.getPoints()
        line = QgsLineString(points)
        polygon = QgsPolygon(line)
        return polygon
