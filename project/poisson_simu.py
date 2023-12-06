## this file offers functions to simulate the Possion process 
## which are used to produce spike trains 

## there is a potential problem, that is I ignored the effect of whether the track is linear or circular

import numpy as np
from parameter import *

def evaluate_lambda_t(t, phi_start, phase0):
    """
    Evaluates firing rate(t, x) = tuning_curve(x) * theta_modulation(t, x) at given time points
    :param t: sample time points
    :param phi_start: starting point of the place field (in rad)
    :param phase0: init. phase (used to calc. phase precession)
    :return: lambda_t sampled at the given time points
    """

    x = np.mod(w_mice * t, 2*np.pi)  # positions of the mice [rad]
    mid_PF = phi_start + phi_PF_rad/2.0
    tau_x = np.exp(-np.power(x-mid_PF, 2)/(2*std**2))
    
    # theta modulation of firing rate + phase precession
    phase = phase0 + 2*np.pi * f_theta * t
    phase_shift = -np.pi / phi_PF_rad * (x - phi_start)
    theta_mod = np.cos(phase - phase_shift)

    lambda_t = tau_x * theta_mod
    lambda_t[np.where(lambda_t < 0.0)] = 0.0

    return lambda_t

def hom_poisson(lambda_, n_rnds, t_max, seed):
    """
    Generates Poisson process (interval times X_i = -ln(U_i)/lambda_, where lambda_ is the rate and U_i ~ Uniform(0,1))
    :param lambda_: rate of the Poisson process
    :param n_rnds: number of random numbers to gerenerate
    :param t_max: length of the generate Poisson process
    :param seed: seed for random number generation (see `_generate_exp_rand_numbers()`)
    :return: poisson_proc: np.array which represent a homogenos Poisson process
    """
    np.random.seed(seed)
    rnd_isis = -1.0 / lambda_ * np.log(np.random.rand(n_rnds))
    poisson_proc = np.cumsum(rnd_isis)
    
    return poisson_proc[np.where(poisson_proc <= t_max)]
    #event_times=[]
    #t=0
    #while t<t_max:
    #   np.random.seed(seed)
    #   U=np.random.uniform(0,1)
    #   t-=np.log(U)/lambda_
    #   t+=refra_period
    #   event_times.append(t)
    #return np.array(event_times)

def inhom_poisson(lambda_, t_max, phi_start, seed, phase0=0.0):
    """
    Generates a homogeneous Poisson process and converts it to inhomogeneous
    via keeping only a subset of spikes based on the (time and space dependent) rate of the place cell (see `evaluate_lambda_t()`)
    :param lambda_: rate of the hom. Poisson process (see `hom_poisson()`)
    :param t_max: length of the generate Poisson process
    :param phi_start: starting point of the place field (see `evaluate_lambda_t()`)
    :param linear: flag for circular vs. linear track (see `evaluate_lambda_t()`)
    :param seed: seed for random number generation
    :param phase0: initial phase (see `evaluate_lambda_t()`)
    :return: inhom_poisson_proc: inhomogenos Poisson process representing the spike train of a place cell
    """

    poisson_proc=hom_poisson(lambda_,10000,t_max,seed)

    # keep only a subset of spikes
    lambda_t=evaluate_lambda_t(poisson_proc,phi_start,phase0)
    np.random.seed(seed)
    inhom_poisson_proc=poisson_proc[np.where(lambda_t>=np.random.rand(poisson_proc.shape[0]))]

    return inhom_poisson_proc
