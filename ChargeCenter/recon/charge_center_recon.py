#!/bin/python3
from .recon_res import ReconResData
from General import TAOSiPM
from TaoDataAPI import TAOData
from tqdm import trange
import numpy as np

class ChargeCenterRecon:

    def __init__(self,
            p0 = -1.0*0.8499/0.6997,
            p1 = 1.0/0.6997
            ):
        """Charge Center Vertex Reconstruction
        rec_r = charge_center_r*p1 + p0
        Args:
            p0 : intercept of linear relation between R_edep and R_true
            p1 : slope of linear relation between R_edep and R_true
        """
        self.p0 = p0
        self.p1 = p1
        self.initialize()

    def initialize(self):
        """Initialize the reconstruction class
        """
        self.recon_result = ReconResData()
        self.tao_sipm = TAOSiPM()
        self.sipm_xyz = self.tao_sipm.get_xyz()

    def reconstruct_single_evt(self, data, idx):
        """reconstruct single event

        Args:
            data : TAOData (raw data)
            idx  : The event id you want to reconstruct

        Return:
            recon_idx : index of reconstruction data
        """
        data.GetEntry(idx)
        hit_id = data.GetAttr("fSiPMHitID")
        hits = data.GetAttr("fNSiPMHit")
        edep = data.GetAttr("fGdLSEdep")
        x_edep = data.GetAttr("fGdLSEdepX")
        y_edep = data.GetAttr("fGdLSEdepY")
        z_edep = data.GetAttr("fGdLSEdepZ")
        particle = data.GetAttr("fPrimParticlePDG")[0] # only record first particle

        x_rec= self.p0 + self.p1*np.sum(self.sipm_xyz["x"][hit_id])/hits
        y_rec= self.p0 + self.p1*np.sum(self.sipm_xyz["y"][hit_id])/hits
        z_rec= self.p0 + self.p1*np.sum(self.sipm_xyz["z"][hit_id])/hits

        recon_idx = self.recon_result.push(
                x_edep,y_edep,z_edep,
                x_rec,y_rec,z_rec,
                edep,particle
                )
        recon_idx -= 1

        return recon_idx

    def reconstruct(self, data,
            idx_start = None, idx_end = None,
            show_detail = False
            ):
        """vertex reconstruction

        Args:
            data : TAOData
            idx_start : start index
            idx_end   : end index

        Return:
            data : ReconResData
        """
        if idx_start is None:
            idx_start = 0
        if idx_end is None:
            idx_end = data.GetEntries()

        if show_detail:
            for idx in trange(idx_start,idx_end):
                self.reconstruct_single_evt(data,idx)
        else:
            for idx in range(idx_start,idx_end):
                self.reconstruct_single_evt(data,idx)

        return self.recon_result
