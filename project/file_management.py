## this file offer functions to store data in specific form 
## and parse the data stored in certain file

import numpy as np
import os

fig_dir = os.path.join(os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-2]), "result")
if not os.path.exists(fig_dir):
    os.mkdir(fig_dir)

def generate_file_path(file_name = str):
    file_path = os.path.join(fig_dir, file_name)
    return file_path

def save_place_field(dictionary,file_name):
    file_path = generate_file_path(file_name)
    with open(file_path, 'w') as file:
        for key, value in dictionary.items():
            file.write(f"{key}: {value}\n")
    return None

def read_place_field(file_path):
    return None

def read_spike_train(file_path, allow_pickle):
    ## numpy can take the task of saving spike trains
    data = np.load(file_path, allow_pickle=allow_pickle)
    arrays = {}
    for key in data.keys():
        arrays[key] = data[key]
    return arrays