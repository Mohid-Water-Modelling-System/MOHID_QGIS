from qgis.PyQt.QtCore import QObject, pyqtSignal
from .grid_double_field import GridGreaterThanZeroDoubleField

class GridVariableSpacingField(QObject):
    filled = pyqtSignal(bool)

    def __init__(self, spacingStartField: GridGreaterThanZeroDoubleField, spacingEndField: GridGreaterThanZeroDoubleField):
        super().__init__()
        self.setSpacingStartField(spacingStartField)
        self.setSpacingEndField(spacingEndField)

    def setSpacingStartField(self, f: GridGreaterThanZeroDoubleField):
        f.filled.connect(self.fieldFilled)
        self.__spacingStartField = f

    def getSpacingStartField(self) -> GridGreaterThanZeroDoubleField:
        return self.__spacingStartField
    
    def setSpacingEndField(self, f: GridGreaterThanZeroDoubleField):
        f.filled.connect(self.fieldFilled)
        self.__spacingEndField = f

    def getSpacingEndField(self) -> GridGreaterThanZeroDoubleField:
        return self.__spacingEndField
    
    def fieldFilled(self, filled: bool):
        if not filled:
            self.filled.emit(False)
        else:
            self.filled.emit(self.isFilled())
    
    def isFilled(self) -> bool:
        fields = [self.getSpacingStartField(),
                  self.getSpacingEndField()]
        
        for field in fields:
            if not field.isFilled():
                return False
        
        return True

    def setVisible(self, v: bool):
        items = [self.getSpacingStartField(),
                  self.getSpacingEndField()]
        
        for item in items:
            item.setVisible(v)
        
        if v:
            self.filled.emit(self.isFilled())