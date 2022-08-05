import shapefile
import os

def XYZ2shp(input_path):
    with open(input_path, "r") as input_f:
        with shapefile.Writer(os.path.splitext(input_path)[0]) as writer:
            writer.autoBalance = 1
            writer.field("depth", "F", size=20, decimal=8)

            for line in input_f:
                line = line.strip("\n")
                if line in ["<begin_xyz>", "<end_xyz>", ""]:
                    continue
                else:
                    nums = list(filter(lambda x: x != '', line.split(" ")))
                    writer.record(float(nums[2]))
                    writer.point(float(nums[0]), float(nums[1]))

    return f"{os.path.splitext(input_path)[0]}.shp" 