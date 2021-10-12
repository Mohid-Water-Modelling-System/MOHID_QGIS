from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.core import QgsPointXY, Qgis, QgsMessageLog

from .grid_double_field import GridDoubleField
from .capture_point_tool import CapturePointTool
from .point import Point

class GridOriginField(QObject):
    filled = pyqtSignal(bool)

    def __init__(self, latitudeField: GridDoubleField, longitudeField: GridDoubleField, capturePointTool: CapturePointTool):
        QgsMessageLog.logMessage("GridOriginField: initiating", 'MOHID plugin', level=Qgis.Info)
        super().__init__()
        self.setLatitudeField(latitudeField)
        self.setLongitudeField(longitudeField)
        self.setCapturePointTool(capturePointTool)

    def setLatitudeField(self, l: GridDoubleField):
        QgsMessageLog.logMessage("GridOriginField: set latitudeField", 'MOHID plugin', level=Qgis.Info)
        l.filled.connect(self.fieldFilled)
        self.__latitudeField = l
    
    def getLatitudeField(self) -> GridDoubleField:
        QgsMessageLog.logMessage("GridOriginField: get latitudeField", 'MOHID plugin', level=Qgis.Info)
        return self.__latitudeField
    
    def setLongitudeField(self, l: GridDoubleField):
        QgsMessageLog.logMessage("GridOriginField: set longitudeField", 'MOHID plugin', level=Qgis.Info)
        self.__longitudeField = l
    
    def getLongitudeField(self) -> GridDoubleField:
        QgsMessageLog.logMessage("GridOriginField: get longitudeField", 'MOHID plugin', level=Qgis.Info)
        return self.__longitudeField
    
    def setCapturePointTool(self, t: CapturePointTool):
        QgsMessageLog.logMessage("GridOriginField: set capturePointTool", 'MOHID plugin', level=Qgis.Info)
        t.canvasClicked.connect(self.capturePointToolCanvasClicked)
        self.__capturePointTool = t
    
    def getCapturePointTool(self) -> CapturePointTool:
        QgsMessageLog.logMessage("GridOriginField: get capturePointTool", 'MOHID plugin', level=Qgis.Info)
        return self.__capturePointTool
    
    def capturePointToolCanvasClicked(self, point: QgsPointXY):
        QgsMessageLog.logMessage("GridOriginField: capturePointTool canvas clicked", 'MOHID plugin', level=Qgis.Info)
        latitudeField = self.getLatitudeField()
        longitudeField = self.getLongitudeField()

        latitudeField.setValue(point.x())
        longitudeField.setValue(point.y())
    
    def fieldFilled(self, filled: bool):
        QgsMessageLog.logMessage("GridOriginField: field filled", 'MOHID plugin', level=Qgis.Info)
        if not filled:
            self.filled.emit(False)
        else:
            self.filled.emit(self.isFilled())
    
    def isFilled(self) -> bool:
        QgsMessageLog.logMessage("GridOriginField: checking if field is filled", 'MOHID plugin', level=Qgis.Info)
        fields = [self.getLatitudeField(),
                  self.getLongitudeField()]
        
        for field in fields:
            if not field.isFilled():
                return False
            
        return True
    
    def getOrigin(self) -> Point:
        QgsMessageLog.logMessage("GridOriginField: get origin", 'MOHID plugin', level=Qgis.Info)
        latitudeField = self.getLatitudeField()
        longitudeField = self.getLongitudeField()

        x = latitudeField.getValue()
        y = longitudeField.getValue()

        origin = Point(x, y)
        return origin