from qgis.core import QgsVectorLayer, QgsFeature
from .grid_layout import GridLayout, GridRegularLayout, GridVariableLayout
from .point import Origin
from .crs import CRS
from .angle import Angle
from .gridUtils import loadFromFile


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
    def __init__(self, crs: CRS = None, origin: Origin = None, angle: Angle =None, layout: GridLayout =None):
        if crs is not None:
            self.setCrs(crs)
        if origin is not None:
            self.setOrigin(origin)
        if angle is not None:
            self.setAngle(angle)
        if layout is not None:
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
        upperRightCorner = layout.toPoints(origin, angle)[-1][-1]
        lon = (origin.x() + upperRightCorner.x()) / 2.0
        lat = (origin.y() + upperRightCorner.y()) / 2.0
        output = origin.toString(config) + angle.toString(config) \
            + crs.toString(config) + layout.toString(config)
        output += f"LATITUDE               : {lat}\n"
        output += f"LONGITUDE              : {lon}\n"
        
        if isinstance(layout, GridVariableLayout):
            DX, DY = layout.offsets()

            output += "\n\n"
            output += "<BeginXX>\n"
            for p in DX:
                output += f"{p:.15f}\n"
            output += "<EndXX>\n"

            output += "<BeginYY>\n"
            for p in DY:
                output += f"{p:.15f}\n"
            output += "<EndYY>\n"

        return output
    
    def fromGridFile(self, gridFile):
        
        try:
            gridData = loadFromFile(gridFile)
        except:
            raise ValueError
            #TODO: missing important parameter
            # min max rows and columns must be present
            # send popup message

        # Go through every line
        if gridData['SRID'] is not None:
            self.setCrs(CRS(gridData['SRID']))
        if gridData['ORIGIN_X'] is not None:
            originX = gridData['ORIGIN_X']
        if gridData['ORIGIN_Y'] is not None:
            originY = gridData['ORIGIN_Y']
        if gridData['GRID_ANGLE'] is not None:
            self.setAngle(gridData['GRID_ANGLE'])
        if gridData['COORD_TIP'] is not None:
            coordTip = gridData['COORD_TIP']
        self.setOrigin(Origin(originX, originY))

        # Get x axis
        if gridData['CONSTANT_SPACING_X'] and gridData['CONSTANT_SPACING_Y']:
            # set regular layout
            nCols = gridData['JUB'] - gridData['JLB'] + 1
            nRows = gridData['IUB'] - gridData['ILB'] + 1
            layout = GridRegularLayout(nCols, nRows, gridData['DX'], gridData['DY'])
        else:
            # set variable 
            raise NotImplementedError

        # Get Y axis
        self.setLayout(layout)
