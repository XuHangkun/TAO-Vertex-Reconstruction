#!/bin/python3
import pandas as pd

class ReconResData:
    """
    Result of recon
    """
    def __init__(self):
        self.evt_num = 0
        self.x_true = []
        self.y_true = []
        self.z_true = []
        self.x_rec = []
        self.y_rec = []
        self.z_rec = []
        self.e_true = []
        self.particle_true = []

    def push(self,
            x_true,
            y_true,
            z_true,
            x_rec,
            y_rec,
            z_rec,
            e_true = None,
            particle_true = None):
        """
        Return:
            evt_number
        """
        self.x_true.append(x_true)
        self.y_true.append(y_true)
        self.z_true.append(z_true)
        self.x_rec.append(x_rec)
        self.y_rec.append(y_rec)
        self.z_rec.append(z_rec)
        self.e_true.append(e_true)
        self.particle_true.append(particle_true)
        self.evt_num += 1

        return self.evt_num

    def __add__(self,another):
        """ +
        Return:
            evt_number
        """
        self.x_true += other.x_true
        self.y_true += other.y_true
        self.z_true += other.z_true
        self.x_rec  += other.x_rec
        self.y_rec  += other.y_rec
        self.z_rec  += other.z_rec
        self.e_true += other.e_true
        self.particle_true += other.particle_true
        self.evt_num += other.evt_num

        return self.evt_num

    def to_df(self):
        """pack the data into a DataFrame
        """
        data = {
            "x_true":self.x_true,
            "y_true":self.y_true,
            "z_true":self.z_true,
            "x_rec":self.x_rec ,
            "y_rec":self.y_rec ,
            "z_rec":self.z_rec ,
            "e_true":self.e_true,
            "particle_true":self.particle_true
        }
        data = pd.DataFrame(data)
        return data

    def __getitem__(self,index):
        """index
        """
        data = {
            "x_true":self.x_true[index],
            "y_true":self.y_true[index],
            "z_true":self.z_true[index],
            "x_rec":self.x_rec[index] ,
            "y_rec":self.y_rec[index] ,
            "z_rec":self.z_rec[index] ,
            "e_true":self.e_true[index],
            "particle_true":self.particle_true[index]
        }
        return data

