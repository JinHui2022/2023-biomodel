## this file store all the classes used in this project

import brainpy as bp
import brainpy.math as bm
import numpy as np
from brainpy.synapses import DualExponential
from parameter import *

class STDP(bp.synapses.TwoEndConn):
    def __init__(self,pre,post,conn,tau_s,tau_t,A1,A2,wmax,delay_step=0,method='exp_auto',**kwargs):
        super(STDP, self).__init__(pre=pre,post=post,conn=conn,**kwargs)

        # initialize parameters
        self.tau_s=tau_s
        self.tau_t=tau_t
        self.A1=A1 # Apre
        self.A2=A2 # Apost
        self.delay_step=delay_step
        self.wmax=wmax

        # fetch pre_idexes and post_idexes
        self.pre_ids,self.post_ids,self.pre2post=self.conn.require('pre_ids','post_ids','pre2post')

        # initialize variables
        num=len(self.pre_ids)
        self.Apre=bm.Variable(bm.zeros(num))
        self.Apost=bm.Variable(bm.zeros(num))
        self.w=bm.Variable(bm.ones(num))

        # define a delay processor
        self.delay=bm.LengthDelay(self.pre.spike,delay_step)

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
        self.w.value=bm.where(pre_spikes,self.w+self.Apost,self.w)
        # if (post spikes)
        Apost=bm.where(post_spikes,self.Apost+self.A2,self.Apost)
        self.w.value=bm.where(post_spikes,self.w+self.Apre,self.w)
        self.w.value=bm.where(self.w<0,0,self.w)
        self.w.value=bm.where(self.w>self.wmax,self.wmax,self.w)
        self.Apre.value=Apre
        self.Apost.value=Apost

# class PoissonStim(bp.NeuGroup):
#     ## neurons group can produce Poisson stimulation
#     def __init__(self, size, ferq_mean, freq_var, t_interval, **kwargs):
#         super(PoissonStim, self).__init__(size=size,**kwargs)

#         # to initialize parameters
#         self.freq_mean=ferq_mean
#         self.freq_var=freq_var
#         self.t_interval=t_interval

#         # tp initialize variables
#         self.freq=bm.Variable(bm.zeros(1))
#         self.freq_t_last_change=bm.Variable(bm.ones(1)*-1e7)
#         self.spike=bm.Variable(bm.zeros(self.num, dtype=bool))
#         self.rng=bm.random.RandomState()

#     def update(self):
#         t=bp.share.load('t')
#         in_interval=bm.logical_and(pre_stimulus_period<t,t<pre_stimulus_period+stimulus_period)
#         freq=bm.where(in_interval, self.freq[0],0.)

#         # judge whether to change the value of freq
#         change=bm.logical_and(in_interval,(t-self.freq_t_last_change[0])>=self.t_interval)

#         # update
#         self.freq[:]=bm.where(change, self.rng.normal(self.freq_mean,self.freq_var),freq)
#         self.freq_t_last_change[:]=bm.where(change,t,self.freq_t_last_change[0])

#         # produce spike
#         self.spike.value=self.rng.random(self.num)<self.freq[0]*t/1000.

class ca3simu(bp.Network):
    def __init__(self, freq, conn_PC_E, wmx_PC_E, mode, seed):
        super(ca3simu, self).__init__()

        np.random.seed(seed)

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
                                   delay_step=delay_PC_E,output=bp.synouts.COBA(Erev_E))
        ## PC -> PC
        self.PC_E=DualExponential(PCs,PCs,conn_PC_E,g_max=z*w_PC_E,tau_decay=decay_PC_E,tau_rise=rise_PC_E,
                                   delay_step=delay_PC_E,output=bp.synouts.COBA(Erev_E))
        
        ## BC -> PC
        conn_PC_I=bp.conn.FixedProb(prob=connection_prob_BC,include_self=False,seed=42)
        self.PC_I=DualExponential(BCs,PCs,conn_PC_I,g_max=z*w_PC_I,tau_decay=decay_PC_I,tau_rise=rise_PC_I,
                                    delay_step=delay_PC_E,output=bp.synouts.COBA(Erev_I))
        
        ## PC -> BC
        conn_BC_E=bp.conn.FixedProb(prob=connection_prob_PC,include_self=False,seed=seed//13)
        self.BC_E=DualExponential(PCs,BCs,conn_BC_E,g_max=z*w_BC_E,tau_decay=decay_BC_E,tau_rise=rise_BC_E,
                                  delay_step=delay_BC_E,output=bp.synouts.COBA(Erev_E))
        
        ## BC -> BC
        conn_BC_I=bp.conn.FixedProb(prob=connection_prob_BC,include_self=False,seed=seed//7)
        self.BC_I=DualExponential(BCs,BCs,conn_BC_I,g_max=z*w_BC_I,tau_decay=decay_BC_I,tau_rise=rise_BC_I,
                                  delay_step=delay_BC_I,output=bp.synouts.COBA(Erev_I))
        
        ## store the variables in all these neuron group
        self.MF=I_MF
        self.PCs=PCs
        self.BCs=BCs        