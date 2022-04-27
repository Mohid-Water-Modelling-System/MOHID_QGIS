import shapefile
import os
import sys
import getopt

def polygon2WKT(input_path):
    input_f = open(input_path, "r")
    output_f = open(input_path + "_WKT", "w")
    l = input_f.readline()
    while (l != ""):
        if l == "<beginpolygon>\n":
            curr_polygon = "POLYGON(("
            print(l)
        elif l == "<endpolygon>\n":
            curr_polygon = curr_polygon[:-2]
            curr_polygon += "))\n"
            output_f.write(curr_polygon)
            print(l)
        else:
            coord = l.split(" ")
            print(l)
            if len(coord) != 3:
                input_f.close()
                output_f.close()
                return
            curr_polygon += l.rstrip() + ", " 
        l = input_f.readline()
    input_f.close()
    output_f.close()
    return

def polygon2shp(input_path):
    input_f = open(input_path, "r")
    writer = shapefile.Writer(os.path.splitext(input_path)[0])
    writer.field("name", "C")
    poly_count = 0
    
    l = input_f.readline()
    curr_polygon = []
    coord_size = 0

    while (l != ""):
        l = l.rstrip()
        if l == "<beginpolygon>":
            curr_polygon = []
            coord_size = 0
        elif l == "<endpolygon>":
            print(curr_polygon)
            if coord_size == 3:
                writer.polyz([curr_polygon])
                writer.record('polygonz ' + str(++poly_count))
            elif coord_size == 2:
                writer.poly([curr_polygon])
                writer.record('polygon ' + str(++poly_count))
        else:
            coord = l.split(" ")
            coord = list(filter(lambda x: x != '', coord))
            print(coord)
            if not curr_polygon:
                coord_size = len(coord)

            elif len(coord) != coord_size:
                print('invalid coordinates')
                input_f.close()
                writer.close()
                return
            curr_polygon.append(list(map(float,coord)))

        l = input_f.readline()
    print('done')
    input_f.close()
    writer.close()
    
    return

def main(argv):
    inputfile = ''
    _format = ''
    try:
        opts, args = getopt.getopt(argv,"hf:i:",["format=","ifile="])
    except getopt.GetoptError:
        print('polygonConverter.py -f <format> -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('polygonConverter.py -f <format> -i <inputfile>\nformat := { shp | wkt }')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-f", "--format"):
            _format = arg
    if _format == 'shp':
        polygon2shp(inputfile)
    elif _format == 'wkt':
        polygon2WKT(inputfile)
                                                                                                                        
if __name__ == "__main__":
    main(sys.argv[1:])
