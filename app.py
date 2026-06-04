import streamlit as st

from constants import (
    APP_TITLE,
    APP_VERSION,
    DATE_FORMAT
)

from calculations import (
    calculate_pay_schedule,
    calculate_return_date,
    calculate_qualifying_week,
    qualifies_for_smp,
    qualifies_for_oxford_scheme,
    calculate_maternity_timeline,
    calculate_leave_accrual,
    calculate_leave_available_on_return
)

from calendar_view import render_month
from pdf_report import generate_pdf_report


def fmt(date_value):
    return date_value.strftime(DATE_FORMAT)


st.set_page_config(
    page_title=APP_TITLE,
    layout="wide"
)

st.title(APP_TITLE)
st.caption(APP_VERSION)

st.info(
    """
    This calculator provides an estimate only.

    Please confirm maternity leave and pay entitlements
    with Oxford University HR and Payroll.

    This tool is not an official University system.
    """
)

with st.expander(
    "Employee Details",
    expanded=True
):

    annual_salary = st.number_input(
        "Annual Salary (£)",
        min_value=0.0,
        value=45000.0,
        step=1000.0
    )

    fte = st.number_input(
        "FTE",
        min_value=0.1,
        max_value=1.0,
        value=1.0,
        step=0.1
    )

    annual_leave_entitlement = st.number_input(
        "Full-Time Annual Leave Entitlement (Days)",
        min_value=0.0,
        value=38.0,
        step=0.5
    )

    current_leave_balance = st.number_input(
        "Current Leave Balance",
        min_value=0.0,
        value=0.0,
        step=0.5
    )

    leave_unit = st.selectbox(
        "Leave Balance Unit",
        [
            "Days",
            "Hours"
        ]
    )

    hours_per_day = st.number_input(
        "Hours Per Day",
        min_value=1.0,
        value=7.4,
        step=0.1
    )

    employment_start_date = st.date_input(
        "Employment Start Date"
    )

    due_date = st.date_input(
        "Expected Due Date"
    )

    leave_start = st.date_input(
        "Maternity Leave Start Date"
    )

    pdf_filename = st.text_input(
        "Employee Name for PDF",
        value=""
    )

    intends_to_return = st.checkbox(
        "I intend to return to work",
        value=True
    )

calculate = st.button(
    "Calculate",
    type="primary",
    width="stretch"
)

