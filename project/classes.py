## this file store all the classes used in this project

import brainpy as bp
import brainpy.math as bm
import numpy as np
from brainpy.synapses import DualExponential
from parameter import *

class STDP(bp.synapses.TwoEndConn):
    def __init__(self,pre,post,conn,tau_s,tau_t,A1,A2,method='exp_auto',**kwargs):
        super(STDP, self).__init__(pre=pre,post=post,conn=conn,**kwargs)

        # initialize parameters
        self.tau_s=tau_s
        self.tau_t=tau_t
        self.A1=A1 # Apre
        self.A2=A2 # Apost

        # fetch pre_idexes and post_idexes
        self.pre_ids,self.post_ids,self.pre2post=self.conn.require('pre_ids','post_ids','pre2post')

        # initialize variables
        num=len(self.pre_ids)
        self.Apre=bm.Variable(bm.zeros(num))
        self.Apost=bm.Variable(bm.zeros(num))
        self.w=bm.Variable(bm.ones(num))

        # functions
        self.integral=bp.odeint(method=method,f=self.derivative)

    @property
    def derivative(self):
        dApre=lambda Apre, t: -Apre/self.tau_s
        dApost=lambda Apost, t: -Apost/self.tau_t
        return bp.JointEq([dApre,dApost])
        
    def update(self):
        t=bp.share.load('t')
        dt=bp.share.load('dt')
        ## update the variables
        pre_spikes=bm.pre2syn(self.pre.spike,self.pre_ids)
        post_spikes=bm.pre2syn(self.post.spike,self.post_ids)

        self.Apre.value, self.Apost.value=self.integral(self.Apre,self.Apost,t,dt)

        # if (pre spikes)
        Apre=bm.where(pre_spikes,self.Apre+self.A1,self.Apre)
        self.w.value=bm.where(pre_spikes,self.w-self.Apost,self.w)
        # if (post spikes)
        Apost=bm.where(post_spikes,self.Apost+self.A2,self.Apost)
        self.w.value=bm.where(post_spikes,self.w+self.Apre,self.w)

        self.Apre.value=Apre
        self.Apost.value=Apost

class ca3simu(bp.Network):
    def __init__(self, freq, conn_PC_E, wmx_PC_E, mode, seed):
        super(ca3simu, self).__init__()

        np.random.seed(seed)
        dt=bp.share.load('dt')
        # to initialize synaptic weights
        w_PC_I = 0.65  # nS
        w_BC_E = 0.85
        w_BC_I = 5.
        w_PC_E=wmx_PC_E
        if mode == "asym":
            w_PC_MF = 21.5
        elif mode == "sym":
            w_PC_MF = 19.15
        else:
            raise ValueError("STDP_mode has to be either 'sym' or 'asym'!")
        
        # produce the input
        I_MF=bp.neurons.PoissonGroup(n_PC,freqs=freq)

        # produce the excitory neuron group
        PCs=bp.neurons.AdExIF(n_PC, V_rest=Vrest_PC,V_reset=Vreset_PC,V_th=spike_th_PC,V_T=theta_PC,
                              delta_T=delta_T_PC,a=a_PC,b=b_PC,R=Rm_PC,tau=tau_mem_PC,tau_w=tau_w_PC,tau_ref=tref_PC)
        
        # produce the inhibitory neuron group
        BCs=bp.neurons.AdExIF(n_BC, V_rest=Vrest_BC,V_reset=Vreset_BC,V_th=spike_th_BC,V_T=theta_BC,
                              delta_T=delta_T_BC,a=a_BC,b=b_BC,R=Rm_BC,tau=tau_mem_BC,tau_w=tau_w_BC,tau_ref=tref_BC)
        
        # construct the connections
        ## MF -> PC
        self.MF2PC=DualExponential(I_MF,PCs,bp.conn.One2One(),g_max=z*w_PC_MF,tau_decay=decay_PC_MF,tau_rise=rise_PC_MF,
                                   delay_step=delay_PC_E/dt,output=bp.synouts.COBA(Erev_E))
        ## PC -> PC
        self.PC_E=DualExponential(PCs,PCs,conn_PC_E,g_max=z*w_PC_E,tau_decay=decay_PC_E,tau_rise=rise_PC_E,
                                   delay_step=delay_PC_E/dt,output=bp.synouts.COBA(Erev_E))
        
        ## BC -> PC
        conn_PC_I=bp.conn.FixedProb(prob=connection_prob_BC,include_self=False,seed=42)
        self.PC_I=DualExponential(BCs,PCs,conn_PC_I,g_max=z*w_PC_I,tau_decay=decay_PC_I,tau_rise=rise_PC_I,
                                    delay_step=delay_PC_E/dt,output=bp.synouts.COBA(Erev_I))
        
        ## PC -> BC
        conn_BC_E=bp.conn.FixedProb(prob=connection_prob_PC,include_self=False,seed=seed//13)
        self.BC_E=DualExponential(PCs,BCs,conn_BC_E,g_max=z*w_BC_E,tau_decay=decay_BC_E,tau_rise=rise_BC_E,
                                  delay_step=delay_BC_E/dt,output=bp.synouts.COBA(Erev_E))
        
        ## BC -> BC
        conn_BC_I=bp.conn.FixedProb(prob=connection_prob_BC,include_self=False,seed=seed//7)
        self.BC_I=DualExponential(BCs,BCs,conn_BC_I,g_max=z*w_BC_I,tau_decay=decay_BC_I,tau_rise=rise_BC_I,
                                  delay_step=delay_BC_I/dt,output=bp.synouts.COBA(Erev_I))
        
        ## store the variables in all these neuron group
        self.MF=I_MF
        self.PCs=PCs
        self.BCs=BCs        