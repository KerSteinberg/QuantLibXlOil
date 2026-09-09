import QuantLib as ql
import pytest

from quantlib_xloil.cashflows import (
    qDurationType,
    qRateAveragingType,
    qlAsCoupon,
    qlAsCappedFlooredOvernightIndexedCoupon,
    qlAsOvernightIndexedCoupon,
    qlAveragingMultipleResetsPricer,
    qlBlackAveragingOvernightIndexedCouponPricer,
    qlBlackCompoundingOvernightIndexedCouponPricer,
    qlBlackIborCouponPricer,
    qlCappedFlooredCouponCap,
    qlCappedFlooredIborCoupon,
    qlCappedFlooredOvernightIndexedCoupon,
    qlMultipleResetsCoupon,
    qlCashFlowAmount,
    qlCashFlowDate,
    qlCashFlowHasOccurred,
    qlCashFlowsAccrualDays,
    qlCashFlowsAccrualPeriod,
    qlCashFlowsAccruedAmount,
    qlCashFlowsAccruedDays,
    qlCashFlowsAccruedPeriod,
    qlCashFlowsAtmRate,
    qlCashFlowsBasisPointValueFromInterestRate,
    qlCashFlowsBasisPointValueFromRate,
    qlCashFlowsBps,
    qlCashFlowsBpsFromInterestRate,
    qlCashFlowsBpsFromRate,
    qlCashFlowsConvexityFromInterestRate,
    qlCashFlowsDurationFromRate,
    qlCashFlowsMaturityDate,
    qlCashFlowsNextCashFlow,
    qlCashFlowsNpv,
    qlCashFlowsNpvBps,
    qlCashFlowsPreviousCashFlow,
    qlCashFlowsStartDate,
    qlCashFlowsYieldRate,
    qlCashFlowsZSpread,
    qlCappedFlooredCouponEffectiveCap,
    qlCappedFlooredCouponEffectiveFloor,
    qlCappedFlooredCouponFloor,
    qlCappedFlooredCouponIsCapped,
    qlCappedFlooredCouponIsFloored,
    qlCappedFlooredOvernightIndexedCouponAveragingMethod,
    qlCappedFlooredOvernightIndexedCouponCompoundSpreadDaily,
    qlCappedFlooredOvernightIndexedCouponDailyCapFloor,
    qlCappedFlooredOvernightIndexedCouponEffectiveCapletVolatility,
    qlCappedFlooredOvernightIndexedCouponEffectiveFloorletVolatility,
    qlCappedFlooredOvernightIndexedCouponNakedOption,
    qlCappedFlooredOvernightIndexedCouponUnderlying,
    qlCompoundingMultipleResetsPricer,
    qlCouponAccrualDays,
    qlCouponAccrualEndDate,
    qlCouponAccrualPeriod,
    qlCouponAccrualStartDate,
    qlCouponAccruedAmount,
    qlCouponDayCounter,
    qlCouponExCouponDate,
    qlCouponNominal,
    qlCouponRate,
    qlCouponReferencePeriodEnd,
    qlCouponReferencePeriodStart,
    qlCmsLeg,
    qlCmsSpreadLeg,
    qlCmsZeroLeg,
    qlFixedRateCoupon,
    qlFixedRateLeg,
    qlFloatingRateCouponAdjustedFixing,
    qlFloatingRateCouponConvexityAdjustment,
    qlFloatingRateCouponFixingDate,
    qlFloatingRateCouponFixingDays,
    qlFloatingRateCouponGearing,
    qlFloatingRateCouponIndex,
    qlFloatingRateCouponIndexFixing,
    qlFloatingRateCouponIsInArrears,
    qlFloatingRateCouponPrice,
    qlFloatingRateCouponSetPricer,
    qlFloatingRateCouponSpread,
    qlIborCoupon,
    qlIborLeg,
    qlMultipleResetsLeg,
    qlOvernightIndexedCoupon,
    qlOvernightIndexedCouponApplyObservationShift,
    qlOvernightIndexedCouponAveragingMethod,
    qlOvernightIndexedCouponCanApplyTelescopicFormula,
    qlOvernightIndexedCouponCompoundSpreadDaily,
    qlOvernightIndexedCouponDt,
    qlOvernightIndexedCouponEffectiveIndexFixing,
    qlOvernightIndexedCouponEffectiveSpread,
    qlOvernightIndexedCouponFixingDates,
    qlOvernightIndexedCouponIndexFixings,
    qlOvernightIndexedCouponInterestDates,
    qlOvernightIndexedCouponLockoutDays,
    qlOvernightIndexedCouponRateComputationEndDate,
    qlOvernightIndexedCouponRateComputationStartDate,
    qlOvernightIndexedCouponValueDates,
    qlOvernightLeg,
    qlRangeAccrualLeg,
    qlSetCouponPricer,
    qlSimpleCashFlow,
)
from quantlib_xloil.calendars import (
    qBusinessDayConvention,
    qCalendar,
    qPeriod,
    qlCalendar,
)
from quantlib_xloil.currencies import qCurrency
from quantlib_xloil.date import qFrequency, qlDate
from quantlib_xloil.daycounters import qlDayCounter
from quantlib_xloil.indexes import qlEuribor, qlSofr, qlSwapIndex, qlSwapSpreadIndex
from quantlib_xloil.termstructures import qCompounding, qlFlatForward


