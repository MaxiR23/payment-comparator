# INFO: orquesta el flujo completo de comparación: leer -> comparar -> escribir.
from pathlib import Path
from src.reader import read_aulica, read_control
from src.comparator import compare
from src.writer import write_report
from config.settings import CONTROL_SHEET, CUOTA_COLUMN, TOLERANCE, OUTPUT_FILE

def run(path_aulica: str, path_control: str, output_dir: Path = Path(".")) -> None:
    """Run the full comparison pipeline."""
    aulica = read_aulica(path_aulica)
    control = read_control(path_control, sheet=CONTROL_SHEET, cuota_column=CUOTA_COLUMN)
    diffs, control_only = compare(aulica, control, tolerance=TOLERANCE)
    output_path = output_dir / OUTPUT_FILE
    write_report(diffs, control_only, aulica, str(output_path))