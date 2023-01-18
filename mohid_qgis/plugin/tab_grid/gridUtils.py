

""" 
ILB_IUB - Two integer numbers defining the minimum and maximum I values along the Y-axis of the grid.
JLB_JUB - Two integer numbers defining the minimum and maximum J values along the X-axis of the grid.
COORD_TIP - A flag which indicates the used coordinates type.
    1 - Geographic coordinates
    2 - UTM coordinates
    3 - Portuguese military coordinates
    4 - Simplified geographic coordinates: in Degrees
    5 - Metric coordinates referred to the origin of the grid
    6 - Circular coordinates
    7 - NRLD - Dutch metric coordinate system
ORIGIN - Two real values, which indicate the origin of the lower left corner of the grid (X Y), longlat
ZONE - Integer values defining the UTM Zone where the bathymetry is located.
GRID_ANGLE - Counter-clock mesh rotation relative to the north. The base point is the origin of the grid.
LATITUDE - Average latitude value used to compute Coriolis frequency and solar radiation when metric coordinates cannot be converted to WGS84 geographic coordinates.
LONGITUDE - Average longitude value used to compute Coriolis frequency and solar radiation when metric coordinates cannot be converted to WGS84 geographic coordinates.
CONSTANT_SPACING_X - Boolean defining if the spacing in the X axis is constant
CONSTANT_SPACING_Y - Boolean defining if the spacing in the Y axis is constant
DX - Constant spacing distance in XX axis
DY - Constant spacing distance in YY axis 
"""

from typing import Any, Dict


def loadFromFile(filename)-> Dict[str, Any]:
    """ 
    Notes
    -----
    
     """
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
    }
    with open(filename, "r") as file:
        
        # Go through every line
        for line in file:
            elems = line.replace("\n", "").split(":")
            if elems[0].replace(" ", "") == "SRID":
                gridData['SRID'] = int(elems[1].replace(" ",""))
            elif elems[0].replace(" ", "") == "ILB_IUB": # YY axis
                gridData['ILB'] = int(elems[1].strip().split(" ")[0])
                gridData['IUB'] = int(elems[1].strip().split(" ")[1])
            elif elems[0].replace(" ", "") == "JLB_JUB": # XX axis
                gridData['JLB'] = int(elems[1].strip().split(" ")[0])
                gridData['JUB'] = int(elems[1].strip().split(" ")[1])
            elif elems[0].replace(" ", "") == "COORD_TIP":
                gridData['COORD_TIP'] = elems[1].replace(" ","")
            elif elems[0].replace(" ", "") == "ORIGIN":
                gridData['ORIGIN_X'] = float(elems[1].strip().split(" ")[0])
                gridData['ORIGIN_Y'] = float(elems[1].strip().split(" ")[1])
            # TODO: Is ZONE an integer?
            elif elems[0].replace(" ", "") == "ZONE":
                gridData['ZONE'] = elems[1].replace(" ","")
            elif elems[0].replace(" ", "") == "GRID_ANGLE":
                gridData['GRID_ANGLE'] = float(elems[1].replace(" ",""))
            elif elems[0].replace(" ", "") == "LATITUDE":
                gridData['LATITUDE'] = float(elems[1].replace(" ", ""))
            elif elems[0].replace(" ", "") == "LONGITUDE":
                gridData['LONGITUDE'] = float(elems[1].replace(" ", ""))
            elif elems[0].replace(" ", "") == "CONSTANT_SPACING_X":
                gridData['CONSTANT_SPACING_X'] = int(elems[1].replace(" ", ""))
            elif elems[0].replace(" ", "") == "CONSTANT_SPACING_Y":
                gridData['CONSTANT_SPACING_Y'] = int(elems[1].replace(" ", ""))
            elif elems[0].replace(" ", "") == "DX":
                gridData['DX'] = float(elems[1].replace(" ", ""))
            elif elems[0].replace(" ", "") == "DY":
                gridData['DY'] = float(elems[1].replace(" ", ""))
        return gridData