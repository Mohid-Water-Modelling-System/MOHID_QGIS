from qgis.PyQt.QtWidgets import QPushButton, QFileDialog

# from ..utils.gridConverter import grid2shp
# from ..utils.polygonConverter import polygon2shp
import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(module)s:%(funcName)s:%(message)s')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

class BathymetryTool():

    def __init__(self, dockedwidget):

        logger.debug("Connect buttons with functions")
        self.dockedwidget = dockedwidget
        self.dockedwidget.bat_loadButton.clicked.connect(self.loadToLayer)
        self.dockedwidget.bat_fsBrowser.clicked.connect(self.openFileBrowser)
    
    def loadGrid(self, inFilename):

        # TODO: check if file type is supported

        # Convert to shapefile and load layer
        # Run conversion process
        #outFilename = grid2shp(inFilename)
        pass

    def openFileBrowser(self):
        logger.debug("Pressed browser button")
        filename = QFileDialog.getOpenFileName(None, 'Load MOHID file', 
                            filter='Mohid files (*.dat *.grid *.xy *.xyz)')[0]
        self.dockedwidget.bat_inputPath.setText(filename)

    def loadToLayer(self):
        logger.debug("Pressed load button")
        if self.inputhPath.text() != "":
            # check file type

            # Polygon (MOHID format, .xy)

            # polygon2shp(self.inputhPath.text())
            # shpPath = self.inputhPath.text().split(".")[0] + ".shp"
            # vlayer = self.iface.addVectorLayer(shpPath, "Polygon layer", "ogr")
            # crs = vlayer.crs()
            # # crs.createFromId(4326) 
            # crs.EpsgCrsId = 4326  # Whatever CRS you want
            # vlayer.setCrs(crs)
            # if not vlayer:
            #     print("Layer failed to load!")
            pass
    
    def convert(self, input, convertFunction, output=None,):

        if output is None:
            # TODO: check if convertFunctions needs outputh path
            convertFunction(input)
        else:
            return convertFunction(input)

    def loadLayer(self):
        raise NotImplementedError
