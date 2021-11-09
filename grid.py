from qgis.core import QgsVectorLayer, QgsFeature
from .grid_layout import GridLayout
from .point import Origin
from .crs import CRS
from .angle import Angle


# TODO: Remove MohidGridLayer string and bind object instance to layer
"""
The Grid class implements the grid.
A layer can be obtained from this class to display a grid in QGIS interface.
Also, a string can be obtained from this class to write the grid in MOHID format
"""
class Grid:
    MohidGridLayer = "MohidGridLayer"

    """
    The constructor of the Grid class receives:
        - the Coordinate Reference System in which the cells of the grid are represented
        - the coordinates of the origin of the grid (bottom-left point)
        - the angle of the grid, that defines how the grid is rotated around the origin 
        - the layout of the grid, which can be regular or variable. The layout specifies how many
        rows and columns the grid has and what is the spacing between them.
    """
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

    """
    The toQgsVectorLayer function creates a Qgis Vector layer to display the grid in the
    interface map.
    The function receives the name of the layer as argument. This name will appear in the list of
    layers in the Qgis interface.
    After populating the layer with the polygons that represent the grid cells, this function
    labels this layer with the custom property "MohidGridLayer: True" to identify the type of layer
    from the list of layers.
    """
    def toQgsVectorLayer(self, layerName: str) -> QgsVectorLayer:
        crsId = self.getCrs().authid()
        layer = QgsVectorLayer("Polygon?crs=" + crsId, layerName, "memory")
        self.populateQgsVectorLayer(layer)
        layer.setCustomProperty(Grid.MohidGridLayer, True)
        return layer

    """
    The updateQgsVectorLayer function erases the cells of the grid layer and populates the layer
    new cells. This is useful when the user changes the properties of an existing layer.
    """
    def updateQgsVectorLayer(self, layer: QgsVectorLayer):
        provider = layer.dataProvider()
        provider.truncate()
        self.populateQgsVectorLayer(layer)
        layer.reload()

    """
    The populateQgsVectorLayer creates the grid cells from the layout, the origin and the angle
    and populates the layer with a QgsPolygon representing each cell.
    """
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

    """
    The toString function is used to write the grid in the MOHID format.
    The string is built according to the first argument of the function, which is
    the configuration provided in form of a dictionary.
    This configuration was previously read from the config.json file.
    """
    def toString(self, config: dict) -> str:
        origin = self.getOrigin()
        angle = self.getAngle()
        crs = self.getCrs()
        layout = self.getLayout()

        output = origin.toString(config) + angle.toString(config) \
            + crs.toString(config) + layout.toString(config)

        return output