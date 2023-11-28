## using the weight matrix produced in network_learn.py to construct a neuron
## network to simulate the SWRs 
import brainpy as bp
import brainpy.math as bm
from parameter import *
class EINet(bp.Network):
    def __init__(self,num_PC,num_BC,PC_PC_conn,PC_PC_wmx,seed,**kwargs):
        super(EINet, self).__init__(**kwargs)
        pars1 = dict(V_rest=-75.1884554193901,V_reset = -29.738747396665072,V_th=-24.4255910105977+5*4.2340696257631,V_T=-24.4255910105977,delta_T=4.2340696257631,
                    a=-0.274347065652738,b=206.841448096415,tau=41.7488927175169,tau_w=84.9358017225512,tau_ref=5.96326930945599)
        pars2 = dict(V_rest=-74.74167987795019,V_reset =-64.99190523539687,V_th=-57.7092044103536+5*4.58413312063091,V_T=-57.7092044103536,delta_T=4.58413312063091,
                    a= 3.05640210724374,b=0.916098931234532,tau=15.773412296065,tau_w=178.581099914024,tau_ref=1.15622717832178)
        PCs=bp.neurons.AdExIF(num_PC, **pars1)
        BCs=bp.neurons.AdExIF(num_BC, **pars2)
        I_MF=bp.neurons.PoissonGroup(num_PC,freqs=freq)
        w_PC_I = 0.65  # nS
        w_BC_E = 0.85
        w_BC_I = 5.
        w_PC_E=wmx_PC_E
        if mode == "asym":
            w_PC_MF = 21.5
        elif mode == "sym":
            w_PC_MF = 19.15
        self.MF2PC=DualExponential(I_MF,PCs,bp.conn.One2One(),g_max=z*w_PC_MF,tau_decay=decay_PC_MF,tau_rise=rise_PC_MF,
                                   delay_step=delay_PC_E,E=Erev_E)
        self.PC_E=DualExponential(PCs,PCs,conn_PC_E,g_max=z*w_PC_E,tau_decay=decay_PC_E,tau_rise=rise_PC_E,
                                   delay_step=delay_PC_E,E=Erev_E)
        conn_PC_I=bp.conn.FixedProb(prob=connection_prob_BC,include_self=False,seed=seed//3)
        self.PC_I=DualExponential(BCs,PCs,conn_PC_I,g_max=z*w_PC_I,tau_decay=decay_PC_I,tau_rise=rise_PC_I,
                                    delay_step=delay_PC_E,E=Erev_I)
        conn_BC_E=bp.conn.FixedProb(prob=connection_prob_PC,include_self=False,seed=seed//6)
        self.BC_E=DualExponential(PCs,BCs,conn_BC_E,g_max=z*w_BC_E,tau_decay=decay_BC_E,tau_rise=rise_BC_E,
                                  delay_step=delay_BC_E,E=Erev_E)
        conn_BC_I=bp.conn.FixedProb(prob=connection_prob_BC,include_self=False,seed=seed//9)
        self.BC_I=DualExponential(BCs,BCs,conn_BC_I,g_max=z*w_BC_I,tau_decay=decay_BC_I,tau_rise=rise_BC_I,
                                  delay_step=delay_BC_I,E=Erev_I)
        self.MF=I_MF
        self.PCs=PCs
        self.BCs=BCs    