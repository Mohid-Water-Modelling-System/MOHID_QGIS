from qgis.PyQt.QtWidgets import QTableWidgetItem

"""
The GridItemLayout class stores the layout of a set of rows or columns.
This class is used for the variable layouts.
It is the parent class of the GridColLayout and GridRowLayout classes.
"""
class GridItemLayout:
    """
    Each GridItemLayout object is represented in a row of the layout table on the plugin interface.
    Thus each object has a "type" attribute which is the string that will specify the type of item
    in the layout table. This string can either be "row" or "column".
    """
    type = ""

    """
    The constructor of the GridItemLayout receiver:
        - The number of items in the set
        - The spacing between the items at the beginning of the set
        - The spacing between the items at the end of the set
    """
    def __init__(self, n: int, spacingStart: float, spacingEnd: float):
        self.setN(n)
        self.setSpacingStart(spacingStart)
        self.setSpacingEnd(spacingEnd)
    
    def setN(self, n: int):
        if n < 1 :
            raise Exception("Quantity lower than 1")
        self.__n = n
    
    def getN(self) -> int:
        return self.__n

    def setSpacingStart(self, s: float):
        if s <= 0 :
            raise Exception("Spacing start not greater than 0")
        self.__spacingStart = s
    
    def getSpacingStart(self) -> float:
        return self.__spacingStart

    def setSpacingEnd(self, s: float):
        if s <= 0 :
            raise Exception("Spacing end not greater than 0")
        self.__spacingEnd = s
    
    def getSpacingEnd(self) -> float:
        return self.__spacingEnd
    
    """
    The getTableWidgetItems returns a row for listing the layout of the items in the Layout table
    of the Grid Tool interface for variable spaced grids.
    """
    def getTableWidgetItems(self) -> list[QTableWidgetItem]:
        n = self.getN()
        type = self.type
        spacingStart = self.getSpacingStart()
        spacingEnd = self.getSpacingEnd()
        spacing = str(spacingStart) + " to " + str(spacingEnd)

        items = [QTableWidgetItem(str(n)), QTableWidgetItem(type), QTableWidgetItem(spacing)]
        return items

"""
The GridColLayout class is a child class of the GridItemLayout class.
The only difference is that this class as the type attribute with the string "Column" and therefore
can represent columns in the Layout table of the plugin interface.
"""
class GridColLayout(GridItemLayout):
    type = "Column"
    pass

"""
The GridRowLayout class is a child class of the GridItemLayout class.
The only difference is that this class as the type attribute with the string "Row" and therefore
can represent rows in the Layout table of the plugin interface.
"""
class GridRowLayout(GridItemLayout):
    type = "Row"
    pass