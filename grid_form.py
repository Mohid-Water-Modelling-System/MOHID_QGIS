from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.gui import QgsProjectionSelectionWidget
from .grid_origin_field import GridOriginField
from .grid_double_field import GridDoubleField
from .grid_layout_field import GridLayoutField
from .grid_layer_name_field import GridLayerNameField
from .grid import Grid

class GridForm(QObject):
    filled = pyqtSignal(bool)

    def __init__(self, crsField: QgsProjectionSelectionWidget, originField: GridOriginField, angleField: GridDoubleField,
                 layoutField: GridLayoutField, layerNameField: GridLayerNameField):
        super().__init__()
        self.setCrsField(crsField)
        self.setOriginField(originField)
        self.setAngleField(angleField)
        self.setLayoutField(layoutField)
        self.setLayerNameField(layerNameField)

    def setCrsField(self, f: QgsProjectionSelectionWidget):
        f.crsChanged.connect(self.crsFieldChanged)
        self.__crsField = f

    def getCrsField(self) -> QgsProjectionSelectionWidget:
        return self.__crsField
    
    def crsFieldChanged(self):
        crsField = self.getCrsField()
        crs = crsField.crs()

        originField = self.getOriginField()
        capturePointTool = originField.getCapturePointTool()
        capturePointTool.setCrs(crs)

    def setOriginField(self, f: GridOriginField):
        f.filled.connect(self.fieldFilled)
        self.__originField = f

    def getOriginField(self) -> GridOriginField:
        return self.__originField

    def setAngleField(self, f: GridDoubleField):
        f.filled.connect(self.fieldFilled)
        self.__angleField = f

    def getAngleField(self) -> GridDoubleField:
        return self.__angleField

    def setLayoutField(self, f: GridLayoutField):
        f.filled.connect(self.fieldFilled)
        self.__layoutField = f

    def getLayoutField(self) -> GridLayoutField:
        return self.__layoutField

    def setLayerNameField(self, f: GridLayerNameField):
        f.filled.connect(self.fieldFilled)
        self.__layerNameField = f

    def getLayerNameField(self) -> GridLayerNameField:
        return self.__layerNameField

    def fieldFilled(self, filled: bool):
        if not filled:
            self.filled.emit(False)
        else:
            self.filled.emit(self.isFilled())

    def isFilled(self) -> bool:
        fields = [self.getOriginField(),
                  self.getAngleField(),
                  self.getLayoutField(),
                  self.getLayerNameField()]

        for field in fields:
            if not field.isFilled():
                return False
        return True

    def toGrid(self) -> Grid:
        crsField = self.getCrsField()
        originField = self.getOriginField()
        angleField = self.getAngleField()
        layoutField = self.getLayoutField()

        crs = crsField.crs()
        origin = originField.getOrigin()
        angle = angleField.getValue()
        layout = layoutField.getLayout()

        grid = Grid(crs, origin, angle, layout)
        return grid
