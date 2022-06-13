from ..grid.grid import Grid
import os

class MOHIDBathymetry(Grid):

    grid: Grid = None
    #xyz: XYZ = 
    # landmask = 

    def __init__(self, filepath):
        
        self._filepath = filepath
        self.filename = os.path.basename(filepath).split(".")[0]
        self.grid = Grid()
        self.gridData = {}
        self.readMohidBathymetry(filepath)

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
        }
        with open(filepath) as f:
            
            # Parse MOHID file
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
                # elif elems[0] == "CONSTANT_SPACING_X":
                #     self.gridData['CONSTANT_SPACING_X'] = int(elems[1])
                # elif elems[0] == "CONSTANT_SPACING_Y":
                #     self.gridData['CONSTANT_SPACING_Y'] = int(elems[1])
                # elif elems[0] == "DX":
                #     self.gridData['DX'] = float(elems[1])
                # elif elems[0] == "DY":
                #     self.gridData['DY'] = float(elems[1])
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
                
        return None, None, None