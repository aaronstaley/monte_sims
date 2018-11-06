"""
Defines deductions for federal and state taxes
"""

import constants


# standard deductions
state_standard_deduction = {
    constants.CA: {
        constants.FILING_MARRIED : 8472
    }
}

federal_standard_deduction = {
    constants.FILING_MARRIED : 24000
}


# 401k limits
limit_401k = {
    constants.FILING_MARRIED: 18500*2 # two people!
}