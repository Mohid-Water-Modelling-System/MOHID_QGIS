from typing import Dict
from ..tab_grid.grid import Grid
from pathlib import Path
from abc import ABC, abstractmethod

import logging

logger = logging.getLogger(__name__)

VALID_TAGS = {
        "regular": [
                "<BeginGridData2D>", "<EndGridData2D>"
            ,   "<BeginXX>", "<EndXX>", "<BeginYY>", "<EndYY>"]
    ,   "curvillinear": ["<BeginGridData2D>", "<EndGridData2D>"
            ,   "<CornersXY>", "<\\CornersXY>"]}

class MOHIDBathymetry(Grid):

    grid: Grid = None
    type: str
    #xyz: XYZ = 
    # landmask = 

    def __init__(self, filepath):
        
        self._filepath = filepath
        self.file = Path(filepath)
        self.filename = Path(filepath).stem
        self.grid = Grid()
        self.type = self.getGridType()
        self.gridData = {}
        self.readMohidBathymetry(filepath)

    def getGridType(self):
        with self.file.open() as f: 
            cleanFile = list(map(lambda x: x.strip(), f.readlines()))
        if "<CornersXY>" in cleanFile:
            return "curvillinear"
        elif "<BeginXX>" in cleanFile:
            return "regular"
        else:
            raise RuntimeError("Invalid MOHID format!")

    def isValid(self):
        with self.file.open() as f: 
            cleanFile = list(map(lambda x: x.strip(), f.readlines()))
        return True if all(tag in cleanFile for tag in VALID_TAGS[self.type]) \
            else False

    def readMohidBathymetry(self, filepath):

        self.gridData = {
            'SRID' : 4326,
            'ILB' : None,
            'IUB' : None,
            'JLB' : None,
            'JUB' : None,
            'COORD_TIP' : None,
            'ORIGIN_X' : None,
            'ORIGIN_Y' : None,
            'ZONE' : None,
            'GRID_ANGLE' : 0,
            'LATITUDE' : None,
            'LONGITUDE' : None,
            # 'CONSTANT_SPACING_X' : None,
            # 'CONSTANT_SPACING_Y' : None,
            # 'DX' : None,
            # 'DY' : None,
            'FILL_VALUE': -99,
            'POINTS_XX': [],
            'POINTS_YY': [],
            'DATA_2D': [],
            'CORNERS': []
        }
        with open(filepath) as f:
            
            # Parse MOHID file
            if self.type == "regular":
                for line in f:
                    line = line.strip('\n').split(" ")
                    elems = list(filter(lambda x: x not in ('',':','\t','\n'), line))
                
                    if not elems:
                        continue
                    elif 'COMENT' in elems[0]:
                        continue
                    elif elems[0] == "SRID":
                        self.gridData['SRID'] = int(elems[1])
                    elif elems[0] == "ILB_IUB": # YY axis
                        self.gridData['ILB'] = int(elems[1])
                        self.gridData['IUB'] = int(elems[2])
                    elif elems[0] == "JLB_JUB": # XX axis
                        self.gridData['JLB'] = int(elems[1])
                        self.gridData['JUB'] = int(elems[2])
                    elif elems[0] == "COORD_TIP":
                        self.gridData['COORD_TIP'] = elems[1]
                    elif elems[0] == "ORIGIN":
                        self.gridData['ORIGIN_X'] = float(elems[1])
                        self.gridData['ORIGIN_Y'] = float(elems[2])
                    # TODO: Is ZONE an integer?
                    elif elems[0] == "ZONE":
                        self.gridData['ZONE'] = elems[1]
                    elif elems[0] == "GRID_ANGLE":
                        self.gridData['GRID_ANGLE'] = float(elems[1])
                    elif elems[0] == "LATITUDE":
                        self.gridData['LATITUDE'] = float(elems[1])
                    elif elems[0] == "LONGITUDE":
                        self.gridData['LONGITUDE'] = float(elems[1])
                    elif elems[0] == "<BeginXX>":
                        # Read block of points
                        isPoint = True
                        while isPoint:
                            line = next(f).strip('\n').split(" ")
                            elems = list(filter(lambda x: x not in ('',':','\t','\n'), line))
                            if elems[0] == "<EndXX>":
                                isPoint = False
                            else:
                                self.gridData['POINTS_XX'].append(float(elems[0]))
                    elif elems[0] == "<BeginYY>":
                        # Read block of points
                        isPoint = True
                        while isPoint:
                            line = next(f).strip('\n').split(" ")
                            elems = list(filter(lambda x: x not in ('',':','\t','\n'), line))
                            if elems[0] == "<EndYY>":
                                isPoint = False
                            else:
                                self.gridData['POINTS_YY'].append(float(elems[0]))
                    elif elems[0] == "<BeginGridData2D>":
                        # Read block of points
                        isPoint = True
                        while isPoint:
                            line = next(f).strip('\n').split(" ")
                            elems = list(filter(lambda x: x not in ('',':','\t','\n'), line))
                            if elems[0] == "<EndGridData2D>":
                                isPoint = False
                            else:
                                self.gridData['DATA_2D'].append(float(elems[0]))
            elif self.type == "curvillinear":
                corners = []
                for line in f:
                    line = line.strip('\n').split(" ")
                    elems = list(filter(lambda x: x not in ('',':','\t','\n'), line))
                    if not elems:
                        continue
                    elif 'COMENT' in elems[0]:
                        continue
                    elif elems[0] == 'LATITUDE':
                        self.gridData['LATITUDE'] = float(elems[1])
                    elif elems[0] == 'LONGITUDE':
                        self.gridData['LONGITUDE'] = float(elems[1])
                    elif elems[0] == 'ORIGIN':
                        self.gridData['ORIGIN_X'] = float(elems[1])
                        self.gridData['ORIGIN_Y'] = float(elems[2])
                    # TODO: Is ZONE an integer?
                    elif elems[0] == "ZONE":
                        self.gridData['ZONE'] = elems[1]
                    elif elems[0] == 'GRID_ANGLE':
                        self.gridData['GRID_ANGLE'] = float(elems[1])
                    elif elems[0] == 'ILB_IUB':
                        self.gridData['ILB'] = int(elems[1])
                        self.gridData['IUB'] = int(elems[2])
                    elif elems[0] == 'JLB_JUB':
                        self.gridData['JLB'] = int(elems[1])
                        self.gridData['JUB'] = int(elems[2])
                    elif elems[0] == "<CornersXY>":
                        # Read corners
                        isPoint = True
                        while isPoint:
                            line = next(f).strip('\n').split(" ")
                            elems = list(filter(
                                lambda x: x not in ('',':','\t','\n'), line))
                            if elems[0] == "<\\CornersXY>":
                                isPoint = False
                            else:
                                corners.append([float(elems[0]), float(elems[1])])
                    elif elems[0] == "<BeginGridData2D>":
                        # Read block of points
                        isPoint = True
                        while isPoint:
                            line = next(f).strip('\n').split(" ")
                            elems = list(filter(lambda x: x not in ('',':','\t','\n'), line))
                            if elems[0] == "<EndGridData2D>":
                                isPoint = False
                            else:
                                self.gridData['DATA_2D'].append(float(elems[0]))
                    else:
                        continue
                self.gridData["CORNERS"] = corners
        return None, None, None