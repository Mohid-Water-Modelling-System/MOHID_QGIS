from qgis.PyQt.QtCore import QObject, pyqtSignal
from .grid_regular_layout import GridRegularLayout
from .grid_double_field import GridGreaterThanZeroDoubleField
from qgis.PyQt.QtWidgets import QLabel, QSpinBox
from qgis.core import Qgis, QgsMessageLog


class GridRegularLayoutField(QObject):
    filled = pyqtSignal(bool)

    def __init__(self, colQuantityField: QSpinBox, rowQuantityField: QSpinBox,
                 colSpacingField: GridGreaterThanZeroDoubleField, rowSpacingField: GridGreaterThanZeroDoubleField,
                 spacingLabel: QLabel):
        QgsMessageLog.logMessage("GridRegularLayoutField: initiating", 'MOHID plugin', level=Qgis.Info)
        super().__init__()

        self.setColQuantityField(colQuantityField)
        self.setRowQuantityField(rowQuantityField)
        self.setColSpacingField(colSpacingField)
        self.setRowSpacingField(rowSpacingField)
        self.setSpacingLabel(spacingLabel)

    def setColQuantityField(self, f: QSpinBox):
        QgsMessageLog.logMessage("GridRegularLayoutField: set colQuantityField", 'MOHID plugin', level=Qgis.Info)
        self.__colQuantityField = f

    def getColQuantityField(self) -> QSpinBox:
        QgsMessageLog.logMessage("GridRegularLayoutField: get colQuantityField", 'MOHID plugin', level=Qgis.Info)
        return self.__colQuantityField

    def setRowQuantityField(self, f: QSpinBox):
        QgsMessageLog.logMessage("GridRegularLayoutField: set rowQuantityField", 'MOHID plugin', level=Qgis.Info)
        self.__rowQuantityField = f

    def getRowQuantityField(self) -> QSpinBox:
        QgsMessageLog.logMessage("GridRegularLayoutField: get rowQuantityField", 'MOHID plugin', level=Qgis.Info)
        return self.__rowQuantityField

    def setColSpacingField(self, f: GridGreaterThanZeroDoubleField):
        QgsMessageLog.logMessage("GridRegularLayoutField: set colSpacingField", 'MOHID plugin', level=Qgis.Info)
        f.filled.connect(self.fieldFilled)
        self.__colSpacingField = f

    def getColSpacingField(self) -> GridGreaterThanZeroDoubleField:
        QgsMessageLog.logMessage("GridRegularLayoutField: get colSpacingField", 'MOHID plugin', level=Qgis.Info)
        return self.__colSpacingField

    def setRowSpacingField(self, f: GridGreaterThanZeroDoubleField):
        QgsMessageLog.logMessage("GridRegularLayoutField: set rowSpacingField", 'MOHID plugin', level=Qgis.Info)
        f.filled.connect(self.fieldFilled)
        self.__rowSpacingField = f

    def getRowSpacingField(self) -> GridGreaterThanZeroDoubleField:
        QgsMessageLog.logMessage("GridRegularLayoutField: get rowSpacingField", 'MOHID plugin', level=Qgis.Info)
        return self.__rowSpacingField

    def setSpacingLabel(self, l: QLabel):
        QgsMessageLog.logMessage("GridRegularLayoutField: set spacingLabel", 'MOHID plugin', level=Qgis.Info)
        self.__spacingLabel = l

    def getSpacingLabel(self) -> QLabel:
        QgsMessageLog.logMessage("GridRegularLayoutField: get spacingLabel", 'MOHID plugin', level=Qgis.Info)
        return self.__spacingLabel

    def fieldFilled(self, filled: bool):
        QgsMessageLog.logMessage("GridRegularLayoutField: field is filled", 'MOHID plugin', level=Qgis.Info)
        if not filled:
            self.filled.emit(False)
        else:
            self.filled.emit(self.isFilled())

    def isFilled(self) -> bool:
        QgsMessageLog.logMessage("GridRegularLayoutField: checking if field is filled", 'MOHID plugin', level=Qgis.Info)
        fields = [self.getColSpacingField(),
                  self.getRowSpacingField()]

        for field in fields:
            if not field.isFilled():
                return False
        return True

    def setVisible(self, v: bool):
        QgsMessageLog.logMessage("GridRegularLayoutField: set visible", 'MOHID plugin', level=Qgis.Info)
        items = [self.getColSpacingField(),
                 self.getRowSpacingField(),
                 self.getSpacingLabel()]
        
        for item in items:
            item.setVisible(v)
        
        if v:
            self.filled.emit(self.isFilled())
    
    def getLayout(self) -> GridRegularLayout:
        QgsMessageLog.logMessage("GridRegularLayoutField: get layout", 'MOHID plugin', level=Qgis.Info)
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