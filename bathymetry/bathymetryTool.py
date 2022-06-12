import os
from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtWidgets import QPushButton, QFileDialog

from .mohidBathymetry import MOHIDBathymetry

from ..utils.gridConverter import grid2shp
from ..utils.polygonConverter import polygon2shp
from ..utils.xyzConverter import XYZ2shp
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
        self.dock.bat_fsXYZ.clicked.connect(self.openXYZBrowser)
        self.dock.bat_fsLand.clicked.connect(self.openLandBrowser)
        self.dock.bat_fsBat.clicked.connect(self.openBatBrowser)
        self.dock.bat_loadGrdBtn.clicked.connect(self.loadGridToLayer)
        self.dock.bat_loadXYZBtn.clicked.connect(self.loadXYZToLayer)
        self.dock.bat_loadLandBtn.clicked.connect(self.loadLandToLayer)
        self.dock.bat_loadBatBtn.clicked.connect(self.loadBatToLayer)
    
    def setIface(self, iface):
        logger.debug("Setting Bathymetry tool iface")
        self.iface = iface

    def openGridBrowser(self):
        logger.debug("Pressed Grid browser button")
        filepath = QFileDialog.getOpenFileName(None, 'Load MOHID Grid file', 
                            filter='Mohid files (*.dat *.grid *.xy *.xyz)')[0]
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
            crs = vlayer.crs()
            crs.createFromId(CRS_ID_DEFAULT) 
            vlayer.setCrs(crs)
            if not vlayer:
                print("Layer failed to load!")
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
            crs = vlayer.crs()
            crs.createFromId(CRS_ID_DEFAULT) 
            vlayer.setCrs(crs)
            if not vlayer:
                print("Layer failed to load!")
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
            crs = vlayer.crs()
            crs.createFromId(CRS_ID_DEFAULT) 
            vlayer.setCrs(crs)
            if not vlayer:
                print("Layer failed to load!")
        else:
            logger.debug(f"Filename is empty")
    
    def loadBatToLayer(self):
        
        filepath = self.dock.bat_batPath.text()
        logger.debug(f"Loading {filepath}")
        if filepath != "":
            # check file type
            mohidBat = MOHIDBathymetry(filepath)
            # grid2shp(self.dock.bat_batPath.text())
            # shpPath = self.dock.bat_batPath.text().split(".")[0] + ".shp"
            # filename = os.path.basename(shpPath).split(".")[0]
            # vlayer = self.iface.addVectorLayer(shpPath, f"Grid - {filename}", "ogr")
            # crs = vlayer.crs()
            # crs.createFromId(CRS_ID_DEFAULT) 
            # vlayer.setCrs(crs)
            # if not vlayer:
            #     print("Layer failed to load!")
            # else:
            #     logger.debug(f"Filename is empty")
    
    def convert(self, input, convertFunction, output=None,):

        if output is None:
            # TODO: check if convertFunctions needs outputh path
            convertFunction(input)
        else:
            return convertFunction(input)

    def loadLayer(self):
        raise NotImplementedError
