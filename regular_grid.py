from qgis.core import (QgsPoint, QgsLineString, QgsFeature, QgsVectorLayer, QgsPolygon, QgsCoordinateReferenceSystem)
import math

class RegularGrid:
    def __init__(self, crs: QgsCoordinateReferenceSystem, origin: QgsPoint, nCols: int, nRows: int,
                colSpacing: float, rowSpacing: float, angle: float):
        self.setCrs(crs)
        self.setOrigin(origin)
        self.setNCols(nCols)
        self.setNRows(nRows)
        self.setColSpacing(colSpacing)
        self.setRowSpacing(rowSpacing)
        self.setAngle(angle)
        self.__points = []
        self.__polygons = []

    def setCrs(self, crs: QgsCoordinateReferenceSystem):
        self.__crs = crs

    def getCrs(self) -> QgsCoordinateReferenceSystem:
        return self.__crs

    def setOrigin(self, origin: QgsPoint):
        self.__origin = origin

    def getOrigin(self) -> QgsPoint:
        return self.__origin

    def getOrigin(self) -> QgsPoint:
        return self.__origin

    def setNCols(self, nCols: int):
        if(nCols < 1):
            raise Exception("Number of columns lower than 1")
        self.__nCols = nCols

    def getNCols(self) -> int:
        return self.__nCols

    def setNRows(self, nRows: int):
        if(nRows < 1):
            raise Exception("Number of rows lower than 1")
        self.__nRows = nRows

    def getNRows(self) -> int:
        return self.__nRows

    def setColSpacing(self, colSpacing: float):
        if(colSpacing <= 0):
            raise Exception("Column spacing not greater than 0")
        self.__colSpacing = colSpacing

    def getColSpacing(self) -> float:
        return self.__colSpacing

    def setRowSpacing(self, rowSpacing: float):
        if(rowSpacing < 0):
            raise Exception("Row spacing not greater than 0")
        self.__rowSpacing = rowSpacing

    def getRowSpacing(self) -> float:
        return self.__rowSpacing

    def setAngle(self, angle: float):
        self.__angle = angle

    def getAngle(self) -> float:
        return self.__angle
    
    def setPoints(self, points: list[list[QgsPoint]]):
        self.__points = points

    def getPoints(self) -> list[list[QgsPoint]]:
        return self.__points
    
    def renderPoints(self):
        origin = self.getOrigin()
        originX = origin.x()
        originY = origin.y()
        nX = self.getNCols() + 1
        nY = self.getNRows() + 1
        colSpacing = self.getColSpacing()
        rowSpacing = self.getRowSpacing()
        angle = self.getAngle()

        for y in range(nY):
            offsetY = rowSpacing * y
            points = []
            for x in range(nX):
                offsetX = colSpacing * x
                point = QgsPoint(originX + offsetX, originY + offsetY)
                point = rotate(point, origin, angle)
                points.append(point)
            self.__points.append(points)
    
    def setPolygons(self, polygons: list[list[QgsPolygon]]):
        self.__polygons = polygons

    def getPolygons(self) -> list[list[QgsPolygon]]:
        return self.__polygons

    def renderPolygons(self):
        nCols = self.getNCols()
        nRows = self.getNRows()

        self.renderPoints()
        points = self.getPoints()

        for row in range(nRows):
            polygons = []
            for col in range(nCols):
                a = points[row][col]
                b = points[row][col + 1]
                c = points[row + 1][col + 1]
                d = points[row + 1][col]
                line = QgsLineString([a, b, c, d])
                polygon = QgsPolygon(line)
                polygons.append(polygon)
            self.__polygons.append(polygons)

    def toQgsVectorLayer(self, layerName:str) -> QgsVectorLayer:
        layer = QgsVectorLayer("Polygon?crs=" + self.getCrs().geographicCrsAuthId(), layerName, "memory")
        provider = layer.dataProvider()
        features = []

        self.renderPolygons()
        polygons = self.getPolygons()
        nCols = self.getNCols()
        nRows = self.getNRows()

        for row in range(nRows):
            for col in range(nCols):
                feature = QgsFeature()
                feature.setGeometry(polygons[row][col])
                features += [feature]
        provider.addFeatures(features)
        layer.updateExtents()
        return layer

def rotate(point: QgsPoint, origin: QgsPoint, angle: float) -> QgsPoint:
    cos = math.cos(math.radians(angle))
    sin = math.sin(math.radians(angle))
    x = point.x()
    y = point.y()
    xOrigin = origin.x()
    yOrigin = origin.y()

    xRot = xOrigin + cos * (x - xOrigin) - sin * (y - yOrigin)
    yRot = yOrigin + sin * (x - xOrigin) + cos * (y - yOrigin)
    pointRot = QgsPoint(xRot, yRot)
    return pointRot