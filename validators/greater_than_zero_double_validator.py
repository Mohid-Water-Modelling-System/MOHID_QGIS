from qgis.PyQt.QtGui import QDoubleValidator, QValidator
from qgis.PyQt.QtCore import QObject


"""
The GreaterThanZeroDoubleValidator class is a child of the QDoubleValidator class.
It implements a validator that allows the user to input positive double values only.
This validator is used for the fields of the Grid Tool where the user enters the spacing
of rows and columns.
"""
class GreaterThanZeroDoubleValidator(QDoubleValidator):
    """
    The GreaterThanZeroDoubleValidator constructor sets the bottom value to 0, disabling
    the user from entering negative numbers to the field (generally a QLineEdit). 
    """
    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self.setBottom(0)

    """
    The validate function is called when the user edits the field.
    It returns the state of the input which is either Acceptable, Intermediate or Invalid.
    Since a spacing cannot be equal to zero, the validate function of the
    GreaterThanZeroDoubleValidator cannot return Acceptable for 0.
    This function return Intermediate if the input is 0.
    """
    def validate(self, text, pos):
        state, text, pos = super().validate(text, pos)
        if state == QValidator.Acceptable:
            if float(text.replace(",",".")) == 0:
                state = QValidator.Intermediate
        return state, text, pos
