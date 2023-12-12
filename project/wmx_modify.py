import numpy as np

def erase(wmx,start_source,end_target,refsrc_start,refsrc_end,reftag_start,reftag_end):
    reset=np.mean(wmx[refsrc_start:refsrc_end,reftag_start:reftag_end])
    wmx[start_source:,:end_target]=reset
    return wmx

def normalize_wmx(wmx,sigma):
    size = wmx.shape[0]
    distances = np.abs(np.arange(size) - np.arange(size)[:, np.newaxis])
    paras = 1/(np.sqrt(2*np.pi) * sigma) * np.exp(-distances**2/(2*sigma**2))    
    normalized_weight_matrix = wmx * paras
    return normalized_weight_matrix