## using the weight matrix produced in network_learn.py to construct a neuron
## network to simulate the SWRs 

import sys
import numpy as np
import brainpy as bp
from classes import ca3simu
from parameter import *
from plots import plot_raster

# build the network
def run_ca3simu(dur,freq,conn_PC,weight_matrix_PC,mode,mode_stp,seed):
    net=ca3simu(freq=freq,conn_PC_E=conn_PC,wmx_PC_E=weight_matrix_PC,mode=mode,mode_stp=mode_stp,seed=seed)
    runner=bp.DSRunner(
        net,
        monitors=['PCs.spike','MF.spike']
    )
    runner(dur)

    ts=runner.mon.ts
    PC_spikes=runner.mon['PCs.spike']
    MF_spikes=runner.mon['MF.spike']

    return ts, PC_spikes,MF_spikes

if __name__=="__main__":
    # input file name
    mode_sym=sys.argv[1]
    mode_stp=int(sys.argv[2])

    header=".\data\\"+mode_sym
    weight_file='_weight.npy'
    preid_file='_pre_id.npy'
    postid_file='_post_id.npy'

    # get the pre2post and weight 
    weight_PC=np.load(header+weight_file)
    pre_id=np.load(header+preid_file)
    post_id=np.load(header+postid_file)
    weight_PC*=0.283 # rescale

    freq=rate_MF
    seed=1234
    dur=3000 ## ms

    # to run
    wmx_PC=np.zeros((n_PC,n_PC))
    wmx_PC[pre_id,post_id]=weight_PC
    conn=bp.conn.IJConn(i=pre_id,j=post_id)
    conn = conn(pre_size=n_PC, post_size=n_PC)
    ts,PC_spikes,MF_spikes=run_ca3simu(dur=dur,freq=freq,conn_PC=conn,weight_matrix_PC=wmx_PC,mode=mode_sym,seed=seed,mode_stp=mode_stp)

    plot_raster(ts,PC_spikes,name="for test1")