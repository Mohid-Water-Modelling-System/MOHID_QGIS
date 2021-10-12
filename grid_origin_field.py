from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.core import QgsPointXY
from .grid_double_field import GridDoubleField
from .capture_point_tool import CapturePointTool
from .point import Point

class GridOriginField(QObject):
    filled = pyqtSignal(bool)

    def __init__(self, latitudeField: GridDoubleField, longitudeField: GridDoubleField, capturePointTool: CapturePointTool):
        super().__init__()
        self.setLatitudeField(latitudeField)
        self.setLongitudeField(longitudeField)
        self.setCapturePointTool(capturePointTool)

    def setLatitudeField(self, l: GridDoubleField):
        l.filled.connect(self.fieldFilled)
        self.__latitudeField = l
    
    def getLatitudeField(self) -> GridDoubleField:
        return self.__latitudeField
    
    def setLongitudeField(self, l: GridDoubleField):
        self.__longitudeField = l
    
    def getLongitudeField(self) -> GridDoubleField:
        return self.__longitudeField
    
    def setCapturePointTool(self, t: CapturePointTool):
        t.canvasClicked.connect(self.capturePointToolCanvasClicked)
        self.__capturePointTool = t
    
    def getCapturePointTool(self) -> CapturePointTool:
        return self.__capturePointTool
    
    def capturePointToolCanvasClicked(self, point: QgsPointXY):
        latitudeField = self.getLatitudeField()
        longitudeField = self.getLongitudeField()

        latitudeField.setValue(point.x())
        longitudeField.setValue(point.y())
    
    def fieldFilled(self, filled: bool):
        if not filled:
            self.filled.emit(False)
        else:
            self.filled.emit(self.isFilled())
    
    def isFilled(self) -> bool:
        fields = [self.getLatitudeField(),
                  self.getLongitudeField()]
        
        for field in fields:
            if not field.isFilled():
                return False
            
        return True
    
    def getOrigin(self) -> Point:
        latitudeField = self.getLatitudeField()
        longitudeField = self.getLongitudeField()

        x = latitudeField.getValue()
        y = longitudeField.getValue()

        origin = Point(x, y)
        return origin