import QuantLib as ql

from quantlib_xloil.payoffs import (
    qOptionType,
    qlPayoffValue,
    qlTypePayoffOptionType,
    qlStrikedTypePayoffStrike,
    qlPlainVanillaPayoff,
    qlAsPlainVanillaPayoff,
    qlPercentageStrikePayoff,
    qlCashOrNothingPayoff,
    qlAssetOrNothingPayoff,
    qlSuperSharePayoff,
    qlGapPayoff,
    qlVanillaForwardPayoff,
)


def test_payoff_option_type_converter_and_name():
    assert qOptionType.__wrapped__("call") == ql.Option.Call
    assert qOptionType.__wrapped__("PUT") == ql.Option.Put


def test_plain_vanilla_payoff_and_cast():
    payoff = qlPlainVanillaPayoff(qOptionType.__wrapped__("call"), 100.0)

    assert qlTypePayoffOptionType(payoff) == "CALL"
    assert qlStrikedTypePayoffStrike(payoff) == 100.0
    assert qlPayoffValue(payoff, 110.0) == 10.0
    assert qlAsPlainVanillaPayoff(payoff) is not None


def test_other_payoff_constructors_and_values():
    pct = qlPercentageStrikePayoff(qOptionType.__wrapped__("call"), 0.90)
    con = qlCashOrNothingPayoff(qOptionType.__wrapped__("call"), 100.0, 10.0)
    aon = qlAssetOrNothingPayoff(qOptionType.__wrapped__("call"), 100.0)
    sup = qlSuperSharePayoff(qOptionType.__wrapped__("call"), 100.0, 5.0)
    gap = qlGapPayoff(qOptionType.__wrapped__("call"), 100.0, 95.0)
    vf = qlVanillaForwardPayoff(qOptionType.__wrapped__("call"), 100.0)

    assert qlTypePayoffOptionType(pct) == "CALL"
    assert qlStrikedTypePayoffStrike(pct) > 0.0

    assert qlPayoffValue(con, 110.0) == 10.0
    assert qlPayoffValue(aon, 110.0) == 110.0
    assert qlPayoffValue(sup, 110.0) >= 0.0
    assert qlPayoffValue(gap, 110.0) == 15.0
    assert qlPayoffValue(vf, 110.0) == 10.0
