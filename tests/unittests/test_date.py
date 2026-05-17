

def test_qlPeriod():
    from quantlibxloil import qlPeriod
    import QuantLib as ql
    period = qlPeriod(3, ql.Months)
    assert isinstance(period, ql.Period)
