from qgis.PyQt.QtCore import QObject, pyqtSignal
from .grid_double_field import GridGreaterThanZeroDoubleField

"""
The GridVariableSpacingField class is the class used to define a spacing range for the layout of grid items (rows or columns).
This class is used by GridItemAdder to build the layout of a variable spaced grid.
This class is a child of QObject to be able to have a pyqtSignal attribute.
GridVariableSpacingFields are only visible when the radioButtonVariableSpaced is checked.
"""
class GridVariableSpacingField(QObject):
    """
    The filled attribute is a signal that emits a boolean value when the state of the field changes.
    If the field is correctly filled, true is emitted.
    If the field becomes not correctly filled, false is emitted.
    """
    filled = pyqtSignal(bool)

    """
    The constructor of the GridVariableSpacingField receives:
        - a field for setting the spacing at the first item of the set (a set of rows or columns)
        - a field for setting the spacing at the last item of the set (a set of rows or columns)
    """
    def __init__(self, spacingStartField: GridGreaterThanZeroDoubleField, spacingEndField: GridGreaterThanZeroDoubleField):
        super().__init__()
        self.setSpacingStartField(spacingStartField)
        self.setSpacingEndField(spacingEndField)

    """
    The SpacingStartField setter receives a GridGreaterThanZeroDoubleField object and connects
    its filled signal to the fieldFilled function.
    When the value entered in the GridGreaterThanZeroDoubleField changes, the fieldFilled function is called.
    """
    def setSpacingStartField(self, f: GridGreaterThanZeroDoubleField):
        f.filled.connect(self.fieldFilled)
        self.__spacingStartField = f

    def getSpacingStartField(self) -> GridGreaterThanZeroDoubleField:
        return self.__spacingStartField
    
    """
    The setSpacingEndField setter receives a GridGreaterThanZeroDoubleField object and connects
    its filled signal to the fieldFilled function.
    When the value entered in the GridGreaterThanZeroDoubleField changes, the fieldFilled function is called.
    """
    def setSpacingEndField(self, f: GridGreaterThanZeroDoubleField):
        f.filled.connect(self.fieldFilled)
        self.__spacingEndField = f

    def getSpacingEndField(self) -> GridGreaterThanZeroDoubleField:
        return self.__spacingEndField
    
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
    The isFilled function returns true if both the SpacingStartField and the SpacingEndField are
    filled with a number greater than 0 and false otherwise.
    """
    def isFilled(self) -> bool:
        fields = [self.getSpacingStartField(),
                  self.getSpacingEndField()]
        
        for field in fields:
            if not field.isFilled():
                return False
        
        return True

    """
    The setVisible function displays the SpacingStartField and the SpacingEndField
    if the "v" argument is true and hides them if the "v" argument is false.
    This is used when the user selects which type of grid is being constructed.
    If the grid is variable these items are displayed.
    If the grid is regular, they are hidden.
    """
    def setVisible(self, v: bool):
        items = [self.getSpacingStartField(),
                  self.getSpacingEndField()]
        
        for item in items:
            item.setVisible(v)
        
        if v:
            self.filled.emit(self.isFilled())