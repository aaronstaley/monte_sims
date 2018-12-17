"""
Python file to define tax brackets.
2018 brackets
"""

import constants

# Ordinary income: Brackets are based on taxable income.
# Map lowest end of bracket to rate

EMPTY_BRACKET = {}  # used when a type of income isn't assessed

federal_ordinary_married = {
    # ordinary income (no payroll tax)
    0: 0.1,
    19050: 0.12,
    77401: 0.22,
    165000: 0.24,
    315000: 0.32,
    400000: 0.35,
    600000: 0.37
}

federal_ltcg_married = {
    # long term capital gains (before net investment tax)
    0: 0,
    77200: 0.15,
    479000: 0.238
}

federal_net_investment_tax_married = {
    # surcharge for investment income
    250000: 0.038
}

# Now CA taxes. Everything is ordinary for CA

ca_ordinary_married = {
    0: 0.01,
    17088: 0.02,
    40510: 0.04,
    63938: 0.06,
    88754: 0.08,
    112170: 0.093,
    572984: 0.103,
    687567: 0.113,
    1000000: 0.123,
    # mental health tax often not listed in standard brackets;
    #  as it doesn't adjust for inflation
    1145960: 0.133
}


# Merge tables
federal_married = {
    constants.INCOME_ORDINARY: federal_ordinary_married,
    constants.INCOME_LTCG: federal_ltcg_married,
    constants.INCOME_STCG: federal_ordinary_married,
    # stcg is just ordinary income (possibly with investment tax)
    constants.INCOME_INVESTMENT: federal_net_investment_tax_married
}

ca_married = {
    # all sources the same for CA
    constants.INCOME_ORDINARY: ca_ordinary_married,
    constants.INCOME_LTCG: ca_ordinary_married,
    constants.INCOME_STCG: ca_ordinary_married,
    constants.INCOME_INVESTMENT: EMPTY_BRACKET
}

state = {
    constants.CA: {
        constants.FILING_MARRIED: ca_married
    }
}


federal = {
    constants.FILING_MARRIED: federal_married
}
