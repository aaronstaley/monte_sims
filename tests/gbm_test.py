import numpy as np

import finance_helpers
import gbm
import monte_carlo

SPY_MEAN = 0.1  # LOG RETURNs
SPY_STDEV = 0.16  # stdev of log returns

TEST_EPSILON = 0.01


def brownian_motion_test():
    """return last element of brownian motion"""
    X = gbm.generate_brownian_motion(1, 1 / 1000.0, SPY_MEAN, SPY_STDEV)
    return X[-1]


def assert_approx(test_value, expected_value):
    """assert test_value within TEST_EPSILON of expected_value"""
    lower = expected_value - TEST_EPSILON
    upper = expected_value + TEST_EPSILON
    assert lower < test_value < upper


def test_simple_brownian_motion_sanity():
    """validate monte carlo sim of brownian motion"""
    runtime = 1
    sim_period = 1 / 1000.0

    S = gbm.generate_brownian_motion(runtime, sim_period, SPY_MEAN, SPY_STDEV)
    assert len(S) == 1 / sim_period
    assert S.ndim == 1


def test_brownian_motion_metrics():
    """validate distribution generated conforms to expectations"""
    returns = monte_carlo.monte_carlo(brownian_motion_test, tries=100000)

    # Validate expectation/variance per GBM
    mean = finance_helpers.average_log_return(returns)
    assert_approx(mean, SPY_MEAN)

    # now we look at all the log returns and compute variance on them
    volatility = finance_helpers.volatility_of_returns(returns)
    assert_approx(volatility, SPY_STDEV)


STOCK_STDEV = 0.5  # stock standard deviation
STOCK_SPY_CORREL = 0.9


def multi_brownian_motion_test():
    """run some correlated brownian motion

    Returns last val
    """
    mean = np.ones(shape=(1, 2)) * SPY_MEAN
    stdev = np.ones(shape=(1, 2)) * SPY_STDEV
    stdev[0][1] = STOCK_STDEV

    corr_matrix = gbm.correl_matrix_from_corr(STOCK_SPY_CORREL)

    runtime = 1
    return gbm.multi_generate_brownian_motion_single_step(
        runtime, mean, stdev, corr_matrix)

    # FIXME: don't comment-out; use or delete
    # sim_period = 1/1000.0
    # S = gbm.multi_generate_brownian_motion(runtime, sim_period,
    #                                        mean, stdev, corr_matrix)
    # return S[-1]


def test_multi_brownian_motion_metrics():
    """Validate multi_generate_brownian_motion sanity"""
    returns = monte_carlo.monte_carlo(multi_brownian_motion_test, tries=100000)
    spy_returns, stock_returns = zip(*returns)

    spy_mean = np.log(np.mean(spy_returns))
    assert_approx(spy_mean, SPY_MEAN)

    stock_mean = np.log(np.mean(stock_returns))
    assert_approx(stock_mean, SPY_MEAN)  # same returns

    spy_log_returns = finance_helpers.log_returns(spy_returns)
    stock_log_returns = finance_helpers.log_returns(stock_returns)

    spy_stdev = np.std(spy_log_returns)
    assert_approx(spy_stdev, SPY_STDEV)

    stock_stdev = np.std(stock_log_returns)
    assert_approx(stock_stdev, STOCK_STDEV)

    # correlate the returns together
    corr = np.corrcoef(spy_log_returns, stock_log_returns)
    assert corr.shape == (2, 2)
    correlation = corr[0][1]
    assert_approx(correlation, corr[1][0])

    # tolerance assertion
    assert_approx(correlation, STOCK_SPY_CORREL)
