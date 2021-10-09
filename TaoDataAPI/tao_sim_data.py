# -*- coding: utf-8 -*-
"""
    read tao simulation data
    ~~~~~~~~~~~~~~~~~~~~~~

    :author: Xu Hangkun (许杭锟)
    :copyright: © 2020 Xu Hangkun <xuhangkun@163.com>
    :license: MIT, see LICENSE for more details.
"""

import ROOT
ROOT.gSystem.Load("libEDMUtil")
ROOT.gSystem.Load("libSimEvent")

class TAOData:
    """read tao data from input files
    """

    def __init__(self,files,tree_name="Event/Sim/SimEvent"):
        """
        pars:
            files: list of simulation files,eg: ["file1","file2"]
        """
        self.tree_name = tree_name
        self.sim_event = self.get_event_tree(files)

    def get_event_tree(self,files):
        sim_event = ROOT.TChain(self.tree_name)
        for file in files:
            sim_event.Add(file)
        return sim_event

    def GetEntry(self,n):
        """
        Get n'th event
        Return:
            True: if we get the n'th entry
            False: ...
        """
        if n>=self.GetEntries() or n<0:
            return False

        self.sim_event.GetEntry(n)
        return True

    def SetBranchStatus(self,bnames=["*"],statu=1):
        for branch in bnames:
            self.sim_event.SetBranchStatus(branch,statu)

    def GetEntries(self):
        """Get total number of events
        """
        return self.sim_event.GetEntries()

    def GetAttr(self,attr_name):
        """Get value of attr_name

        return:
            value:
            None: loss
        """
        n_name = attr_name
        if attr_name[0] == "f":
            n_name = attr_name[1:]
        event = getattr(self.sim_event,"SimEvent")
        method = getattr(event,n_name,None)
        if method is not None:
            return method()
        else:
            return None

    def GetHist(self,hist,attr_name):
        self.SetBranchStatus(["*"],0)
        self.SetBranchStatus([attr_name],1)
        for i in range(self.GetEntries()):
            self.GetEntry(i)
            hist.Fill(self.GetAttr(attr_name))
        return hist

    def GetFullEdepHitMean(self,gaus_fit=False,add_edep=0):
        self.SetBranchStatus(["*"],0)
        self.SetBranchStatus(["fGdLSEdep","fNSiPMHit","fPrimParticleKE"],1)
        hits = []
        for i in range(self.GetEntries()):
            self.GetEntry(i)
            prim_ke = sum(self.GetAttr("fPrimParticleKE")) + add_edep
            if (self.GetAttr("fGdLSEdep")) < prim_ke*0.9995:
                continue
            else:
                hits.append(self.GetAttr("fNSiPMHit"))
        if gaus_fit:
            hist = ROOT.TH1F("full_edep_hits","full_edep_hits",100,min(hits),max(hits))
            for hit in hits:
                hist.Fill(hit)
            hist.Fit("gaus")
            mean = hist.GetFunction("gaus").GetParameter(1)
        else:
            mean = sum(hits)/len(hits)
        return mean

def Test(files):
    """ Test if the class can be used to Read
    """
    import time
    data = TAOData(files)
    data.SetBranchStatus(["*"],0)
    data.SetBranchStatus(["fNSiPMHit"],1)
    print("Entries: ",data.GetEntries())
    time_start=time.time()
    for i in range(1000):
        data.GetEntry(1)
        hits = data.GetAttr("fNSiPMHit")
        # print("N Hit for 1st Event: ",data.GetAttr("fNSiPMHit"))
    time_end=time.time()
    print('totally cost',time_end-time_start)

if __name__ == "__main__":
    files=["/dybfs/users/xuhangkun/SimTAO/TAO-Vertex-Reconstruction/data/uni_ibd/ibd_1MeV_v0.root"]
    Test(files)
