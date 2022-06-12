from ..grid.grid import Grid
import os

class MOHIDBathymetry(Grid):

    grid: Grid = None
    #xyz: XYZ = 
    # landmask = 

    def __init__(self, filepath):
        
        self._filepath = filepath
        self._filename = os.path.basename(filepath).split(".")[0]
        self.grid = Grid()
        self.readMohidBathymetry(filepath)

    def readMohidBathymetry(self, filepath):

        gridData = {
            'SRID' : None,
            'ILB' : None,
            'IUB' : None,
            'JLB' : None,
            'JUB' : None,
            'COORD_TIP' : None,
            'ORIGIN_X' : None,
            'ORIGIN_Y' : None,
            'ZONE' : None,
            'GRID_ANGLE' : None,
            'LATITUDE' : None,
            'LONGITUDE' : None,
            'CONSTANT_SPACING_X' : None,
            'CONSTANT_SPACING_Y' : None,
            'DX' : None,
            'DY' : None,
            'FILL_VALUE': None,
        }
        with open(filepath) as f:
            
            # Parse MOHID file
            for line in f.readlines():
                line = line.strip('\n').split(" ")
                elems = list(filter(lambda x: x not in ('',':','\t','\n'), line))
            
                if not elems:
                    continue
                elif 'COMENT' in elems[0]:
                    continue
                elif elems[0] == "SRID":
                    gridData['SRID'] = int(elems[1])
                elif elems[0] == "ILB_IUB": # YY axis
                    gridData['ILB'] = int(elems[1])
                    gridData['IUB'] = int(elems[2])
                elif elems[0] == "JLB_JUB": # XX axis
                    gridData['JLB'] = int(elems[1])
                    gridData['JUB'] = int(elems[2])
                elif elems[0] == "COORD_TIP":
                    gridData['COORD_TIP'] = elems[1]
                elif elems[0] == "ORIGIN":
                    gridData['ORIGIN_X'] = float(elems[1])
                    gridData['ORIGIN_Y'] = float(elems[2])
                # TODO: Is ZONE an integer?
                elif elems[0] == "ZONE":
                    gridData['ZONE'] = elems[1]
                elif elems[0] == "GRID_ANGLE":
                    gridData['GRID_ANGLE'] = float(elems[1])
                elif elems[0] == "LATITUDE":
                    gridData['LATITUDE'] = float(elems[1])
                elif elems[0] == "LONGITUDE":
                    gridData['LONGITUDE'] = float(elems[1])
                elif elems[0] == "CONSTANT_SPACING_X":
                    gridData['CONSTANT_SPACING_X'] = int(elems[1])
                elif elems[0] == "CONSTANT_SPACING_Y":
                    gridData['CONSTANT_SPACING_Y'] = int(elems[1])
                elif elems[0] == "DX":
                    gridData['DX'] = float(elems[1])
                elif elems[0] == "DY":
                    gridData['DY'] = float(elems[1])
                
                print(gridData.values())
                print(gridData)
                print(gridData.items())
                # elif line[0] == 'LATITUDE':
                #     latitude = float(line[1])
                #     print("LATITUDE ", latitude)
                # elif line[0] == 'LONGITUDE':
                #     longitude = float(line[1])
                #     print("LONGITUDE ", longitude)
                # elif line[0] == 'ORIGIN':
                #     origin_x = float(line[1])
                #     origin_y = float(line[2])
                #     print(origin_x, origin_y)
                # elif line[0] == 'DX':
                #     dx = float(line[1])
                #     print("DX ",dx)
                # elif line[0] == 'DY':
                #     dy = float(line[1])
                #     print("DY ",dy)
                # elif line[0] == 'GRID_ANGLE':
                #     angle = float(line[1])
                #     print(angle)
                # elif line[0] == 'ILB_IUB':
                #     i_min = int(line[1])
                #     i_max = int(line[2])
                #     print("ILB_IUB ", i_min, i_max)
                # elif line[0] == 'JLB_JUB':
                #     j_min = int(line[1])
                #     j_max = int(line[2])
                #     print("JLB_JUB ", j_min, j_max)
                # elif line[0] == 'CONSTANT_SPACING_X':
                #     if int(line[1]) == 1:
                #         constant_x = True
                #     else:
                #         constant_x = False
                # elif line[0] == 'CONSTANT_SPACING_Y':
                #     if int(line[1]) == 1:
                #         constant_y = True
                #     else:
                #         constant_y = False
                # else:
                #     continue
        return None, None, None