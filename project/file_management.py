## this file offer functions to store data in specific form 
## and parse the data stored in certain file

import numpy as np
import pickle
import json
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

def save_pre2post(pre2post, file_name):
    dict_pre2post={
        "post_id":np.array(pre2post[0]).tolist(),
        "pre_pt":np.array(pre2post[1]).tolist()
    }
    with open(file_name,'w') as f:
        json.dump(dict_pre2post,f)
    return None

def save_weight(weight, file_name):
    arr=np.array(weight)
    np.save(file_name,arr)
    return None

def read_spike_train(file_path):
    with open(file_path, "rb") as file:
        # Load the data from the file
        data = pickle.load(file)
    return data

def read_pre2post(file_name):
    with open(file_name, 'r') as file:
        pre2post = json.load(file)
    return pre2post

def read_weight(file_name):
    weight=np.load(file_name)
    return weight

def save_prepost_weight(wmx,file_name):
    nonzero_indices = np.nonzero(wmx)
    pre_id = nonzero_indices[0]
    post_id = nonzero_indices[1]
    weight = wmx[nonzero_indices]
    np.save(file_name[0],pre_id)
    np.save(file_name[1],post_id)
    np.save(file_name[2],weight)
    
    return None