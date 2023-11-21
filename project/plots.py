## render the plot function used in this project

import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import cm
config = {"axes.titlesize":"20", "axes.labelsize":"15", "axes.labelweight":"medium"}
rcParams.update(config)

fig_dir = os.path.join(os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-2]), "result")
if not os.path.exists(fig_dir):
    os.mkdir(fig_dir)

def plot_tuning_curves(l_route, n_sample):
    """
    :param l_route:路线总长(cm)
    :param n_sample:位置细胞采样个数
    """
    l_place_field = 30.0
    phi_PF_rad = l_place_field/l_route * 2*np.pi
    std = 0.146 
    x = np.arange(0, l_route, 0.1)
    x_rad = x/l_route * 2*np.pi
    sample = l_route/n_sample
    fig = plt.figure()
    plt.axis([0, l_route, 0.0, 1.0])
    j = -l_place_field/2
    while j <= l_route:
        mid_PF = j/l_route * 2*np.pi + phi_PF_rad/2.0
        tau = [np.exp(-np.power(i-mid_PF, 2)/(2*std**2)) for i in x_rad]
        plt.plot(x, tau, color=cm.jet(j/l_route))
        j = j + sample
    plt.title("Place Cell Tuning Curves")
    plt.xlabel("Position(cm)")
    plt.ylabel(r"$\tau_{i}$(x)")
    fig.savefig(os.path.join(fig_dir, "Place Cell Tuning Curves.png"), dpi=200)

def plot_weight_matrix(weight_matrix, ax):
    return None

def plot_raster(input, ax):
    return None

def plot_spike_events(event_time, ax):
    return None