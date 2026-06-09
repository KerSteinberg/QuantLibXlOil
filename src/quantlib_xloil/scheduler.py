import QuantLib as ql
import xloil as xlo

from .date import qDate, qFrequency, qPeriod
from .calendars import (
    qBusinessDayConvention,
    qCalendar,
    QL_BUSINESSDAYCONVENTION,
)
from .config import EXCEL_GROUP_NAME
from .utilities import enum_value, first_key, UNKNOWN_KEY, UNKNOWN_VALUE

QL_DATEGENERATION_RULE = {
    "BACKWARD": ql.DateGeneration.Backward,
    "CDS": ql.DateGeneration.CDS,
    "CDS2015": ql.DateGeneration.CDS2015,
    "FORWARD": ql.DateGeneration.Forward,
    "OLDCDS": ql.DateGeneration.OldCDS,
    "THIRDWEDNESDAY": ql.DateGeneration.ThirdWednesday,
    "THIRDWEDNESDAYINCLUSIVE": ql.DateGeneration.ThirdWednesdayInclusive,
    "TWENTIETH": ql.DateGeneration.Twentieth,
    "TWENTIETHIMM": ql.DateGeneration.TwentiethIMM,
    "ZERO": ql.DateGeneration.Zero,
    UNKNOWN_KEY: UNKNOWN_VALUE,
}


def _qDateGenerationRule(rule: str) -> ql.DateGeneration:
    return enum_value(rule, QL_DATEGENERATION_RULE)


@xlo.converter()
def qDateGenerationRule(rule: str) -> ql.DateGeneration:
    return _qDateGenerationRule(rule)


@xlo.func(
    help="Create a QuantLib Schedule object.",
    args={
        "effective_date": "The effective date of the schedule.",
        "termination_date": "The termination date of the schedule.",
        "tenor": "The tenor of the schedule.",
        "calendar": "The calendar to use for date adjustments.",
        "convention": "The business day convention to use for date adjustments.",
        "termination_date_convention": "The business day convention to use for adjusting the termination date.",
        "date_generation_rule": "Backward, Forward, CDS, etc.",
        "end_of_month": "Whether to adjust dates to the end of the month.",
        "first_date": "The first date of the schedule (optional).",
        "last_date": "The last date of the schedule (optional).",
    },
    group=EXCEL_GROUP_NAME,
)
def qlSchedule(
    effective_date: qDate,
    termination_date: qDate,
    tenor: qPeriod,
    calendar: qCalendar,
    convention: qBusinessDayConvention,
    termination_date_convention: qBusinessDayConvention,
    date_generation_rule: qDateGenerationRule,
    end_of_month: bool,
    first_date: qDate = ql.Date(),
    last_date: qDate = ql.Date(),
    trigger=None,
) -> ql.Schedule:
    return ql.Schedule(
        effective_date,
        termination_date,
        tenor,
        calendar,
        convention,
        termination_date_convention,
        date_generation_rule,
        end_of_month,
        first_date,
        last_date,
    )


@xlo.func(
    help="Create a QuantLib Schedule object from a list of dates.",
    args={
        "dates": "A list of dates to create the schedule from.",
        "calendar": "The calendar to use for date adjustments (optional). Default is NullCalendar.",
        "convention": "The business day convention to use for date adjustments (optional). Default is Unadjusted.",
    },
    group=EXCEL_GROUP_NAME,
)
def qlScheduleFromDates(
    dates: xlo.Array(dims=1),
    calendar: qCalendar = ql.NullCalendar(),
    convention: qBusinessDayConvention = ql.Unadjusted,
    trigger=None,
) -> ql.Schedule:
    _dates = [ql.Date(round(d)) for d in dates]
    _dates
    return ql.Schedule(
        _dates,
        calendar,
        convention,
    )


@xlo.func(
    help="Return the list of dates in a QuantLib Schedule.",
    args={
        "schedule": "The QuantLib Schedule to extract dates from.",
    },
    group=EXCEL_GROUP_NAME,
)
def qlScheduleDates(schedule: ql.Schedule, trigger=None) -> list:
    return [d for d in schedule.dates()]


@xlo.func(
    help="Return the schedule date before a reference date.",
    args={
        "schedule": "QuantLib Schedule.",
        "ref_date": "Reference date.",
    },
    group=EXCEL_GROUP_NAME,
)
def qlSchedulePreviousDate(
    schedule: ql.Schedule, ref_date: qDate, trigger=None
) -> ql.Date:
    return schedule.previousDate(ref_date)


