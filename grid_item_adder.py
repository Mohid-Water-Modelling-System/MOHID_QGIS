from qgis.PyQt.QtWidgets import QToolButton, QSpinBox
from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.PyQt.QtGui import QIcon
from .grid_variable_spacing_field import GridVariableSpacingField
from .grid_item_layout import GridItemLayout, GridColLayout, GridRowLayout

"""
The GridItemAdder class is the class used to had rows or columns to the layout of a variable spaced
grid.
It handles a field with the quantity of items to add, the spacing of the items and a button to
add the items to the layout which is displayed in the layout table.
"""
class GridItemAdder(QObject):
    """
    The adderButtonClicked attribute is a signal that emits the layout of the added item
    when the add butteon is pressed by the user.
    """
    adderButtonClicked = pyqtSignal(GridItemLayout)

    """
    The GridItemAdder constructor receives:
        - a field for the user to enters the quantity of items (rows or columns) to add to the layout.
        - a field where the used enters the spacing of the items.
        - a add button to add the items with the specified layout (quantity and spacing) to the grid
        layout
    """
    def __init__(self, quantityField: QSpinBox, spacingField: GridVariableSpacingField, btn: QToolButton):
        super().__init__()

        self.setQuantityField(quantityField)
        self.setSpacingField(spacingField)
        self.setButton(btn)

    def setQuantityField(self, f: QSpinBox):
        self.__quantityField = f

    def getQuantityField(self) -> QSpinBox:
        return self.__quantityField
    
    """
    The SpacingField setter receives a GridVariableSpacingField object and connects its "filled"
    signal to the fieldFilled function.
    When the spacing is changed, the fieldFilled function is called.
    """
    def setSpacingField(self, f: GridVariableSpacingField):
        f.filled.connect(self.fieldFilled)
        self.__spacingField = f

    def getSpacingField(self) -> GridVariableSpacingField:
        return self.__spacingField

    def fieldFilled(self, filled: bool):
        b = self.getButton()
        b.setEnabled(filled)

    """
    The button setter receives a QToolButton object and connects its clicked signal
    to the buttonClicked function.
    When the button is clicked, the buttonClicked function is called.
    """
    def setButton(self, b: QToolButton):
        icon = QIcon(":images/themes/default/mActionAdd.svg")
        b.setIcon(icon)
        b.clicked.connect(self.buttonClicked)
        self.__button = b

    def getButton(self) -> QToolButton:
        return self.__button

    def getItemLayout(self) -> GridItemLayout:
        pass

    """
    The buttonClicked function is called when the button is clicked.
    This function retrieves an item layout (which can be a set of rows or columns)
    and emits it to be added to the grid layout.
    """
    def buttonClicked(self):
        l = self.getItemLayout()
        self.adderButtonClicked.emit(l)

    """
    The setVisible function displays the variable spacing field and the button if the "v" argument
    is true and hides them if the "v" argument is false.
    This is used when the user selects which type of grid is being constructed.
    If the grid is regular the variable spacing field and the button are hidden.
    If the grid is variable, they are displayed.
    """
    def setVisible(self, v: bool):
        items = [self.getSpacingField(),
                 self.getButton()]
        
        for item in items:
            item.setVisible(v)

"""
The GridColAdder class is a child of the GridItemAdder class.
It does everything the GridItemAdder class does and implements a itemLayout getter that retrieves
a GridColLayout object.
Thus this class is the GridItemAdder for columns.
"""
class GridColAdder(GridItemAdder):
    def getItemLayout(self) -> GridColLayout:  
        quantityField = self.getQuantityField()
        spacingField = self.getSpacingField()
        spacingStartField = spacingField.getSpacingStartField()
        spacingEndField = spacingField.getSpacingEndField()

        n = quantityField.value()
        spacingStart = spacingStartField.getValue()
        spacingEnd = spacingEndField.getValue()

        l = GridColLayout(n, spacingStart, spacingEnd)
        return l

"""
The GridRowAdder class is a child of the GridItemAdder class.
It does everything the GridItemAdder class does and implements an itemLayout getter that retrieves
a GridRowLayout object.
Thus this class is the GridItemAdder for rows.
"""
class GridRowAdder(GridItemAdder):
    def getItemLayout(self) -> GridRowLayout:  
        quantityField = self.getQuantityField()
        spacingField = self.getSpacingField()
        spacingStartField = spacingField.getSpacingStartField()
        spacingEndField = spacingField.getSpacingEndField()

        n = quantityField.value()
        spacingStart = spacingStartField.getValue()
        spacingEnd = spacingEndField.getValue()

        l = GridRowLayout(n, spacingStart, spacingEnd)
        return l