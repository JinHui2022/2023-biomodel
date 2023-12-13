## using the weight matrix produced in network_learn.py to construct a neuron
## network to simulate the SWRs 

import numpy as np
import brainpy as bp
import matplotlib.pyplot as plt
from classes import ca3simu
from parameter import *

# build the network
def run_ca3simu(dur,freq,conn_PC,weight_matrix_PC,mode,seed):
    net=ca3simu(freq=freq,conn_PC_E=conn_PC,wmx_PC_E=weight_matrix_PC,mode=mode,seed=seed)
    runner=bp.DSRunner(
        net,
        monitors=['PCs.spike','MF.spike']
    )
    runner(dur)

    ts=runner.mon.ts
    PC_spikes=runner.mon['PCs.spike']
    MF_spikes=runner.mon['MF.spike']

    return ts, PC_spikes,MF_spikes

# input file name
header=".\data\\asym_"
weight_file='weight.npy'
preid_file='pre_id.npy'
postid_file='post_id.npy'

# get the pre2post and weight 
weight_PC=np.load(header+weight_file)
pre_id=np.load(header+preid_file)
post_id=np.load(header+postid_file)
weight_PC/=4 # rescale

freq=rate_MF
mode="asym"
seed=1234
dur=2000 ## ms

# to run
wmx_PC=np.zeros((n_PC,n_PC))
wmx_PC[pre_id,post_id]=weight_PC
conn=bp.conn.IJConn(i=pre_id,j=post_id)
conn = conn(pre_size=n_PC, post_size=n_PC)
ts,PC_spikes,MF_spikes=run_ca3simu(dur=dur,freq=freq,conn_PC=conn,weight_matrix_PC=wmx_PC,mode=mode,seed=seed)

# to plot
fig,gs=plt.subplots()

bp.visualize.raster_plot(ts,PC_spikes,markersize=0.5)
plt.title('just for test')
plt.ylabel("Neuron Index")
plt.show()