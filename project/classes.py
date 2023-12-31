## this file store all the classes used in this project

import brainpy as bp
import brainpy.math as bm
import numpy as np
from brainpy.synapses import DualExponential
from parameter import *
import jax.numpy as jnp
from brainpy.check import is_float
from brainpy._src.initialize import variable

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
        self.w.value=bm.where(pre_spikes,self.w+self.Apost,self.w)
        # if (post spikes)
        Apost=bm.where(post_spikes,self.Apost+self.A2,self.Apost)
        self.w.value=bm.where(post_spikes,self.w+self.Apre,self.w)

        self.Apre.value=Apre
        self.Apost.value=Apost

class ca3simu(bp.Network):
    def __init__(self, freq, conn_PC_E, wmx_PC_E, mode, seed, mode_stp):
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
        
        # initialize
        PCs.V[:]=Vrest_PC 
        BCs.V[:]= Vrest_BC
        
        # construct the connections
        ## MF -> PC
        self.MF2PC=DualExponential(I_MF,PCs,bp.conn.One2One(),g_max=norm_PC_MF*w_PC_MF,tau_decay=decay_PC_MF,tau_rise=rise_PC_MF,
                                   delay_step=delay_PC_E/dt,output=bp.synouts.COBA(Erev_E))
        ## PC -> PC
        ## choose if use STP synapses
        if mode_stp == 0:
            self.PC_E=DualExponential(PCs,PCs,conn_PC_E,g_max=norm_PC_E*w_PC_E,tau_decay=decay_PC_E,tau_rise=rise_PC_E,
                                   delay_step=delay_PC_E,output=bp.synouts.COBA(Erev_E))
        else:
            self.PC_E=DualExponential(PCs,PCs,conn_PC_E,g_max=norm_PC_E*w_PC_E,stp = STD(),tau_decay=decay_PC_E,tau_rise=rise_PC_E,
                                   delay_step=delay_PC_E,output=bp.synouts.COBA(Erev_E))        
        ## BC -> PC
        conn_PC_I=bp.conn.FixedProb(prob=connection_prob_BC,include_self=False,seed=42)
        self.PC_I=DualExponential(BCs,PCs,conn_PC_I,g_max=norm_BC_E*w_PC_I,tau_decay=decay_PC_I,tau_rise=rise_PC_I,
                                    delay_step=delay_PC_E/dt,output=bp.synouts.COBA(Erev_I))
        
        ## PC -> BC
        conn_BC_E=bp.conn.FixedProb(prob=connection_prob_PC,include_self=False,seed=13)
        self.BC_E=DualExponential(PCs,BCs,conn_BC_E,g_max=norm_PC_I*w_BC_E,tau_decay=decay_BC_E,tau_rise=rise_BC_E,
                                  delay_step=delay_BC_E/dt,output=bp.synouts.COBA(Erev_E))
        
        ## BC -> BC
        conn_BC_I=bp.conn.FixedProb(prob=connection_prob_BC,include_self=False,seed=7)
        self.BC_I=DualExponential(BCs,BCs,conn_BC_I,g_max=norm_BC_I*w_BC_I,tau_decay=decay_BC_I,tau_rise=rise_BC_I,
                                  delay_step=delay_BC_I/dt,output=bp.synouts.COBA(Erev_I))
        
        ## store the variables in all these neuron group
        self.MF=I_MF
        self.PCs=PCs
        self.BCs=BCs        

class STD(bp.synapses.SynSTP):

  def __init__(
      self,
      tau: float = 200.,
      U: float = 0.07,
      method: str = 'exp_auto',
      name: str = None
  ):
    super(STD, self).__init__(name=name)

    # parameters
    is_float(tau, 'tau', min_bound=0, )
    is_float(U, 'U', min_bound=0, )
    self.tau = tau
    self.U = U
    self.method = method

    # integral function
    self.integral = bp.odeint(lambda x, t: (1 - x) / self.tau, method=self.method)


  def register_master(self, master):
    super(STD, self).register_master(master)

    # variables
    self.x = variable(jnp.ones, self.master.mode, self.master.pre.num)

  def reset_state(self, batch_size=None):
    self.x.value = variable(jnp.ones, batch_size, self.master.pre.num)

  def update(self, tdi, pre_spike):
    t=bp.share.load('t')
    dt=bp.share.load('dt')
    x = self.integral(self.x.value, t, dt)
    self.x.value = jnp.where(pre_spike, x - self.U * self.x, x)

  def filter(self, g):
    if jnp.shape(g) != self.x.shape:
      raise ValueError('Shape does not match.')
    return g * self.x