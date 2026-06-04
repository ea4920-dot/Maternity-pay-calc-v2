from datetime import timedelta, date

from constants import SMP_RATE


def weekly_salary(annual_salary, fte=1.0):
    return (annual_salary * fte) / 52


def calculate_return_date(leave_start):
    return leave_start + timedelta(weeks=52)


def calculate_pay_schedule(annual_salary, fte=1.0):
    weekly_pay = weekly_salary(
        annual_salary,
        fte
    )

    full_pay_total = weekly_pay * 26
    smp_total = SMP_RATE * 13

    total_pay = (
        full_pay_total +
        smp_total
    )

    return {
        "weekly_salary": round(weekly_pay, 2),
        "full_pay_total": round(full_pay_total, 2),
        "smp_total": round(smp_total, 2),
        "total_pay": round(total_pay, 2)
    }


def calculate_qualifying_week(due_date):
    days_since_sunday = (
        due_date.weekday() + 1
    ) % 7

    ewc_start = due_date - timedelta(
        days=days_since_sunday
    )

    qualifying_start = ewc_start - timedelta(
        weeks=15
    )

    qualifying_end = qualifying_start + timedelta(
        days=6
    )

    return {
        "ewc_start": ewc_start,
        "qualifying_start": qualifying_start,
        "qualifying_end": qualifying_end
    }


def qualifies_for_smp(
    employment_start_date,
    due_date
):
    qualifying = calculate_qualifying_week(
        due_date
    )

    service_days = (
        qualifying["qualifying_end"]
        - employment_start_date
    ).days

    service_weeks = service_days / 7

    return service_weeks >= 26


def qualifies_for_oxford_scheme(
    employment_start_date,
    due_date,
    intends_to_return
):
    if employment_start_date > due_date:
        return False

    if not intends_to_return:
        return False

    return True


def calculate_maternity_timeline(
    leave_start
):
    
    full_pay_end = (
        leave_start +
        timedelta(weeks=26) -
        timedelta(days=1)
    )

    smp_start = (
        full_pay_end +
        timedelta(days=1)
    )

    smp_end = (
        smp_start +
        timedelta(weeks=13) -
        timedelta(days=1)
    )

    unpaid_start = (
        smp_end +
        timedelta(days=1)
    )

    return_date = (
        leave_start +
        timedelta(weeks=52)
    )

    unpaid_end = (
        return_date -
        timedelta(days=1)
    )

    return {
        "full_pay_start": leave_start,
        "full_pay_end": full_pay_end,
        "smp_start": smp_start,
        "smp_end": smp_end,
        "unpaid_start": unpaid_start,
        "unpaid_end": unpaid_end,
        "return_date": return_date
    }

def calculate_leave_accrual(
    leave_start,
    return_date,
    annual_entitlement,
    current_balance_days
):
    """
    Calculates annual leave accrued during maternity leave.

    Oxford leave year:
    1 October -> 30 September
    """

    total_leave_days = (
        return_date - leave_start
    ).days

    accrual_rate = (
        annual_entitlement / 365
    )

    accrued_leave = round(
        total_leave_days * accrual_rate,
        1
    )

    return {
        "current_balance": round(
            current_balance_days,
            1
        ),
        "accrued_leave": accrued_leave,
        "total_available": round(
            current_balance_days + accrued_leave,
            1
        )
    }

from datetime import date


def calculate_leave_available_on_return(
    return_date,
    annual_entitlement,
    current_balance_days
):
    if return_date.month >= 10:
        leave_year_start = date(
            return_date.year,
            10,
            1
        )
    else:
        leave_year_start = date(
            return_date.year - 1,
            10,
            1
        )

    days_since_october = (
        return_date - leave_year_start
    ).days

    daily_accrual_rate = (
        annual_entitlement / 365
    )

    accrued_since_october = round(
        days_since_october *
        daily_accrual_rate,
        1
    )

    available_on_return = round(
        current_balance_days +
        accrued_since_october,
        1
    )

    return {
        "leave_year_start": leave_year_start,
        "days_since_october": days_since_october,
        "accrued_since_october": accrued_since_october,
        "available_on_return": available_on_return
    }