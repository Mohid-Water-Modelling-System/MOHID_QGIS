from qgis.PyQt.QtWidgets import QLabel
from qgis.PyQt.QtCore import QObject, pyqtSignal
from .grid_layout import GridVariableLayout
from .grid_item_layout import GridColLayout, GridRowLayout
from .grid_item_adder import GridColAdder, GridRowAdder
from .grid_layout_table import GridLayoutTable


class GridVariableLayoutField(QObject):
    filled = pyqtSignal(bool)

    def __init__(self, layoutTable: GridLayoutTable, spacingLabel: QLabel,
                 colAdder: GridColAdder, rowAdder: GridRowAdder):
        super().__init__()

        self.setLayoutTable(layoutTable)
        self.setSpacingLabel(spacingLabel)
        self.setColAdder(colAdder)
        self.setRowAdder(rowAdder)

    def setLayoutTable(self, t: GridLayoutTable):
        t.filled.connect(self.fieldFilled)
        self.__layoutTable = t
    
    def getLayoutTable(self) -> GridLayoutTable:
        return self.__layoutTable

    def setSpacingLabel(self, l: QLabel):
        self.__spacingLabel = l

    def getSpacingLabel(self) -> QLabel:
        return self.__spacingLabel
    
    def setColAdder(self, a: GridColAdder):
        a.adderButtonClicked.connect(self.colAdderButtonClicked)
        self.__colAdder = a

    def getColAdder(self) -> GridColAdder:
        return self.__colAdder
    
    def setRowAdder(self, a: GridRowAdder):
        a.adderButtonClicked.connect(self.rowAdderButtonClicked)
        self.__rowAdder = a

    def getRowAdder(self) -> GridRowAdder:
        return self.__rowAdder

    def colAdderButtonClicked(self, l: GridColLayout):
        t = self.getLayoutTable()
        t.addColLayout(l)
    
    def rowAdderButtonClicked(self, l: GridRowLayout):
        t = self.getLayoutTable()
        t.addRowLayout(l)

    def setVisible(self, v: bool):
        items = [self.getLayoutTable(),
                 self.getSpacingLabel(),
                 self.getColAdder(),
                 self.getRowAdder()]

        for item in items:
            item.setVisible(v)

    def fieldFilled(self, filled: bool):
        if not filled:
            self.filled.emit(False)
        else:
            self.filled.emit(self.isFilled())

    def isFilled(self) -> bool:
        t = self.getLayoutTable()
        return t.isFilled()

    def getLayout(self) -> GridVariableLayout:
        t = self.getLayoutTable()
        colLayouts = t.getColLayouts()
        rowLayouts = t.getRowLayouts()
        l = GridVariableLayout(colLayouts, rowLayouts)
        return l