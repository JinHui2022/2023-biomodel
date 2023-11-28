## this file store all the parameters used in this project

import numpy as np

## parameter about motion of vertual mice
f_theta = 7.0  # theta osc. freq. [Hz]
v_mice = 32.43567842  # [cm/s]
l_route = 300.0  # circumference [cm]
l_place_field = 30.0  # [cm]
r = l_route / (2*np.pi)  # [cm]
phi_PF_rad = l_place_field / r  # [rad]
t_route = l_route / v_mice  # [s]
w_mice = 2*np.pi / t_route  # angular velocity

## parameter about place field
s = 47.0  # phase-locking (param of circular Gaussian)
std = 0.146  # std (param of Gaussian, defined in [0,2*np.pi])


## parameter about the characteristic of neurons
refra_period = 5e-3 ## [s] the average refractory period

## parameter about neuron network
n_PC=8000
n_BC=150
place_cell_ratio=0.5
connection_prob_PC=0.1
connection_prob_BC=0.25
w_init=1e-10 #S

## parameter about AdExpIF model
# AdExpIF parameters for PCs (re-optimized by Szabolcs)
g_leak_PC = 4.31475791937223 # nS
tau_mem_PC = 41.7488927175169 # ms =tau
Rm_PC = 1 / g_leak_PC # =R
Cm_PC = tau_mem_PC * g_leak_PC
Vrest_PC = -75.1884554193901 # mV =V_rest
Vreset_PC = -29.738747396665072 # mV =V_reset
theta_PC = -24.4255910105977 # mV =V_T
tref_PC = 5.96326930945599 # ms =tau_ref
delta_T_PC = 4.2340696257631 # mV =delta_T
spike_th_PC = theta_PC + 5 * delta_T_PC # =V_th
a_PC = -0.274347065652738 # nS =a
b_PC = 206.841448096415 # pA =b
tau_w_PC = 84.9358017225512 # ms =tau_w

# parameters for BCs (re-optimized by Szabolcs)
g_leak_BC = 7.51454086502288 # nS
tau_mem_BC = 15.773412296065 # ms
Rm_BC = 1 / g_leak_BC # =R 
Cm_BC = tau_mem_BC * g_leak_BC
Vrest_BC = -74.74167987795019 # mV
Vreset_BC = -64.99190523539687 # mV
theta_BC = -57.7092044103536 # mV
tref_BC = 1.15622717832178 # ms
delta_T_BC = 4.58413312063091 # mV
spike_th_BC = theta_BC + 5 * delta_T_BC
a_BC = 3.05640210724374 # nS
b_BC = 0.916098931234532 # pA
tau_w_BC = 178.581099914024 # ms

## parameter about biexponential models
# rise time constants=tau_rise
rise_PC_E = 1.3 # ms # Guzman 2016 (only from Fig.1 H - 20-80%)
rise_PC_MF = 0.65 # ms  # Vyleta ... Jonas 2016 (20-80%)
rise_PC_I = 0.3 # ms  # Bartos 2002 (20-80%)
rise_BC_E = 1. # ms  # Lee 2014 (data from CA1)
rise_BC_I = 0.25 # ms  # Bartos 2002 (20-80%)
# decay time constants=tau_decay
decay_PC_E = 9.5 # ms  # Guzman 2016 ("needed for temporal summation of EPSPs")
decay_PC_MF = 5.4 # ms  # Vyleta ... Jonas 2016
decay_PC_I = 3.3 # ms  # Bartos 2002
decay_BC_E = 4.1 # ms  # Lee 2014 (data from CA1)
decay_BC_I = 1.2 # ms  # Bartos 2002
# Normalization factors (normalize the peak of the PSC curve to 1)
tp = (decay_PC_E * rise_PC_E)/(decay_PC_E - rise_PC_E) * np.log(decay_PC_E/rise_PC_E)  # time to peak
norm_PC_E = 1.0 / (np.exp(-tp/decay_PC_E) - np.exp(-tp/rise_PC_E))
tp = (decay_PC_MF * rise_PC_MF)/(decay_PC_MF - rise_PC_MF) * np.log(decay_PC_MF/rise_PC_MF)
norm_PC_MF = 1.0 / (np.exp(-tp/decay_PC_MF) - np.exp(-tp/rise_PC_MF))
tp = (decay_PC_I * rise_PC_I)/(decay_PC_I - rise_PC_I) * np.log(decay_PC_I/rise_PC_I)
norm_PC_I = 1.0 / (np.exp(-tp/decay_PC_I) - np.exp(-tp/rise_PC_I))
tp = (decay_BC_E * rise_BC_E)/(decay_BC_E - rise_BC_E) * np.log(decay_BC_E/rise_BC_E)
norm_BC_E = 1.0 / (np.exp(-tp/decay_BC_E) - np.exp(-tp/rise_BC_E))
tp = (decay_BC_I * rise_BC_I)/(decay_BC_I - rise_BC_I) * np.log(decay_BC_I/rise_BC_I)
norm_BC_I = 1.0 / (np.exp(-tp/decay_BC_I) - np.exp(-tp/rise_BC_I))
# synaptic delays=delay_step
delay_PC_E = 2.2 # ms  # Guzman 2016
delay_PC_I = 1.1 # ms  # Bartos 2002
delay_BC_E = 0.9 # ms  # Geiger 1997 (data from DG)
delay_BC_I = 0.6 # ms  # Bartos 2002
# synaptic reversal potentials=E
Erev_E = 0.0 # mV
Erev_I = -70.0 # mV

rate_MF = 15.0 # Hz  # mossy fiber input freq

z=1. # nS =g_max
## STDP parameters(p: pre; m: post)
stdp={
    'taup': [20., 62.5], ## ms
    'taum': [20., 62.5], ## ms
    'Ap': [0.01, 4e-3],
    'Am': [0.01, -4e-3],
    'wmax': [4e-8, 2e-8], ## S
    'scale_factor': [1.27, 0.62], 
    'w_init': 1e-10 ## S
}
w_PC_MF=np.array([21.5,19.15])