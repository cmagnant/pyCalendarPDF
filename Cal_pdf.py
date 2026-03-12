from fpdf import FPDF
import calendar

# 1. Generate calendar data (weeks Sun–Sat so one row = one week)
year = 2026
month = 3
calendar.setfirstweekday(calendar.SUNDAY)
cal = calendar.monthcalendar(year, month)
month_name = calendar.month_name[month]

# 2. Create PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", size=16)

# Title
pdf.cell(200, 10, txt=f"{month_name} {year}", ln=True, align='C')
pdf.set_font("Courier", size=12)

# Header (Sunday on the left)
days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
for day in days:
    pdf.cell(25, 10, day, border=1, align='C')
pdf.ln()

# Calendar Days (week is already Sun..Sat)
for week in cal:
    for day in week:
        day_str = str(day) if day != 0 else "\u00A0"
        pdf.cell(25, 10, day_str, border=1, align='C')
    pdf.ln()

# 3. Save
pdf.output("calendar.pdf")