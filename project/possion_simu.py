## this file offers functions to simulate the Possion process 
## which are used to produce spike trains 

import numpy as np
from parameter import *

def hom_poisson(lambda_, t_max, seed):
    """
    Generates Poisson process (interval times X_i = -ln(U_i)/lambda_, where lambda_ is the rate and U_i ~ Uniform(0,1))
    :param lambda_: rate of the Poisson process
    :param n_rnds: number of random numbers to generate
    :param t_max: length of the generate Poisson process
    :param seed: seed for random number generation (see `_generate_exp_rand_numbers()`)
    :return: poisson_proc: np.array which represent a homogenos Poisson process
    """
    event_times=[]
    t=0
    while t<t_max:
        U=np.random.uniform(0,1,seed=seed)
        t-=np.log(U)/lambda_
        event_times.append(t)
    return np.array(event_times)

def inhom_poisson(lambda_, t_max, phi_start, seed, phase0=0.):
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
    return None
