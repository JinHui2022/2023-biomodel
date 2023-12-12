## based on the STDP rule, using the spike train produced in generate_spike_trains.py
## to create the weight matrix after learning

"""
Loads in hippocampal like spike train (produced by `generate_spike_trains.py`) and runs STD learning rule in a recurrent spiking neuron population
-> creates weight matrix for PC population, used by `spw*` scripts
updated to produce symmetric STDP curve as reported in Mishra et al. 2016 - 10.1038/ncomms11552
"""

import numpy as np
import brainpy as bp
import brainpy.math as bm
import matplotlib.pyplot as plt
from classes import STDP
from parameter import *
from file_management import read_spike_train, save_pre2post, save_weight

def load_spike_trains(file_path):
    """
    Loads in spike trains and converts it to 2 np.arrays for brainpy's SpikeTimeGroup
    :param file_path: file name of saved spike trains
    :return spiking_neurons, spike_times: same spike trains converted into SpikeTimeGroup
    """
    spike_trains=read_spike_train(file_path)
    spiking_neurons = 0 * np.ones_like(spike_trains[0])
    spike_times = np.asarray(spike_trains[0])
    for neuron_id in range(1, n_PC):
        tmp = neuron_id * np.ones_like(spike_trains[neuron_id])
        spiking_neurons = np.concatenate((spiking_neurons, tmp), axis=0)
        spike_times = np.concatenate((spike_times, np.asarray(spike_trains[neuron_id])), axis=0)

    return spiking_neurons, spike_times

def run_STDP(spiking_neurons, spiking_time, dur, mode, **kwargs):
    bm.set_dt(0.5)
    # STDP parameter
    if mode==0: ## asym
        taup=stdp['taup'][0]
        taum=stdp['taum'][0]
        Ap=stdp['Ap'][0]
        Am=stdp['Am'][0]
        wmax=stdp['wmax'][0]
        scale_factor=stdp['scale_factor'][0]
    elif mode==1:
        taup=stdp['taup'][1]
        taum=stdp['taum'][1]
        Ap=stdp['Ap'][1]
        Am=stdp['Am'][1]
        wmax=stdp['wmax'][1]
        scale_factor=stdp['scale_factor'][1]
    w_init=stdp['w_init']
    Ap*=wmax;Am*=wmax

    # construct the neuron network
    pre=bp.neurons.SpikeTimeGroup(size=n_PC, times=spiking_time, indices=spiking_neurons)
    post=bp.neurons.SpikeTimeGroup(size=n_PC, times=spiking_time, indices=spiking_neurons)
    conn=bp.conn.FixedProb(prob=connection_prob_PC, include_self=False, seed=42)
    syn=STDP(pre,post,conn,tau_s=taup,tau_t=taum,A1=Ap,A2=Am,wmax=wmax)
    syn.w*=w_init
    net=bp.Network(pre=pre,syn=syn,post=post)

    # to run
    runner=bp.DSRunner(
        net,
    )
    runner.run(dur)    
    syn.w *= scale_factor  # quick and dirty additional scaling! (in an ideal world the STDP parameters should be changed to include this scaling...)

    return syn.w,syn.pre2post

if __name__=="__main__":
    spike_train_file="spike_trains.npz"
    spiking_neurons, spiking_times=load_spike_trains(file_path=spike_train_file)
    weight_asym,pre2post=run_STDP(spiking_neurons=spiking_neurons,spiking_time=spiking_times,dur=1*1000,mode=0)
    
    ## save the result
    header="asym_"
    weight_file="weight.npy"
    pre2post_file='pre2post.json'
    save_weight(weight_asym,header+weight_file)
    save_pre2post(pre2post,file_name=header+pre2post_file)