def _schedule(start: ql.Date, end: ql.Date) -> ql.Schedule:
    return ql.Schedule(
        start,
        end,
        ql.Period(ql.Annual),
        qlCalendar("TARGET"),
        ql.Unadjusted,
        ql.Unadjusted,
        ql.DateGeneration.Forward,
        False,
    )


def _curve(reference_date: ql.Date, rate: float = 0.05) -> ql.YieldTermStructureHandle:
    return qlFlatForward(
        reference_date,
        rate,
        qlDayCounter("ACTUAL365FIXED"),
        qCompounding.__wrapped__("COMPOUNDED"),
        qFrequency.__wrapped__("ANNUAL"),
        qlCalendar("TARGET"),
    )


def test_cashflow_converters():
    assert qDurationType.__wrapped__("simple") == ql.Duration.Simple
    assert qDurationType.__wrapped__("MODIFIED") == ql.Duration.Modified
    assert qRateAveragingType.__wrapped__("compound") == ql.RateAveraging.Compound


def test_simple_cashflow_accessors_and_cast():
    payment_date = qlDate(2025, 1, 2)
    cf = qlSimpleCashFlow(12.5, payment_date)

    assert qlCashFlowAmount(cf) == 12.5
    assert qlCashFlowDate(cf) == payment_date
    assert qlCashFlowHasOccurred(cf, qlDate(2024, 12, 31)) is False
    assert qlAsCoupon(cf) is None


def test_coupon_methods_on_fixed_rate_coupon():
    start_date = qlDate(2024, 1, 2)
    end_date = qlDate(2025, 1, 2)
    payment_date = end_date
    ref_period_start = start_date
    ref_period_end = end_date
    ex_coupon_date = ql.Date()
    day_counter = qlDayCounter("ACTUAL365FIXED")

    coupon = qlFixedRateCoupon(
        payment_date,
        100.0,
        0.05,
        day_counter,
        start_date,
        end_date,
        ref_period_start,
        ref_period_end,
        ex_coupon_date,
    )

    assert qlCouponNominal(coupon) == 100.0
    assert qlCouponAccrualStartDate(coupon) == start_date
    assert qlCouponAccrualEndDate(coupon) == end_date
    assert qlCouponReferencePeriodStart(coupon) == ref_period_start
    assert qlCouponReferencePeriodEnd(coupon) == ref_period_end
    assert qlCouponExCouponDate(coupon) == ex_coupon_date
    assert qlCouponRate(coupon) == 0.05
    assert qlCouponAccrualPeriod(coupon) > 0.0
    assert qlCouponAccrualDays(coupon) > 0
    assert qlCouponDayCounter(coupon).name() == day_counter.name()
    assert qlCouponAccruedAmount(coupon, qlDate(2024, 7, 2)) > 0.0


def test_floatingratecoupon_methods_on_ibor_coupon():
    original_eval = ql.Settings.instance().evaluationDate

    start_date = qlDate(2024, 7, 2)
    end_date = qlDate(2025, 1, 2)
    payment_date = end_date
    fixing_days = 2
    day_counter = qlDayCounter("ACTUAL365FIXED")
    curve = _curve(qlDate(2024, 1, 2), 0.03)
    index = qlEuribor(ql.Period("6M"), curve)

    # Force forecasting path (instead of historical fixing lookup) for deterministic tests.
    ql.Settings.instance().evaluationDate = qlDate(2024, 1, 2)

    coupon = qlIborCoupon(
        payment_date,
        100.0,
        start_date,
        end_date,
        fixing_days,
        index,
        1.0,
        0.001,
        start_date,
        end_date,
        day_counter,
        False,
        ql.Date(),
    )

    coupon_2 = qlIborCoupon(
        payment_date,
        100.0,
        start_date,
        end_date,
        fixing_days,
        index,
        1.0,
        0.001,
        start_date,
        end_date,
        day_counter,
        False,
        ql.Date(),
        ql.Following,
    )

    assert qlFloatingRateCouponFixingDate(coupon) < start_date
    assert qlFloatingRateCouponFixingDays(coupon) == fixing_days
    assert qlFloatingRateCouponIsInArrears(coupon) is False
    assert qlFloatingRateCouponGearing(coupon) == 1.0
    assert qlFloatingRateCouponSpread(coupon) == 0.001

    try:
        index_fixing = qlFloatingRateCouponIndexFixing(coupon)
        adjusted_fixing = qlFloatingRateCouponAdjustedFixing(coupon)
        convexity_adjustment = qlFloatingRateCouponConvexityAdjustment(coupon)
        price = qlFloatingRateCouponPrice(coupon, curve)

        assert index_fixing > 0.0
        assert adjusted_fixing > 0.0
        assert convexity_adjustment >= 0.0
        assert price > 0.0
        assert qlFloatingRateCouponIndex(coupon) is not None

        pricer = qlBlackIborCouponPricer()
        assert qlFloatingRateCouponSetPricer(coupon, pricer) is True
    finally:
        ql.Settings.instance().evaluationDate = original_eval


