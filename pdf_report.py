from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)

from reportlab.lib import colors

from reportlab.lib.styles import getSampleStyleSheet

from constants import DATE_FORMAT

def build_table(data):
    table = Table(data)

    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1),
                 [colors.whitesmoke, colors.lightgrey]),
            ]
        )
    )

    return table


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

    content.append(
        Paragraph(
            "Oxford University Maternity Pay Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"Generated: {return_date.strftime(DATE_FORMAT)}",
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Key Dates",
            styles["Heading2"]
        )
    )

    content.append(
        build_table(
            [
                ["Item", "Date"],
                [
                    "Employment Start",
                    employment_start_date.strftime(
                        DATE_FORMAT
                    )
                ],
                [
                    "Expected Due Date",
                    due_date.strftime(
                        DATE_FORMAT
                    )
                ],
                [
                    "Maternity Leave Start",
                    leave_start.strftime(
                        DATE_FORMAT
                    )
                ],
                [
                    "Expected Return",
                    return_date.strftime(
                        DATE_FORMAT
                    )
                ]
            ]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Eligibility",
            styles["Heading2"]
        )
    )

    content.append(
        build_table(
            [
                ["Scheme", "Status"],
                [
                    "Oxford Enhanced Scheme",
                    "Eligible"
                    if oxford_eligible
                    else "Not Eligible"
                ],
                [
                    "SMP",
                    "Eligible"
                    if smp_eligible
                    else "Not Eligible"
                ]
            ]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Pay Summary",
            styles["Heading2"]
        )
    )

    content.append(
        build_table(
            [
                ["Item", "Amount"],
                [
                    "Weekly Salary",
                    f"£{results['weekly_salary']:,.2f}"
                ],
                [
                    "Full Pay Total",
                    f"£{results['full_pay_total']:,.2f}"
                ],
                [
                    "SMP Total",
                    f"£{results['smp_total']:,.2f}"
                ],
                [
                    "Total Pay",                    f"£{results['total_pay']:,.2f}"
                ]
            ]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Leave Periods",
            styles["Heading2"]
        )
    )

    content.append(
        build_table(
            [
                [
                    "Period",
                    "Start",
                    "End"
                ],
                [
                    "Full Pay",
                    timeline["full_pay_start"].strftime(
                        DATE_FORMAT
                    ),
                    timeline["full_pay_end"].strftime(
                        DATE_FORMAT
                    )
                ],
                [
                    "SMP",
                    timeline["smp_start"].strftime(
                        DATE_FORMAT
                    ),
                    timeline["smp_end"].strftime(
                        DATE_FORMAT
                        )
                ],
                [
                    "Unpaid Leave",
                    timeline["unpaid_start"].strftime(
                        DATE_FORMAT
                    ),
                    timeline["unpaid_end"].strftime(
                        DATE_FORMAT
                    )
                ]
            ]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Qualifying Week",
            styles["Heading2"]
        )
    )

    content.append(
        build_table(
            [
                [
                    "Start",
                    "End"
                ],
                [
                    qualifying["qualifying_start"].strftime(
                        DATE_FORMAT
                    ),
                    qualifying["qualifying_end"].strftime(
                        DATE_FORMAT
                    )
                ]
            ]
        )
    )

    doc.build(content)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf