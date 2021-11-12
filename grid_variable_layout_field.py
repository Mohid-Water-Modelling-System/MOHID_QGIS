from qgis.PyQt.QtWidgets import QLabel
from qgis.PyQt.QtCore import QObject, pyqtSignal
from .grid_layout import GridVariableLayout
from .grid_item_layout import GridColLayout, GridRowLayout
from .grid_item_adder import GridColAdder, GridRowAdder
from .grid_layout_table import GridLayoutTable

"""
The GridVariableLayoutField class handles the fields of the GridTool for setting
the layout of a variable spaced grid.
With this field the user specifies the number of columns and rows as well as their spacings.
This class is a child of QObject to be able to have a pyqtSignal attribute.
The GridVariableLayoutField is only visible when the radioButtonVariableSpaced is checked.
"""
class GridVariableLayoutField(QObject):
    """
    The filled attribute is a signal that emits a boolean value when the state of the field changes.
    If the field is correctly filled, true is emitted.
    If the field becomes not correctly filled, false is emitted.
    """
    filled = pyqtSignal(bool)

    """
    The constructor of the GridVariableLayoutField receives:
        - a table for registering and displaying the layout built by the user
        - a label saying "Spacing Range" that heads the fields for entering the spacing
        - a tool to add columns (specifying their quantity and spacing range)
        - a tool to add rows (specifying their quantity and spacing range)
    """
    def __init__(self, layoutTable: GridLayoutTable, spacingLabel: QLabel,
                 colAdder: GridColAdder, rowAdder: GridRowAdder):
        super().__init__()

        self.setLayoutTable(layoutTable)
        self.setSpacingLabel(spacingLabel)
        self.setColAdder(colAdder)
        self.setRowAdder(rowAdder)

    """
    The LayoutTable setter receives a GridLayoutTable object and connects
    its filled signal to the fieldFilled function.
    When the layout registered on the LayoutTable is changed, the fieldFilled function is called.
    """
    def setLayoutTable(self, t: GridLayoutTable):
        t.filled.connect(self.fieldFilled)
        self.__layoutTable = t
    
    def getLayoutTable(self) -> GridLayoutTable:
        return self.__layoutTable

    def setSpacingLabel(self, l: QLabel):
        self.__spacingLabel = l

    def getSpacingLabel(self) -> QLabel:
        return self.__spacingLabel
    
    """
    The ColAdder setter receives a GridColAdder object and connects
    its adderButtonClicked signal to the colAdderButtonClicked function.
    When the ColAdder button is clicked, the colAdderButtonClicked function is called.
    """
    def setColAdder(self, a: GridColAdder):
        a.adderButtonClicked.connect(self.colAdderButtonClicked)
        self.__colAdder = a

    def getColAdder(self) -> GridColAdder:
        return self.__colAdder
    
    """
    The RowAdder setter receives a GridRowAdder object and connects
    its rowAdderButtonClicked signal to the rowAdderButtonClicked function.
    When the RowAdder button is clicked, the crowdderButtonClicked function is called.
    """
    def setRowAdder(self, a: GridRowAdder):
        a.adderButtonClicked.connect(self.rowAdderButtonClicked)
        self.__rowAdder = a

    def getRowAdder(self) -> GridRowAdder:
        return self.__rowAdder

    """
    The colAdderButtonClicked function is called when the button of the colAdder is clicked.
    The colAdder emits a signal with the a GridColLayout that this function registers in the layoutTable.
    """
    def colAdderButtonClicked(self, l: GridColLayout):
        t = self.getLayoutTable()
        t.addColLayout(l)

    """
    The rowAdderButtonClicked function is called when the button of the rowAdder is clicked.
    The rowAdder emits a signal with the a GridRowLayout that this function registers in the layoutTable.
    """    
    def rowAdderButtonClicked(self, l: GridRowLayout):
        t = self.getLayoutTable()
        t.addRowLayout(l)

    """
    The setVisible function displays the layout table, the "spacing range" label and the column and row adders
    if the "v" argument is true and hides them if the "v" argument is false.
    This is used when the user selects which type of grid is being constructed.
    If the grid is variable these items are displayed.
    If the grid is regular, they are hidden.
    """
    def setVisible(self, v: bool):
        items = [self.getLayoutTable(),
                 self.getSpacingLabel(),
                 self.getColAdder(),
                 self.getRowAdder()]

        for item in items:
            item.setVisible(v)

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
    The isFilled function returns true if the layout registered in the layoutTable is acceptable, i.e.
    has both columns and rows.
    """
    def isFilled(self) -> bool:
        t = self.getLayoutTable()
        return t.isFilled()

    """
    The get layout function builds GridVariableLayout from the settings entered in the field.
    (the layout of the columns and the layout of the rows) 
    """
    def getLayout(self) -> GridVariableLayout:
        t = self.getLayoutTable()
        colLayouts = t.getColLayouts()
        rowLayouts = t.getRowLayouts()
        l = GridVariableLayout(colLayouts, rowLayouts)
        return l