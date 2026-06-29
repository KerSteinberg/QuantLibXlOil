import numpy as np
import QuantLib as ql
import xloil as xlo
import pandas as pd

from xloil.pandas import PDFrame
from .config import EXCEL_GROUP_NAME

from .cashflows import qlAsFixedRateCoupon, qlAsFloatingRateCoupon


@xlo.func(
    help="Analyzes fixed rate cashflows from a QuantLib leg.",
    args={
        "leg": "Array of QuantLib FixedRateLeg cashflow objects to be analyzed.",
        "discount_curve": "QuantLib YieldTermStructureHandle for discounting cashflows to present value.",
        "nominal_exchange_start": "",
        "nominal_exchange_end": "",
        "fx_rate": "",
    },
    group=EXCEL_GROUP_NAME,
)
def qlFixedFlows(
    leg: xlo.Array(dims=1),
    discount_curve: ql.YieldTermStructureHandle,
    nominal_exchange_start: bool = False,
    nominal_exchange_maturity: bool = False,
):

    # Prüfung auf isinstance(ql.FixedRateLeg)
    # collect coupons
    analysis = []
    df_initial = pd.DataFrame()

    for cf in leg:
        coupon = qlAsFixedRateCoupon(cf)
        cf_info = {
            "StartDate": coupon.accrualStartDate().serialNumber(),
            "EndDate": coupon.accrualEndDate().serialNumber(),
            "PayDate": coupon.date().serialNumber(),
            "Notional": coupon.nominal(),
            "Rate": coupon.rate(),
            "Amount": coupon.amount(),
            "YearFraction": coupon.accrualPeriod(),
            "DayCounter": coupon.dayCounter(),
            # "AccrualDays": coupon.accrualDays(),
        }
        discount = (
            discount_curve.discount(coupon.date())
            if coupon.date() >= discount_curve.referenceDate()
            else 0.0
        )
        cf_info["Discount"] = discount
        analysis.append(cf_info)

    df = pd.DataFrame(analysis)

    if nominal_exchange_start == True:
        if len(leg) > 0:
            cf = qlAsFixedRateCoupon(leg[0])
            cf_info = {
                "StartDate": "",
                "EndDate": "",
                "PayDate": cf.accrualStartDate().serialNumber(),
                "Notional": cf.nominal(),
                "Rate": "",
                "Amount": -cf.nominal(),
                "YearFraction": "",
                "DayCounter": "",
                "Discount": (
                    discount_curve.discount(cf.accrualStartDate())
                    if cf.date() >= discount_curve.referenceDate()
                    else 0.0
                ),
            }
            df_start = pd.DataFrame([cf_info])
            df = pd.concat(
                [df_start, df],
                ignore_index=True,
            )

    if nominal_exchange_maturity == True:
        # add notional cash flow at maturity
        if len(leg) > 0:
            cf = qlAsFixedRateCoupon(leg[-1])
            cf_info = {
                "PayDate": cf.date().serialNumber(),
                "Notional": cf.nominal(),
                "Amount": cf.nominal(),
                "Discount": (
                    discount_curve.discount(cf.date())
                    if cf.date() >= discount_curve.referenceDate()
                    else 0.0
                ),
            }
            df_end = pd.DataFrame([cf_info])
            df = pd.concat(
                [df, df_end],
                ignore_index=True,
            )

    return df


@xlo.func(
    help="Analyzes float rate cashflows from a QuantLib leg.",
    args={
        "leg": "Array of QuantLib FixedRateLeg cashflow objects to be analyzed.",
        "discountCurve": "QuantLib YieldTermStructureHandle for discounting cashflows to present value.",
        "nominal_exchange_start": "",
        "nominal_exchange_end": "",
    },
    group=EXCEL_GROUP_NAME,
)
def qlFloatFlows(
    leg: xlo.Array(dims=1),
    discount_curve: ql.YieldTermStructureHandle,
    nominal_exchange_start: bool = False,
    nominal_exchange_maturity: bool = False,
):

    # Prüfung auf isinstance(iborLeg)
    # collect coupons
    analysis = []
    for cf in leg:
        coupon = qlAsFloatingRateCoupon(cf)
        cf_info = {
            "FixingDate": (coupon.accrualStartDate() - ql.Period("2D")).serialNumber(),
            "StartDate": coupon.accrualStartDate().serialNumber(),
            "EndDate": coupon.accrualEndDate().serialNumber(),
            "PayDate": coupon.date().serialNumber(),
            "Notional": coupon.nominal(),
            "Rate": coupon.rate(),
            "Amount": coupon.amount(),
            "YearFraction": coupon.accrualPeriod(),
            "DayCounter": coupon.dayCounter(),
            "Fixing": coupon.indexFixing(),
            "Index": coupon.index().name(),
            "Spread": coupon.spread(),
            # "AccrualDays": coupon.accrualDays(),
        }
        discount = (
            discount_curve.discount(coupon.date())
            if coupon.date() >= discount_curve.referenceDate()
            else 0.0
        )
        cf_info["Discount"] = discount
        analysis.append(cf_info)
    df = pd.DataFrame(analysis)

    if nominal_exchange_start == True:
        if len(leg) > 0:
            cf = qlAsFloatingRateCoupon(leg[0])
            cf_info = {
                "FixingDate": "",
                "StartDate": "",
                "EndDate": "",
                "PayDate": cf.accrualStartDate().serialNumber(),
                "Notional": cf.nominal(),
                "Rate": "",
                "Amount": -cf.nominal(),
                "YearFraction": "",
                "DayCounter": "",
                "Discount": (
                    discount_curve.discount(cf.accrualStartDate())
                    if cf.date() >= discount_curve.referenceDate()
                    else 0.0
                ),
            }
            df_start = pd.DataFrame([cf_info])
            df = pd.concat(
                [df_start, df],
                ignore_index=True,
            )

    if nominal_exchange_maturity == True:
        # add notional cash flow at maturity
        if len(leg) > 0:
            cf = qlAsFloatingRateCoupon(leg[-1])
            cf_info = {
                "PayDate": cf.date().serialNumber(),
                "Notional": cf.nominal(),
                "Amount": cf.nominal(),
                "Discount": (
                    discount_curve.discount(cf.date())
                    if cf.date() >= discount_curve.referenceDate()
                    else 0.0
                ),
            }
            df_end = pd.DataFrame([cf_info])
            df = pd.concat(
                [df, df_end],
                ignore_index=True,
            )

    return df
