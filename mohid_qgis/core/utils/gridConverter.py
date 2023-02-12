import shapefile
import os
import sys
import getopt
import netCDF4
import math
import numpy as np
import logging
logger = logging.getLogger(__name__)
"""
ILB_IUB - Two integer numbers defining the minimum and maximum I values along the Y-axis of the grid.
JLB_JUB - Two integer numbers defining the minimum and maximum J values along the X-axis of the grid.
COORD_TIP - A flag which indicates the used coordinates type.
ORIGIN - Two real values, which indicate the origin of the lower left corner of the grid (X Y).
ZONE - Integer values defining the UTM Zone where the bathymetry is located.
GRID_ANGLE - Counter-clock mesh rotation relative to the north. The base point is the origin of the grid.
LATITUDE - Average latitude value used to compute Coriolis frequency and solar radiation when metric coordinates cannot be converted to WGS84 geographic coordinates.
LONGITUDE - Average longitude value used to compute Coriolis frequency and solar radiation when metric coordinates cannot be converted to WGS84 geographic coordinates.
CONSTANT_SPACING_X - Boolean defining if the spacing in the X axis is constant
CONSTANT_SPACING_Y - Boolean defining if the spacing in the Y axis is constant
DX - Constant spacing distance in XX axis
DY - Constant spacing distance in YY axis
"""
#TESTAR AS DIFERENÇAS ENTRE O NETCDF QUE FUNCIONA E O GERADO

#rootgrp1 = netCDF4.Dataset("../Projects/TagusBathymetry.nc", "r", format="NETCDF4")
#rootgrp2 = netCDF4.Dataset("../Projects/2021051400.nc", "r", format="NETCDF4")
###print(rootgrp.dimensions)
#print(rootgrp1.variables["lat"][:])
#print(rootgrp2.variables["lat"][:])
#print(rootgrp1.dimensions)
#print(rootgrp2.dimensions)


def grid2netCDF(input_path):
    rootgrp = netCDF4.Dataset(os.path.splitext(input_path)[0] + ".nc", "w", format="NETCDF4")

    is_reading = "info"
    info = []
    x_values = []
    y_values = []
    data_values = []

    with open(input_path, "r") as input_f:
        l = input_f.readline()
        while (l != ""):
            l = l.rstrip()
            l = l.split(" ")
            l = list(filter(lambda x: x not in ('',':','\t','\n'), l))
            if ("<BeginXX>" in l):
                is_reading = "x"
            elif ("<BeginYY>" in l):
                is_reading = "y"
            elif ("<BeginGridData2D>" in l):
                is_reading = "data"
            elif (is_reading == "info"):
                info += [l]
            elif (is_reading == "x"):
                x_values += l
            elif (is_reading == "y"):
                y_values += l
            elif (is_reading == "data"):
                data_values += l
            l = input_f.readline()
    
    info = [x for x in info if x != []]

    for i in info:
        if 'COMENT' in i[0]:
            continue
        elif i[0] == 'LATITUDE':
            latitude = float(i[1])
            print("LATITUDE ", latitude)
        elif i[0] == 'LONGITUDE':
            longitude = float(i[1])
            print("LONGITUDE ", longitude)
        elif i[0] == 'ORIGIN':
            origin_x = float(i[1])
            origin_y = float(i[2])
            print(origin_x, origin_y)
        elif i[0] == 'DX':
            dx = float(i[1])
            print("DX ",dx)
        elif i[0] == 'DY':
            dy = float(i[1])
            print("DY ",dy)
        elif i[0] == 'GRID_ANGLE':
            angle = float(i[1])
            print(angle)
        elif i[0] == 'ILB_IUB':
            i_min = int(i[1])
            i_max = int(i[2])
            print("ILB_IUB ", i_min, i_max)
        elif i[0] == 'JLB_JUB':
            j_min = int(i[1])
            j_max = int(i[2])
            print("JLB_JUB ", j_min, j_max)
        elif i[0] == 'CONSTANT_SPACING_X':
            if int(i[1]) == 1:
                constant_x = True
            else:
                constant_x = False
        elif i[0] == 'CONSTANT_SPACING_Y':
            if int(i[1]) == 1:
                constant_y = True
            else:
                constant_y = False

    x_values = [(float(x) + origin_x) for x in x_values[:-1]]
    y_values = [(float(y) + origin_y)for y in y_values[:-1]]
    data_values = [float(d) for d in data_values[:-1]]


    lon = rootgrp.createDimension("lon", j_max)
    lat = rootgrp.createDimension("lat", i_max)
    level = rootgrp.createDimension("level", None)
    time = rootgrp.createDimension("time", None)

    times = rootgrp.createVariable("time","f8",("time",))
    levels = rootgrp.createVariable("level","i4",("level",))
    latitudes = rootgrp.createVariable("lat", "f4", ("lat",))
    longitudes = rootgrp.createVariable("lon", "f4", ("lon",))
    bathymetry = rootgrp.createVariable("bathymetry", "f4", ("lat", "lon"))
    
    latitudes.longname = "latitude"
    latitudes.standard_name = "latitude"
    latitudes.units = "degrees_north"
    latitudes.valid_min = -90.0
    latitudes.valid_max = 90.0
    latitudes.axis = "Y"
    latitudes.reference = "geographical coordinates, WGS84 projection"

    longitudes.longname = "longitude"
    longitudes.standard_name = "longitude"
    longitudes.units = "degrees_east"
    longitudes.valid_min = -180.0
    longitudes.valid_max = 180.0
    longitudes.axis = "X"
    longitudes.reference = "geographical coordinates, WGS84 projection"

    latitudes[:] = np.array(y_values[1:])
    longitudes[:] = np.array(x_values[1:])
    bathymetry[:] = np.array(data_values).reshape(i_max, j_max)
    rootgrp.close()
    return


