import numpy as np

def get_wmx_preid(n_pre,n_post,pre2post,weight):
    matrix=np.zeros((n_pre,n_post))
    pre_id=np.zeros_like(pre2post[0])
    for id_vec in range(len(pre2post[1])-1):
        start=pre2post[1][id_vec]
        end=pre2post[1][id_vec+1]
        post_ides=pre2post[0][start:end]
        matrix[id_vec][post_ides]=weight[start:end]
        pre_id[start:end]=id_vec
    return matrix,pre_id