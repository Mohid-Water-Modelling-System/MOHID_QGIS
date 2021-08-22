from qgis.core import QgsCoordinateReferenceSystem, QgsVectorLayer, QgsFeature
from .cell import Cell


class Grid:
    MohidGridLayer = "MohidGridLayer"
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
        self.populateQgsVectorLayer(layer)
        layer.setCustomProperty(Grid.MohidGridLayer, True)
        return layer
    
    def updateQgsVectorLayer(self, layer: QgsVectorLayer):
        provider = layer.dataProvider()
        provider.truncate()
        self.populateQgsVectorLayer(layer)
        layer.reload()
    
    def populateQgsVectorLayer(self, layer: QgsVectorLayer):
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