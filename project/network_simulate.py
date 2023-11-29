## using the weight matrix produced in network_learn.py to construct a neuron
## network to simulate the SWRs 

import numpy as np
import brainpy as bp
import brainpy.math as bm
import matplotlib.pyplot as plt
from file_management import read_pre2post, read_weight
from classes import ca3simu
from parameter import *

# build the network
def run_ca3simu(dur,freq,conn_PC,weight_matrix_PC,mode,seed):
    net=ca3simu(freq=freq,conn_PC_E=conn_PC,wmx_PC_E=weight_matrix_PC,mode=mode,seed=seed)
    runner=bp.DSRunner(
        net,
        monitors=['PCs.spike','PCs.freq']
    )
    runner(dur)

    ts=runner.mon.ts
    PC_spikes=runner.mon['PCs.spike']
    PC_freqs=runner.mon['PCs.freq']
    return ts, PC_spikes, PC_freqs

def get_wmx_preid(n_pre,n_post,pre2post,weight):
    matrix=np.zeros((n_pre,n_post))
    pre_id=np.zeros(n_pre)
    for id_vec in range(len(pre2post[1])-1):
        start=pre2post[1][id_vec]
        end=pre2post[1][id_vec+1]
        post_ides=pre2post[0][start:end]
        matrix[id_vec][post_ides]=weight[start:end]
        pre_id[start:end]=id_vec
    return matrix,pre_id

# input file name
header="asym_"
pre2post_file="pre2post.npy"
weight_file="weight.npy"

# get the pre2post and weight 
pre2post_PC=read_pre2post(pre2post_file)
weight_PC=read_weight(weight_file)

freq=rate_MF
mode="asym"
seed=1234
dur=1000 ## ms

# to run
wmx_PC,pre_id=get_wmx_preid(n_pre=n_PC,n_post=n_PC,pre2post=pre2post_PC,weight=weight_PC)
post_id=np.array(weight_PC[0])
conn=bp.conn.IJConn(i=pre_id,j=post_id)
conn = conn(pre_size=n_PC, post_size=n_PC)
ts,PC_spikes,PC_freqs=run_ca3simu(dur=dur,freq=freq,conn_PC=conn,weight_matrix_PC=wmx_PC,mode=mode,seed=seed)
