# INFO: punto de entrada para el comparador de pagos.
import logging
import sys
from pathlib import Path

from config.settings import DATA_DIR, OUTPUT_DIR
from compare import run

logger = logging.getLogger(__name__)

def _find_files(folder: Path):
    """Escanea la carpeta en busca de archivos Excel de Aulica y Control."""
    aulica_path = None
    control_path = None

    for f in folder.glob("*.xlsx"):
        name = f.name.upper()
        if "AULICA" in name or "ÁULICA" in name:
            aulica_path = f
        elif "CONTROL" in name:
            control_path = f

    return aulica_path, control_path

def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    logger.info("Comparador de cupones Áulica vs Control — buscando archivos...")

    output_folder = Path(OUTPUT_DIR)
    output_folder.mkdir(parents=True, exist_ok=True)

    try:
        if len(sys.argv) == 3:
            path_aulica = sys.argv[1]
            path_control = sys.argv[2]
        else:
            folder = Path(DATA_DIR)
            if not folder.exists():
                folder.mkdir(parents=True)
                logger.error("Carpeta '%s' creada. Colocá los archivos ahí y volvé a ejecutar.", DATA_DIR)
                sys.exit(1)

            path_aulica, path_control = _find_files(folder)

            if not path_aulica:
                logger.error("No se encontró archivo con 'AULICA' en %s/", DATA_DIR)
                sys.exit(1)
            if not path_control:
                logger.error("No se encontró archivo con 'CONTROL' en %s/", DATA_DIR)
                sys.exit(1)

            logger.info("Aulica:  %s", path_aulica.name)
            logger.info("Control: %s", path_control.name)

        run(str(path_aulica), str(path_control), output_dir=output_folder)

    except FileNotFoundError as e:
        logger.error("Archivo no encontrado: %s", e)
        sys.exit(1)
    except KeyError as e:
        logger.error("Columna no encontrada en el Excel: %s — revisá config/settings.py", e)
        sys.exit(1)
    except Exception as e:
        logger.error("Error inesperado: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()