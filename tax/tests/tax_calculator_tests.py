import tax.tax_calculator as txc
from tax.constants import *



def test_tax_calcation():
    tc = txc.CA_MARRIED

    def calc_ordinary(agi, base_agi=0):
        return tc.calc_tax(base_agi, agi, INCOME_ORDINARY)

    assert calc_ordinary(0) == 0
    assert calc_ordinary(8472) == 0  # state deduction
    assert round(calc_ordinary(24000)) == 155  # at fed deduction (with some state)
    assert round(calc_ordinary(25000)) == 265 # lowest bracket in fed and state
    assert round(calc_ordinary(40000)) == 2060  # low fed rate
    assert round(calc_ordinary(100000)) == 12026
