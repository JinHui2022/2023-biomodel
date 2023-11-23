## this file offer functions to store data in specific form 
## and parse the data stored in certain file

import numpy as np
import pickle
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

def save_spike_trains(spike_trains, file_name):
    with open(file_name, 'wb') as file:
        pickle.dump(spike_trains, file)
    return None

def read_place_field(file_path):
    return None

def read_spike_train(file_path):
    with open(file_path, "rb") as file:
        # Load the data from the file
        data = pickle.load(file)
    return data