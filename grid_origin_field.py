from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.core import QgsPointXY
from .grid_double_field import GridDoubleField
from .capture_point_tool import CapturePointTool
from .point import Origin

"""
The GridOriginField class handles the fields of the GridTool for setting the coordinates of the
origin of the grid. This class also manages the capturePointTool used to get coordinates from the
map with a mouse click.
This class is a child of QObject to be able to have a pyqtSignal attribute.
"""
class GridOriginField(QObject):
    """
    The filled attribute is a signal that emits a boolean value when the state of the field changes.
    If the field is correctly filled, true is emitted.
    If the field becomes not correctly filled, false is emitted.
    """
    filled = pyqtSignal(bool)

    """
    The constructor of the GridOriginField receives:
        - a field for entering the latitude
        - a field for entering the longitude
        - a capturePointTool for setting the latitude and the longitude with a mouse click
    """
    def __init__(self, latitudeField: GridDoubleField, longitudeField: GridDoubleField, capturePointTool: CapturePointTool):
        super().__init__()
        self.setLatitudeField(latitudeField)
        self.setLongitudeField(longitudeField)
        self.setCapturePointTool(capturePointTool)

    """
    The LatitudeField setter receives a GridDoubleField object and connects
    its filled signal to the fieldFilled function.
    When the content of the LatitudeField changes, the fieldFilled function is called.
    """
    def setLatitudeField(self, l: GridDoubleField):
        l.filled.connect(self.fieldFilled)
        self.__latitudeField = l
    
    def getLatitudeField(self) -> GridDoubleField:
        return self.__latitudeField
    
    """
    The LongitudeField setter receives a GridDoubleField object and connects
    its filled signal to the fieldFilled function.
    When the content of the LongitudeField changes, the fieldFilled function is called.
    """
    def setLongitudeField(self, l: GridDoubleField):
        l.filled.connect(self.fieldFilled)
        self.__longitudeField = l
    
    def getLongitudeField(self) -> GridDoubleField:
        return self.__longitudeField
    
    """
    The CapturePointTool setter receives a CapturePointTool object and connects
    its canvasClicked signal to the capturePointToolCanvasClicked function.
    When the content of the tool is armed and the a point in the canvas is clicked,
    the capturePointToolCanvasClicked function is called.
    """
    def setCapturePointTool(self, t: CapturePointTool):
        t.canvasClicked.connect(self.capturePointToolCanvasClicked)
        self.__capturePointTool = t
    
    def getCapturePointTool(self) -> CapturePointTool:
        return self.__capturePointTool
    
    """
    When the capturePointTool is activated and a the user clicks on a point on the map, the
    capturePointToolCanvasClicked is called with a signal that emits the point that was clicked
    as an argument of the function.
    The coordinates of this point are then written to the latitude and longitude fields of the
    GridTool.
    """
    def capturePointToolCanvasClicked(self, point: QgsPointXY):
        latitudeField = self.getLatitudeField()
        longitudeField = self.getLongitudeField()

        latitudeField.setValue(point.x())
        longitudeField.setValue(point.y())
    
    """
    The fieldFilled function is called when the filled signal of a field emits a new state.
    If the state is false, it means that the field was correctly field and became unfilled.
    In this case the fieldFilled function emits a filled signal with false too.
    Otherwise it checks whether everything is filled with an acceptable input and emits a signal
    that can either be true or false.
    """
    def fieldFilled(self, filled: bool):
        if not filled:
            self.filled.emit(False)
        else:
            self.filled.emit(self.isFilled())
    
    """
    The isFilled function returns true if the latitude and longitude fields are both filled with 
    an acceptable value and false otherwise.
    """
    def isFilled(self) -> bool:
        fields = [self.getLatitudeField(),
                  self.getLongitudeField()]
        
        for field in fields:
            if not field.isFilled():
                return False
            
        return True
    
    """
    The getOrigin function reads the longitude and latitude values from the corresponding fields
    and creates a Origin object with these coordinates. An origin object is a point (the bottom
    left point of the grid).
    """    
    def getOrigin(self) -> Origin:
        latitudeField = self.getLatitudeField()
        longitudeField = self.getLongitudeField()

        x = latitudeField.getValue()
        y = longitudeField.getValue()

        origin = Origin(x, y)
        return origin
    
    """
    The close function deactivates the CapturePointTool.
    This function is called when the plugin is closed.
    """
    def close(self):
        t = self.getCapturePointTool()
        t.close()