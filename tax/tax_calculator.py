"""
Module that defines logic to calculate taxes
"""
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

        Our tax brackets already consider standard deduction, so we don't need
        to do AGI->taxable_income->tax

        However, as this is AGI, things like 401(k) contributions should
        already be removed
        """
        raise NotImplementedError

    def calc_tax(self, base_agi, source_agi, income_source):
        """calculate tax for a given income source.

        base_agi: What this income source starts at (e.g. LTCG comes after
            ordinary income)
        source_agi: AGI from this source. (note AGI is effectively just
            income from source).
        income_source: source of this income
        """
        last_rate = 0
        last_bottom = 0
        tax_so_far = 0

        top_agi = source_agi + base_agi  # highest bracket we'll look at

        for bottom, rate in self.bracket[income_source]:
            assert bottom >= last_bottom, "ordering"

            if base_agi > last_bottom:
                if base_agi < bottom:
                    # income is now being taxed -> partially count it
                    income_to_tax = min(bottom, top_agi) - base_agi
                else:
                    # this bracket is entirely skipped (base is above)
                    income_to_tax = 0
            else:
                # tax entire bracket (up to limit)
                income_to_tax = min(bottom, top_agi) - last_bottom

            tax_so_far += income_to_tax * last_rate
            if top_agi <= bottom:
                # no need to look at further brackets
                break

            last_rate = rate
            last_bottom = bottom

        return tax_so_far


CA_MARRIED = TaxCalculation(constants.CA, constants.FILING_MARRIED)
