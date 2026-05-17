import QuantLib as ql
import xloil as xlo

from .config import EXCEL_GROUP_NAME

QL_FREQUENCY = {
    "ANNUAL": ql.Annual,
    "BIMONTHLY": ql.Bimonthly,
    "BIWEEKLY": ql.Biweekly,
    "DAILY": ql.Daily,
    "EVERYFOURTHMONTH": ql.EveryFourthMonth,
    "EVERYFOURTHWEEK": ql.EveryFourthWeek,
    "MONTHLY": ql.Monthly,
    "NOFREQUENCY": ql.NoFrequency,
    "ONCE": ql.Once,
    "OTHERFREQUENCY": ql.OtherFrequency,
    "QUARTERLY": ql.Quarterly,
    "SEMIANNUAL": ql.Semiannual,
    "WEEKLY": ql.Weekly,
}

@xlo.converter()
def qFrequency(s : str) -> ql.Frequency:
    return QL_FREQUENCY.get(s.upper())

QL_TIMEUNIT = {
    "DAYS": ql.Days,
    "HOURS": ql.Hours,
    "MINUTES": ql.Minutes,
    "MONTHS": ql.Months,
    "SECONDS": ql.Seconds,
    "WEEKS": ql.Weeks,
    "YEARS": ql.Years,
}

@xlo.converter()
def qTimeUnit(s : str) -> ql.TimeUnit:
    return QL_TIMEUNIT.get(s.upper())

@xlo.converter()
def qPeriod(s : str) -> ql.Period:
    return ql.Period(s)

@xlo.returner(target=ql.Period, register=True)
def xPeriod(period : ql.Period):
  return str(period)

@xlo.func(
    help='Create a QuantLib Period from an integer and a time unit.',
    args={
        'n': 'The number of time units.',
        'unit': 'The time unit (e.g. "DAYS", "MONTHS", "YEARS").',
    },
    group=EXCEL_GROUP_NAME,
)
def qlPeriod(n : int, unit : qTimeUnit, Trigger = None) -> ql.Period:
    return ql.Period(n, unit)
