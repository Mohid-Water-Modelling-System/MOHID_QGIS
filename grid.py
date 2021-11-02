from qgis.core import QgsVectorLayer, QgsFeature
from .grid_layout import GridLayout
from .point import Origin
from .crs import CRS
from .angle import Angle


# TODO: Remove MohidGridLayer string and bind object instance to layer
class Grid:
    MohidGridLayer = "MohidGridLayer"

    def __init__(self, crs: CRS, origin: Origin, angle: Angle, layout: GridLayout):
        self.setCrs(crs)
        self.setOrigin(origin)
        self.setAngle(angle)
        self.setLayout(layout)

    def setCrs(self, crs: CRS):
        self.__crs = crs

    def getCrs(self) -> CRS:
        return self.__crs

    def setOrigin(self, o: Origin):
        self.__origin = o

    def getOrigin(self) -> Origin:
        return self.__origin

    def setAngle(self, a: Angle):
        self.__angle = a

    def getAngle(self) -> Angle:
        return self.__angle

    def setLayout(self, l: GridLayout):
        self.__layout = l

    def getLayout(self) -> GridLayout:
        return self.__layout

    def toQgsVectorLayer(self, layerName: str) -> QgsVectorLayer:
        crsId = self.getCrs().authid()
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

        layout = self.getLayout()
        origin = self.getOrigin()
        angle = self.getAngle()
        cells = layout.toCells(origin, angle)

        for row in cells:
            for cell in row:
                feature = QgsFeature()
                polygon = cell.toQgsPolygon()
                feature.setGeometry(polygon)
                features += [feature]
        provider.addFeatures(features)
        layer.updateExtents()

    def toString(self, config: dict) -> str:
        origin = self.getOrigin()
        angle = self.getAngle()
        crs = self.getCrs()
        layout = self.getLayout()

        output = origin.toString(config) + angle.toString(config) \
            + crs.toString(config) + layout.toString(config)

        return output