def test_cappedflooredcoupon_methods_on_cappedfloored_ibor_coupon():
    start_date = qlDate(2024, 7, 2)
    end_date = qlDate(2025, 1, 2)
    payment_date = end_date
    fixing_days = 2
    day_counter = qlDayCounter("ACTUAL365FIXED")
    curve = _curve(qlDate(2024, 1, 2), 0.03)
    index = qlEuribor(ql.Period("6M"), curve)

    coupon = qlCappedFlooredIborCoupon(
        payment_date,
        100.0,
        start_date,
        end_date,
        fixing_days,
        index,
        1.0,
        0.0,
        0.06,
        0.01,
        start_date,
        end_date,
        day_counter,
        False,
        ql.Date(),
    )

    assert qlCappedFlooredCouponIsCapped(coupon) is True
    assert qlCappedFlooredCouponIsFloored(coupon) is True
    assert qlCappedFlooredCouponCap(coupon) == 0.06
    assert qlCappedFlooredCouponFloor(coupon) == 0.01
    assert qlCappedFlooredCouponEffectiveCap(coupon) == 0.06
    assert qlCappedFlooredCouponEffectiveFloor(coupon) == 0.01


def test_overnightindexedcoupon_methods_on_sofr_coupon():
    original_eval = ql.Settings.instance().evaluationDate

    start_date = qlDate(2024, 1, 2)
    end_date = qlDate(2024, 7, 2)
    payment_date = end_date
    day_counter = qlDayCounter("ACTUAL365FIXED")
    curve = _curve(start_date, 0.03)
    index = qlSofr(curve)

    # Force forecasting path for stable fixing-dependent quantities.
    ql.Settings.instance().evaluationDate = start_date

    coupon = qlOvernightIndexedCoupon(
        payment_date,
        100.0,
        start_date,
        end_date,
        index,
        1.0,
        0.0,
        start_date,
        end_date,
        day_counter,
        False,
        qRateAveragingType.__wrapped__("COMPOUND"),
        ql.nullInt(),
        0,
        False,
        False,
    )

    try:
        assert qlOvernightIndexedCouponAveragingMethod(coupon) == "COMPOUND"
        assert isinstance(
            qlOvernightIndexedCouponCanApplyTelescopicFormula(coupon), bool
        )
        assert qlOvernightIndexedCouponApplyObservationShift(coupon) is False
        assert qlOvernightIndexedCouponCompoundSpreadDaily(coupon) is False
        assert qlOvernightIndexedCouponLockoutDays(coupon) == 0

        assert qlOvernightIndexedCouponRateComputationStartDate(coupon) is not None
        assert qlOvernightIndexedCouponRateComputationEndDate(coupon) is not None

        value_dates = qlOvernightIndexedCouponValueDates(coupon)
        fixing_dates = qlOvernightIndexedCouponFixingDates(coupon)
        interest_dates = qlOvernightIndexedCouponInterestDates(coupon)
        dt = qlOvernightIndexedCouponDt(coupon)
        index_fixings = qlOvernightIndexedCouponIndexFixings(coupon)

        assert len(value_dates) > 1
        assert len(fixing_dates) == len(value_dates) - 1
        assert len(interest_dates) == len(value_dates)
        assert len(dt) == len(fixing_dates)
        assert len(index_fixings) == len(fixing_dates)
        assert qlOvernightIndexedCouponEffectiveIndexFixing(coupon) > 0.0
        assert qlOvernightIndexedCouponEffectiveSpread(coupon) == 0.0
    finally:
        ql.Settings.instance().evaluationDate = original_eval


def test_multiple_resets_coupon():
    original_eval = ql.Settings.instance().evaluationDate

    start_date = qlDate(2024, 1, 2)
    end_date = qlDate(2024, 7, 2)
    payment_date = end_date
    curve = _curve(start_date, 0.03)
    index = qlEuribor(ql.Period("6M"), curve)

    # Create a reset schedule with multiple reset dates
    reset_schedule = ql.Schedule(
        start_date,
        end_date,
        ql.Period(ql.Monthly),
        qlCalendar("TARGET"),
        ql.Unadjusted,
        ql.Unadjusted,
        ql.DateGeneration.Forward,
        False,
    )

    ql.Settings.instance().evaluationDate = start_date

    try:
        coupon = qlMultipleResetsCoupon(
            payment_date,
            100.0,
            reset_schedule,
            fixing_days=2,
            index=index,
            gearing=1.0,
            coupon_spread=0.001,
            rate_spread=0.0,
        )

        assert coupon is not None
        assert qlCouponNominal(coupon) == 100.0
        assert qlCouponAccrualStartDate(coupon) == start_date
        assert qlCouponAccrualEndDate(coupon) == end_date
        assert qlFloatingRateCouponIndex(coupon) is not None
    finally:
        ql.Settings.instance().evaluationDate = original_eval


