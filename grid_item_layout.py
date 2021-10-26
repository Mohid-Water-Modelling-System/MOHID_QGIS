from qgis.PyQt.QtWidgets import QTableWidgetItem

class GridItemLayout:
    type = ""
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
    
    def getTableWidgetItems(self) -> list[QTableWidgetItem]:
        n = self.getN()
        type = self.type
        spacingStart = self.getSpacingStart()
        spacingEnd = self.getSpacingEnd()
        spacing = str(spacingStart) + " to " + str(spacingEnd)

        items = [QTableWidgetItem(str(n)), QTableWidgetItem(type), QTableWidgetItem(spacing)]
        return items

class GridColLayout(GridItemLayout):
    type = "Column"
    pass

class GridRowLayout(GridItemLayout):
    type = "Row"
    pass