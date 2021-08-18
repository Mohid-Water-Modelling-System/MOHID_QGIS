from qgis.core import QgsCoordinateReferenceSystem, QgsVectorLayer, QgsFeature
from .cell import Cell


class Grid:
    def __init__(self, crs: QgsCoordinateReferenceSystem, cells: list[list[Cell]]):
        self.setCrs(crs)
        self.setCells(cells)

    def setCrs(self, crs: QgsCoordinateReferenceSystem):
        self.__crs = crs

    def getCrs(self) -> QgsCoordinateReferenceSystem:
        return self.__crs

    def setCells(self, cells: list[list[Cell]]):
        self.__cells = cells

    def getCells(self) -> list[list[Cell]]:
        return self.__cells

    def toQgsVectorLayer(self, layerName: str) -> QgsVectorLayer:
        crsId = self.getCrs().geographicCrsAuthId()
        layer = QgsVectorLayer("Polygon?crs=" + crsId, layerName, "memory")
        provider = layer.dataProvider()
        features = []
        cells = self.getCells()

        for row in cells:
            for cell in row:
                feature = QgsFeature()
                polygon = cell.toQgsPolygon()
                feature.setGeometry(polygon)
                features += [feature]
        provider.addFeatures(features)
        layer.updateExtents()
        return layer
