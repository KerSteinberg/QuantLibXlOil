import QuantLib as ql
import xloil as xlo

from .config import EXCEL_GROUP_NAME
from .date import qDate, _to_date_list
from .utilities import to_float_list


@xlo.func(
    help="Creates a fixed dividend.",
    args={"amount": "The dividend amount.", "date": "The dividend date."},
    group=EXCEL_GROUP_NAME,
)
def qlFixedDividend(amount: float, date: qDate, trigger=None) -> ql.FixedDividend:
    return ql.FixedDividend(amount, date)


@xlo.func(
    help="Creates a fractional dividend.",
    args={"amount": "The dividend amount.", "date": "The dividend date."},
    group=EXCEL_GROUP_NAME,
)
def qlFractionalDividend(
    amount: float, date: qDate, trigger=None
) -> ql.FractionalDividend:
    return ql.FractionalDividend(amount, date)


@xlo.func(
    help="Creates a dividend vector.",
    args={
        "dividend_dates": "The dividend dates.",
        "dividend_amounts": "The dividend amounts.",
    },
    group=EXCEL_GROUP_NAME,
)
def qlDividendVector(
    dividend_dates: xlo.Array(dims=1),
    dividend_amounts: xlo.Array(dims=1),
    trigger=None,
) -> ql.DividendVector:
    return ql.DividendVector(
        _to_date_list(dividend_dates), to_float_list(dividend_amounts)
    )