def gridtest():
    logger.debug("Grid test is being called for some unknown reason")
    minx,maxx,miny,maxy = 38.4386, 48.75, -9.8435, 10.1
    dx = 1
    dy = 1

    nx = int(math.ceil(abs(maxx - minx)/dx))
    ny = int(math.ceil(abs(maxy - miny)/dy))

    w = shapefile.Writer("..\Projects\TestGrid")
    w.autoBalance = 1
    w.field("ID")
    id=0

    for i in range(ny):
        for j in range(nx):
            id+=1
            vertices = []
            parts = []
            vertices.append([min(minx+dx*j,maxx),max(maxy-dy*i,miny)])
            vertices.append([min(minx+dx*(j+1),maxx),max(maxy-dy*i,miny)])
            vertices.append([min(minx+dx*(j+1),maxx),max(maxy-dy*(i+1),miny)])
            vertices.append([min(minx+dx*j,maxx),max(maxy-dy*(i+1),miny)])
            parts.append(vertices)
            w.poly(parts)
            w.record(id)
    w.close()
    return

def grid2shp(input_path, output_path = None):

    if not output_path:
        output_path = input_path
    logger.info(f"Converting {input_path} to shapefile")
    try:
        with open(input_path, "r") as input_f:
            with shapefile.Writer(os.path.splitext(output_path)[0]) as writer:
                writer.field("ID", "N")
                origin_x = 0.0
                origin_y = 0.0
                latitude = 0.0
                longitude = 0.0
                constant_x = False
                constant_y = False
                dx = 0.0
                dy = 0.0
                i_min = 0
                i_max = 0
                j_min = 0
                j_max = 0
                angle = 0.0
                POINTS_XX = []
                POINTS_YY = []
                # for l in input_f:
                #     l = l.rstrip()
                #     l = l.split(" ")
                #     l = list(filter(lambda x: x not in ('',':','\t','\n'), l))
                #     info += [l]
                
                # info = [x for x in info if x != []]
                logger.debug("MOHID Grid parameters:")
                for line in input_f:
                    line = line.strip('\n').split(" ")
                    i = list(filter(lambda x: x not in ('',':','\t','\n'), line))
                    
                    if not i:
                        continue
                    elif 'COMENT' in i[0]:
                        continue
                    elif i[0] == 'LATITUDE':
                        latitude = float(i[1])
                        logger.debug(f"LATITUDE: {latitude}")
                    elif i[0] == 'LONGITUDE':
                        longitude = float(i[1])
                        logger.debug(f"LONGITUDE: {longitude}")
                    elif i[0] == 'ORIGIN':
                        origin_x = float(i[1])
                        origin_y = float(i[2])
                        logger.debug(f"Origin: {origin_x}, {origin_y}")
                    elif i[0] == 'DX':
                        dx = float(i[1])
                        logger.debug(f"DX: {dx}")
                    elif i[0] == 'DY':
                        dy = float(i[1])
                        logger.debug(f"DY {dy}")
                    elif i[0] == 'GRID_ANGLE':
                        angle = float(i[1])
                        logger.debug(f"Angle: {angle}")
                    elif i[0] == 'ILB_IUB':
                        i_min = int(i[1])
                        i_max = int(i[2])
                        logger.debug(f"ILB_IUB: {i_min}, {i_max}")
                    elif i[0] == 'JLB_JUB':
                        j_min = int(i[1])
                        j_max = int(i[2])
                        logger.debug(f"JLB_JUB {j_min}, {j_max}")
                    elif i[0] == 'CONSTANT_SPACING_X':
                        if int(i[1]) == 1:
                            constant_x = True
                        else:
                            constant_x = False
                    elif i[0] == 'CONSTANT_SPACING_Y':
                        if int(i[1]) == 1:
                            constant_y = True
                        else:
                            constant_y = False
                    elif "<BeginXX>" in i[0]:
                        # Read block of points
                        isPoint = True
                        while isPoint:
                            line = next(input_f).strip('\n').split(" ")
                            i = list(filter(
                                lambda x: x not in ('',':','\t','\n'), line))
                            if "<EndXX>" in i[0]:
                                isPoint = False
                            else:
                                POINTS_XX.append(float(i[0]))
                    elif "<BeginYY>" in i[0]:
                        # Read block of points
                        isPoint = True
                        while isPoint:
                            line = next(input_f).strip('\n').split(" ")
                            i = list(filter(
                                lambda x: x not in ('',':','\t','\n'), line))
                            if "<EndYY>" in i[0]:
                                isPoint = False
                            else:
                                POINTS_YY.append(float(i[0]))
                    else:
                        continue
                writer.autoBalance = 1
                id=0
                if constant_x and constant_y:
                    # Regular grid, built with DX, DY intervals
                    logger.info("Converting Regular Grid")
                    # i_max and j_max are the max number of cells
                    for i in range(i_max):
                        for j in range(j_max):
                            vertices = []
                            parts = []
                            
                            vertices.append([origin_x + dx * j, origin_y + (i_max - i - 1) * dy]) #4
                            vertices.append([origin_x + dx * (j + 1), origin_y + (i_max - i - 1)* dy]) #3
                            vertices.append([origin_x + dx * (j + 1), origin_y + (i_max - i) * dy]) #2
                            vertices.append([origin_x + dx * j, origin_y + (i_max - i) * dy]) #1
                            
                            parts.append(vertices)
                            writer.poly(parts)
                            writer.record(id)
                            id+=1
                elif POINTS_XX and POINTS_YY:
                    # Irregular grid, built with XX and YY points
                    logger.info("Converting Irregular Grid")
                    yPoints = i_max + 1
                    xPoints = j_max + 1
                    # Remove 1 as we iterate two elements at the same time
                    for i in range(yPoints-1):
                        for j in range(xPoints-1):
                            vertices = []
                            parts = []
                            
                            # Cell vertices
                            # Special attention to first cell of each row
                            ind_bLeft = xPoints * i + j
                            ind_bRight = xPoints * i + j + 1
                            ind_tRight = xPoints * (i + 1) + j + 1
                            ind_tLeft = xPoints * (i + 1) + j
                            vertices.append([
                                    POINTS_XX[ind_bLeft] 
                                ,   POINTS_YY[ind_bLeft]]) # Bottom left corner
                            vertices.append([
                                    POINTS_XX[ind_bRight]
                                ,   POINTS_YY[ind_bRight]]) # Bottom rigth corner
                            vertices.append([
                                    POINTS_XX[ind_tRight]
                                ,   POINTS_YY[ind_tRight]]) # Top rigth corner
                            vertices.append([
                                    POINTS_XX[ind_tLeft]
                                ,   POINTS_YY[ind_tLeft]]) # Top left corner
                            
                            parts.append(vertices)
                            writer.poly(parts)
                            writer.record(id)
                            id+=1
                else:
                    logger.warning("Invalid grid file")
                    return None
        logger.info(f"Successfully converted grid to shapefile {os.path.splitext(output_path)[0]}.shp")
        return f"{os.path.splitext(output_path)[0]}.shp"
    except Exception:
        logger.exception("Unable to convert grid file to shapefile")
        return None

