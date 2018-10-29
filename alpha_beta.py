import statsmodels.api as sm
from statsmodels import regression

def linreg(x,y):
    """return alpha/beta between two values"""
    x = sm.add_constant(x)
    model = regression.linear_model.OLS(y,x).fit()

    return model.params[0], model.params[1]