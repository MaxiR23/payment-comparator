# INFO: compara los cupones de Aulica contra los totales de Control y devuelve las diferencias.
import logging
from typing import Tuple

import pandas as pd

logger = logging.getLogger(__name__)

def compare(
    aulica: pd.DataFrame,
    control: pd.DataFrame,
    tolerance: float = 1.0,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Devuelve (differences, control_only) entre Aulica y Control.
        Args:
            aulica:    DataFrame con al menos las columnas Legajo y Monto.
            control:   DataFrame con al menos las columnas Legajo y Total.
            tolerance: ignora diferencias absolutas por debajo de este valor.

        Returns:
            differences:  alumnos donde el total de Aulica != total de Control.
            control_only: alumnos presentes en Control pero ausentes en Aulica.
    """
    aulica_totals = (
        aulica.groupby("Legajo")["Monto"]
        .sum()
        .reset_index()
        .rename(columns={"Monto": "Monto_Aulica"})
    )

    merged = control.merge(aulica_totals, on="Legajo", how="outer", indicator=True)

    both = merged[merged["_merge"] == "both"].copy()
    both["Diferencia"] = both["Monto_Aulica"] - both["Total"]

    differences = (
        both[both["Diferencia"].abs() > tolerance]
        .sort_values("Diferencia", ascending=False)
    )

    control_only = (
        merged[merged["_merge"] == "left_only"][["Alumno", "Legajo", "Cuota_Abril", "Total"]]
    )

    logger.info(
        "Differences: %d students | total $%s",
        len(differences),
        f"{differences['Diferencia'].sum():,.2f}",
    )
    logger.info("Control only (no coupons): %d students", len(control_only))

    return differences, control_only