def test_cappedflooredovernightindexedcoupon_methods():
    original_eval = ql.Settings.instance().evaluationDate

    start_date = qlDate(2024, 1, 2)
    end_date = qlDate(2024, 7, 2)
    payment_date = end_date
    day_counter = qlDayCounter("ACTUAL365FIXED")
    curve = _curve(start_date, 0.03)
    index = qlSofr(curve)

    ql.Settings.instance().evaluationDate = start_date

    underlying = qlOvernightIndexedCoupon(
        payment_date,
        100.0,
        start_date,
        end_date,
        index,
        1.0,
        0.0,
        start_date,
        end_date,
        day_counter,
        False,
        qRateAveragingType.__wrapped__("COMPOUND"),
        ql.nullInt(),
        0,
        False,
        False,
    )
    coupon = qlCappedFlooredOvernightIndexedCoupon(underlying, 0.06, 0.01, False, False)

    try:
        assert qlCappedFlooredOvernightIndexedCouponUnderlying(coupon) is not None
        assert qlCappedFlooredOvernightIndexedCouponNakedOption(coupon) is False
        assert qlCappedFlooredOvernightIndexedCouponDailyCapFloor(coupon) is False
        assert (
            qlCappedFlooredOvernightIndexedCouponAveragingMethod(coupon) == "COMPOUND"
        )
        assert qlCappedFlooredOvernightIndexedCouponCompoundSpreadDaily(coupon) is False

        # These two accessors require a compatible pricer setup in QuantLib.
        with pytest.raises(RuntimeError):
            qlCappedFlooredOvernightIndexedCouponEffectiveCapletVolatility(coupon)
        with pytest.raises(RuntimeError):
            qlCappedFlooredOvernightIndexedCouponEffectiveFloorletVolatility(coupon)
    finally:
        ql.Settings.instance().evaluationDate = original_eval


def test_fixed_rate_leg_cashflows_analytics():
    start = qlDate(2024, 1, 2)
    end = qlDate(2027, 1, 2)
    schedule = _schedule(start, end)
    day_counter = qlDayCounter("ACTUAL365FIXED")

    leg = qlFixedRateLeg(schedule, day_counter, [100.0], [0.05])
    curve = _curve(start, 0.05)

    assert qlCashFlowsStartDate(leg) == start
    assert qlCashFlowsMaturityDate(leg) == end

    npv = qlCashFlowsNpv(leg, curve, False)
    ytm = qlCashFlowsYieldRate(
        leg,
        npv,
        day_counter,
        qCompounding.__wrapped__("COMPOUNDED"),
        qFrequency.__wrapped__("ANNUAL"),
        False,
    )
    duration = qlCashFlowsDurationFromRate(
        leg,
        ytm,
        day_counter,
        qCompounding.__wrapped__("COMPOUNDED"),
        qFrequency.__wrapped__("ANNUAL"),
        qDurationType.__wrapped__("MODIFIED"),
        False,
    )
    bpv = qlCashFlowsBasisPointValueFromRate(
        leg,
        ytm,
        day_counter,
        qCompounding.__wrapped__("COMPOUNDED"),
        qFrequency.__wrapped__("ANNUAL"),
        False,
    )
    z_spread = qlCashFlowsZSpread(
        leg,
        npv,
        curve.currentLink(),
        day_counter,
        qCompounding.__wrapped__("COMPOUNDED"),
        qFrequency.__wrapped__("ANNUAL"),
        False,
    )

    assert npv > 0.0
    assert ytm > 0.0
    assert duration > 0.0
    assert abs(bpv) > 0.0
    assert abs(z_spread) < 1.0e-6


def test_cashflows_step3_objects_and_accruals():
    start = qlDate(2024, 1, 2)
    end = qlDate(2027, 1, 2)
    schedule = _schedule(start, end)
    day_counter = qlDayCounter("ACTUAL365FIXED")
    leg = qlFixedRateLeg(schedule, day_counter, [100.0], [0.05])

    # Settlement before first coupon: only next cash flow should exist.
    settlement_early = qlDate(2024, 1, 15)
    prev_cf_early = qlCashFlowsPreviousCashFlow(leg, False, settlement_early)
    next_cf_early = qlCashFlowsNextCashFlow(leg, False, settlement_early)
    assert prev_cf_early is None
    assert next_cf_early is not None

    # Settlement after maturity: only previous cash flow should exist.
    settlement_late = qlDate(2028, 1, 15)
    prev_cf_late = qlCashFlowsPreviousCashFlow(leg, False, settlement_late)
    next_cf_late = qlCashFlowsNextCashFlow(leg, False, settlement_late)
    assert prev_cf_late is not None
    assert next_cf_late is None

    accrual_period = qlCashFlowsAccrualPeriod(leg, False, settlement_early)
    accrual_days = qlCashFlowsAccrualDays(leg, False, settlement_early)
    accrued_period = qlCashFlowsAccruedPeriod(leg, False, settlement_early)
    accrued_days = qlCashFlowsAccruedDays(leg, False, settlement_early)
    accrued_amount = qlCashFlowsAccruedAmount(leg, False, settlement_early)

    assert accrual_period > 0.0
    assert accrual_days > 0
    assert accrued_period >= 0.0
    assert accrued_days >= 0
    assert accrued_amount >= 0.0


