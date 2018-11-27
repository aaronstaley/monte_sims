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
        todo AGI->taxable_income->tax

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
        base_remain = base_agi
        agi_remain = top_agi

        for bottom, rate in self.bracket[income_source]:
            # TODO: Fix me -- sourcing?
            assert bottom >= last_bottom, "ordering"

            if bottom > source_agi:  # partially count tax and move forward
                assert base_remain < (bottom - last_bottom)
                # actual agi for this income sourcing used
                agi_consumed = min(agi_remain, (bottom - source_agi))

                tax_so_far += agi_consumed * last_rate
                agi_remain -= agi_consumed
                assert agi_remain >= 0
                base_remain = 0

                last_rate = rate
                last_bottom = bottom
                continue

            if bottom > top_agi:
                assert base_remain == 0
                tax_so_far += agi_remain * last_rate
                break

            if base_remain > 0:
                base_remain -= (bottom - last_bottom)
            else:
                tax_so_far += (bottom - last_bottom) * last_rate
            agi_remain -= (bottom - last_bottom)

            last_rate = rate
            last_bottom = bottom
        return tax_so_far


CA_MARRIED = TaxCalculation(constants.CA, constants.FILING_MARRIED)
