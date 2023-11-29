## using the weight matrix produced in network_learn.py to construct a neuron
## network to simulate the SWRs 

import numpy as np
import brainpy as bp
import brainpy.math as bm
import matplotlib.pyplot as plt
from file_management import read_conn_matrix, read_weight_matrix
from classes import ca3simu
from parameter import *

# input file name
conn_file="connection_PC.txt"
weight_matrix_file="weight_matrix_PC.txt"

# get the conn and weight matrix
conn_PC=read_conn_matrix(conn_file)
weight_matrix_PC=read_weight_matrix(weight_matrix_file)

freq=rate_MF
mode=0 # asym
seed=1234

# build the network
def run_ca3simu(dur,freq,conn_PC,weight_matrix_PC,mode,seed):
    net=ca3simu(freq=freq,conn_PC_E=conn_PC,wmx_PC_E=weight_matrix_PC,mode=mode,seed=seed)
    runner=bp.DSRunner(
        net,
        monitors=['PCs.spike','PCs.freq']
    )
    runner(dur)

    ## to plot