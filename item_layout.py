class ItemLayout:
    def __init__(self, n: int, spacingStart: float, spacingEnd: float):
        if n < 1 :
            raise Exception("Number of items lower than 1")
        elif spacingStart <= 0 :
            raise Exception("Item spacing start not greater than 0")
        elif spacingEnd <= 0 :
            raise Exception("Item spacing end not greater than 0")
        
        self.setN(n)
        self.setSpacingStart(spacingStart)
        self.setSpacingEnd(spacingEnd)
    
    def setN(self, n: int):
        if n < 1 :
            raise Exception("Number of items lower than 1")
        
        self.__n = n

    def getN(self) -> int:
        return self.__n

    def setSpacingStart(self, spacingStart: float):
        if spacingStart <= 0 :
            raise Exception("Item spacing start not greater than 0")
        
        self.__spacingStart = spacingStart
    
    def getSpacingStart(self) -> float:
        return self.__spacingStart

    def setSpacingEnd(self, spacingEnd: float):
        if spacingEnd <= 0 :
            raise Exception("Item spacing end not greater than 0")
        
        self.__spacingEnd = spacingEnd
    
    def getSpacingEnd(self) -> float:
        return self.__spacingEnd