import unittest
import gbm
import monte_carlo
import math
import finance_helpers
import numpy as np
from scipy.stats.mstats import gmean

SPY_MEAN = 0.1  # LOG RETURNs
SPY_STDEV = 0.16 # stdev of log returns

TEST_EPSILON = 0.01


def brownian_motion_test():
    """return last element of brownian motion"""
    X = gbm.generate_brownian_motion(1, 1 / 1000.0, SPY_MEAN, SPY_STDEV)
    return X[-1]


def test_simple_brownian_motion_sanity():
    """validate monte carlo sim of brownian motion"""
    runtime = 1
    sim_period = 1/1000.0

    S = gbm.generate_brownian_motion(runtime, sim_period, SPY_MEAN, SPY_STDEV)
    assert len(S) == 1/sim_period
    assert S.ndim == 1

def test_brownian_motion_metrics():
    """validate distribution generated conforms to expectations"""

    returns = monte_carlo.monte_carlo(brownian_motion_test, tries=100000)

    # Validate expectation/variance per GBM
    mean = np.log(np.mean(returns))
    assert SPY_MEAN - TEST_EPSILON < mean < SPY_MEAN + TEST_EPSILON

    # now we look at all the log returns and compute variance on them
    log_returns = finance_helpers.log_returns(returns)
    stdev = np.std(log_returns)
    assert SPY_STDEV - TEST_EPSILON < stdev < SPY_STDEV + TEST_EPSILON

# Now run a test on multi_generate_brownian_motion ensuring sanity
