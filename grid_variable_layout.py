from .grid_layout import GridLayout
from .grid_item_layout import GridItemLayout
from .point import Point

class GridVariableLayout(GridLayout):
    def __init__(self, colLayouts: list[GridItemLayout], rowLayouts: list[GridItemLayout]):
        self.setColLayouts(colLayouts)
        self.setRowLayouts(rowLayouts)

    def setColLayouts(self, l: list[GridItemLayout]):
        if l:
            self.__colLayouts = l
        else:
            raise Exception("Column layout list is empty")
    
    def getColLayouts(self) -> list[GridItemLayout]:
        return self.__colLayouts
    
    def setRowLayouts(self, l: list[GridItemLayout]):
        if l:
            self.__rowLayouts = l
        else:
            raise Exception("Row layout list is empty")
    
    def getRowLayouts(self) -> list[GridItemLayout]:
        return self.__rowLayouts
    
    def getNCols(self) -> int:
        l = self.getColLayouts()
        n = sum([i.getN() for i in l])
        return n
    
    def getNRows(self) -> int:
        l = self.getRowLayouts()
        n = sum([i.getN() for i in l])
        return n

    def toPoints(self, origin: Point, angle: float) -> list[list[Point]]:
        cls = self.getColLayouts()
        rls = self.getRowLayouts()
        x = origin.x()
        y = origin.y()

        points = []
        yOffset = 0
        for rl in rls:
            yVariation = (rl.getSpacingEnd() - rl.getSpacingStart()) / rl.getN()
            for r in range(rl.getN() + 1):
                row = []
                xOffset = 0
                for cl in cls:
                    xVariation = (cl.getSpacingEnd() - cl.getSpacingStart()) / cl.getN()
                    for c in range(cl.getN() + 1):
                        point = Point(x + xOffset, y + yOffset)
                        point.rotate(origin, angle)
                        row.append(point)
                        xOffset += cl.getSpacingStart() + (c * xVariation)
                points.append(row)
                yOffset += rl.getSpacingStart() + (r * yVariation)
        
        return points