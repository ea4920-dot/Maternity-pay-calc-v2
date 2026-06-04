import calendar
from datetime import datetime

from constants import (
    DEFAULT_COLOUR,
    FULL_PAY_COLOUR,
    SMP_COLOUR,
    UNPAID_COLOUR,
)


def render_month(year, month, timeline):
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]

    html = (
        f"<div style='border:1px solid #333;"
        f"padding:10px;"
        f"border-radius:8px;"
        f"background:#111827;'>"
        f"<h4 style='text-align:center;'>"
        f"{month_name} {year}"
        f"</h4>"
        f"<table style='width:100%;"
        f"text-align:center;"
        f"font-size:12px;"
        f"border-collapse:collapse;'>"
        f"<tr>"
        f"<th>M</th>"
        f"<th>T</th>"
        f"<th>W</th>"
        f"<th>T</th>"
        f"<th>F</th>"
        f"<th>S</th>"
        f"<th>S</th>"
        f"</tr>"
    )

    for week in cal:
        html += "<tr>"

        for day in week:
            if day == 0:
                html += "<td></td>"
                continue

            current_date = datetime(
                year,
                month,
                day
            ).date()

            colour = DEFAULT_COLOUR

            if (
                timeline["full_pay_start"]
                <= current_date
                <= timeline["full_pay_end"]
            ):
                colour = FULL_PAY_COLOUR

            elif (
                timeline["smp_start"]
                <= current_date
                <= timeline["smp_end"]
            ):
                colour = SMP_COLOUR

            elif (
                timeline["unpaid_start"]
                <= current_date
                <= timeline["unpaid_end"]
            ):
                colour = UNPAID_COLOUR

            html += (
                f"<td style='"
                f"background:{colour};"
                f"padding:4px;"
                f"border:1px solid #222;'>"
                f"{day}"
                f"</td>"
            )

        html += "</tr>"

    html += "</table></div>"

    return html