def test_cashflows_step3_empty_leg_edge_cases():
    empty_leg = []
    settlement = qlDate(2024, 1, 2)

    assert qlCashFlowsPreviousCashFlow(empty_leg, False, settlement) is None
    assert qlCashFlowsNextCashFlow(empty_leg, False, settlement) is None
    assert qlCashFlowsAccrualPeriod(empty_leg, False, settlement) == 0.0
    assert qlCashFlowsAccrualDays(empty_leg, False, settlement) == 0
    assert qlCashFlowsAccruedPeriod(empty_leg, False, settlement) == 0.0
    assert qlCashFlowsAccruedDays(empty_leg, False, settlement) == 0
    assert qlCashFlowsAccruedAmount(empty_leg, False, settlement) == 0.0


def test_cashflows_overload_analytics_step2():
    start = qlDate(2024, 1, 2)
    end = qlDate(2027, 1, 2)
    schedule = _schedule(start, end)
    day_counter = qlDayCounter("ACTUAL365FIXED")
    compounding = qCompounding.__wrapped__("COMPOUNDED")
    frequency = qFrequency.__wrapped__("ANNUAL")

    leg = qlFixedRateLeg(schedule, day_counter, [100.0], [0.05])
    curve_handle = _curve(start, 0.05)

    npv = qlCashFlowsNpv(leg, curve_handle, False)
    assert npv > 0.0

    bps = qlCashFlowsBps(leg, curve_handle, False)
    assert bps > 0.0

    ytm = qlCashFlowsYieldRate(leg, npv, day_counter, compounding, frequency, False)
    ir = ql.InterestRate(ytm, day_counter, compounding, frequency)

    bps_ir = qlCashFlowsBpsFromInterestRate(leg, ir, False)
    bps_rate = qlCashFlowsBpsFromRate(
        leg, ytm, day_counter, compounding, frequency, False
    )
    assert abs(bps_ir - bps_rate) < 1.0e-10

    npvbps = qlCashFlowsNpvBps(leg, curve_handle, False)
    assert len(npvbps) == 2
    assert abs(npvbps[0] - npv) < 1.0e-10
    assert abs(npvbps[1] - bps) < 1.0e-10

    atm_rate = qlCashFlowsAtmRate(leg, curve_handle, False)
    assert atm_rate > 0.0

    convexity_ir = qlCashFlowsConvexityFromInterestRate(leg, ir, False)
    bpv_ir = qlCashFlowsBasisPointValueFromInterestRate(leg, ir, False)
    assert convexity_ir > 0.0
    assert abs(bpv_ir) > 0.0


def test_ibor_leg_pricer_assignment_smoke():
    start = qlDate(2024, 1, 2)
    end = qlDate(2026, 1, 2)
    schedule = _schedule(start, end)
    curve = _curve(start, 0.03)

    index = qlEuribor(ql.Period("6M"), curve)
    leg = qlIborLeg([100.0], schedule, index)
    pricer = qlBlackIborCouponPricer()

    assert len(leg) > 0
    assert qlSetCouponPricer(leg, pricer) is True


def test_overnight_cappedfloored_coupon_and_casts():
    start = qlDate(2024, 1, 2)
    end = qlDate(2024, 7, 2)
    payment_date = end
    curve = _curve(start, 0.03)
    overnight_index = qlSofr(curve)

    underlying = qlOvernightIndexedCoupon(
        payment_date,
        100.0,
        start,
        end,
        overnight_index,
    )
    capped_floored = qlCappedFlooredOvernightIndexedCoupon(underlying, 0.07, 0.01)

    assert qlAsOvernightIndexedCoupon(underlying) is not None
    assert qlAsCappedFlooredOvernightIndexedCoupon(capped_floored) is not None


def test_additional_pricer_constructors():
    assert isinstance(
        qlBlackCompoundingOvernightIndexedCouponPricer(),
        ql.BlackCompoundingOvernightIndexedCouponPricer,
    )
    assert isinstance(
        qlBlackAveragingOvernightIndexedCouponPricer(),
        ql.BlackAveragingOvernightIndexedCouponPricer,
    )
    assert isinstance(
        qlCompoundingMultipleResetsPricer(), ql.CompoundingMultipleResetsPricer
    )
    assert isinstance(
        qlAveragingMultipleResetsPricer(), ql.AveragingMultipleResetsPricer
    )


