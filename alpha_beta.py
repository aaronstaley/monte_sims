import math

import statsmodels.api as sm
from statsmodels import regression

DAYS = 250  # trading days in year


def linreg(x, y):
    """return alpha/beta between two values"""
    x = sm.add_constant(x)
    model = regression.linear_model.OLS(y, x).fit()

    return model.params[0], model.params[1]


def calc_correlation(x, y, beta):
    """Calculate correlation between x & y with beta calculated via linreg
    See https://en.wikipedia.org/wiki/Beta_(finance)
    """
    return beta * x.std() / y.std()


def print_info(return_base, return_asset):  # asset is asset under test
    frames = float(len(return_base))
    assert frames == len(return_asset)

    alpha, beta = linreg(return_base, return_asset)
    print('base time return', return_base.mean() * frames)
    print('base stdev', return_base.std() * math.sqrt(DAYS))

    # time based alpha
    print('alpha over time', alpha * frames)
    print('beta', beta)  # no time unit
    cor = calc_correlation(return_base, return_asset, beta)

    print('correlation', cor)

    # TODO: Dont comment-out code; use or delete
    # print return_base.corr(return_asset)
