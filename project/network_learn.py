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

def run_STDP(spiking_neurons, spike_times, tau_s, tau_t, A1, A2, wmax, w_init):
    # define pre, post neurons and connection
    pre=bp.neurons.AdExIF(n_PC)
    post=bp.neurons.AdExIF(n_PC)
    syn=STDP(pre,post,bp.connect.All2All())
    net=bp.Network(pre,syn,post)