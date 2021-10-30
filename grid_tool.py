from qgis.PyQt.QtWidgets import QPushButton, QFileDialog
from .grid_form import GridForm
from qgis.core import QgsProject
from .grid import Grid

class GridTool:
    def __init__(self, f: GridForm, previewBtn: QPushButton, loadBtn: QPushButton, saveBtn: QPushButton):
        self.setForm(f)
        self.setPreviewBtn(previewBtn)
        self.setLoadBtn(loadBtn)
        self.setSaveBtn(saveBtn)

    def setForm(self, f: GridForm):
        f.filled.connect(self.formFilled)
        self.__form = f
    
    def getForm(self) -> GridForm:
        return self.__form
    
    def setPreviewBtn(self, b: QPushButton):
        b.clicked.connect(self.previewBtnClicked)
        self.__previewBtn = b
    
    def getPreviewBtn(self) -> QPushButton:
        return self.__previewBtn
    
    def setLoadBtn(self, b: QPushButton):
        b.clicked.connect(self.loadBtnClicked)
        self.__loadBtn = b
    
    def getLoadBtn(self) -> QPushButton:
        return self.__loadBtn
    
    def setSaveBtn(self, b: QPushButton):
        b.clicked.connect(self.saveBtnClicked)
        self.__saveBtn = b
    
    def getSaveBtn(self) -> QPushButton:
        return self.__saveBtn

    def formFilled(self, filled: bool):
        previewBtn = self.getPreviewBtn()
        previewBtn.setEnabled(filled)

        saveBtn = self.getSaveBtn()
        saveBtn.setEnabled(filled)
    
    def previewBtnClicked(self):
        form = self.getForm()
        grid = form.toGrid()
        nameField = form.getLayerNameField()
        name = nameField.getText()
        project = QgsProject.instance()

        layers = project.mapLayersByName(name)
        if layers:
            for layer in layers:
                if layer.customProperty(Grid.MohidGridLayer):
                    grid.updateQgsVectorLayer(layer)
                    break
        else:
            layer = grid.toQgsVectorLayer(name)
            project.addMapLayer(layer)

    def loadBtnClicked(self):
        pass

    def saveBtnClicked(self):
        form = self.getForm()
        grid = form.toGrid()
        nameField = form.getLayerNameField()
        name = nameField.getText()
        fileName = QFileDialog.getSaveFileName(None, 'Save grid', name +'.dat', '*.dat')[0]
        if fileName:
            f = open(fileName, "w")
            f.write(str(grid))
            f.close()
        

    def close(self):
        f = self.getForm()
        f.close()