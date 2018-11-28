import tax.tax_calculator as txc


def test_tax_calcation():
    tc = txc.CA_MARRIED
    assert tc.agi_to_tax(0) == 0
    assert tc.agi_to_tax(8472) == 0  # state deduction
    assert round(tc.agi_to_tax(24000)) == 155  # federal deduction (some state)
    assert round(tc.agi_to_tax(40000)) == 2060  # low fed rate
    assert round(tc.agi_to_tax(100000)) == 12026
