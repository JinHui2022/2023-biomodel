## using the weight matrix produced in network_learn.py to construct a neuron
## network to simulate the SWRs 

import numpy as np
import brainpy as bp
import matplotlib.pyplot as plt
from file_management import read_pre2post, read_weight
from classes import ca3simu
from parameter import *
from tools import get_wmx_preid

# build the network
def run_ca3simu(dur,freq,conn_PC,weight_matrix_PC,mode,seed):
    net=ca3simu(freq=freq,conn_PC_E=conn_PC,wmx_PC_E=weight_matrix_PC,mode=mode,seed=seed)
    runner=bp.DSRunner(
        net,
        monitors=['PCs.spike']
    )
    runner(dur)

    ts=runner.mon.ts
    PC_spikes=runner.mon['PCs.spike']

    return ts, PC_spikes

# input file name
header=".\data\asym_"
pre2post_file="pre2post.json"
weight_file="weight.npy"

# get the pre2post and weight 
pre2post_PC_tmp=read_pre2post(header+pre2post_file)
weight_PC=read_weight(header+weight_file)
pre2post_PC=np.zeros((2,), dtype=np.object_)
pre2post_PC[0]=np.array(pre2post_PC_tmp['post_id'])
pre2post_PC[1]=np.array(pre2post_PC_tmp['pre_pt'])

freq=rate_MF
mode="asym"
seed=1234
dur=5000 ## ms

# to run
wmx_PC,pre_id=get_wmx_preid(n_pre=n_PC,n_post=n_PC,pre2post=pre2post_PC,weight=weight_PC)
post_id=pre2post_PC[0]
conn=bp.conn.IJConn(i=pre_id,j=post_id)
conn = conn(pre_size=n_PC, post_size=n_PC)
ts,PC_spikes=run_ca3simu(dur=dur,freq=freq,conn_PC=conn,weight_matrix_PC=wmx_PC,mode=mode,seed=seed)

# to plot
fig,gs=plt.subplots()

bp.visualize.raster_plot(ts,PC_spikes,markersize=0.1)
plt.title('just for test')
plt.ylabel("Neuron Index")
plt.show()