from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from constants import DATE_FORMAT


def generate_pdf_report(
    employment_start_date,
    due_date,
    leave_start,
    return_date,
    results,
    timeline,
    qualifying,
    oxford_eligible,
    smp_eligible
):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    content = []

    def add_text(text):
        content.append(
            Paragraph(
                text,
                styles["BodyText"]
            )
        )

    content.append(
        Paragraph(
            "Oxford University Maternity Pay Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    add_text(
        f"Employment Start Date: "
        f"{employment_start_date.strftime(DATE_FORMAT)}"
    )

    add_text(
        f"Expected Due Date: "
        f"{due_date.strftime(DATE_FORMAT)}"
    )

    add_text(
        f"Maternity Leave Start Date: "
        f"{leave_start.strftime(DATE_FORMAT)}"
    )

    add_text(
        f"Expected Return Date: "
        f"{return_date.strftime(DATE_FORMAT)}"
    )

    content.append(Spacer(1, 12))

    add_text(
        f"Oxford Enhanced Scheme: "
        f"{'Eligible' if oxford_eligible else 'Not Eligible'}"
    )

    add_text(
        f"SMP Eligibility: "
        f"{'Eligible' if smp_eligible else 'Not Eligible'}"
    )

    content.append(Spacer(1, 12))

    add_text(
        f"Weekly Salary: "
        f"£{results['weekly_salary']:,.2f}"
    )

    add_text(
        f"Estimated Total Pay: "
        f"£{results['total_pay']:,.2f}"
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Leave Periods",
            styles["Heading2"]
        )
    )

    add_text(
        f"Full Pay: "
        f"{timeline['full_pay_start'].strftime(DATE_FORMAT)} "
        f"to "
        f"{timeline['full_pay_end'].strftime(DATE_FORMAT)}"
    )

    add_text(
        f"SMP: "
        f"{timeline['smp_start'].strftime(DATE_FORMAT)} "
        f"to "
        f"{timeline['smp_end'].strftime(DATE_FORMAT)}"
    )

    add_text(
        f"Unpaid Leave: "
        f"{timeline['unpaid_start'].strftime(DATE_FORMAT)} "
        f"to "
        f"{timeline['unpaid_end'].strftime(DATE_FORMAT)}"
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Qualifying Week",
            styles["Heading2"]
        )
    )

    add_text(
        f"{qualifying['qualifying_start'].strftime(DATE_FORMAT)} "
        f"to "
        f"{qualifying['qualifying_end'].strftime(DATE_FORMAT)}"
    )

    doc.build(content)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf