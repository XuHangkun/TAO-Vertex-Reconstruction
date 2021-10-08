#!/bin/python
from math import cos,acos,asin,sin,pow
import numpy as np
import pandas as pd

b_file = open("./basic/run_2d_vertex_positron.sh","r")
lines = b_file.readlines()

sim_info = {
        "radius":[],
        "theta":[],
        "x":[],
        "y":[],
        "z":[]
        }

theta_num = 20
radius_num = 20
radius_max = 900
for theta_index in range(theta_num+1):
    for radius_index in range(radius_num+1):
        theta = acos(1 - 2.0*(theta_index)/theta_num)
        radius = pow(radius_index*pow(radius_max,3)/radius_num,1.0/3)
        x = int(radius*sin(theta))
        y = int(0)
        z = int(radius*cos(theta))
        theta = 180*theta/np.pi

        sim_info["radius"].append(radius)
        sim_info["theta"].append(theta)
        sim_info["x"].append(x)
        sim_info["y"].append(y)
        sim_info["z"].append(z)

        # open another file
        new_f = open("./map2d/run_vertex_x%d_y%d_z%d_positron.sh"%(x,y,z),"w")
        for line in lines:
            new_line = line.replace("x=${3}","x=%d"%(x))\
                    .replace("y=${4}","y=%d"%(y))\
                    .replace("z=${5}","z=%d"%(z))
            new_f.write(new_line)
        new_f.close()

b_file.close()
# store position
data = pd.DataFrame(sim_info)
data.to_csv("./template_sim_2dmap_position.csv",index=None)
