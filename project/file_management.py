## this file offer functions to store data in specific form 
## and parse the data stored in certain file

def save_place_field(dictionary,file_path):
    with open(file_path, 'w') as file:
        for key, value in dictionary.items():
            file.write(f"{key}: {value}\n")
    return None

def read_place_field(file_path):
    return None

def read_spike_train(file_path):
    ## numpy can take the task of saving spike trains
    return None