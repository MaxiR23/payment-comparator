# INFO: aplicación Flask para comparar archivos de Aulica vs Control y generar reportes Excel
import os
import uuid
import logging
from pathlib import Path

from flask import Flask, render_template, request, send_file, jsonify

# ajusta sys.path para que los módulos en src/ se resuelvan correctamente
import sys
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import MONTH, YEAR, TOLERANCE, CUOTA_COLUMN, CONTROL_SHEET
from src.reader import read_aulica, read_control
from src.comparator import compare
from src.writer import write_report

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024  # tamaño máximo de subida 20 MB

UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("output")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

@app.route("/")
def index():
    # renderiza la página principal con valores por defecto
    return render_template("index.html", default_month=MONTH, default_year=YEAR, default_tol=TOLERANCE)

@app.route("/compare", methods=["POST"])
def run_compare():
    # procesa la comparación entre archivos Aulica y Control
    aulica_file = request.files.get("aulica")
    control_file = request.files.get("control")
    month = request.form.get("month", MONTH).upper()
    year = int(request.form.get("year", YEAR))
    tolerance = float(request.form.get("tolerance", TOLERANCE))

    if not aulica_file or not control_file:
        return jsonify(error="Faltan archivos."), 400

    # guarda archivos con nombres únicos para evitar colisiones
    uid = uuid.uuid4().hex[:8]
    aulica_path = UPLOAD_DIR / f"{uid}_aulica.xlsx"
    control_path = UPLOAD_DIR / f"{uid}_control.xlsx"
    aulica_file.save(aulica_path)
    control_file.save(control_path)

    try:
        # construye nombres de hoja y columna según mes/año
        sheet = f"{month} {year}"
        cuota_col = f"CUOTA \n{month}"

        # lee y procesa los archivos
        aulica_df = read_aulica(str(aulica_path))
        control_df = read_control(str(control_path), sheet=sheet, cuota_column=cuota_col)
        diffs, ctrl_only = compare(aulica_df, control_df, tolerance=tolerance)

        # genera el reporte de salida
        output_path = OUTPUT_DIR / f"{uid}_Diferencias.xlsx"
        write_report(diffs, ctrl_only, aulica_df, str(output_path))

        return jsonify(
            ok=True,
            report_id=uid,
            n_diffs=len(diffs),
            n_ctrl_only=len(ctrl_only),
            total_diff=round(float(diffs["Diferencia"].sum()), 2),
        )

    except Exception as e:
        logger.exception("Comparison failed")
        return jsonify(error=str(e)), 500

    finally:
        # limpia los archivos subidos
        aulica_path.unlink(missing_ok=True)
        control_path.unlink(missing_ok=True)

@app.route("/download/<report_id>")
def download(report_id):
    # valida el ID del reporte (solo caracteres alfanuméricos)
    if not report_id.isalnum() or len(report_id) != 8:
        return "ID inválido", 400
    
    # busca el archivo por uid sin importar el timestamp
    matches = list(OUTPUT_DIR.glob(f"{report_id}_Diferencias_*.xlsx"))
    if not matches:
        return "Reporte no encontrado.", 404
    
    path = matches[0]
    return send_file(path, as_attachment=True, download_name=path.name)

@app.route("/clear", methods=["POST"])
def clear_files():
    # elimina todos los archivos de uploads y output
    try:
        for f in UPLOAD_DIR.glob("*"):
            f.unlink(missing_ok=True)

        for f in OUTPUT_DIR.glob("*"):
            f.unlink(missing_ok=True)

        return jsonify(ok=True)
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    # inicia la aplicación Flask
    app.run(host="0.0.0.0", port=8080, debug=False)