"""
Geometric brownian motion modeler
Taken from https://en.wikipedia.org/wiki/Geometric_Brownian_motion


More resources:

"""

import numpy as np

from scipy.linalg import cholesky


def correl_matrix_from_corr(corr):
    """generate a 2x2 correlation matrix from a simple correlation"""
    corr_matrix = np.ones((2, 2))
    corr_matrix[1][0] = corr
    corr_matrix[0][1] = corr

    return corr_matrix


def generate_brownian_motion(total_time, sim_period, mean, stdev):
    n = int(np.round(total_time / float(sim_period)))  # number of simulations
    t = np.linspace(0, total_time, n)

    # generate Weiner process
    normal_values = np.random.standard_normal(size=n)

    # brownian motion (Weiner process)
    W = np.cumsum(normal_values) * np.sqrt(sim_period)

    # Generate geometric brownian motion
    X = (mean - 0.5 * stdev ** 2) * t + stdev * W
    return np.exp(X)  # geometric


def multi_generate_brownian_motion(total_time, sim_period,
                                   mean, stdev, corr_matrix):
    """
    multivariate version like above with a correlation matrix
    Based on https://gist.github.com/athirara/49bf24cbffdc0a07343fad09ccd7f411
    (and corrected errors..)
    """
    assert mean.ndim == stdev.ndim == corr_matrix.ndim
    assert len(mean) == len(stdev) == 1
    assert len(corr_matrix) == corr_matrix.ndim  # square

    upper_cholesky = cholesky(corr_matrix, lower=False)
    num_assets = mean.ndim

    n = int(np.round(total_time / float(sim_period)))  # number of simulations
    t = np.linspace(0, total_time, n)

    # generate correlated weiner process
    normal_values = np.random.standard_normal(size=(n, num_assets))
    correl_normal_values = np.matmul(normal_values, upper_cholesky)

    # full brownian motion
    W = np.cumsum(correl_normal_values, axis=0) * np.sqrt(sim_period)

    # Generate geometric brownian motion
    drift_component = np.outer(t, (mean - 0.5 * stdev ** 2))
    X = drift_component + stdev * W
    return np.exp(X)  # geometric


def multi_generate_brownian_motion_single_step(total_time, mean, stdev,
                                               corr_matrix, sub_steps=100):
    """return a single step of brownian motion"""
    # We use 100 sub steps to minimize probability range
    #  (it's akin to running more samples,
    #  but it is faster to do it this way due to vector math)

    S = multi_generate_brownian_motion(total_time,
                                       total_time / float(sub_steps),
                                       mean, stdev,
                                       corr_matrix)
    return S[-1]
