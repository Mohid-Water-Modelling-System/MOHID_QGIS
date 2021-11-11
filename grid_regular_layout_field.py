from qgis.PyQt.QtCore import QObject, pyqtSignal
from .grid_layout import GridRegularLayout
from .grid_double_field import GridGreaterThanZeroDoubleField
from qgis.PyQt.QtWidgets import QLabel, QSpinBox

"""
The GridRegularLayoutField class handles the fields of the GridTool for setting
the layout of a regular spaced grid.
With this field the user specifies the number of columns and rows as well as their spacings.
This class is a child of QObject to be able to have a pyqtSignal attribute.
The GridRegularLayoutField is only visible when the radioButtonRegular is checked.
"""
class GridRegularLayoutField(QObject):
    """
    The filled attribute is a signal that emits a boolean value when the state of the field changes.
    If the field is correctly filled, true is emitted.
    If the field becomes not correctly filled, false is emitted.
    """
    filled = pyqtSignal(bool)

    """
    The constructor of the GridRegularLayoutField receives:
        - a field for entering the quantity of columns
        - a field for entering the quantity of rows
        - a field for entering the spacing of the columns
        - a field for entering the spacing of the rows
        - the label that heads the spacing fields
    """
    def __init__(self, colQuantityField: QSpinBox, rowQuantityField: QSpinBox,
                 colSpacingField: GridGreaterThanZeroDoubleField, rowSpacingField: GridGreaterThanZeroDoubleField,
                 spacingLabel: QLabel):
        super().__init__()

        self.setColQuantityField(colQuantityField)
        self.setRowQuantityField(rowQuantityField)
        self.setColSpacingField(colSpacingField)
        self.setRowSpacingField(rowSpacingField)
        self.setSpacingLabel(spacingLabel)

    def setColQuantityField(self, f: QSpinBox):
        self.__colQuantityField = f

    def getColQuantityField(self) -> QSpinBox:
        return self.__colQuantityField

    def setRowQuantityField(self, f: QSpinBox):
        self.__rowQuantityField = f

    def getRowQuantityField(self) -> QSpinBox:
        return self.__rowQuantityField

    """
    The ColSpacingField setter receives a GridGreaterThanZeroDoubleField object and connects
    its filled signal to the fieldFilled function.
    When the text of the GridGreaterThanZeroDoubleField changes, the fieldFilled function is called.
    """
    def setColSpacingField(self, f: GridGreaterThanZeroDoubleField):
        f.filled.connect(self.fieldFilled)
        self.__colSpacingField = f

    def getColSpacingField(self) -> GridGreaterThanZeroDoubleField:
        return self.__colSpacingField

    """
    The RowSpacingField setter receives a GridGreaterThanZeroDoubleField object and connects
    its filled signal to the fieldFilled function.
    When the text of the GridGreaterThanZeroDoubleField changes, the fieldFilled function is called.
    """
    def setRowSpacingField(self, f: GridGreaterThanZeroDoubleField):
        f.filled.connect(self.fieldFilled)
        self.__rowSpacingField = f

    def getRowSpacingField(self) -> GridGreaterThanZeroDoubleField:
        return self.__rowSpacingField

    def setSpacingLabel(self, l: QLabel):
        self.__spacingLabel = l

    def getSpacingLabel(self) -> QLabel:
        return self.__spacingLabel

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
    The isFilled function returns true if the column spacing and row spacing fields are both 
    filled with  an acceptable value and false otherwise.
    """
    def isFilled(self) -> bool:
        fields = [self.getColSpacingField(),
                  self.getRowSpacingField()]

        for field in fields:
            if not field.isFilled():
                return False
        return True

    """
    The setVisible function displays the regular column spacing field, the row
    spacing field and the label if the "v" argument
    is true and hides them if the "v" argument is false.
    This is used when the user selects which type of grid is being constructed.
    If the grid is regular these items are displayed.
    If the grid is variable, they are hidden.
    """
    def setVisible(self, v: bool):
        items = [self.getColSpacingField(),
                 self.getRowSpacingField(),
                 self.getSpacingLabel()]
        
        for item in items:
            item.setVisible(v)
        
        if v:
            self.filled.emit(self.isFilled())
    
    """
    The get layout function builds GridRegularLayout from the settings entered in the field.
    (the number of columns, number of rows, spacing of the columns, spacing of the rows) 
    """
    def getLayout(self) -> GridRegularLayout:
        colQuantityField = self.getColQuantityField()
        rowQuantityField = self.getRowQuantityField()
        colSpacingField = self.getColSpacingField()
        rowSpacingField = self.getRowSpacingField()

        nCols = colQuantityField.value()
        nRows = rowQuantityField.value()
        colSpacing = colSpacingField.getValue()
        rowSpacing = rowSpacingField.getValue()

        layout = GridRegularLayout(nCols, nRows, colSpacing, rowSpacing)
        return layout