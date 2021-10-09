#!/bin/python3
import os
import pandas as pd
import numpy as np
from math import cos,sin

class TAOSiPM:
    """Info of SiPM
    """

    def __init__(self,
            info_path = os.path.join(
                os.getenv("GENERALPATH"),
                "sipm_pos.csv"
                )
            ):
        self.sipm_pos = pd.read_csv(info_path)
        self.sipm_center_radius = 930.2

    def get_xyz(self,index = None):
        """get xyz of sipm

        Args:
            index : index of SiPM, if index = None, we will return position of all sipm

        Return:
            {"x":x,"y":y,"z":z}
        """
        if index is not None:
            theta = self.sipm_pos["theta"][index]*np.pi/180
            phi   = self.sipm_pos["phi"][index]*np.pi/180

            x = self.sipm_center_radius*sin(theta)*cos(phi)
            y = self.sipm_center_radius*sin(theta)*sin(phi)
            z = self.sipm_center_radius*cos(theta)
            ids = index
        else:
            ids = self.sipm_pos["index"].to_numpy()
            theta  = self.sipm_pos["theta"].to_numpy()*np.pi/180
            phi    = self.sipm_pos["phi"].to_numpy()*np.pi/180

            x = self.sipm_center_radius*np.sin(theta)*np.cos(phi)
            y = self.sipm_center_radius*np.sin(theta)*np.sin(phi)
            z = self.sipm_center_radius*np.cos(theta)


        return {"x":x,"y":y,"z":z,"index":ids}

def test():
    data = TAOSiPM()
    print(data.get_xyz(1))
    print(pd.DataFrame(data.get_xyz()))

if __name__ == "__main__":
    test()