@xlo.func(
    help="Return the schedule date at or after a reference date.",
    args={
        "schedule": "QuantLib Schedule.",
        "ref_date": "Reference date.",
    },
    group=EXCEL_GROUP_NAME,
)
def qlScheduleNextDate(schedule: ql.Schedule, ref_date: qDate, trigger=None) -> ql.Date:
    return schedule.nextDate(ref_date)


@xlo.func(
    help="Return whether regularity flags are available for a QuantLib Schedule.",
    args={
        "schedule": "QuantLib Schedule.",
    },
    group=EXCEL_GROUP_NAME,
)
def qlScheduleHasIsRegular(schedule: ql.Schedule, trigger=None) -> bool:
    return schedule.hasIsRegular()


@xlo.func(
    help="Return whether the i-th interval in a QuantLib Schedule is regular.",
    args={
        "schedule": "QuantLib Schedule.",
        "i": "The interval index (one-based).",
    },
    group=EXCEL_GROUP_NAME,
)
def qlScheduleIsRegular(schedule: ql.Schedule, i: int, trigger=None) -> bool:
    return schedule.isRegular(i)


@xlo.func(
    help="Return regularity flags for all intervals in a QuantLib Schedule.",
    args={
        "schedule": "QuantLib Schedule.",
    },
    group=EXCEL_GROUP_NAME,
)
def qlScheduleIsRegular2(schedule: ql.Schedule, trigger=None) -> list:
    return list(schedule.isRegular())


@xlo.func(
    help="Return the calendar used by a QuantLib Schedule.",
    args={
        "schedule": "QuantLib Schedule.",
    },
    group=EXCEL_GROUP_NAME,
)
def qlScheduleCalendar(schedule: ql.Schedule, trigger=None) -> ql.Calendar:
    return schedule.calendar()


@xlo.func(
    help="Return the start date of a QuantLib Schedule.",
    args={
        "schedule": "QuantLib Schedule.",
    },
    group=EXCEL_GROUP_NAME,
)
def qlScheduleStartDate(schedule: ql.Schedule, trigger=None) -> ql.Date:
    return schedule.startDate()


@xlo.func(
    help="Return the end date of a QuantLib Schedule.",
    args={
        "schedule": "QuantLib Schedule.",
    },
    group=EXCEL_GROUP_NAME,
)
def qlScheduleEndDate(schedule: ql.Schedule, trigger=None) -> ql.Date:
    return schedule.endDate()


@xlo.func(
    help="Return whether a QuantLib Schedule has an associated tenor.",
    args={
        "schedule": "QuantLib Schedule.",
    },
    group=EXCEL_GROUP_NAME,
)
def qlScheduleHasTenor(schedule: ql.Schedule, trigger=None) -> bool:
    return schedule.hasTenor()


@xlo.func(
    help="Return the tenor of a QuantLib Schedule.",
    args={
        "schedule": "QuantLib Schedule.",
    },
    group=EXCEL_GROUP_NAME,
)
def qlScheduleTenor(schedule: ql.Schedule, trigger=None) -> ql.Period:
    return schedule.tenor()


@xlo.func(
    help="Return the business day convention of a QuantLib Schedule.",
    args={
        "schedule": "QuantLib Schedule.",
    },
    group=EXCEL_GROUP_NAME,
)
def qlScheduleBusinessDayConvention(schedule: ql.Schedule, trigger=None) -> str:
    return first_key(
        QL_BUSINESSDAYCONVENTION, schedule.businessDayConvention(), UNKNOWN_VALUE
    )


@xlo.func(
    help="Return whether a QuantLib Schedule has a termination date convention.",
    args={
        "schedule": "QuantLib Schedule.",
    },
    group=EXCEL_GROUP_NAME,
)
def qlScheduleHasTerminationDateBusinessDayConvention(
    schedule: ql.Schedule, trigger=None
) -> bool:
    return schedule.hasTerminationDateBusinessDayConvention()


@xlo.func(
    help="Return the termination date business day convention of a QuantLib Schedule.",
    args={
        "schedule": "QuantLib Schedule.",
    },
    group=EXCEL_GROUP_NAME,
)
def qlScheduleTerminationDateBusinessDayConvention(
    schedule: ql.Schedule, trigger=None
) -> str:
    return first_key(
        QL_BUSINESSDAYCONVENTION,
        schedule.terminationDateBusinessDayConvention(),
        UNKNOWN_VALUE,
    )


@xlo.func(
    help="Return whether a QuantLib Schedule has a date generation rule.",
    args={
        "schedule": "QuantLib Schedule.",
    },
    group=EXCEL_GROUP_NAME,
)
def qlScheduleHasRule(schedule: ql.Schedule, trigger=None) -> bool:
    return schedule.hasRule()


