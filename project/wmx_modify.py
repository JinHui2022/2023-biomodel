import numpy as np
from parameter import *

def normalize_wmx(wmx,sigma):
    size = wmx.shape[0]
    distances = np.abs(np.arange(size) - np.arange(size)[:, np.newaxis])
    paras = np.exp(-distances**2/(2*sigma**2))    
    normalized_weight_matrix = wmx * paras
    return normalized_weight_matrix

def shuffle(wmx_orig):
    """
    Randomly shuffles the weight matrix (keeps weight distribution, but no spatial pattern)
    :param wmx_orig: original weight matrix
    :return: wmx_modified: modified weight matrix
    """

    np.random.seed(12345)

    wmx_modified = wmx_orig
    np.random.shuffle(wmx_modified)  # shuffle's only rows (keeps output weights)
    np.random.shuffle(wmx_modified.T)  # transpose and shuffle rows -> shuffle columns

    return wmx_modified


def column_shuffle(wmx_orig):
    """
    Randomly shuffles the rows of the weight matrix (keeps weight distribution in single postsyn. neuron level, but no spatial pattern)
    :param wmx_orig: original weight matrix
    :return: wmx_modified: modified weight matrix
    """

    np.random.seed(12345)

    wmx_modified = wmx_orig  # stupid numpy...
    np.random.shuffle(wmx_modified)  # transpose and shuffle rows -> shuffle columns

    return wmx_modified.T


def binarize(wmx_orig, ratio=0.03):
    """
    Makes the matrix binary by averaging the highest x and the lowest 1-x part of the nonzero weights
    :param wmx_orig: original weight matrix
    :param ratio: highest x part of the matrix
    :return: wmx_modified: modified weight matrix
    """

    # sort non-zero values, get avg of min and max weights
    nonzero_idx = np.nonzero(wmx_orig)
    nonzero = wmx_orig[nonzero_idx]
    th = int(len(nonzero) * (1-ratio))  # binarization threshold
    weights = np.sort(nonzero, kind="mergsort")
    min_ = np.mean(weights[:th])
    max_ = np.mean(weights[th:])

    # create weight matrix filled with the min value
    wmx_modified_min = np.zeros((n_PC, n_PC))
    wmx_modified_min[nonzero_idx] = min_
    tmp = wmx_modified_min.flatten()
    # update max values in the weight matrix
    N = int(len(nonzero) * ratio)
    max_idx = np.argpartition(wmx_orig.flatten(), -N)[-N:]  # numpy magic to get the idx of N max values
    tmp[max_idx] = max_
    wmx_modified = np.reshape(tmp, (n_PC, n_PC))

    return wmx_modified