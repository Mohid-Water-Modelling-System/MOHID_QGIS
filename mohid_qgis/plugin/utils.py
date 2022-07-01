from PyQt5.QtWidgets import QWidget, QScrollArea
from PyQt5.QtGui import QPalette

class WhiteScroll(QScrollArea):
    def __init__(self, widget: QWidget) -> None:
        super().__init__()
        self.setBackgroundRole(QPalette.Light)
        self.setWidgetResizable(True)
        self.setWidget(widget)