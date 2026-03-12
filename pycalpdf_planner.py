"""
Planner PDF: month/year title, day list with weekend styling, three square columns,
Weekly area, Monthly Goals, and a small month calendar at bottom right.
"""
from datetime import datetime
from fpdf import FPDF
import calendar

# --- Config ---
YEAR = 2026
MONTH = 3
MARGIN = 10
ROW_H = 5.5
DAY_COL_W = 10
THREE_COL_W = ROW_H * 3  # each square = ROW_H x ROW_H
THICK = 0.6
NORMAL_LW = 0.2

# Page
PAGE_W = 210
PAGE_H = 297
RIGHT_EDGE = PAGE_W - MARGIN

# Table bounds
TABLE_X = MARGIN
TABLE_Y0 = 22
THREE_COL_X = TABLE_X + DAY_COL_W
WEEKLY_COL_X = THREE_COL_X + THREE_COL_W
WEEKLY_COL_W = RIGHT_EDGE - WEEKLY_COL_X

# Small calendar (bottom right)
CAL_W = 35
CAL_H = 25
CAL_X = RIGHT_EDGE - CAL_W
CAL_Y = PAGE_H - MARGIN - CAL_H

# Bottom section Y is TABLE_Y0 + last_day * ROW_H + 4


def weekday_for_day(year: int, month: int, day: int) -> int:
    """0=Mon .. 6=Sun."""
    return datetime(year, month, day).weekday()


def is_weekend(year: int, month: int, day: int) -> bool:
    w = weekday_for_day(year, month, day)
    return w == 5 or w == 6  # Sat, Sun


def is_saturday(year: int, month: int, day: int) -> bool:
    return weekday_for_day(year, month, day) == 5


def draw_small_calendar(pdf: FPDF, year: int, month: int, x0: float, y0: float, cw: float, ch: float):
    """Draw the month grid at (x0, y0) with cell size (cw, ch). Sunday on the left."""
    calendar.setfirstweekday(calendar.SUNDAY)
    cal = calendar.monthcalendar(year, month)
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    pdf.set_font("Helvetica", size=6)
    pdf.set_line_width(NORMAL_LW)

    # Header
    cur_x, cur_y = x0, y0
    for d in days:
        pdf.set_xy(cur_x, cur_y)
        pdf.cell(cw, ch * 0.6, d, border=1, align="C")
        cur_x += cw
    cur_y += ch * 0.6
    cur_x = x0

    # Weeks
    for week in cal:
        cur_x = x0
        for day in week:
            day_str = str(day) if day != 0 else "\u00A0"
            pdf.set_xy(cur_x, cur_y)
            pdf.cell(cw, ch, day_str, border=1, align="C")
            cur_x += cw
        cur_y += ch

    pdf.set_font("Helvetica", size=12)


def main():
    last_day = calendar.monthrange(YEAR, MONTH)[1]
    month_name = calendar.month_name[MONTH]
    goals_y = TABLE_Y0 + last_day * ROW_H + 4

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(False)

    # --- Title: Month, Year (bold, underlined) top left ---
    pdf.set_font("Helvetica", "B", size=14)
    pdf.set_xy(TABLE_X, MARGIN)
    pdf.set_line_width(NORMAL_LW)
    pdf.cell(80, 10, txt=f"{month_name}, {YEAR}", border=0, align="L", ln=False)
    pdf.set_font("Helvetica", size=14)
    # underline (manual)
    uy = MARGIN + 10
    pdf.line(TABLE_X, uy, TABLE_X + 50, uy)
    pdf.set_font("Helvetica", size=10)

    # --- "Weekly" header above the right (three columns + weekly area) ---
    pdf.set_xy(THREE_COL_X, TABLE_Y0 - 8)
    pdf.set_font("Helvetica", "B", size=10)
    pdf.cell(THREE_COL_W + WEEKLY_COL_W, 6, "Weekly", border=0, align="L")
    pdf.set_font("Helvetica", size=10)

    # --- Main table: day number column + three square columns + weekly column ---
    pdf.set_line_width(NORMAL_LW)
    for day in range(1, last_day + 1):
        row_y = TABLE_Y0 + (day - 1) * ROW_H
        weekend = is_weekend(YEAR, MONTH, day)
        sat = is_saturday(YEAR, MONTH, day)

        # Day number cell (left column)
        pdf.set_xy(TABLE_X, row_y)
        day_x, day_y = pdf.get_x(), pdf.get_y()
        pdf.cell(DAY_COL_W, ROW_H, str(day), border=1, align="C")
        if weekend:
            pdf.set_line_width(THICK)
            pdf.rect(day_x, day_y, DAY_COL_W, ROW_H)
            pdf.set_line_width(NORMAL_LW)

        # Thick horizontal line between Saturday and Sunday (below Saturday row)
        if sat:
            pdf.set_line_width(THICK)
            line_y = row_y + ROW_H
            pdf.line(TABLE_X, line_y, RIGHT_EDGE, line_y)
            pdf.set_line_width(NORMAL_LW)

        # Three square columns (thick left and right of the group)
        pdf.set_xy(THREE_COL_X, row_y)
        for i in range(3):
            bx = THREE_COL_X + i * ROW_H
            pdf.set_xy(bx, row_y)
            pdf.cell(ROW_H, ROW_H, "", border=1, align="C")
        # Thick left and right borders for the group
        pdf.set_line_width(THICK)
        pdf.line(THREE_COL_X, row_y, THREE_COL_X, row_y + ROW_H)
        pdf.line(WEEKLY_COL_X, row_y, WEEKLY_COL_X, row_y + ROW_H)
        pdf.set_line_width(NORMAL_LW)

        # Weekly column (right of the three)
        pdf.set_xy(WEEKLY_COL_X, row_y)
        pdf.cell(WEEKLY_COL_W, ROW_H, "", border=1, align="L")

    # --- Bottom: "Monthly Goals" left, small calendar right ---
    pdf.set_font("Helvetica", "B", size=10)
    pdf.set_xy(TABLE_X, goals_y)
    pdf.cell(80, 8, "Monthly Goals", border=0, align="L")
    pdf.set_font("Helvetica", size=10)

    # Small calendar at bottom right
    cw = CAL_W / 7
    ch = (CAL_H - 4) / 6  # ~1 row header + 5 weeks
    if ch > cw:
        ch = cw
    draw_small_calendar(pdf, YEAR, MONTH, CAL_X, CAL_Y, cw, ch)

    pdf.output("planner.pdf")
    print("Wrote planner.pdf")


if __name__ == "__main__":
    main()
