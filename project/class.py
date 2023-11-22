## this file store all the classes used in this project

import brainpy as bp
import brainpy.math as bm
import numpy as np

class STDP(bp.TwoEndConn):
    def __init__(self,pre,post,conn,tau_s,tau_t,tau,A1,A2,E,delay_step,method='exp_auto',**kwargs):
        super(STDP, self).__init__(pre=pre,post=post,conn=conn,**kwargs)

        # initialize parameters
        self.tau_s=tau_s
        self.tau_t=tau_t
        self.tau=tau
        self.A1=A1 # Apre
        self.A2=A2 # Apost
        self.E=E
        self.delay_step=delay_step

        # fetch pre_idexes and post_idexes
        self.pre_ids,self.post_ids=self.conn.require('pre_ids','post_ids')

        # initialize variables
        num=len(self.pre_ids)
        self.Apre=bm.Variable(bm.zeros(num))
        self.Apost=bm.Variable(bm.zeros(num))
        self.w=bm.Variable(bm.ones(num))
        self.g=bm.Variable(bm.zeros(num))

        # define a delay processor
        self.delay=bm.LengthDelay(self.pre.spike,delay_step)

        # functions
        self.integral=bp.odeint(method=method,f=self.derivative)

        def derivative(self):
            dApre=lambda Apre, t: -Apre/self.tau_s
            dApost=lambda Apost, t: -Apost/self.tau_t
            dg=lambda g,t: -g/self.tau
            return bp.JointEq([dApre,dApost,dg])
        
        def update(self,tdi):
            delayed_g=self.delay(self.delay_step)

            ## calculate the post input current
            post_g=bm.syn2post(delayed_g,self.post_ids,self.post.num)
            self.post.input+=post_g*(self.E-self.post.V_rest)

            ## update the variables
            pre_spikes=bm.pre2syn(self.pre.spike,self.pre_ids)
            post_spikes=bm.pre2syn(self.post.spike,self.post_ids)

            self.Apre.value, self.Apost.value,self.g.value=self.integral(self.Apre,self.Apost,self.g,tdi.t,tdi.dt)

            # if (pre spikes)
            Apre=bm.where(pre_spikes,self.Apre+self.A1,self.Apre)
            self.w.value=bm.where(pre_spikes,self.w-self.Apost,self.w)
            # if (post spikes)
            Apost=bm.where(post_spikes,self.Apost+self.A2,self.Apost)
            self.w.value=bm.where(post_spikes,self.w+self.Apre,self.w)
            self.Apre.value=Apre
            self.Apost.value=Apost

            self.g.value=bm.where(pre_spikes,self.g+self.w,self.g)
            self.delay.update(self.g)
            