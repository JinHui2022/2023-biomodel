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
place_cell_ratio=0.5
connection_prob_PC=0.1
w_init=1e-10 #S

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