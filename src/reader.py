# INFO: lee y normaliza las planillas de cupones de Aulica y de Control.
import logging
import pandas as pd

logger = logging.getLogger(__name__)

AULICA_COLUMNS = ["Legajo", "Alumno", "Nro_Cupon", "Fecha_Debito", "Monto"]

# un DataFrame es, básicamente, una tabla de datos en memoria.
def read_aulica(path: str, sheet: int = 0) -> pd.DataFrame:
    """Devuelve un DataFrame limpio procesado desde el archivo de cupones de Aulica."""
    df = pd.read_excel(path, sheet_name=sheet, header=1)
    df.columns = AULICA_COLUMNS
    df["Legajo"] = pd.to_numeric(df["Legajo"], errors="coerce")
    df["Monto"] = pd.to_numeric(df["Monto"], errors="coerce")
    df = df[df["Legajo"].notna()].copy()
    df["Legajo"] = df["Legajo"].astype(int)

    logger.info(
        "Aulica: %d coupons | %d students | total $%s",
        len(df),
        df["Legajo"].nunique(),
        f"{df['Monto'].sum():,.2f}",
    )
    return df

def read_control(path: str, sheet: str, cuota_column: str) -> pd.DataFrame:
    """Devuelve un DataFrame limpio procesado desde el archivo de Control."""
    source_cols = ["ALUMNO", "COD ÁULICA", cuota_column, "TOTAL"]
    raw = pd.read_excel(path, sheet_name=sheet, header=0)
    df = raw[source_cols].copy()
    df.columns = ["Alumno", "Legajo", "Cuota_Abril", "Total"]
    df["Legajo"] = pd.to_numeric(df["Legajo"], errors="coerce")
    df["Cuota_Abril"] = pd.to_numeric(df["Cuota_Abril"], errors="coerce")
    df["Total"] = pd.to_numeric(df["Total"], errors="coerce")
    df = df[df["Legajo"].notna()].copy()
    df["Legajo"] = df["Legajo"].astype(int)

    logger.info(
        "Control: %d students | total $%s",
        len(df),
        f"{df['Total'].sum():,.2f}",
    )
    return df