def test_qlFixedRateLeg_constructor():
    start = qlDate(2024, 1, 2)
    end = qlDate(2027, 1, 2)
    schedule = _schedule(start, end)
    day_counter = qlDayCounter("ACTUAL365FIXED")

    nominals = [100.0, 100.0, 100.0]
    coupon_rates = [0.05, 0.05, 0.05]

    leg = qlFixedRateLeg(
        schedule,
        day_counter,
        nominals,
        coupon_rates,
    )

    assert len(leg) == 3
    assert qlCashFlowsStartDate(leg) == start
    assert qlCashFlowsMaturityDate(leg) == end

    leg = qlFixedRateLeg(
        schedule,
        day_counter,
        nominals,
        None,
        payment_adjustment=qBusinessDayConvention.__wrapped__("FOLLOWING"),
        first_period_day_count=qlDayCounter("ACTUAL360"),
        ex_coupon_period=ql.Period("1D"),
        ex_coupon_calendar=qlCalendar("TARGET"),
        ex_coupon_convention=qBusinessDayConvention.__wrapped__("UNADJUSTED"),
        ex_coupon_end_of_month=True,
        payment_calendar=qlCalendar("TARGET"),
        payment_lag=2,
        compounding=qCompounding.__wrapped__("COMPOUNDED"),
        compounding_frequency=qFrequency.__wrapped__("SEMIANNUAL"),
        interest_rates=[
            ql.InterestRate(
                0.01,
                qlDayCounter("ACTUAL365FIXED"),
                qCompounding.__wrapped__("COMPOUNDED"),
                qFrequency.__wrapped__("SEMIANNUAL"),
            ),
            ql.InterestRate(
                0.01,
                qlDayCounter("ACTUAL365FIXED"),
                qCompounding.__wrapped__("COMPOUNDED"),
                qFrequency.__wrapped__("SEMIANNUAL"),
            ),
            ql.InterestRate(
                0.01,
                qlDayCounter("ACTUAL365FIXED"),
                qCompounding.__wrapped__("COMPOUNDED"),
                qFrequency.__wrapped__("SEMIANNUAL"),
            ),
        ],
    )

    assert len(leg) == 3
    assert qlCashFlowsStartDate(leg) == start
    assert qlCashFlowsMaturityDate(leg) == end

    leg = qlFixedRateLeg(
        schedule,
        day_counter,
        nominals,
        coupon_rates,
        payment_adjustment=qBusinessDayConvention.__wrapped__("FOLLOWING"),
        first_period_day_count=qlDayCounter("ACTUAL360"),
        ex_coupon_period=ql.Period("1D"),
        ex_coupon_calendar=qlCalendar("TARGET"),
        ex_coupon_convention=qBusinessDayConvention.__wrapped__("UNADJUSTED"),
        ex_coupon_end_of_month=True,
        payment_calendar=qlCalendar("TARGET"),
        payment_lag=2,
        compounding=qCompounding.__wrapped__("COMPOUNDED"),
        compounding_frequency=qFrequency.__wrapped__("SEMIANNUAL"),
    )

    assert len(leg) == 3
    assert qlCashFlowsStartDate(leg) == start
    assert qlCashFlowsMaturityDate(leg) == end


def test_qlIborLeg_constructor():
    start = qlDate(2024, 1, 2)
    end = qlDate(2026, 1, 2)
    schedule = _schedule(start, end)
    curve = _curve(start, 0.03)
    index = qlEuribor(ql.Period("6M"), curve)

    nominals = [100.0, 100.0]

    leg = qlIborLeg(
        nominals,
        schedule,
        index,
        payment_day_counter=qlDayCounter("ACTUAL365FIXED"),
    )

    assert len(leg) == 2
    assert qlCashFlowsStartDate(leg) == start
    assert qlCashFlowsMaturityDate(leg) == end

    leg = qlIborLeg(
        nominals,
        schedule,
        index,
        payment_day_counter=qlDayCounter("ACTUAL365FIXED"),
        payment_convention=qBusinessDayConvention.__wrapped__("FOLLOWING"),
        fixing_days=(2,),
        gearings=[1.0, 1.0],
        spreads=[0.001, 0.001],
        caps=[0.06, 0.06],
        floors=[0.01, 0.01],
        is_in_arrears=False,
        ex_coupon_period=ql.Period("1D"),
        ex_coupon_calendar=qlCalendar("TARGET"),
        ex_coupon_convention=qBusinessDayConvention.__wrapped__("UNADJUSTED"),
        ex_coupon_end_of_month=True,
        payment_calendar=qlCalendar("TARGET"),
        payment_lag=2,
        with_indexed_coupons=False,
    )

    assert len(leg) == 2
    assert qlCashFlowsStartDate(leg) == start
    assert qlCashFlowsMaturityDate(leg) == end


def test_qlOvernightLeg_constructor():
    start = qlDate(2024, 1, 2)
    end = qlDate(2026, 1, 2)
    schedule = _schedule(start, end)
    curve = _curve(start, 0.03)
    index = qlSofr(curve)

    nominals = [100.0, 100.0]

    leg = qlOvernightLeg(
        nominals,
        schedule,
        index,
        payment_day_counter=qlDayCounter("ACTUAL365FIXED"),
    )

    assert len(leg) == 2
    assert qlCashFlowsStartDate(leg) == start
    assert qlCashFlowsMaturityDate(leg) == end

    leg = qlOvernightLeg(
        nominals,
        schedule,
        index,
        payment_day_counter=qlDayCounter("ACTUAL365FIXED"),
        payment_convention=qBusinessDayConvention.__wrapped__("FOLLOWING"),
        gearings=[1.0, 1.0],
        spreads=[0.001, 0.001],
        telescopic_value_dates=False,
        averaging_method=qRateAveragingType.__wrapped__("COMPOUND"),
        payment_calendar=qlCalendar("TARGET"),
        payment_lag=2,
        lookback_days=ql.nullInt(),
        lockout_days=1,
        apply_observation_shift=False,
        compound_spread_daily=False,
        caps=[0.06, 0.06],
        floors=[0.01, 0.01],
        daily_cap_floor=False,
        in_arrears=True,
        naked_option=False,
        payment_dates=[ql.Date(2, 1, 2025), ql.Date(2, 1, 2026)],
    )

    assert len(leg) == 2
    assert qlCashFlowsStartDate(leg) == start
    assert qlCashFlowsMaturityDate(leg) == end


