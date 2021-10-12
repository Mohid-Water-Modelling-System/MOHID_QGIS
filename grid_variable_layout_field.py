from qgis.PyQt.QtWidgets import QTableWidget, QTableWidgetItem, QToolButton, QSpinBox, QLabel
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QObject, pyqtSignal
from .grid_double_field import GridGreaterThanZeroDoubleField
from .grid_variable_layout import GridVariableLayout
from .grid_item_layout import GridItemLayout, GridColLayout, GridRowLayout


class GridVariableLayoutField(QObject):
    filled = pyqtSignal(bool)

    def __init__(self, tableWidget: QTableWidget,
                 colQuantityField: QSpinBox, rowQuantityField: QSpinBox,
                 colSpacingStartField: GridGreaterThanZeroDoubleField, colSpacingEndField: GridGreaterThanZeroDoubleField,
                 rowSpacingStartField: GridGreaterThanZeroDoubleField, rowSpacingEndField: GridGreaterThanZeroDoubleField,
                 toolButtonAddCols: QToolButton, toolButtonAddRows: QToolButton, spacingLabel: QLabel):
        super().__init__()

        self.setTableWidget(tableWidget)
        self.setColQuantityField(colQuantityField)
        self.setRowQuantityField(rowQuantityField)
        self.setColSpacingStartField(colSpacingStartField)
        self.setColSpacingEndField(colSpacingEndField)
        self.setRowSpacingStartField(rowSpacingStartField)
        self.setRowSpacingEndField(rowSpacingEndField)
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
    
    def setColSpacingStartField(self, f: GridGreaterThanZeroDoubleField):
        f.filled.connect(self.colSpacingFieldFilled)
        self.__colSpacingStartField = f

    def getColSpacingStartField(self) -> GridGreaterThanZeroDoubleField:
        return self.__colSpacingStartField
    
    def setColSpacingEndField(self, f: GridGreaterThanZeroDoubleField):
        f.filled.connect(self.colSpacingFieldFilled)
        self.__colSpacingEndField = f

    def getColSpacingEndField(self) -> GridGreaterThanZeroDoubleField:
        return self.__colSpacingEndField
    
    def colSpacingFieldFilled(self, filled: bool):
        b = self.getToolButtonAddCols()
        if not filled:
            b.setEnabled(False)
        else:
            b.setEnabled(self.colSpacingFieldIsFilled())
    
    def colSpacingFieldIsFilled(self) -> bool:
        fields = [self.getColSpacingStartField(),
                  self.getColSpacingEndField()]

        for field in fields:
            if not field.isFilled():
                return False
        return True

    def setRowSpacingStartField(self, f: GridGreaterThanZeroDoubleField):
        f.filled.connect(self.rowSpacingFieldFilled)
        self.__rowSpacingStartField = f

    def getRowSpacingStartField(self) -> GridGreaterThanZeroDoubleField:
        return self.__rowSpacingStartField
    
    def setRowSpacingEndField(self, f: GridGreaterThanZeroDoubleField):
        f.filled.connect(self.rowSpacingFieldFilled)
        self.__rowSpacingEndField = f

    def getRowSpacingEndField(self) -> GridGreaterThanZeroDoubleField:
        return self.__rowSpacingEndField

    def rowSpacingFieldFilled(self, filled: bool):
        b = self.getToolButtonAddRows()
        if not filled:
            b.setEnabled(False)
        else:
            b.setEnabled(self.rowSpacingFieldIsFilled())
    
    def rowSpacingFieldIsFilled(self) -> bool:
        fields = [self.getRowSpacingStartField(),
                  self.getRowSpacingEndField()]

        for field in fields:
            if not field.isFilled():
                return False
        return True

    def setToolButtonAddCols(self, b: QToolButton):
        icon = QIcon(":images/themes/default/mActionAdd.svg")
        b.setIcon(icon)
        b.clicked.connect(self.toolButtonAddColsClicked)
        self.__toolButtonAddCols = b

    def getToolButtonAddCols(self) -> QToolButton:
        return self.__toolButtonAddCols

    def toolButtonAddColsClicked(self):
        colQuantityField = self.getColQuantityField()
        colSpacingStartField = self.getColSpacingStartField()
        colSpacingEndField = self.getColSpacingEndField()

        n = colQuantityField.value()
        spacingStart = colSpacingStartField.getValue()
        spacingEnd = colSpacingEndField.getValue()

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
        rowQuantityField = self.getRowQuantityField()
        rowSpacingStartField = self.getRowSpacingStartField()
        rowSpacingEndField = self.getRowSpacingEndField()

        n = rowQuantityField.value()
        spacingStart = rowSpacingStartField.getValue()
        spacingEnd = rowSpacingEndField.getValue()

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
                 self.getColSpacingStartField(),
                 self.getColSpacingEndField(),
                 self.getRowSpacingStartField(),
                 self.getRowSpacingEndField(),
                 self.getToolButtonAddCols(),
                 self.getToolButtonAddRows(),
                 self.getSpacingLabel()]
        
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