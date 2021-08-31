from qgis.PyQt.QtWidgets import QTableWidget, QTableWidgetItem, QLineEdit, QToolButton, QSpinBox
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QObject, pyqtSignal
from .greater_than_zero_double_validator import GreaterThanZeroDoubleValidator
from .layout import Layout

class LayoutBuilder(QObject):
    layoutChanged = pyqtSignal()
    def __init__(self, tableWidget: QTableWidget,
                 spinBoxColQuantity: QSpinBox, spinBoxRowQuantity: QSpinBox,
                 lineEditColSpacingStart: QLineEdit, lineEditColSpacingEnd: QLineEdit,
                 lineEditRowSpacingStart: QLineEdit, lineEditRowSpacingEnd: QLineEdit,
                 toolButtonAddCols: QToolButton, toolButtonAddRows: QToolButton):
        super().__init__()
        self.setTableWidget(tableWidget)
        self.setSpinBoxColQuantity(spinBoxColQuantity)
        self.setSpinBoxRowQuantity(spinBoxRowQuantity)
        self.setLineEditColSpacingStart(lineEditColSpacingStart)
        self.setLineEditColSpacingEnd(lineEditColSpacingEnd)
        self.setLineEditRowSpacingStart(lineEditRowSpacingStart)
        self.setLineEditRowSpacingEnd(lineEditRowSpacingEnd)
        self.setToolButtonAddCols(toolButtonAddCols)
        self.setToolButtonAddRows(toolButtonAddRows)
        
        layout = Layout()
        self.setLayout(layout)

    def setTableWidget(self, t: QTableWidget):
        labels = ["Quantity", "Type", "Spacing"]
        columnCount = len(labels)
        t.setColumnCount(columnCount)
        t.setHorizontalHeaderLabels(labels)
        self.__tableWidget = t

    def getTableWidget(self) -> QTableWidget:
        return self.__tableWidget
    
    def addItemToTableWidget(self, n: int, type: str, spacingStart: float, spacingEnd: float):
        if n < 1 :
            raise Exception("Quantity lower than 1")
        elif spacingStart <= 0 :
            raise Exception("Spacing start not greater than 0")
        elif spacingEnd <= 0 :
            raise Exception("Spacing end not greater than 0")

        table = self.getTableWidget()
        rowCount = table.rowCount()
        colCount = table.columnCount()

        items = [QTableWidgetItem(str(n)),
                 QTableWidgetItem(type),
                 QTableWidgetItem(str(spacingStart) + " to " + str(spacingEnd))]

        table.insertRow(rowCount)
        for col in range(colCount):
            item = items[col]
            table.setItem(rowCount, col, item)
    
    def setSpinBoxRowQuantity(self, s: QSpinBox):
        self.__spinBoxRowQuantity = s
    
    def getSpinBoxRowQuantity(self) -> QSpinBox:
        return self.__spinBoxRowQuantity

    def setSpinBoxColQuantity(self, s: QSpinBox):
        self.__spinBoxColQuantity = s
    
    def getSpinBoxColQuantity(self) -> QSpinBox:
        return self.__spinBoxColQuantity

    def setLineEditColSpacingStart(self, l: QLineEdit):
        validator = GreaterThanZeroDoubleValidator(l)
        l.setValidator(validator)
        l.textChanged.connect(self.updateToolButtonAddCols)
        self.__lineEditColSpacingStart = l

    def getLineEditColSpacingStart(self) -> QLineEdit:
        return self.__lineEditColSpacingStart

    def setLineEditColSpacingEnd(self, l: QLineEdit):
        validator = GreaterThanZeroDoubleValidator(l)
        l.setValidator(validator)
        l.textChanged.connect(self.updateToolButtonAddCols)
        self.__lineEditColSpacingEnd = l

    def getLineEditColSpacingEnd(self) -> QLineEdit:
        return self.__lineEditColSpacingEnd

    def setLineEditRowSpacingStart(self, l: QLineEdit):
        validator = GreaterThanZeroDoubleValidator(l)
        l.setValidator(validator)
        l.textChanged.connect(self.updateToolButtonAddRows)
        self.__lineEditRowSpacingStart = l

    def getLineEditRowSpacingStart(self) -> QLineEdit:
        return self.__lineEditRowSpacingStart

    def setLineEditRowSpacingEnd(self, l: QLineEdit):
        validator = GreaterThanZeroDoubleValidator(l)
        l.setValidator(validator)
        l.textChanged.connect(self.updateToolButtonAddRows)
        self.__lineEditRowSpacingEnd = l

    def getLineEditRowSpacingEnd(self) -> QLineEdit:
        return self.__lineEditRowSpacingEnd

    def setToolButtonAddCols(self, b: QToolButton):
        icon = QIcon(":images/themes/default/mActionAdd.svg")
        b.setIcon(icon)
        b.clicked.connect(self.toolButtonAddColsClicked)
        self.__toolButtonAddCols = b

    def getToolButtonAddCols(self) -> QToolButton:
        return self.__toolButtonAddCols
    
    def updateToolButtonAddCols(self):
        toolButtonAddCols = self.getToolButtonAddCols()
        lineEditColSpacingStart = self.getLineEditColSpacingStart()
        lineEditColSpacingEnd = self.getLineEditColSpacingEnd()
        
        enabled = True
        lineEdits = [lineEditColSpacingStart, lineEditColSpacingEnd]

        for lineEdit in lineEdits:
            if not lineEdit.hasAcceptableInput():
                enabled = False
                break
        toolButtonAddCols.setEnabled(enabled)

    def toolButtonAddColsClicked(self):
        spinBoxColQuantity = self.getSpinBoxColQuantity()
        lineEditColSpacingStart = self.getLineEditColSpacingStart()
        lineEditColSpacingEnd = self.getLineEditColSpacingEnd()
        layout = self.getLayout()

        n = spinBoxColQuantity.value()
        spacingStart = float(lineEditColSpacingStart.text())
        spacingEnd = float(lineEditColSpacingEnd.text())
        layout.addCols(n, spacingStart, spacingEnd)
        self.addItemToTableWidget(n, "Column", spacingStart, spacingEnd)
        self.layoutChanged.emit()

    def setToolButtonAddRows(self, b: QToolButton):
        icon = QIcon(":images/themes/default/mActionAdd.svg")
        b.setIcon(icon)
        b.clicked.connect(self.toolButtonAddRowsClicked)
        self.__toolButtonAddRows = b

    def getToolButtonAddRows(self) -> QToolButton:
        return self.__toolButtonAddRows
    
    def updateToolButtonAddRows(self):
        toolButtonAddRows = self.getToolButtonAddRows()
        lineEditRowSpacingStart = self.getLineEditRowSpacingStart()
        lineEditRowSpacingEnd = self.getLineEditRowSpacingEnd()
        
        enabled = True
        lineEdits = [lineEditRowSpacingStart, lineEditRowSpacingEnd]

        for lineEdit in lineEdits:
            if not lineEdit.hasAcceptableInput():
                enabled = False
                break
        toolButtonAddRows.setEnabled(enabled)

    def toolButtonAddRowsClicked(self):
        spinBoxRowQuantity = self.getSpinBoxRowQuantity()
        lineEditRowSpacingStart = self.getLineEditRowSpacingStart()
        lineEditRowSpacingEnd = self.getLineEditRowSpacingEnd()
        layout = self.getLayout()

        n = spinBoxRowQuantity.value()
        spacingStart = float(lineEditRowSpacingStart.text())
        spacingEnd = float(lineEditRowSpacingEnd.text())
        layout.addRows(n, spacingStart, spacingEnd)
        self.addItemToTableWidget(n, "Row", spacingStart, spacingEnd)
        self.layoutChanged.emit()
    
    def setLayout(self, l: Layout):
        self.__layout = l
    
    def getLayout(self) -> Layout:
        return self.__layout