def test_qlCmsLeg_constructor():
    start = qlDate(2024, 1, 2)
    end = qlDate(2026, 1, 2)
    schedule = _schedule(start, end)
    curve = _curve(start, 0.03)
    index = qlEuribor(ql.Period("6M"), curve)
    swap_index = qlSwapIndex(
        family_name="TestSwapIndex",
        tenor=ql.Period("10Y"),
        settlement_days=2,
        currency=qCurrency.__wrapped__("EUR"),
        calendar=qlCalendar("TARGET"),
        fixed_leg_tenor=ql.Period("1Y"),
        fixed_leg_convention=qBusinessDayConvention.__wrapped__("MODIFIEDFOLLOWING"),
        fixed_leg_day_counter=qlDayCounter("ACTUAL365FIXED"),
        ibor_index=index,
        discount_curve=curve,
    )

    nominals = [100.0, 100.0]

    leg = qlCmsLeg(
        nominals,
        schedule,
        swap_index,
        payment_day_counter=qlDayCounter("ACTUAL365FIXED"),
    )

    assert len(leg) == 2
    assert qlCashFlowsStartDate(leg) == start
    assert qlCashFlowsMaturityDate(leg) == end

    leg = qlCmsLeg(
        nominals,
        schedule,
        swap_index,
        payment_day_counter=qlDayCounter("ACTUAL365FIXED"),
        payment_convention=qBusinessDayConvention.__wrapped__("FOLLOWING"),
        fixing_days=(2,),
        gearings=[1.0, 1.0],
        spreads=[0.001, 0.001],
        caps=[0.06, 0.06],
        floors=[0.01, 0.01],
        is_in_arrears=False,
        ex_coupon_period=ql.Period("1D"),
        ex_coupon_calendar=qlCalendar("TARGET"),
        ex_coupon_convention=qBusinessDayConvention.__wrapped__("UNADJUSTED"),
        ex_coupon_end_of_month=True,
        fixing_convention=qBusinessDayConvention.__wrapped__("PRECEDING"),
    )

    assert len(leg) == 2
    assert qlCashFlowsStartDate(leg) == start
    assert qlCashFlowsMaturityDate(leg) == end


def test_qlCmsZeroLeg_constructor():
    start = qlDate(2024, 1, 2)
    end = qlDate(2026, 1, 2)
    schedule = _schedule(start, end)
    curve = _curve(start, 0.03)
    index = qlEuribor(ql.Period("6M"), curve)
    swap_index = qlSwapIndex(
        family_name="TestSwapIndex",
        tenor=ql.Period("10Y"),
        settlement_days=2,
        currency=qCurrency.__wrapped__("EUR"),
        calendar=qlCalendar("TARGET"),
        fixed_leg_tenor=ql.Period("1Y"),
        fixed_leg_convention=qBusinessDayConvention.__wrapped__("MODIFIEDFOLLOWING"),
        fixed_leg_day_counter=qlDayCounter("ACTUAL365FIXED"),
        ibor_index=index,
        discount_curve=curve,
    )

    nominals = [100.0, 100.0]

    leg = qlCmsZeroLeg(
        nominals,
        schedule,
        swap_index,
        payment_day_counter=qlDayCounter("ACTUAL365FIXED"),
    )

    assert len(leg) == 2
    assert qlCashFlowsStartDate(leg) == start
    assert qlCashFlowsMaturityDate(leg) == end

    leg = qlCmsZeroLeg(
        nominals,
        schedule,
        swap_index,
        payment_day_counter=qlDayCounter("ACTUAL365FIXED"),
        payment_convention=qBusinessDayConvention.__wrapped__("FOLLOWING"),
        fixing_days=(2,),
        gearings=[1.0, 1.0],
        spreads=[0.001, 0.001],
        caps=[0.06, 0.06],
        floors=[0.01, 0.01],
        ex_coupon_period=ql.Period("1D"),
        ex_coupon_calendar=qlCalendar("TARGET"),
        ex_coupon_convention=qBusinessDayConvention.__wrapped__("UNADJUSTED"),
        ex_coupon_end_of_month=True,
    )

    assert len(leg) == 2
    assert qlCashFlowsStartDate(leg) == start
    assert qlCashFlowsMaturityDate(leg) == end


