import os
from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtWidgets import QPushButton, QFileDialog
from qgis.core import QgsProject
from .mohidBathymetry import MOHIDBathymetry

from ..utils.gridConverter import grid2shp
from ..utils.polygonConverter import polygon2shp
from ..utils.xyzConverter import XYZ2shp
from ..utils.bathymetryConverter import MOHIDBathymetry2shp, saveToMohidFile, \
    saveGenerateMohidFile
import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(module)s:%(funcName)s:%(message)s')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

CRS_ID_DEFAULT = 4326

class BathymetryTool:

    def __init__(self, dock):

        logger.debug("Bathymetry init")
        # logger.debug(btnLoad.clicked.connect(self.loadToLayer))
        self.dock = dock
        self.dock.bat_fsGrid.clicked.connect(self.openGridBrowser)
        self.dock.bat_loadGrdBtn.clicked.connect(self.loadGridToLayer)

        self.dock.bat_fsXYZ.clicked.connect(self.openXYZBrowser)
        self.dock.bat_loadXYZBtn.clicked.connect(self.loadXYZToLayer)

        self.dock.bat_fsLand.clicked.connect(self.openLandBrowser)
        self.dock.bat_loadLandBtn.clicked.connect(self.loadLandToLayer)

        self.dock.bat_fsOutput.clicked.connect(self.openGenerateBrowser)
        self.dock.bat_generateBtn.clicked.connect(self.generateBatMohidFile)

        self.dock.bat_fsBat.clicked.connect(self.openBatBrowser)
        self.dock.bat_loadBatBtn.clicked.connect(self.loadBatToLayer)
        self.dock.bat_saveBatBtn.clicked.connect(self.saveBatToMohidFile)
        
        # Finalized mohid bathymetry
        self.mohidBat = None
        
    
    def setIface(self, iface):
        logger.debug("Setting Bathymetry tool iface")
        self.iface = iface

    def openGridBrowser(self):
        logger.debug("Pressed Grid browser button")
        filepath = QFileDialog.getOpenFileName(None, 'Load MOHID Grid file', 
                            filter='Mohid files (*.grd)')[0]
        self.dock.bat_gridPath.setText(filepath)
    
    def openXYZBrowser(self):
        logger.debug("Pressed XYZ browser button")
        filepath = QFileDialog.getOpenFileName(None, 'Load MOHID XYZ file', 
                            filter='Mohid files (*.xyz)')[0]
        self.dock.bat_XYZPath.setText(filepath)
    
    def openLandBrowser(self):
        logger.debug("Pressed browser button")
        filepath = QFileDialog.getOpenFileName(None, 'Load MOHID Land file', 
                            filter='Mohid files (*.xy)')[0]
        self.dock.bat_landPath.setText(filepath)
    
    def openBatBrowser(self):
        logger.debug("Pressed bathymetry browser button")
        filepath = QFileDialog.getOpenFileName(None, 'Load MOHID Bathymetry file', 
                            filter='Mohid Bathymetry (*.dat)')[0]
        self.dock.bat_batPath.setText(filepath)

    def loadGridToLayer(self):
        
        filepath = self.dock.bat_gridPath.text()
        logger.debug(f"Loading {filepath}")
        if filepath != "":
            # check file type

            grid2shp(self.dock.bat_gridPath.text())
            shpPath = self.dock.bat_gridPath.text().split(".")[0] + ".shp"
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
        filepath = self.dock.bat_XYZPath.text()
        logger.debug(f"Loading {filepath}")
        if filepath != "":
            # check file type

            XYZ2shp(self.dock.bat_XYZPath.text())
            shpPath = self.dock.bat_XYZPath.text().split(".")[0] + ".shp"
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
        filepath = self.dock.bat_landPath.text()
        logger.debug(f"Loading {filepath}")
        if filepath != "":
            # check file type

            polygon2shp(self.dock.bat_landPath.text())
            shpPath = self.dock.bat_landPath.text().split(".")[0] + ".shp"
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
        filepath = QFileDialog.getSaveFileName(None, 'Generate MOHID Bathymetry file', 
                            filter='Mohid Bathymetry (*.dat)')[0]
        self.dock.bat_outputPath.setText(filepath)

    def generateBatMohidFile(self):
        filepath = self.dock.bat_outputPath.text()
        logger.debug(f"Loading {filepath}")
        
        if filepath.endswith(".dat"):
            elems = filepath.split(".")
            outPath = f"{elems[0]}_createBathymetry.dat"
        else:
            outPath = f"{filepath}_createBathymetry.dat"

        gridPath = self.dock.bat_gridPath.text()
        xyzPath = self.dock.bat_XYZPath.text()
        landPath = self.dock.bat_landPath.text()

        # TODO: get options
        if gridPath and xyzPath:
            saveGenerateMohidFile(outPath, gridPath, xyzPath, landPath)
        else:
            logger.debug("Cant generate bathymetry, missing files")


    def loadBatToLayer(self):
        
        filepath = self.dock.bat_batPath.text()
        logger.debug(f"Loading {filepath}")
        if filepath != "":
            # check file type
            self.mohidBat = MOHIDBathymetry(filepath)
            MOHIDBathymetry2shp(filepath, self.mohidBat.gridData)
            shpPath = filepath.split(".")[0] + ".shp"
            vlayer = self.iface.addVectorLayer(shpPath, f"MOHID Bathymetry - {self.mohidBat.filename}", "ogr")
           
            if not vlayer:
                print("Layer failed to load!")
            else:
                crs = vlayer.crs()
                crs.createFromId(CRS_ID_DEFAULT) 
                vlayer.setCrs(crs)

        else:
            logger.debug(f"Filename is empty")
    
    def saveBatToMohidFile(self):
        
        if self.mohidBat is None:
            logger.debug("No bathymetry to save")
            return
        filepath = QFileDialog.getSaveFileName(None, 'Save MOHID Bathymetry file', 
                            filter='Mohid Bathymetry (*.dat)')[0]
        logger.debug(f"Will save to {filepath}")
        if filepath != "":
            
            # TODO: for now this is sufficient, but we should choose the layer 
            # from a comboBox
            for layer in QgsProject.instance().mapLayers().values():
                if layer.name().startswith("MOHID Bathymetry"):
                    vLayer = layer
                    break
            data2D = []
            for feat in vLayer.getFeatures():
                data2D.append(feat.attributes()[0])
            self.mohidBat.gridData['DATA_2D'] = data2D
            saveToMohidFile(filepath, self.mohidBat.gridData)

        else:
            logger.debug(f"Filename is empty")
    
    def updatebatComboBox(self):

        pass
        # for layer in QgsProject.instance().mapLayers().values():
        #     if layer.name().startswith("MOHID Bathymetry"):
        #         self.dock.bat_layerComboBox.addItem(layer.name(), layer)
        # QgsProject.instance().mapLayersByName("Mohid")
    
    def convert(self, input, convertFunction, output=None,):

        if output is None:
            # TODO: check if convertFunctions needs outputh path
            convertFunction(input)
        else:
            return convertFunction(input)

    def loadLayer(self):
        raise NotImplementedError
