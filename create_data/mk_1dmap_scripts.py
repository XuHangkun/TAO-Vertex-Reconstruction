#!/bin/python
from math import cos,acos,asin,sin,pow
import numpy as np
import pandas as pd

b_file = open("./basic/run_1d_vertex_positron.sh","r")
lines = b_file.readlines()

sim_info = {
        "radius":[],
        "theta":[],
        "x":[],
        "y":[],
        "z":[]
        }

radius_num = 50
radius_max = 900

for radius_index in range(radius_num+1):
    theta = 90
    radius = pow(radius_index*pow(radius_max,3)/radius_num,1.0/3)
    x = int(radius)
    y = int(0)
    z = int(0)

    sim_info["radius"].append(radius)
    sim_info["theta"].append(theta)
    sim_info["x"].append(x)
    sim_info["y"].append(y)
    sim_info["z"].append(z)

    # open another file
    new_f = open("./map1d/run_vertex_x%d_y%d_z%d_positron.sh"%(x,y,z),"w")
    for line in lines:
        new_line = line.replace("x=${3}","x=%d"%(x))\
                .replace("y=${4}","y=%d"%(y))\
                .replace("z=${5}","z=%d"%(z))
        new_f.write(new_line)
    new_f.close()

# store position
data = pd.DataFrame(sim_info)
data.to_csv("./template_sim_1dmap_position.csv",index=None)
