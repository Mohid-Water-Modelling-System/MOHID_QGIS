from qgis.PyQt.QtGui import QValidator

"""
The NotEmptyValidator class is a child of the QValidator class.
It implements a validator that only accepts a string that is not an empty string.
This validator is used for the layer name field of the Grid Tool.
"""
class NotEmptyValidator(QValidator):
    """
    The validate function is called when the user edits the field.
    It returns the state of the input which is either Acceptable, Intermediate or Invalid.
    Since a layer name cannot be an empty string, the validate function of the
    NotEmptyValidator cannot return Acceptable for "" or "     ".
    This function return Intermediate if the input is "" or "   ".
    """
    def validate(self, text, pos):
        if text.strip():
            state = QValidator.Acceptable
        else:
            state = QValidator.Intermediate
        return state, text, pos