def curvillinear2shp(input_path, output_path = None):

    if not output_path:
        output_path = input_path
    logger.info(f"Converting {input_path} to shapefile")
    try:
        with open(input_path, "r") as input_f:
            with shapefile.Writer(os.path.splitext(output_path)[0]) as writer:
                writer.field("ID", "N")
                origin_x = 0.0
                origin_y = 0.0
                latitude = 0.0
                longitude = 0.0
                constant_x = False
                constant_y = False
                dx = 0.0
                dy = 0.0
                i_min = 0
                i_max = 0
                j_min = 0
                j_max = 0
                angle = 0.0
                corners = []
                EMPTY_VALUE = float("-9.9e15")
                # for l in input_f:
                #     l = l.rstrip()
                #     l = l.split(" ")
                #     l = list(filter(lambda x: x not in ('',':','\t','\n'), l))
                #     info += [l]
                
                # info = [x for x in info if x != []]
                logger.debug("MOHID Grid parameters:")
                for line in input_f:
                    line = line.strip('\n').split(" ")
                    i = list(filter(lambda x: x not in ('',':','\t','\n'), line))
                    
                    if not i:
                        continue
                    elif 'COMENT' in i[0]:
                        continue
                    elif i[0] == 'LATITUDE':
                        latitude = float(i[1])
                        logger.debug(f"LATITUDE: {latitude}")
                    elif i[0] == 'LONGITUDE':
                        longitude = float(i[1])
                        logger.debug(f"LONGITUDE: {longitude}")
                    elif i[0] == 'ORIGIN':
                        origin_x = float(i[1])
                        origin_y = float(i[2])
                        logger.debug(f"Origin: {origin_x}, {origin_y}")
                    elif i[0] == 'DX':
                        dx = float(i[1])
                        logger.debug(f"DX: {dx}")
                    elif i[0] == 'DY':
                        dy = float(i[1])
                        logger.debug(f"DY {dy}")
                    elif i[0] == 'GRID_ANGLE':
                        angle = float(i[1])
                        logger.debug(f"Angle: {angle}")
                    elif i[0] == 'ILB_IUB':
                        i_min = int(i[1])
                        i_max = int(i[2])
                        logger.debug(f"ILB_IUB: {i_min}, {i_max}")
                    elif i[0] == 'JLB_JUB':
                        j_min = int(i[1])
                        j_max = int(i[2])
                        logger.debug(f"JLB_JUB {j_min}, {j_max}")
                    elif i[0] == 'CONSTANT_SPACING_X':
                        if int(i[1]) == 1:
                            constant_x = True
                        else:
                            constant_x = False
                    elif i[0] == 'CONSTANT_SPACING_Y':
                        if int(i[1]) == 1:
                            constant_y = True
                        else:
                            constant_y = False
                    elif i[0] == "<CornersXY>":
                        # Read corners
                        isPoint = True
                        while isPoint:
                            line = next(input_f).strip('\n').split(" ")
                            i = list(filter(
                                lambda x: x not in ('',':','\t','\n'), line))
                            if i[0] == "<\CornersXY>":
                                isPoint = False
                            else:
                                corners.append([float(i[0]), float(i[1])])
                    else:
                        continue
                writer.autoBalance = 1
                id=0
                if corners:
                    # Curvillinear grid
                    logger.info("Converting curvillinear Grid")
                    numOfRows = i_max + 1
                    numOfColumns = j_max + 1
                    for row in range(0, numOfRows-1):
                        lastLine = corners[row*numOfColumns:row*numOfColumns+numOfColumns]
                        curLine = corners[(row+1)*numOfColumns:(row+1)*numOfColumns+numOfColumns]
                        logger.debug(f"Last line has indexes {row*numOfColumns}:{row*numOfColumns+numOfColumns}")
                        logger.debug(f"Current line has indexes {(row+1)*numOfColumns}:{(row+1)*numOfColumns+numOfColumns}")

                        for i in range(0, len(curLine)-1):
                            # Any group of 4 corners that has empty values is ignored
                            if EMPTY_VALUE in [
                                lastLine[i][0], lastLine[i][1],
                                lastLine[i+1][0], lastLine[i+1][1],
                                curLine[i+1][0], curLine[i+1][1],
                                curLine[i][0], curLine[i][1]
                            ]:
                                continue
                            id += 1
                            vertices = []
                            parts = []
                            vertices.append([origin_x + lastLine[i][0], origin_y + lastLine[i][1]])     # Bottom left corner
                            vertices.append([origin_x + lastLine[i+1][0], origin_y + lastLine[i+1][1]])   # Bottom rigth corner
                            vertices.append([origin_x + curLine[i+1][0], origin_y + curLine[i+1][1]])   # Top rigth corner
                            vertices.append([origin_x + curLine[i][0], origin_y + curLine[i][1]])       # Top left corner
                    
                            parts.append(vertices)
                            writer.poly(parts)
                            writer.record(id)
                        
                else:
                    logger.warning("Invalid grid file")
                    return None
        logger.info(f"Successfully converted grid to shapefile {os.path.splitext(output_path)[0]}.shp")
        return f"{os.path.splitext(output_path)[0]}.shp"
    except Exception:
        logger.exception("Unable to convert grid file to shapefile")
        return None

def main(argv):
    inputfile = ''
    _format = ''
    try:
        opts, args = getopt.getopt(argv,"hf:i:o:",["format=","ifile=", "ofile="])
    except getopt.GetoptError:
        print('gridConverter.py -i <inputfile>')
        sys.exit(2)
    outputfile = None
    for opt, arg in opts:
        if opt == '-h':
            print('gridConverter.py -i <inputfile>')
            sys.exit()
        elif opt in ("-f", "--format"):
            _format = arg
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    if _format == "nc":
        grid2netCDF(inputfile, outputfile)
    elif _format == "shp":
        grid2shp(inputfile, outputfile)
                                                                                                                        
if __name__ == "__main__":
    main(sys.argv[1:])
