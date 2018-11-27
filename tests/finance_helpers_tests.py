
import finance_helpers as fh


def test_options_application():
    returns = range(5)
    call_ret = fh.apply_covered_call(returns, 3)
    assert call_ret == [0, 1, 2, 3, 3]

    put_ret = fh.apply_protected_put(returns, 2)
    assert put_ret == [2, 2, 2, 3, 4]

    collar_ret = fh.apply_collar(returns, 1, 3)
    assert collar_ret == [1, 1, 2, 3, 3]

    devastation = [0] * 5
    blended = fh.blend_returns(returns, devastation, 0.25)
    assert blended == [0, 0.25, 0.5, 0.75, 1]
