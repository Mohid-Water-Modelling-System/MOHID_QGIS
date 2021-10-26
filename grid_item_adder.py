from qgis.PyQt.QtWidgets import QToolButton, QSpinBox
from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.PyQt.QtGui import QIcon
from .grid_variable_spacing_field import GridVariableSpacingField
from .grid_item_layout import GridItemLayout, GridColLayout, GridRowLayout


class GridItemAdder(QObject):
    adderButtonClicked = pyqtSignal(GridItemLayout)

    def __init__(self, quantityField: QSpinBox, spacingField: GridVariableSpacingField, btn: QToolButton):
        super().__init__()

        self.setQuantityField(quantityField)
        self.setSpacingField(spacingField)
        self.setButton(btn)

    def setQuantityField(self, f: QSpinBox):
        self.__quantityField = f

    def getQuantityField(self) -> QSpinBox:
        return self.__quantityField
    
    def setSpacingField(self, f: GridVariableSpacingField):
        f.filled.connect(self.fieldFilled)
        self.__spacingField = f

    def getSpacingField(self) -> GridVariableSpacingField:
        return self.__spacingField

    def fieldFilled(self, filled: bool):
        b = self.getButton()
        b.setEnabled(filled)

    def setButton(self, b: QToolButton):
        icon = QIcon(":images/themes/default/mActionAdd.svg")
        b.setIcon(icon)
        b.clicked.connect(self.buttonClicked)
        self.__button = b

    def getButton(self) -> QToolButton:
        return self.__button

    def getItemLayout(self) -> GridItemLayout:
        pass

    def buttonClicked(self):
        l = self.getItemLayout()
        self.adderButtonClicked.emit(l)

    def setVisible(self, v: bool):
        items = [self.getSpacingField(),
                 self.getButton()]
        
        for item in items:
            item.setVisible(v)

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