## using the weight matrix produced in network_learn.py to construct a neuron
## network to simulate the SWRs 
import brainpy as bp
import brainpy.math as bm
class EINet(bp.Network):
    def __init__(self,num_exc,num_inh,method='exp_auto',**kwargs):
        super(EINet, self).__init__(**kwargs)
        pars = dict()