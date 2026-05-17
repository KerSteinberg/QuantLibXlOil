import QuantLib as ql
import xloil as xlo

from .config import EXCEL_GROUP_NAME
from .utilities import first_key

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
def qFrequency(s : str) -> int:
    return QL_FREQUENCY.get(s.upper())

QL_TIMEUNIT = {
    "DAYS": ql.Days,
    "HOURS": ql.Hours,
    "MICROSECONDS": ql.Microseconds,
    "MILLISECONDS": ql.Milliseconds,
    "MINUTES": ql.Minutes,
    "MONTHS": ql.Months,
    "SECONDS": ql.Seconds,
    "WEEKS": ql.Weeks,
    "YEARS": ql.Years,
}

@xlo.converter()
def qTimeUnit(s : str) -> int:
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

@xlo.func(
    help='Return Period length.',
    args={
        'Period': 'QuantLib Period.',
    },
    group=EXCEL_GROUP_NAME,
)
def qlPeriodLength(period : qPeriod, Trigger = None) -> int:
    return period.length()

@xlo.func(
    help='Return Period time unit.',
    args={
        'Period': 'QuantLib Period.',
    },
    group=EXCEL_GROUP_NAME,
)
def qlPeriodUnits(period : qPeriod, Trigger = None) -> qTimeUnit:
    return first_key(QL_TIMEUNIT, period.units(), ql.Days)

@xlo.func(
    help='Return Period frequency.',
    args={
        'Period': 'QuantLib Period.',
    },
    group=EXCEL_GROUP_NAME,
)
def qlPeriodFrequency(period : qPeriod, Trigger = None) -> qFrequency:
    return first_key(QL_FREQUENCY, period.frequency(), ql.NoFrequency)

@xlo.func(
    help='Return a normalized version of a QuantLib Period.',
    args={
        'Period': 'QuantLib Period.',
    },
    group=EXCEL_GROUP_NAME,
)
def qlPeriodNormalized(period : qPeriod, Trigger = None) -> qPeriod:
    return period.normalized()
