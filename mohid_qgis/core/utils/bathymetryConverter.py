import shapefile
import os
import logging 
logger = logging.getLogger(__name__)

def saveToMohidFile(outputPath, bat):

    data = bat.gridData
    if not outputPath.endswith(".dat"):
        outputPath = outputPath + ".dat"

    with open(outputPath, 'w') as f:
        f.write("COMEMNT: File generated by\n")
        f.write("COMEMNT: MOHID QGIS Plugin\n")
        f.write("\n\n")

        try:
            f.write(f"ILB_IUB :      {data['ILB']} {data['IUB']}\n")
            f.write(f"JLB_JUB :      {data['JLB']} {data['JUB']}\n")
            f.write(f"COORD_TIP :    {data['COORD_TIP']}\n")
            f.write(f"ORIGIN :       {data['ORIGIN_X']} {data['ORIGIN_Y']}\n")
            f.write(f"GRID_ANGLE :   {data['GRID_ANGLE']}\n")
            f.write(f"SRID :         {data['SRID']}\n")
            f.write(f"LATITUDE :     {data['LATITUDE']}\n")
            f.write(f"LONGITUDE :    {data['LONGITUDE']}\n")
            f.write(f"FILL_VALUE :   {data['FILL_VALUE']}\n")

            if data['ZONE'] is not None:
                f.write(f"ZONE :         {data['ZONE']}\n")
            
            f.write("\n\n")
            
            if bat.type == "regular":
                f.write("<BeginXX>\n")
                for p in data['POINTS_XX']:
                    f.write(f"{p:.15f}\n")
                f.write("<EndXX>\n")

                f.write("<BeginYY>\n")
                for p in data['POINTS_YY']:
                    f.write(f"{p:.15f}\n")
                f.write("<EndYY>\n")
            elif bat.type == "curvillinear":
                f.write("<CornersXY>\n")
                for p in data['CORNERS']:
                    f.write(f"{p[0]} {p[1]}\n")
                f.write("<\\CornersXY>\n")

            f.write("<BeginGridData2D>\n")
            for p in data['DATA_2D']:
                f.write(f"{p:.15f}\n")
            f.write("<EndGridData2D>\n")
        except Exception:
            # logger.debug("Something went wrong saving to mohid file")
            pass

def saveGenerateMohidFile(outPath, batFilepath, gridPath, xyzPaths, landPaths):
    
    with open(outPath, "w") as f:
        f.write(f"BATIM_FILE: {batFilepath}\n")
        f.write("\n")
        f.write(f"GRID_FILE: {gridPath}\n")
        f.write("\n")

        if landPaths:
            f.write("<BeginLandAreaFiles>\n")
            for landPath in landPaths:
                f.write(f"{landPath}\n")
            f.write("<EndLandAreaFiles>\n")
        
        f.write("\n\n")

        f.write("<BeginXYZPointsFiles>\n")
        for xyzPath in xyzPaths:
            f.write(f"{xyzPath}\n")
        f.write("<EndXYZPointsFiles>\n")

        f.write("\n\n")

        f.write(f"SMOOTH                    : 0\n")
        f.write(f"RADIUS                    : 0.008\n")
        f.write("\n\n")
        f.write(f"INTERPOLATION             : No Interpolation\n")
        f.write("\n")
        f.write(f"POINTS_FOR_INTERPOLATION  : 3\n")
        f.write(f"EXPAND_GRID_LIMITS        : 1\n")
        f.write(f"GRID_LIMITS_PERCENTAGE    : 0.25\n")

def MOHIDBathymetry2shp(input_path, bathymetry):
    # TODO: filename with dots are not advised, account for this in the future
    readFile = False
    if bathymetry is None:
        readFile = True
    
    if readFile:
        pass
    else:
        logger.debug(f"Converting {input_path} to shapefile")
        with shapefile.Writer(os.path.splitext(input_path)[0]) as writer:
            writer.autoBalance = 1
            id=1
            depthInd = 0
            writer.field("ID", "N")
            writer.field("depth", "F", size="20", decimal=8)
            maxI = bathymetry.gridData['IUB']
            maxJ = bathymetry.gridData['JUB']
            originX = bathymetry.gridData['ORIGIN_X']
            originY = bathymetry.gridData['ORIGIN_Y']
            if bathymetry.type == "regular":
                DX = bathymetry.gridData['POINTS_XX']
                DY = bathymetry.gridData['POINTS_YY']
                depthData = bathymetry.gridData['DATA_2D']
                for i in range(maxI):
                    for j in range(maxJ):
                        vertices = []
                        parts = []
                        # Cell vertices
                        # Special attention to first cell of each row
                        vertices.append([originX + DX[j], originY + DY[i]])     # Bottom left corner
                        vertices.append([originX + DX[j + 1], originY + DY[i]]) # Bottom rigth corner
                        vertices.append([originX + DX[j + 1], originY + DY[i + 1]]) # # Top rigth corner
                        vertices.append([originX + DX[j], originY + DY[i + 1]]) # Top left corner
                        parts.append(vertices)
                        writer.poly(parts)
                        writer.record(ID=id, depth=depthData[depthInd])
                        depthInd += 1
                        id += 1
            elif bathymetry.type == "curvillinear":
                EMPTY_VALUE = float("-9.9e15")
                # Num of corners > Num of cells 
                rowsOfCorners = maxI + 1
                colsOfCorners = maxJ + 1
                corners = bathymetry.gridData["CORNERS"]
                depthData = bathymetry.gridData['DATA_2D']
                # Iterate two rows at a time to gather cells' coords
                for row in range(0, rowsOfCorners-1):
                    lastLine = corners[row*colsOfCorners:row*colsOfCorners+colsOfCorners]
                    curLine = corners[(row+1)*colsOfCorners:(row+1)*colsOfCorners+colsOfCorners]
                    logger.debug(f"Last line has indexes {row*colsOfCorners}:{row*colsOfCorners+colsOfCorners}")
                    logger.debug(f"Current line has indexes {(row+1)*colsOfCorners}:{(row+1)*colsOfCorners+colsOfCorners}")
                    for i in range(0, len(curLine)-1):
                        # Any group of 4 corners that has empty values is ignored
                        if EMPTY_VALUE in [
                                    lastLine[i][0], lastLine[i][1]
                                ,   lastLine[i+1][0], lastLine[i+1][1]
                                ,   curLine[i+1][0], curLine[i+1][1]
                                ,   curLine[i][0], curLine[i][1]]:
                            writer.record(ID=id, depth=depthData[depthInd])
                            id += 1
                            depthInd += 1
                            continue
                        vertices = []
                        parts = []
                        vertices.append([originX + lastLine[i][0], originY + lastLine[i][1]])     # Bottom left corner
                        vertices.append([originX + lastLine[i+1][0], originY + lastLine[i+1][1]])   # Bottom rigth corner
                        vertices.append([originX + curLine[i+1][0], originY + curLine[i+1][1]])   # Top rigth corner
                        vertices.append([originX + curLine[i][0], originY + curLine[i][1]])       # Top left corner
                        parts.append(vertices)
                        # It's important to first write the record and then the 
                        # feature geometry, otherwise, the geometry is written
                        # to the previous record creating bad days
                        writer.record(ID=id, depth=depthData[depthInd])
                        writer.poly(parts)
                        id += 1
                        depthInd += 1
    return