if calculate:

    if leave_start < employment_start_date:
        st.error(
            "Maternity leave start date cannot be before employment start date."
        )
        st.stop()

    current_balance_days = (
        current_leave_balance / hours_per_day
        if leave_unit == "Hours"
        else current_leave_balance
    )

    actual_entitlement = (
        annual_leave_entitlement * fte
    )

    results = calculate_pay_schedule(
        annual_salary=annual_salary,
        fte=fte
    )

    qualifying = calculate_qualifying_week(
        due_date
    )

    return_date = calculate_return_date(
        leave_start
    )

    leave_summary = calculate_leave_accrual(
    leave_start=leave_start,
    return_date=return_date,
    annual_entitlement=actual_entitlement,
    current_balance_days=current_balance_days
)

    accrued_during_leave = (
        leave_summary["accrued_leave"]
)

    total_leave_days = (
        leave_summary["total_available"]
)
    
    available_leave = (
        calculate_leave_available_on_return(
            return_date=return_date,
            annual_entitlement=actual_entitlement,
            current_balance_days=current_balance_days
    )
)

    timeline = calculate_maternity_timeline(
        leave_start
    )

    smp_eligible = qualifies_for_smp(
        employment_start_date,
        due_date
    )

    oxford_eligible = qualifies_for_oxford_scheme(
        employment_start_date,
        due_date,
        intends_to_return
    )

    pdf_data = generate_pdf_report(
        employment_start_date,
        due_date,
        leave_start,
        return_date,
        results,
        timeline,
        qualifying,
        oxford_eligible,
        smp_eligible
    )

    filename = (
        f"{pdf_filename}_Maternity_Report.pdf"
        if pdf_filename
        else "Oxford_Maternity_Report.pdf"
    )

    st.divider()

    card1, card2, card3, card4, card5 = st.columns(5)

    with card1:

        with st.container(border=True):

            st.subheader("📅 Key Dates")

            st.write(
                f"Start: {fmt(employment_start_date)}"
            )

            st.write(
                f"Due: {fmt(due_date)}"
            )

            st.write(
                f"Leave: {fmt(leave_start)}"
            )

            st.write(
                f"Return: {fmt(return_date)}"
            )

    with card2:

        with st.container(border=True):

            st.subheader("✅ Eligibility")

            if oxford_eligible:
                st.success(
                    "Oxford Scheme Eligible"
                )
            else:
                st.error(
                    "Oxford Scheme Not Eligible"
                )

            if smp_eligible:
                st.success(
                    "SMP Eligible"
                )
            else:
                st.error(
                    "SMP Not Eligible"
                )

    with card3:

        with st.container(border=True):

            st.subheader("💷 Pay Summary")

            st.metric(
                "Weekly Salary",
                f"£{results['weekly_salary']:,.2f}"
            )

            st.metric(
                "Total Pay",
                f"£{results['total_pay']:,.2f}"
            )

    with card4:

        with st.container(border=True):

            st.subheader("🕒 Qualifying Week")

            st.write(
                fmt(
                    qualifying["qualifying_start"]
                )
            )

            st.write("to")

            st.write(
                fmt(
                    qualifying["qualifying_end"]
                )
            )

    with card5:

        with st.container(border=True):

            st.subheader("🏖 Leave Summary")

            st.write(
                f"Current Balance: "
                f"{current_leave_balance:,.1f} "
                f"{leave_unit}"
            )

            st.write(
                f"Annual Entitlement: "
                f"{actual_entitlement:,.1f} days"
            )

            st.write(
                f"Accrued During Leave: "
                f"{accrued_during_leave:,.1f} days"
)

            st.write(
                f"Accrued Since Leave Year Start: "
                f"{available_leave['accrued_since_october']:,.1f} days"
)

            st.metric(
                "Available On Return",
                f"{available_leave['available_on_return']:,.1f} days"
)

    st.divider()

    st.subheader(
        "Leave Period Details"
    )

    st.dataframe(
        {
            "Period": [
                "Full Pay",
                "SMP",
                "Unpaid Leave"
            ],
            "Start Date": [
                fmt(
                    timeline["full_pay_start"]
                ),
                fmt(
                    timeline["smp_start"]
                ),
                fmt(
                    timeline["unpaid_start"]
                )
            ],
            "End Date": [
                fmt(
                    timeline["full_pay_end"]
                ),
                fmt(
                    timeline["smp_end"]
                ),
                fmt(
                    timeline["unpaid_end"]
                )
            ]
        },
        width="stretch"
    )

    st.subheader(
        "Maternity Leave Calendar"
    )

    st.markdown(
        """
        🟩 Full Pay &nbsp;&nbsp;&nbsp;
        🟧 SMP &nbsp;&nbsp;&nbsp;
        🟥 Unpaid Leave
        """,
        unsafe_allow_html=True
    )

    start_year = leave_start.year
    start_month = leave_start.month

    months = [
        (
            start_year +
            ((start_month - 1 + i) // 12),

            ((start_month - 1 + i) % 12) + 1
        )
        for i in range(13)
    ]

    for row in range(5):

        cols = st.columns(4)

        for col in range(4):

            idx = (
                row * 4 +
                col
            )

            if idx >= len(months):
                continue

            year, month = months[idx]

            with cols[col]:

                st.markdown(
                    render_month(
                        year,
                        month,
                        timeline
                    ),
                    unsafe_allow_html=True
                )

    st.divider()

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_data,
        file_name=filename,
        mime="application/pdf",
        width="stretch"
    )