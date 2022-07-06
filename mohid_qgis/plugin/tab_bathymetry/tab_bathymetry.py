import os

from qgis.PyQt import uic
from PyQt5.QtWidgets import QTabWidget

from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtWidgets import QPushButton, QFileDialog
from qgis.core import QgsProject
from .mohidBathymetry import MOHIDBathymetry

from mohid_qgis.core.utils.gridConverter import grid2shp
from mohid_qgis.core.utils.polygonConverter import polygon2shp
from mohid_qgis.core.utils.xyzConverter import XYZ2shp
from mohid_qgis.core.utils.bathymetryConverter import MOHIDBathymetry2shp, saveToMohidFile, \
    saveGenerateMohidFile
from mohid_qgis.plugin.base.thread import ProgramThread
import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(module)s:%(funcName)s:%(message)s')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

CRS_ID_DEFAULT = 4326

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'tab_bathymetry.ui'))

class BathymetryTab(QTabWidget, FORM_CLASS):

    def __init__(self, iface) -> None:
        super().__init__()

        # Setup UI elements
        self.setupUi(self)

        self.iface = iface
        # Connect signals
        self.bat_fsGrid.clicked.connect(self.openGridBrowser)
        self.bat_loadGrdBtn.clicked.connect(self.loadGridToLayer)

        self.bat_fsXYZ.clicked.connect(self.openXYZBrowser)
        self.bat_loadXYZBtn.clicked.connect(self.loadXYZToLayer)

        self.bat_fsLand.clicked.connect(self.openLandBrowser)
        self.bat_loadLandBtn.clicked.connect(self.loadLandToLayer)

        self.bat_fsOutput.clicked.connect(self.openGenerateBrowser)
        self.bat_generateBtn.clicked.connect(self.generateBatMohidFile)

        self.bat_fsBat.clicked.connect(self.openBatBrowser)
        self.bat_loadBatBtn.clicked.connect(self.loadBatToLayer)
        self.bat_saveBatBtn.clicked.connect(self.saveBatToMohidFile)
        self.loadedBatLayers = {}
    
    def openGridBrowser(self):
        logger.debug("Pressed Grid browser button")
        filepath = QFileDialog.getOpenFileName(None, 'Load MOHID Grid file', 
                            filter='Mohid files (*.grd)')[0]
        self.bat_gridPath.setText(filepath)
    
    def openXYZBrowser(self):
        logger.debug("Pressed XYZ browser button")
        filepath = QFileDialog.getOpenFileName(None, 'Load MOHID XYZ file', 
                            filter='Mohid files (*.xyz)')[0]
        self.bat_XYZPath.setText(filepath)
    
    def openLandBrowser(self):
        logger.debug("Pressed browser button")
        filepath = QFileDialog.getOpenFileName(None, 'Load MOHID Land file', 
                            filter='Mohid files (*.xy)')[0]
        self.bat_landPath.setText(filepath)
    
    def openBatBrowser(self):
        logger.debug("Pressed bathymetry browser button")
        filepath = QFileDialog.getOpenFileName(None, 'Load MOHID Bathymetry file', 
                            filter='Mohid Bathymetry (*.dat)')[0]
        self.bat_batPath.setText(filepath)

    def loadGridToLayer(self):
        
        filepath = self.bat_gridPath.text()
        logger.debug(f"Loading {filepath}")
        if filepath != "":
            # check file type

            grid2shp(self.bat_gridPath.text())
            shpPath = self.bat_gridPath.text().split(".")[0] + ".shp"
            filename = os.path.basename(shpPath).split(".")[0]
            vlayer = self.iface.addVectorLayer(shpPath, f"Grid - {filename}", "ogr")
            
            if not vlayer:
                print("Layer failed to load!")
            else:
                crs = vlayer.crs()
                crs.createFromId(CRS_ID_DEFAULT) 
                vlayer.setCrs(crs)
        else:
            logger.debug(f"Filename is empty")
    
    
    def loadXYZToLayer(self):
        """
        .xyz file contents:
        latitude longitude attribute
        <begin_xyz>
        -8.7500838888889    38.4880172222222    0.820
        <end_xyz>
        """
        filepath = self.bat_XYZPath.text()
        logger.debug(f"Loading {filepath}")
        if filepath != "":
            # check file type

            XYZ2shp(self.bat_XYZPath.text())
            shpPath = self.bat_XYZPath.text().split(".")[0] + ".shp"
            filename = os.path.basename(shpPath).split(".")[0]
            vlayer = self.iface.addVectorLayer(shpPath, f"Bathymetry points - {filename}", "ogr")

            if not vlayer:
                print("Layer failed to load!")
            else:
                crs = vlayer.crs()
                crs.createFromId(CRS_ID_DEFAULT) 
                vlayer.setCrs(crs)
        else:
            logger.debug(f"Filename is empty")
    
    def loadLandToLayer(self):
        filepath = self.bat_landPath.text()
        logger.debug(f"Loading {filepath}")
        if filepath != "":
            # check file type

            polygon2shp(self.bat_landPath.text())
            shpPath = self.bat_landPath.text().split(".")[0] + ".shp"
            filename = os.path.basename(shpPath).split(".")[0]
            vlayer = self.iface.addVectorLayer(shpPath, f"Land - {filename}", "ogr")
            
            if not vlayer:
                print("Layer failed to load!")
            else:
                crs = vlayer.crs()
                crs.createFromId(CRS_ID_DEFAULT) 
                vlayer.setCrs(crs)
        else:
            logger.debug(f"Filename is empty")
    
    def openGenerateBrowser(self):
        # filepath = QFileDialog.getExistingDirectory(None, "Select output Directory")
        filepath = QFileDialog.getSaveFileName(None, 'Generate MOHID Bathymetry file', 
                            filter='Mohid Bathymetry (*.dat)')[0]
        self.bat_outputPath.setText(filepath)

    def generateBatMohidFile(self):
        batPath = self.bat_outputPath.text()
        logger.debug(f"Saving bathymetry to {batPath}")
        
        if not batPath.endswith(".dat"):
            batPath = f"{batPath}.dat"

        gridPath = self.bat_gridPath.text()
        xyzPath = self.bat_XYZPath.text()
        landPath = self.bat_landPath.text()

        DTCdir = os.path.abspath(os.path.join(os.path.dirname( __file__ ),
                                            '../..',
                                            'core/Digital_Terrain_Creator/'))
        DTCOptionsPath = os.path.join(DTCdir, "CreateBathymetry.dat")
        # TODO: get options
        # Generate CreateBathymetry.dat options file
        if gridPath and xyzPath:
            saveGenerateMohidFile(DTCOptionsPath, batPath, gridPath, xyzPath, landPath)
        else:
            logger.debug("Can't generate bathymetry, missing files")

        if os.path.exists(DTCOptionsPath):
            # Run DTC tool
            logger.debug("Running DTC")
            self._runDigitalTerrain()

    def loadBatToLayer(self):
        
        filepath = self.bat_batPath.text()
        logger.debug(f"Loading {filepath}")
        if filepath != "":
            # check file type
            bat = MOHIDBathymetry(filepath)
            MOHIDBathymetry2shp(filepath, bat.gridData)
            shpPath = filepath.split(".")[0] + ".shp"
            vlayer = self.iface.addVectorLayer(
                            shpPath,
                            f"MOHID Bathymetry - {bat.filename}",
                            "ogr")
           
            if not vlayer:
                print("Layer failed to load!")
            else:
                crs = vlayer.crs()
                crs.createFromId(CRS_ID_DEFAULT) 
                vlayer.setCrs(crs)
                self.loadedBatLayers[vlayer.name()] = bat

        else:
            logger.debug(f"Filename is empty")
    
    def saveBatToMohidFile(self):
        
        lyr = self.iface.activeLayer()
        if lyr.name() not in self.loadedBatLayers:
            logger.debug("No bathymetry to save")
            return
        bat = self.loadedBatLayers[lyr.name()]
        filepath = QFileDialog.getSaveFileName(None, 'Save MOHID Bathymetry file', 
                            filter='Mohid Bathymetry (*.dat)')[0]
        logger.debug(f"Will save to {filepath}")
        if filepath != "":
            
            # TODO: for now this is sufficient, but we should choose the layer 
            # from a comboBox
           
            data2D = []
            for feat in lyr.getFeatures():
                data2D.append(feat.attributes()[0])
            bat.gridData['DATA_2D'] = data2D
            saveToMohidFile(filepath, bat.gridData)

        else:
            logger.debug(f"Filename is empty")
    
    def updatebatComboBox(self):

        pass
        # for layer in QgsProject.instance().mapLayers().values():
        #     if layer.name().startswith("MOHID Bathymetry"):
        #         self.bat_layerComboBox.addItem(layer.name(), layer)
        # QgsProject.instance().mapLayersByName("Mohid")
    
    def convert(self, input, convertFunction, output=None,):

        if output is None:
            # TODO: check if convertFunctions needs outputh path
            convertFunction(input)
        else:
            return convertFunction(input)

    def loadLayer(self):
        raise NotImplementedError

    def _runDigitalTerrain(self):
        # TODO: remove hardcoded configurations after implementing options solution
        DTCpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ),
        '../..',
        'core/Digital_Terrain_Creator/DigitalTerrainCreator_release_double_x64.exe'))
        thread = ProgramThread(DTCpath)

        def on_output(out: str) -> None:
            logger.debug("on_output callback")
            # self.stdout_textarea.appendPlainText(out)
            # vert_scrollbar = self.stdout_textarea.verticalScrollBar()
            # vert_scrollbar.setValue(vert_scrollbar.maximum())

        def on_finished() -> None:
            # When lines come in fast, then the highlighter is not called on each line.
            # Re-highlighting at the end is a work-around to at least have correct
            # highlighting after program termination.
            # self.stdout_highlighter.rehighlight()
            logger.debug("on_finished callback")
            if thread.exc_info:
                # on_done(path, None)
                raise thread.exc_info[0].with_traceback(*thread.exc_info[1:])
            # on_done(path, thread.error)
        thread.output.connect(on_output)
        thread.finished.connect(on_finished)
        thread.start()
        # so that we can kill the program later if requested
        self.thread = thread