@xlo.func(
    help="Return the date generation rule of a QuantLib Schedule.",
    args={
        "schedule": "QuantLib Schedule.",
    },
    group=EXCEL_GROUP_NAME,
)
def qlScheduleRule(schedule: ql.Schedule, trigger=None) -> str:
    return first_key(QL_DATEGENERATION_RULE, schedule.rule(), UNKNOWN_VALUE)


@xlo.func(
    help="Return whether a QuantLib Schedule has an end-of-month flag.",
    args={
        "schedule": "QuantLib Schedule.",
    },
    group=EXCEL_GROUP_NAME,
)
def qlScheduleHasEndOfMonth(schedule: ql.Schedule, trigger=None) -> bool:
    return schedule.hasEndOfMonth()


@xlo.func(
    help="Return the end-of-month flag of a QuantLib Schedule.",
    args={
        "schedule": "QuantLib Schedule.",
    },
    group=EXCEL_GROUP_NAME,
)
def qlScheduleEndOfMonth(schedule: ql.Schedule, trigger=None) -> bool:
    return schedule.endOfMonth()


@xlo.func(
    help="Return a QuantLib Schedule truncated after a date.",
    args={
        "schedule": "QuantLib Schedule.",
        "truncation_date": "Truncation date.",
    },
    group=EXCEL_GROUP_NAME,
)
def qlScheduleAfter(
    schedule: ql.Schedule, truncation_date: qDate, trigger=None
) -> ql.Schedule:
    return schedule.after(truncation_date)


@xlo.func(
    help="Return a QuantLib Schedule truncated until a date.",
    args={
        "schedule": "QuantLib Schedule.",
        "truncation_date": "Truncation date.",
    },
    group=EXCEL_GROUP_NAME,
)
def qlScheduleUntil(
    schedule: ql.Schedule, truncation_date: qDate, trigger=None
) -> ql.Schedule:
    return schedule.until(truncation_date)


@xlo.func(
    help="Create a QuantLib Schedule object with flexible arguments.",
    args={
        "effective_date": "The effective date of the schedule (optional).",
        "termination_date": "The termination date of the schedule (optional).",
        "tenor": "The tenor of the schedule (optional).",
        "frequency": "The frequency of the schedule (optional).",
        "calendar": "The calendar to use for date adjustments (optional).",
        "convention": "The business day convention to use for date adjustments (optional).",
        "terminal_date_convention": "The business day convention to use for adjusting the termination date (optional).",
        "rule": "Backward, Forward, CDS, etc. (optional).",
        "forwards": "Whether to generate dates forwards (optional).",
        "backwards": "Whether to generate dates backwards (optional).",
        "end_of_month": "Whether to adjust dates to the end of the month (optional).",
        "first_date": "The first date of the schedule (optional).",
        "next_to_last_date": "The next-to-last date of the schedule (optional).",
    },
    group=EXCEL_GROUP_NAME,
)
def qlMakeSchedule(
    effective_date=None,
    termination_date=None,
    tenor=None,
    frequency=None,
    calendar=None,
    convention=None,
    terminal_date_convention=None,
    rule=None,
    forwards=False,
    backwards=False,
    end_of_month=None,
    first_date=None,
    next_to_last_date=None,
    trigger=None,
) -> ql.Schedule:
    # we cannot use converters for None defaults
    if effective_date is not None:
        effective_date = qDate.__wrapped__(effective_date)
    if termination_date is not None:
        termination_date = qDate.__wrapped__(termination_date)
    if tenor is not None:
        tenor = qPeriod.__wrapped__(tenor)
    if frequency is not None:
        frequency = qFrequency.__wrapped__(frequency)
    if calendar is not None:
        calendar = qCalendar.__wrapped__(calendar)
    if convention is not None:
        convention = qBusinessDayConvention.__wrapped__(convention)
    if terminal_date_convention is not None:
        terminal_date_convention = qBusinessDayConvention.__wrapped__(
            terminal_date_convention
        )
    if rule is not None:
        rule = qDateGenerationRule.__wrapped__(rule)
    if forwards:
        forwards = bool(forwards)
    if backwards:
        backwards = bool(backwards)
    if end_of_month is not None:
        end_of_month = bool(end_of_month)
    if first_date is not None:
        first_date = qDate.__wrapped__(first_date)
    if next_to_last_date is not None:
        next_to_last_date = qDate.__wrapped__(next_to_last_date)
    return ql.MakeSchedule(
        effective_date,
        termination_date,
        tenor,
        frequency,
        calendar,
        convention,
        terminal_date_convention,
        rule,
        forwards,
        backwards,
        end_of_month,
        first_date,
        next_to_last_date,
    )
