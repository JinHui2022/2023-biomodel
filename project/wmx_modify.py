import numpy as np

def erase(wmx,start_source,end_target,refsrc_start,refsrc_end,reftag_start,reftag_end):
    reset=np.mean(wmx[refsrc_start:refsrc_end,reftag_start:reftag_end])
    wmx[start_source:,:end_target]=reset
    return wmx

def regularization(wmx):
    '''
    This regularization method learned from https://blog.csdn.net/weixin_44085642/article/details/111401340
    '''
    a,_=wmx.shape
    tmp=np.copy(wmx)
    colSums=np.sum(wmx,axis=1)
    colFactors=wmx/colSums
    for i in range(a):
        tmp[i,:]*=colFactors[i]
    
    return tmp

def regularization_digfirst(wmx, diagonal_weight):
    a,b=wmx.shape
    for i in range(a):
        for j in range(b):
            wmx[i, j] = diagonal_weight
            distance = abs(i - j)
            wmx[i, j] = diagonal_weight / np.exp(distance + 1)
    return wmx

def normalize_wmx(wmx,sigma):
    size = wmx.shape[0]
    distances = np.abs(np.arange(size) - np.arange(size)[:, np.newaxis])
    paras = 1/(np.sqrt(2*np.pi) * sigma) * np.exp(-distances**2/(2*sigma**2))    
    normalized_weight_matrix = wmx * paras
    return normalized_weight_matrix