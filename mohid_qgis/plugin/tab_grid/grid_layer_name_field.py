from qgis.PyQt.QtWidgets import QLineEdit, QToolButton
from qgis.PyQt.QtCore import QObject, pyqtSignal
from ..validators.not_empty_validator import NotEmptyValidator

"""
The GridLayerNameField controls a QLineEdit of the GridTool that receives a string as input.
This string is used to set the name of the layer that will display the grid over the map.
The name of the layer will appear in the Qgis interface in the list of layers.
This class is a child of QObject to be able to have a pyqtSignal attribute.
"""
class GridLayerNameField(QObject):
    """
    The filled attribute is a signal that emits a boolean value when the state of the field changes.
    If the field is correctly filled, true is emitted.
    If the field becomes not correctly filled, false is emitted.
    """
    filled = pyqtSignal(bool)

    """
    The GridLayerNameField constructor receives:
        - a QLineEdit field for the user to enter a string with the name of the layer
    """
    def __init__(self, l: QLineEdit):
        super().__init__()
        self.setLineEdit(l)

    """
    The LineEdit setter receives a QLineEdit object,
    creates a validator for the LineEdit to accept non empty strings only and connects
    its textChanged signal to the lineEditTextChanged function.
    When the text of the LineEdit changes, the lineEditTextChanged function is called.
    """
    def setLineEdit(self, l: QLineEdit):
        validator = NotEmptyValidator(l)
        l.setValidator(validator)
        l.textChanged.connect(self.lineEditTextChanged)
        self.__lineEdit = l

    def getLineEdit(self) -> QLineEdit:
        return self.__lineEdit

    """
    The lineEditTextChanged function is called when the content of the LineEdit is changed.
    It checks if the field is correctly filled and emits the signal "filled" which has a boolean
    that is true when the field is correctly filled and false when the field is not correctly filled.
    """
    def lineEditTextChanged(self):
        filled = self.isFilled()
        self.filled.emit(filled)

    """
    The isFilled function returns true if the lineEdit is filled with an acceptable string
    (not empty) and false otherwise.
    """
    def isFilled(self) -> bool:
        l = self.getLineEdit()
        filled = l.hasAcceptableInput()
        return filled

    """
    The getText function returns the string that the user entered in the lineEdit
    """
    def getText(self) -> str:
        l = self.getLineEdit()
        text = l.text()
        return text
