# Calendar PDF

Python scripts that generate PDF calendars using [FPDF](https://pyfpdf.readthedocs.io/).

## Setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Month and year

**Set the month and year at the top of each script** before running:

- **`Cal_pdf.py`** — near the top: `year = 2026` and `month = 3` (1–12).
- **`pycalpdf_planner.py`** — in the config block: `YEAR = 2026` and `MONTH = 3`.

## Scripts

### Cal_pdf.py

Generates a single-page month grid:

- Title: month and year (e.g. *March 2026*).
- Week starts on **Sunday** (left column); one row per week.
- Output: `calendar.pdf`.

```bash
python Cal_pdf.py
```

### pycalpdf_planner.py

Generates a planner-style page for the chosen month:

- **Top left:** Month and year (bold, underlined).
- **Left column:** Day numbers 1 through last day of the month (one per row); weekend days (Sat/Sun) have thicker borders and a thicker rule between Saturday and Sunday.
- **Middle:** A blank column (~45% page width), then three square columns with thicker left/right borders.
- **Top right:** “Weekly” header.
- **Right:** Weekly column for each day row.
- **Bottom:** “Monthly Goals” on the left; a small month calendar (same style as `Cal_pdf.py`) on the bottom right.

Output: `Planner_YYYY-MM.pdf` (e.g. `Planner_2026-04.pdf` for April).

```bash
python pycalpdf_planner.py
```

## Requirements

- Python 3
- [fpdf](https://pypi.org/project/fpdf/) (see `requirements.txt`)
