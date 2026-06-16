# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run Flask web app (development)
python app.py

# Run Flask with gunicorn (production)
gunicorn -w 2 -b 127.0.0.1:5000 app:app

# Run CLI comparator (auto-detects files in data/)
python main.py

# Run CLI with explicit paths
python main.py ruta/aulica.xlsx ruta/control.xlsx

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/test_comparator.py -v

# Run a single test class
pytest tests/test_comparator.py::TestDifferences -v
```

## Architecture

There are two entry points that share the same core pipeline:

- **`app.py`** — Flask web app: receives file uploads via POST `/compare`, runs the pipeline, returns JSON with summary stats and a `report_id` for download via GET `/download/<report_id>`.
- **`main.py`** — CLI: auto-detects files in `data/` (by searching for "AULICA"/"CONTROL" in filename) or accepts explicit paths as argv.

Both delegate to **`compare.py:run()`**, which orchestrates three steps:

1. **`src/reader.py`** — reads and normalizes both Excel files into DataFrames with canonical column names (`Legajo`, `Monto`, `Alumno`, `Total`, etc.).
2. **`src/comparator.py`** — groups Áulica coupons by `Legajo`, outer-merges with Control on `Legajo`, computes `Diferencia = Monto_Aulica - Total`, and returns two DataFrames: `differences` (abs diff > tolerance) and `control_only` (in Control but no coupons in Áulica).
3. **`src/writer.py`** — writes a styled Excel report with two sheets: **Diferencias** and **Solo en Control**. The output filename gets a timestamp suffix appended automatically.

## Configuration

`config/settings.py` must be updated each billing cycle:

```python
MONTH = "ABRIL"   # uppercase Spanish month name
YEAR  = 2026
```

`CONTROL_SHEET` and `CUOTA_COLUMN` are derived from these values automatically. `TOLERANCE = 1.0` means differences ≤ $1.00 are ignored.

## Input file format

- **Áulica**: sheet index 0, header on row 1 (row 0 is skipped), columns assigned as `["Legajo", "Alumno", "Nro_Cupon", "Fecha_Debito", "Monto"]` positionally.
- **Control**: sheet named `"{MONTH} {YEAR}"`, reads columns `["ALUMNO", "COD ÁULICA", "CUOTA \n{MONTH}", "TOTAL"]` by name.

If a `KeyError` is thrown on `read_control`, it almost always means `MONTH`/`YEAR` in `config/settings.py` doesn't match the actual sheet name or column header in the Control file.

## Deployment

See `deploy.md` for the full VPS setup (gunicorn + nginx + systemd + Let's Encrypt). Report files in `output/` accumulate; a cron job deletes files older than 1 hour in production.

## Workflow

Tasks live in `docs/tasks/<name>.md`. These files are the original request and must NEVER be moved or modified — they're the source of truth for what was asked.

When you finish a task, create a NEW file at `docs/completed/<name>.md` with: a short summary of what you did, the files you touched, and any relevant technical decisions.

Do ONLY what the task file asks. Do not explore the codebase unprompted, do not refactor adjacent code, do not search for "improvements" beyond the scope. If something seems off-scope, ask before acting.