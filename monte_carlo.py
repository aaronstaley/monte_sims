"""monte carlo simulation"""
import numpy as np
import multiprocessing as mp

def monte_carlo_single(func, tries=10000):
    """return nd array of every monte carlo result"""
    results = []
    for i in xrange(tries):
        result = func()
        results.append(result)

    return results

def monte_carlo(func, tries=10000, single_batch_size=100):
    """parallel version of monte_carlo_single"""
    pool = mp.Pool()
    singular_args = (func, single_batch_size)

    future_res = [pool.apply_async(monte_carlo_single, singular_args) for _ in xrange(tries/single_batch_size)]
    res = []
    for f in future_res:
        res.extend(f.get())

    return res

def gv():
    import gbm
    total_time = 1
    sim_period = 0.001
    mean = 0.1
    stdev = 0.15
    m = gbm.generate_brownian_motion(total_time, sim_period, mean, stdev)
    return m[-1]