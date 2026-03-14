"""
Planner PDF: month/year title, day list with weekend styling, three square columns,
Weekly area, Monthly Goals, and a small month calendar at bottom right.
"""
from datetime import datetime
from fpdf import FPDF
import calendar

# --- Config ---
YEAR = 2026
MONTH = 4
SCALE = 3.0  # Scale entire page content (e.g. 0.9 = 90%, 1.1 = 110%)
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
CONTENT_W = PAGE_W - 2 * MARGIN

# Table bounds: day numbers | blank (~45%) | three squares | weekly
TABLE_X = MARGIN
TABLE_Y0 = 22
BLANK_COL_W = CONTENT_W * 0.45
THREE_COL_X = TABLE_X + DAY_COL_W + BLANK_COL_W
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


def draw_small_calendar(
    pdf: FPDF, year: int, month: int, x0: float, y0: float, cw: float, ch: float,
    font_size: float = 6, line_width: float = 0.2
):
    """Draw the month grid at (x0, y0) with cell size (cw, ch). Sunday on the left."""
    calendar.setfirstweekday(calendar.SUNDAY)
    cal = calendar.monthcalendar(year, month)
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    pdf.set_font("Helvetica", size=font_size)
    pdf.set_line_width(line_width)

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

    pdf.set_font("Helvetica", size=round(12 * (font_size / 6)) if font_size else 12)


def main():
    last_day = calendar.monthrange(YEAR, MONTH)[1]
    month_name = calendar.month_name[MONTH]
    s = SCALE

    # Scaled page and layout (page size and all content scale with SCALE)
    s_page_w = PAGE_W * s
    s_page_h = PAGE_H * s
    s_margin = MARGIN * s
    s_row_h = ROW_H * s
    s_day_col_w = DAY_COL_W * s
    s_right_edge = s_page_w - s_margin
    s_content_w = s_page_w - 2 * s_margin
    s_blank_col_w = s_content_w * 0.45
    s_three_col_w = s_row_h * 3
    s_table_x = s_margin
    s_table_y0 = TABLE_Y0 * s
    s_three_col_x = s_table_x + s_day_col_w + s_blank_col_w
    s_weekly_col_x = s_three_col_x + s_three_col_w
    s_weekly_col_w = s_right_edge - s_weekly_col_x
    s_goals_y = s_table_y0 + last_day * s_row_h + 4 * s
    s_cal_w = CAL_W * s
    s_cal_h = CAL_H * s
    s_cal_x = s_right_edge - s_cal_w
    s_cal_y = s_page_h - s_margin - s_cal_h
    s_font_title = max(6, round(14 * s))
    s_font_body = max(5, round(10 * s))
    s_font_small = max(4, round(6 * s))
    s_thick = THICK * s
    s_normal_lw = NORMAL_LW * s

    pdf = FPDF(format=(s_page_w, s_page_h))
    pdf.add_page()
    pdf.set_auto_page_break(False)

    # --- Title: Month, Year (bold, underlined) top left ---
    pdf.set_font("Helvetica", "B", size=s_font_title)
    pdf.set_xy(s_table_x, s_margin)
    pdf.set_line_width(s_normal_lw)
    pdf.cell(80 * s, 10 * s, txt=f"{month_name}, {YEAR}", border=0, align="L", ln=False)
    pdf.set_font("Helvetica", size=s_font_title)
    uy = s_margin + 10 * s
    pdf.line(s_table_x, uy, s_table_x + 50 * s, uy)
    pdf.set_font("Helvetica", size=s_font_body)

    # --- "Weekly" header at top right of page ---
    pdf.set_font("Helvetica", "B", size=s_font_body)
    pdf.set_xy(s_right_edge - 25 * s, s_margin)
    pdf.cell(25 * s, 10 * s, "Weekly", border=0, align="R")
    pdf.set_font("Helvetica", size=s_font_body)

    # --- Main table: day number column + blank + three square columns + weekly column ---
    pdf.set_line_width(s_normal_lw)
    for day in range(1, last_day + 1):
        row_y = s_table_y0 + (day - 1) * s_row_h
        weekend = is_weekend(YEAR, MONTH, day)
        sat = is_saturday(YEAR, MONTH, day)

        # Day number cell (left column)
        pdf.set_xy(s_table_x, row_y)
        day_x, day_y = pdf.get_x(), pdf.get_y()
        pdf.cell(s_day_col_w, s_row_h, str(day), border=1, align="C")
        if weekend:
            pdf.set_line_width(s_thick)
            pdf.rect(day_x, day_y, s_day_col_w, s_row_h)
            pdf.set_line_width(s_normal_lw)

        # Blank column (~45% width) between numbers and three columns
        pdf.set_xy(s_table_x + s_day_col_w, row_y)
        pdf.cell(s_blank_col_w, s_row_h, "", border=1, align="L")

        # Thick horizontal line between Saturday and Sunday (below Saturday row)
        if sat:
            pdf.set_line_width(s_thick)
            line_y = row_y + s_row_h
            pdf.line(s_table_x, line_y, s_right_edge, line_y)
            pdf.set_line_width(s_normal_lw)

        # Three square columns (thick left and right of the group)
        pdf.set_xy(s_three_col_x, row_y)
        for i in range(3):
            bx = s_three_col_x + i * s_row_h
            pdf.set_xy(bx, row_y)
            pdf.cell(s_row_h, s_row_h, "", border=1, align="C")
        pdf.set_line_width(s_thick)
        pdf.line(s_three_col_x, row_y, s_three_col_x, row_y + s_row_h)
        pdf.line(s_weekly_col_x, row_y, s_weekly_col_x, row_y + s_row_h)
        pdf.set_line_width(s_normal_lw)

        # Weekly column (right of the three)
        pdf.set_xy(s_weekly_col_x, row_y)
        pdf.cell(s_weekly_col_w, s_row_h, "", border=1, align="L")

    # --- Bottom: "Monthly Goals" left, small calendar right ---
    pdf.set_font("Helvetica", "B", size=s_font_body)
    pdf.set_xy(s_table_x, s_goals_y)
    pdf.cell(80 * s, 8 * s, "Monthly Goals", border=0, align="L")
    pdf.set_font("Helvetica", size=s_font_body)

    # Small calendar at bottom right
    cw = s_cal_w / 7
    ch_cal = (s_cal_h - 4 * s) / 6
    if ch_cal > cw:
        ch_cal = cw
    draw_small_calendar(
        pdf, YEAR, MONTH, s_cal_x, s_cal_y, cw, ch_cal,
        font_size=s_font_small, line_width=s_normal_lw
    )

    out_name = f"Planner_{YEAR}-{MONTH:02d}.pdf"
    pdf.output(out_name)
    print(f"Wrote {out_name}")


if __name__ == "__main__":
    main()
