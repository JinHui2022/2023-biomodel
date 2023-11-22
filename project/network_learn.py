## based on the STDP rule, using the spike train produced in generate_spike_trains.py
## to create the weight matrix after learning

"""
Loads in hippocampal like spike train (produced by `generate_spike_trains.py`) and runs STD learning rule in a recurrent spiking neuron population
-> creates weight matrix for PC population, used by `spw*` scripts
updated to produce symmetric STDP curve as reported in Mishra et al. 2016 - 10.1038/ncomms11552
"""

