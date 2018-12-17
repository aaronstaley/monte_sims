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

    def compute_tax_from_agi_sources(self, agi_dict):
        """Compute tax from various sources of AGI

        agi_dict is a dictionary mapping an income source (as defined in constants) to
        an amount.

        Note that dividends are considered either STCG (ordinary) or LTCG (qualified)
            per purposes of source attribution.

        This will automatically do calculations to use correct blended cap gain rates
        """
        INCOME_SOURCES = [constants.INCOME_ORDINARY, constants.INCOME_LTCG, constants.INCOME_STCG]
        for agi_source in agi_dict:
            assert agi_source in INCOME_SOURCES, "unexpected source %s" % agi_source

        assert constants.INCOME_INVESTMENT not in agi_source, \
            "investment income determined by STCG and LTCG"

        ordinary_income = agi_dict.get(constants.INCOME_ORDINARY, 0)
        stcg = agi_dict.get(constants.INCOME_STCG, 0)
        ltcg = agi_dict.get(constants.INCOME_LTCG, 0)

        tax_so_far = self.calc_tax(0, ordinary_income, constants.INCOME_ORDINARY)
        tax_so_far += self.calc_tax(ordinary_income, stcg, constants.INCOME_STCG)
        tax_so_far += self.calc_tax(ordinary_income + stcg, ltcg, constants.INCOME_LTCG)

        # net investment income is STCG + LTCG (after ordinary)
        tax_so_far += self.calc_tax(ordinary_income, stcg + ltcg, constants.INCOME_INVESTMENT)

        return tax_so_far

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
        else:
            # reached top bracket -- apply it
            assert top_agi > bottom, "should not have reached top bracket"
            assert bottom == last_bottom, "loop not exhausted?"

            income_to_tax = top_agi - max(base_agi, last_bottom)
            tax_so_far += income_to_tax * last_rate


        return tax_so_far


CA_MARRIED = TaxCalculation(constants.CA, constants.FILING_MARRIED)
