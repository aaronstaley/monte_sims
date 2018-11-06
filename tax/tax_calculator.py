"""
Module that defines logic to calculate taxes
"""
import bracket_definitions as bd
import deduction_definitions as dd
import combined_bracket as cb
import constants

class TaxCalculation(object):
    """A tax calculator for a specific filing status and state.

    Note that this only supports standard deduction
    """
    state = None
    filing_status = None
    bracket = None

    def __init__(self, state, filing_status):
        self.state = state
        self.filing_status = filing_status
        self.bracket = cb.combined[state][filing_status]

    def agi_to_tax(self, agi):
        """Convert AGI to tax

        Our tax brackets already consider standard deduction, so we don't need to
        do AGI->taxable_income->tax
[
        However, as this is AGI, things like 401(k) contributions should already be removed
        """
        last_rate = 0
        last_bottom = 0
        tax_so_far = 0
        agi_remain = agi
        for bottom, rate in self.bracket[constants.INCOME_ORDINARY]: # TODO: Fix me -- sourcing?
            assert bottom >= last_bottom, "ordering"

            if bottom > agi:
                tax_so_far += agi_remain * last_rate
                break

            tax_so_far += (bottom - last_bottom) * last_rate
            agi_remain -= (bottom - last_bottom)

            last_rate = rate
            last_bottom = bottom
        return tax_so_far


CA_MARRIED = TaxCalculation(constants.CA, constants.FILING_MARRIED)




