from qgis.PyQt.QtCore import QObject, pyqtSignal
from .grid_layout import GridRegularLayout
from .grid_double_field import GridGreaterThanZeroDoubleField
from qgis.PyQt.QtWidgets import QLabel, QSpinBox


class GridRegularLayoutField(QObject):
    filled = pyqtSignal(bool)

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

    def setColSpacingField(self, f: GridGreaterThanZeroDoubleField):
        f.filled.connect(self.fieldFilled)
        self.__colSpacingField = f

    def getColSpacingField(self) -> GridGreaterThanZeroDoubleField:
        return self.__colSpacingField

    def setRowSpacingField(self, f: GridGreaterThanZeroDoubleField):
        f.filled.connect(self.fieldFilled)
        self.__rowSpacingField = f

    def getRowSpacingField(self) -> GridGreaterThanZeroDoubleField:
        return self.__rowSpacingField

    def setSpacingLabel(self, l: QLabel):
        self.__spacingLabel = l

    def getSpacingLabel(self) -> QLabel:
        return self.__spacingLabel

    def fieldFilled(self, filled: bool):
        if not filled:
            self.filled.emit(False)
        else:
            self.filled.emit(self.isFilled())

    def isFilled(self) -> bool:
        fields = [self.getColSpacingField(),
                  self.getRowSpacingField()]

        for field in fields:
            if not field.isFilled():
                return False
        return True

    def setVisible(self, v: bool):
        items = [self.getColSpacingField(),
                 self.getRowSpacingField(),
                 self.getSpacingLabel()]
        
        for item in items:
            item.setVisible(v)
        
        if v:
            self.filled.emit(self.isFilled())
    
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