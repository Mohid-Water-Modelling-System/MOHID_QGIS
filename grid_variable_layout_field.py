from qgis.PyQt.QtWidgets import QTableWidget, QTableWidgetItem, QToolButton, QSpinBox, QLabel
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QObject, pyqtSignal
from .grid_variable_spacing_field import GridVariableSpacingField
from .grid_variable_layout import GridVariableLayout
from .grid_item_layout import GridColLayout, GridRowLayout


class GridVariableLayoutField(QObject):
    filled = pyqtSignal(bool)

    def __init__(self, tableWidget: QTableWidget, layoutLabel: QLabel,
                 colQuantityField: QSpinBox, rowQuantityField: QSpinBox,
                 colSpacingField: GridVariableSpacingField, rowSpacingField: GridVariableSpacingField,
                 toolButtonAddCols: QToolButton, toolButtonAddRows: QToolButton, spacingLabel: QLabel):
        super().__init__()

        self.setTableWidget(tableWidget)
        self.setLayoutLabel(layoutLabel)
        self.setColQuantityField(colQuantityField)
        self.setRowQuantityField(rowQuantityField)
        self.setColSpacingField(colSpacingField)
        self.setRowSpacingField(rowSpacingField)
        self.setToolButtonAddCols(toolButtonAddCols)
        self.setToolButtonAddRows(toolButtonAddRows)
        self.setSpacingLabel(spacingLabel)
        self.__itemlayouts = []

    def setTableWidget(self, t: QTableWidget):
        labels = ["Quantity", "Type", "Spacing", ""]
        columnCount = len(labels)
        t.setColumnCount(columnCount)
        t.setHorizontalHeaderLabels(labels)
        self.__tableWidget = t

    def getTableWidget(self) -> QTableWidget:
        return self.__tableWidget
    
    def setLayoutLabel(self, l: QLabel):
        self.__layoutLabel = l

    def getLayoutLabel(self) -> QLabel:
        return self.__layoutLabel

    def addItemToTableWidget(self, n: int, type: str, spacingStart: float, spacingEnd: float):
        if n < 1:
            raise Exception("Quantity lower than 1")
        elif spacingStart <= 0:
            raise Exception("Spacing start not greater than 0")
        elif spacingEnd <= 0:
            raise Exception("Spacing end not greater than 0")

        table = self.getTableWidget()
        rowCount = table.rowCount()
        colCount = table.columnCount()

        items = [QTableWidgetItem(str(n)),
                 QTableWidgetItem(type),
                 QTableWidgetItem(str(spacingStart) + " to " + str(spacingEnd))]

        table.insertRow(rowCount)
        for col in range(colCount - 1):
            item = items[col]
            table.setItem(rowCount, col, item)

        b = QToolButton(table)
        icon = QIcon(":images/themes/default/mActionRemove.svg")
        b.setIcon(icon)
        table.setCellWidget(rowCount, colCount - 1, b)
        table.resizeColumnToContents(colCount - 1)

    def setColQuantityField(self, f: QSpinBox):
        self.__colQuantityField = f

    def getColQuantityField(self) -> QSpinBox:
        return self.__colQuantityField

    def setRowQuantityField(self, f: QSpinBox):
        self.__rowQuantityField = f

    def getRowQuantityField(self) -> QSpinBox:
        return self.__rowQuantityField
    
    def setColSpacingField(self, f: GridVariableSpacingField):
        f.filled.connect(self.colSpacingFieldFilled)
        self.__colSpacingField = f

    def getColSpacingField(self) -> GridVariableSpacingField:
        return self.__colSpacingField

    def colSpacingFieldFilled(self, filled: bool):
        b = self.getToolButtonAddCols()
        b.setEnabled(filled)

    def setRowSpacingField(self, f: GridVariableSpacingField):
        f.filled.connect(self.rowSpacingFieldFilled)
        self.__rowSpacingField = f

    def getRowSpacingField(self) -> GridVariableSpacingField:
        return self.__rowSpacingField

    def rowSpacingFieldFilled(self, filled: bool):
        b = self.getToolButtonAddRows()
        b.setEnabled(filled)

    def setToolButtonAddCols(self, b: QToolButton):
        icon = QIcon(":images/themes/default/mActionAdd.svg")
        b.setIcon(icon)
        b.clicked.connect(self.toolButtonAddColsClicked)
        self.__toolButtonAddCols = b

    def getToolButtonAddCols(self) -> QToolButton:
        return self.__toolButtonAddCols

    def toolButtonAddColsClicked(self):
        quantityField = self.getColQuantityField()
        spacingField = self.getColSpacingField()
        spacingStartField = spacingField.getSpacingStartField()
        spacingEndField = spacingField.getSpacingEndField()

        n = quantityField.value()
        spacingStart = spacingStartField.getValue()
        spacingEnd = spacingEndField.getValue()

        colLayout = GridColLayout(n, spacingStart, spacingEnd)
        self.__itemlayouts.append(colLayout)

        self.addItemToTableWidget(n, "Column", spacingStart, spacingEnd)
        self.fieldFilled(True)

    def setToolButtonAddRows(self, b: QToolButton):
        icon = QIcon(":images/themes/default/mActionAdd.svg")
        b.setIcon(icon)
        b.clicked.connect(self.toolButtonAddRowsClicked)
        self.__toolButtonAddRows = b

    def getToolButtonAddRows(self) -> QToolButton:
        return self.__toolButtonAddRows

    def toolButtonAddRowsClicked(self):
        quantityField = self.getRowQuantityField()
        spacingField = self.getRowSpacingField()
        spacingStartField = spacingField.getSpacingStartField()
        spacingEndField = spacingField.getSpacingEndField()

        n = quantityField.value()
        spacingStart = spacingStartField.getValue()
        spacingEnd = spacingEndField.getValue()

        rowLayout = GridRowLayout(n, spacingStart, spacingEnd)
        self.__itemlayouts.append(rowLayout)

        self.addItemToTableWidget(n, "Row", spacingStart, spacingEnd)
        self.fieldFilled(True)

    def setSpacingLabel(self, l: QLabel):
        self.__spacingLabel = l

    def getSpacingLabel(self) -> QLabel:
        return self.__spacingLabel

    def setVisible(self, v: bool):
        items = [self.getTableWidget(),
                 self.getColSpacingField(),
                 self.getRowSpacingField(),
                 self.getToolButtonAddCols(),
                 self.getToolButtonAddRows(),
                 self.getSpacingLabel(),
                 self.getLayoutLabel()]
        
        for item in items:
            item.setVisible(v)
        
        if v:
            self.filled.emit(self.isFilled())
    
    def fieldFilled(self, filled: bool):
        if not filled:
            self.filled.emit(False)
        else:
            self.filled.emit(self.isFilled())

    def isFilled(self) -> bool:
        colLayouts = []
        rowLayouts = []
        for il in self.__itemlayouts:
            if isinstance(il, GridColLayout):
                colLayouts.append(il)
            elif isinstance(il, GridRowLayout):
                rowLayouts.append(il)
        
        filled = bool(colLayouts) and bool(rowLayouts)
        return filled
    
    def getLayout(self) -> GridVariableLayout:
        colLayouts = []
        rowLayouts = []
        for il in self.__itemlayouts:
            if isinstance(il, GridColLayout):
                colLayouts.append(il)
            elif isinstance(il, GridRowLayout):
                rowLayouts.append(il)
        
        l = GridVariableLayout(colLayouts, rowLayouts)
        return l