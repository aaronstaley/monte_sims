"""
Generate combined brackets (state + federal) that are pre-adjusted by standard deduction

TODO: Figure out how to incorporate itemized deductions
"""

combined = {}  # combined brackets go here. map state->filing_status->income_type

import bracket_definitions as bd
import constants
import deduction_definitions as dd

def iter_bracket(bracket, reverse=False):
    """iterate through brackets in sorted order
    yield base_value, marginal_rate
    """
    bracket_keys = sorted(bracket.iterkeys(), reverse=reverse)

    for bracket_key in bracket_keys:
        yield bracket_key, bracket[bracket_key]

def merge_brackets(bracket1, bracket2):
    """merge two brackets and returned a combined bracket

    Combined output is formatted as a list of tuples sorted by 'key'
    """

    # handle empty dicts cleanly
    if not bracket1:
        return bracket2
    elif not bracket2:
        return bracket1

    b1_iter = iter_bracket(bracket1)
    b2_iter = iter_bracket(bracket2)

    last_b1_rate = None
    last_b2_rate = None

    next_b1_key, next_b1_rate = None, None
    next_b2_key, next_b2_key = None, None

    output = [] # list of tuple[key, val]

    while True:
        try:
            if next_b1_key is None:
                next_b1_key, next_b1_rate = next(b1_iter)
        except StopIteration:
            next_b1_key, next_b1_rate = None, None
        try:
            if next_b2_key is None:
                next_b2_key, next_b2_rate = next(b2_iter)
        except StopIteration:
            next_b2_key, next_b2_rate = None, None

        if next_b1_key is None and next_b2_key is None:
            break # no more work

        # Decide what bracket to push

        if next_b2_key == next_b1_key:
            # identical (common case at 0), so sum
            new_key = next_b2_key
            new_rate = next_b1_rate + next_b2_rate
            last_b1_rate = next_b1_rate
            last_b2_rate = next_b2_rate
            next_b2_key = next_b1_key = None
        elif next_b2_key is None or (next_b1_key is not None and next_b1_key < next_b2_key):
            # use bracket 1
            new_key = next_b1_key
            new_rate = next_b1_rate + last_b2_rate
            last_b1_rate = next_b1_rate
            next_b1_key = None
        else:
            # use bracket 2
            new_key = next_b2_key
            new_rate = next_b2_rate + last_b1_rate
            last_b2_rate = next_b2_rate
            next_b2_key = None

        output.append((new_key, new_rate))

    return output

def adjust_bracket(brackets, standard_deduction):
    """generate a new brackets adjusted up by a fixed standard deduction"""
    new_brackets = {
        bottom + standard_deduction: rate for
        bottom, rate in
        brackets.iteritems()

    }
    new_brackets[0] = 0 # simulate deduction
    return new_brackets


def build_combined_bracket():
    """generate and return combined bracket"""
    by_state_combined = {}

    for state, state_filing_dict in bd.state.iteritems():

        combined_filing_dict = {}
        assert sorted(bd.federal.keys()) == sorted(state_filing_dict.keys())
        for filing_status, income_dict in bd.federal.iteritems():
            state_income_dict = state_filing_dict[filing_status]

            combined_income_dict = {}
            assert sorted(state_income_dict.keys()) == sorted(income_dict.keys())
            for income_type, income_brackets in income_dict.iteritems():
                state_income_brackets = state_income_dict[income_type]

                income_brackets_with_deduct = adjust_bracket(income_brackets,
                                                    dd.federal_standard_deduction[filing_status])
                state_income_brackets_with_deduct = adjust_bracket(state_income_brackets,
                                                           dd.state_standard_deduction[state][filing_status])

                combined_bracket = merge_brackets(income_brackets_with_deduct, state_income_brackets_with_deduct)
                combined_income_dict[income_type] = combined_bracket

            combined_filing_dict[filing_status] = combined_income_dict

        by_state_combined[state] = combined_filing_dict
    return by_state_combined

combined = build_combined_bracket()

# default bracket for most calculations
CA_MARRIED = combined[constants.CA][constants.FILING_MARRIED]