def test_qlCmsSpreadLeg_constructor():
    start = qlDate(2024, 1, 2)
    end = qlDate(2026, 1, 2)
    schedule = _schedule(start, end)
    curve = _curve(start, 0.03)
    index1 = qlEuribor(ql.Period("6M"), curve)
    index2 = qlEuribor(ql.Period("12M"), curve)
    swap_index1 = qlSwapIndex(
        family_name="TestSwapIndex1",
        tenor=ql.Period("10Y"),
        settlement_days=2,
        currency=qCurrency.__wrapped__("EUR"),
        calendar=qlCalendar("TARGET"),
        fixed_leg_tenor=ql.Period("1Y"),
        fixed_leg_convention=qBusinessDayConvention.__wrapped__("MODIFIEDFOLLOWING"),
        fixed_leg_day_counter=qlDayCounter("ACTUAL365FIXED"),
        ibor_index=index1,
        discount_curve=curve,
    )
    swap_index2 = qlSwapIndex(
        family_name="TestSwapIndex2",
        tenor=ql.Period("10Y"),
        settlement_days=2,
        currency=qCurrency.__wrapped__("EUR"),
        calendar=qlCalendar("TARGET"),
        fixed_leg_tenor=ql.Period("1Y"),
        fixed_leg_convention=qBusinessDayConvention.__wrapped__("MODIFIEDFOLLOWING"),
        fixed_leg_day_counter=qlDayCounter("ACTUAL365FIXED"),
        ibor_index=index2,
        discount_curve=curve,
    )
    spread_index = qlSwapSpreadIndex("TestSpreadIndex", swap_index1, swap_index2)

    nominals = [100.0, 100.0]

    leg = qlCmsSpreadLeg(
        nominals,
        schedule,
        spread_index,
        payment_day_counter=qlDayCounter("ACTUAL365FIXED"),
    )

    assert len(leg) == 2
    assert qlCashFlowsStartDate(leg) == start
    assert qlCashFlowsMaturityDate(leg) == end

    leg = qlCmsSpreadLeg(
        nominals,
        schedule,
        spread_index,
        payment_day_counter=qlDayCounter("ACTUAL365FIXED"),
        payment_convention=qBusinessDayConvention.__wrapped__("FOLLOWING"),
        fixing_days=(2,),
        gearings=[1.0, 1.0],
        spreads=[0.001, 0.001],
        caps=[0.06, 0.06],
        floors=[0.01, 0.01],
        is_in_arrears=False,
    )

    assert len(leg) == 2
    assert qlCashFlowsStartDate(leg) == start
    assert qlCashFlowsMaturityDate(leg) == end


def test_qlMultipleResetsLeg_constructor():
    start = qlDate(2024, 1, 2)
    end = qlDate(2026, 1, 2)
    full_reset_schedule = _schedule(start, end)
    curve = _curve(start, 0.03)
    index = qlEuribor(ql.Period("6M"), curve)

    nominals = [100.0]
    resets_per_coupon = 2

    leg = qlMultipleResetsLeg(
        full_reset_schedule,
        index,
        resets_per_coupon,
        nominals,
    )

    assert len(leg) > 0
    assert qlCashFlowsStartDate(leg) == start
    assert qlCashFlowsMaturityDate(leg) == end

    leg = qlMultipleResetsLeg(
        full_reset_schedule,
        index,
        resets_per_coupon,
        nominals,
        payment_day_counter=qlDayCounter("ACTUAL365FIXED"),
        payment_convention=qBusinessDayConvention.__wrapped__("FOLLOWING"),
        payment_calendar=qlCalendar("TARGET"),
        payment_lag=2,
        fixing_days=(2,),
        gearings=[1.0],
        coupon_spreads=[0.001],
        rate_spreads=[0.0005],
        ex_coupon_period=ql.Period("1D"),
        ex_coupon_calendar=qlCalendar("TARGET"),
        ex_coupon_convention=qBusinessDayConvention.__wrapped__("UNADJUSTED"),
        ex_coupon_end_of_month=True,
        averaging_method=qRateAveragingType.__wrapped__("COMPOUND"),
    )

    assert len(leg) > 0
    assert qlCashFlowsStartDate(leg) == start
    assert qlCashFlowsMaturityDate(leg) == end


def test_qlRangeAccrualLeg_constructor():
    start = qlDate(2024, 1, 2)
    end = qlDate(2026, 1, 2)
    schedule = _schedule(start, end)
    curve = _curve(start, 0.03)
    index = qlEuribor(ql.Period("6M"), curve)

    nominals = [100.0, 100.0]

    leg = qlRangeAccrualLeg(
        nominals,
        schedule,
        index,
        payment_day_counter=qlDayCounter("ACTUAL365FIXED"),
        payment_convention=qBusinessDayConvention.__wrapped__("FOLLOWING"),
        fixing_days=(2,),
        gearings=[1.0, 1.0],
        spreads=[0.001, 0.001],
        lower_triggers=[0.01, 0.01],
        upper_triggers=[0.06, 0.06],
        observation_tenor=ql.Period("1D"),
        observation_convention=qBusinessDayConvention.__wrapped__("MODIFIEDFOLLOWING"),
    )

    assert len(leg) > 0
