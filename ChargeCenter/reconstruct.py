#!/bin/python3

import os
import argparse
import pandas
from recon import ReconResData, ChargeCenterRecon
from TaoDataAPI import TAOData
import time

def recon_args():
    default_data_path = os.getenv("DATAPATH")
    default_output_path = os.path.join(os.getenv("RESULTPATH"),"ChargeCenter/charge_center_recon.csv")
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputs',nargs="+",
            default=[os.path.join(default_data_path,"uni_ibd/ibd_1MeV_v1.root")])
    parser.add_argument('--show_detail',action="store_true")
    parser.add_argument('--output',default=default_output_path)
    args = parser.parse_args()
    print(args)
    return args

def reconstruct():
    # get args
    args = recon_args()

    # create raw data
    raw_data = TAOData(args.inputs)
    raw_data.SetBranchStatus(["*"],0)
    raw_data.SetBranchStatus(
            ["fSiPMHitID","fNSiPMHit","fGdLSEdep",
                "fGdLSEdepX","fGdLSEdepY","fGdLSEdepZ",
                "fPrimParticlePDG"
                ],
            1)

    # reconstruction
    charge_center_recon = ChargeCenterRecon()
    recon_res = charge_center_recon.reconstruct(
            data = raw_data,show_detail = args.show_detail)
    res_df = recon_res.to_df()
    res_df.to_csv(args.output,index=None)

if __name__ == "__main__":
    reconstruct()
