import tax.tax_calculator as txc
from tax.constants import *



def test_tax_calculation_ordinary():
    tc = txc.CA_MARRIED

    def calc_ordinary(agi, base_agi=0):
        return tc.calc_tax(base_agi, agi, INCOME_ORDINARY)

    assert calc_ordinary(0) == 0
    assert calc_ordinary(8472) == 0  # state deduction
    assert round(calc_ordinary(24000)) == 155  # at fed deduction (with some state)
    assert round(calc_ordinary(25000)) == 265 # lowest bracket in fed and state
    assert round(calc_ordinary(40000)) == 2060  # low fed rate
    assert round(calc_ordinary(100000)) == 12026


def test_tax_calculation_ltcg():
    """does not include net investment income!"""
    tc = txc.CA_MARRIED

    def calc_ltcg(agi, base_agi=0):
        return tc.calc_tax(base_agi, agi, INCOME_LTCG)

    assert calc_ltcg(0) == 0
    assert calc_ltcg(8472) == 0  # state deduction
    assert round(calc_ltcg(24000)) == 155  # state only
    assert round(calc_ltcg(150000)) == 14989 # fed + state

def test_tax_computation_long_term():
    """long term with net investment income"""
    tc = txc.CA_MARRIED
    def calc_ltcg(agi):
        income_dict = {INCOME_LTCG: agi}
        return tc.compute_tax_from_agi_sources(income_dict)

    assert calc_ltcg(0) == 0
    assert calc_ltcg(8472) == 0  # state deduction
    assert round(calc_ltcg(24000)) == 155  # state only
    assert round(calc_ltcg(150000)) == 14989 # fed + state
    assert round(calc_ltcg(300000)) == 52427  # hitting net investment tax

def test_tax_computation_short_term():
    """long term with net investment income"""
    tc = txc.CA_MARRIED
    def calc_stcg(agi):
        income_dict = {INCOME_STCG: agi}
        return tc.compute_tax_from_agi_sources(income_dict)

    assert calc_stcg(0) == 0
    assert calc_stcg(8472) == 0  # state deduction
    assert round(calc_stcg(24000)) == 155  # at fed deduction (with some state)
    assert round(calc_stcg(25000)) == 265 # lowest bracket in fed and state
    assert round(calc_stcg(40000)) == 2060  # low fed rate
    assert round(calc_stcg(100000)) == 12026
    # where net investment tax applies
    assert round(calc_stcg(300000)) == 77426
    # max out federal
    assert round(calc_stcg(700000)) == 265731
    assert round(calc_stcg(1000000)) == 422031

    # max out fed and state
    assert round(calc_stcg(1500000)) == 690902

def test_tax_blended_investment():
    """various blended tax brackets"""
    tc = txc.CA_MARRIED

    income_dict = {INCOME_ORDINARY : 300000,
                   INCOME_STCG : 100000}
    assert round(tc.compute_tax_from_agi_sources(income_dict)) == 118418

    income_dict = {INCOME_ORDINARY : 200000,
                   INCOME_STCG : 100000,
                   INCOME_LTCG : 100000}
    assert round(tc.compute_tax_from_agi_sources(income_dict)) == 105526


