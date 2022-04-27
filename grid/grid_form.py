from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.gui import QgsProjectionSelectionWidget
from .grid_origin_field import GridOriginField
from .grid_double_field import GridDoubleField
from .grid_layout_field import GridLayoutField
from .grid_layer_name_field import GridLayerNameField
from .grid import Grid
from .crs import CRS
from .angle import Angle


"""
The GridForm class is handles all the fields of the form of the GridTool.
This class is a child of QObject to be able to have a pyqtSignal attribute.
"""
class GridForm(QObject):
    """
    The filled attribute is a signal that emits a boolean value when the state of the form changes.
    If the form is correctly filled, true is emitted.
    If the form becomes not correctly filled, false is emitted.
    """
    filled = pyqtSignal(bool)

    """
    The GridForm constructor receives:
        - the field for selecting the Coordinate Reference System 
        - the field for selecting the origin coordinates
        - the field for entering the angle of the grid
        - the field for specifying the layout of the grid (columns and rows and respective spacings)
        - the field for entering the name of the grid to visualize
    """
    def __init__(self, crsField: QgsProjectionSelectionWidget, originField: GridOriginField, angleField: GridDoubleField,
                 layoutField: GridLayoutField, layerNameField: GridLayerNameField):
        super().__init__()
        self.setCrsField(crsField)
        self.setOriginField(originField)
        self.setAngleField(angleField)
        self.setLayoutField(layoutField)
        self.setLayerNameField(layerNameField)

    """
    The CrsField setter receives a QgsProjectionSelectionWidget object and connects its crsChanged
    signal to the crsFieldChanged function.
    When the Coordinate Reference System changes, the crsFieldChanged function is called.
    """
    def setCrsField(self, f: QgsProjectionSelectionWidget):
        f.crsChanged.connect(self.crsFieldChanged)
        self.__crsField = f

    def getCrsField(self) -> QgsProjectionSelectionWidget:
        return self.__crsField
    
    """
    The crsFieldChanged function is called when the user changes the Coordinate Reference System
    in the GridTool.
    This function configures the CapturePointTool of the originField to retreive points in the
    Coordinate Reference System of that was selected.
    """
    def crsFieldChanged(self):
        crsField = self.getCrsField()
        crs = CRS(crsField.crs())

        originField = self.getOriginField()
        capturePointTool = originField.getCapturePointTool()
        capturePointTool.setCrs(crs)

    """
    The OriginField setter receives a GridOriginField object and connects its "filled"
    signal to the fieldFilled function.
    When the origin coordinates are changed, the fieldFilled function is called.
    """
    def setOriginField(self, f: GridOriginField):
        f.filled.connect(self.fieldFilled)
        self.__originField = f

    def getOriginField(self) -> GridOriginField:
        return self.__originField

    """
    The AngleField setter receives a GridDoubleField object and connects its "filled"
    signal to the fieldFilled function.
    When the content of the field changes, the fieldFilled function is called.
    """
    def setAngleField(self, f: GridDoubleField):
        f.filled.connect(self.fieldFilled)
        self.__angleField = f

    def getAngleField(self) -> GridDoubleField:
        return self.__angleField

    """
    The LayoutField setter receives a GridLayoutField object and connects its "filled"
    signal to the fieldFilled function.
    When the content of the layout field changes, the fieldFilled function is called.
    """
    def setLayoutField(self, f: GridLayoutField):
        f.filled.connect(self.fieldFilled)
        self.__layoutField = f

    def getLayoutField(self) -> GridLayoutField:
        return self.__layoutField

    """
    The LayerNameField setter receives a GridLayerNameField object and connects its "filled"
    signal to the fieldFilled function.
    When the name of the layer changes, the fieldFilled function is called.
    """
    def setLayerNameField(self, f: GridLayerNameField):
        f.filled.connect(self.fieldFilled)
        self.__layerNameField = f

    def getLayerNameField(self) -> GridLayerNameField:
        return self.__layerNameField

    """
    The fieldFilled function is called when the content of any field of the form is changed.
    If the fieldFilled function was called when the content of a field was modified to a not
    acceptable value, then the signal "filled" is emitted with the value false.
    Otherwise the function checks if all the other fields of the form are correctly filled and
    emits the signal "filled" with a bollean that is true when all fields are correctly filled
    and false otherwise.
    """
    def fieldFilled(self, filled: bool):
        if not filled:
            self.filled.emit(False)
        else:
            self.filled.emit(self.isFilled())

    """
    The isFilled function returns true if the fields for origin, the angle, the layout
    and the layer name are all filled with an acceptable value and false otherwise.
    """
    def isFilled(self) -> bool:
        fields = [self.getOriginField(),
                  self.getAngleField(),
                  self.getLayoutField(),
                  self.getLayerNameField()]

        for field in fields:
            if not field.isFilled():
                return False
        return True

    """
    The toGrid function creates a Grid from the data specified in the gridForm.
    """
    def toGrid(self) -> Grid:
        crsField = self.getCrsField()
        originField = self.getOriginField()
        angleField = self.getAngleField()
        layoutField = self.getLayoutField()

        crs = CRS(crsField.crs())
        origin = originField.getOrigin()
        angle = Angle(angleField.getValue())
        layout = layoutField.getLayout()

        grid = Grid(crs, origin, angle, layout)
        return grid

    """
    The close function deactivates the CapturePointTool of the OriginField.
    This function is called when the plugin is closed.
    """
    def close(self):
        f = self.getOriginField()
        f.close()