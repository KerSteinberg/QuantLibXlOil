

def test_qlPeriod():
    from quantlibxloil import qlPeriod
    import QuantLib as ql
    period = qlPeriod(3, ql.Months)
    assert isinstance(period, ql.Period)

def test_qlPeriodLength():
    from quantlibxloil import qlPeriod, qlPeriodLength
    import QuantLib as ql
    period = qlPeriod(3, ql.Months)
    assert qlPeriodLength(period) == 3

def test_qlPeriodUnits():
    from quantlibxloil import qlPeriod, qlPeriodUnits
    import QuantLib as ql
    period = qlPeriod(3, ql.Months)
    assert qlPeriodUnits(period) == "MONTHS"

def test_qlPeriodFrequency():
    from quantlibxloil import qlPeriod, qlPeriodFrequency
    import QuantLib as ql
    period = qlPeriod(3, ql.Months)
    assert qlPeriodFrequency(period) == "QUARTERLY"

def test_qlPeriodNormalized():
    from quantlibxloil import qlPeriod, qlPeriodNormalized
    import QuantLib as ql
    period = qlPeriod(12, ql.Months)
    normalized_period = qlPeriodNormalized(period)
    assert normalized_period.length() == 1
    assert normalized_period.units() == ql.Years
