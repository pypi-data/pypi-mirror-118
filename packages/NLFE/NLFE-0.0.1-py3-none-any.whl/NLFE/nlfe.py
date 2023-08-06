# -*- utf-8 -*-
"""
a series of methods using non linear features extraction.
"""

import numpy as np
from scipy.spatial.distance import pdist, squareform


def approximate_entropy(ts, m, r, **kwargs):
    """
    Return approximate entropy of time series ts within parameters m and r.

    Parameters
    ----------
    ts : time series of array_like
        Input data.
    m : the embedding dimension.
    r : the threshold which is equivalent to 0.25 * std,
        and std is the standard deviation of input segment.
    kwargs : other parameters are unfrequently used by user
    .. versionadded:: 0.0.1

    Returns
    -------
    ApEn : float retaining five decimals
    """
    N = len(ts)

    assert N > m - 1

    try:
        en = kwargs['en']
        flag = kwargs['flag']
    except KeyError:
        en = 0
        flag = False

    x_i = np.array([ts[i:i + m] for i in range(N - m + 1)])
    x_j = np.copy(x_i)

    C_m = np.array([np.sum(np.abs(x_ii - x_j).max(axis=1) <= r) for x_ii in x_i]) / (N - m + 1)
    ApEn = en - np.mean(np.log(C_m))

    if flag:
        return round(ApEn, 5)
    return approximate_entropy(ts, m - 1, r, en=-ApEn, flag=True)


def sample_entropy(ts, m, r, **kwargs):
    """
    Return sample entropy of time series ts within parameters m and r.

    Parameters
    ----------
    ts : time series of array_like
        Input data.
    m : the embedding dimension.
    r : the threshold which is equivalent to 0.25 * std,
        and std is the standard deviation of input segment.
    kwargs : other parameters
    .. versionadded:: 0.0.1

    Returns
    -------
    SampEn : float retaining five decimals
    """
    N = len(ts)

    assert N > m - 1

    try:
        samp_en = kwargs['samp_en']
        flag = kwargs['flag']
    except KeyError:
        samp_en = 0
        flag = False

    x_i = np.array([ts[i:i + m] for i in range(N - m + 1)])
    x_j = np.copy(x_i)

    C_m = np.array([np.sum(np.abs(x_ii - x_j).max(axis=1) <= r) for x_ii in x_i]) / (N - m)
    SampEn = np.mean(C_m)
    if flag:
        return round(np.log(samp_en) - np.log(SampEn), 5)
    return sample_entropy(ts, m + 1, r, samp_en=SampEn, flag=True)


def fuzzy_entropy(ts, m, n, r, **kwargs):
    """
    Return fuzzy entropy of time series ts within parameters m, n, r.

    Parameters
    ----------
    ts : time series of array_like
        Input data.
    m : the embedding dimensions.
    n : an exponent of each distance during computing fuzzy function.
    r : an divisor during computing fuzzy function.
    kwargs : other parameters which are non-frequently used by users.
    .. versionadded:: 0.0.1

    Returns
    -------
    FE : the fuzzy entropy of time series.
    """
    N = len(ts)

    assert N > m - 1

    try:
        FuEn = kwargs['FuEn']
        flag = kwargs['flag']
    except KeyError:
        FuEn = 1
        flag = False

    X_i = np.array([ts[i:i + m] for i in range(N - m + 1)])
    X_i_mean = np.mean(X_i, axis=1)
    X_i_bar = np.vstack([X_i_mean for _ in range(m)]).transpose()

    assert X_i.shape == X_i_bar.shape

    X_i_m = X_i - X_i_bar

    X_j_m = np.copy(X_i_m)

    D_ij = [np.abs(X_ii_m - X_j_m).max(axis=1) for X_ii_m in X_i_m]
    D_ij = np.exp(-np.power(D_ij, n) / r)

    FE = np.sum(D_ij) - np.trace(D_ij) / ((N - m) * (N - m + 1))

    if flag:
        return round(np.log(FuEn / FE), 5)
    return fuzzy_entropy(ts, m + 1, n, r, FuEn=FE, flag=True)


def correct_cond_entropy():
    # TODO
    pass


def shannon_entropy():
    # TODO
    pass


def poincare_plot(ts):
    """
    Return three features extracted from the powerful method of  poincare plot(PP).
    Parameters
    ----------
    ts : time series of array_like
        Input data.
    .. versionadded:: 0.0.1

    Returns
    -------
    sd1     : the short-time standard deviation.
    sd2     : the long-time standard deviation.
    ratio   : the value of sd1 divided by sd2
    """
    x_bar = np.mean(ts)

    i_0, i_1 = ts[:-1], ts[1:]

    d1_i = np.abs(i_0 - i_1) / np.power(2, 0.5)

    sd1 = np.sqrt(np.var(d1_i))

    d2_i = np.abs(i_0 + i_1 - (2 * x_bar)) / np.power(2, 0.5)

    sd2 = np.sqrt(np.var(d2_i))

    ratio = sd1 / sd2
    return sd1, sd2, ratio


def recurrence_plot(ts, m, lag, theta):
    """
    Return RP that is a symmetric matrix which has a dimension of [N-(m-1)*lag X N-(m-1)*lag]
    and Recurrence rate(REC).

    Parameters
    ----------
    ts : time series of array_like
        Input data.
    m : the embedding dimension.
    lag : the embedding lag.
    theta : the threshold
    .. versionadded:: 0.0.1

    Returns
    -------
    RP : a symmetric matrix which has a dimension of [N-(m-1)*lag X N-(m-1)*lag],
        and contains elements of one and zeros.
    REC: a value calculated by sum of the all elements of matrix RP divided by N-m+1
    """
    N = ts.shape[0]

    assert N - ((m - 1) * lag) >= 1

    X = np.array([ts[st:((m - 1) * lag + st + 1):lag] for st in range(N - (m - 1) * lag)])

    d = pdist(X, metric="euclidean")
    d = np.where(d <= theta, 1, 0)

    RP = squareform(d)
    REC = np.sum(RP) / (N * (m - 1))
    return RP, REC
