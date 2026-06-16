# tests/test_comparator.py
#
# testeamos: src/comparator.py
# - compare() → (differences, control_only)
#   · detecta diferencias entre totales Áulica y Control
#   · respeta tolerancia
#   · agrupa múltiples cupones por legajo
#   · separa alumnos solo en Control
#   · ordena diferencias de mayor a menor
#

import pytest
import pandas as pd
from src.comparator import compare

# ════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════
def make_aulica(rows: list[dict]) -> pd.DataFrame:
    """Crea un DataFrame de Áulica con columnas mínimas."""
    return pd.DataFrame(rows, columns=["Legajo", "Monto"])

def make_control(rows: list[dict]) -> pd.DataFrame:
    """Crea un DataFrame de Control con columnas mínimas."""
    return pd.DataFrame(rows, columns=["Legajo", "Alumno", "Total", "Cuota_Abril"])

# ════════════════════════════════════════════════════════
# DIFERENCIAS
# ════════════════════════════════════════════════════════
class TestDifferences:
    def test_detects_difference_above_tolerance(self):
        aulica  = make_aulica([{"Legajo": 1, "Monto": 1000.0}])
        control = make_control([{"Legajo": 1, "Alumno": "Juan", "Total": 1500.0, "Cuota_Abril": 1500.0}])
        diffs, _ = compare(aulica, control, tolerance=1.0)
        assert len(diffs) == 1
        assert diffs.iloc[0]["Diferencia"] == pytest.approx(-500.0)

    def test_ignores_difference_within_tolerance(self):
        aulica  = make_aulica([{"Legajo": 1, "Monto": 1000.0}])
        control = make_control([{"Legajo": 1, "Alumno": "Juan", "Total": 1000.5, "Cuota_Abril": 1000.5}])
        diffs, _ = compare(aulica, control, tolerance=1.0)
        assert len(diffs) == 0

    def test_ignores_difference_exactly_at_tolerance(self):
        aulica  = make_aulica([{"Legajo": 1, "Monto": 1000.0}])
        control = make_control([{"Legajo": 1, "Alumno": "Juan", "Total": 1001.0, "Cuota_Abril": 1001.0}])
        diffs, _ = compare(aulica, control, tolerance=1.0)
        assert len(diffs) == 0

    def test_flags_difference_just_above_tolerance(self):
        aulica  = make_aulica([{"Legajo": 1, "Monto": 1000.0}])
        control = make_control([{"Legajo": 1, "Alumno": "Juan", "Total": 1001.01, "Cuota_Abril": 1001.01}])
        diffs, _ = compare(aulica, control, tolerance=1.0)
        assert len(diffs) == 1

    def test_zero_tolerance_flags_any_difference(self):
        aulica  = make_aulica([{"Legajo": 1, "Monto": 1000.0}])
        control = make_control([{"Legajo": 1, "Alumno": "Juan", "Total": 1000.01, "Cuota_Abril": 1000.01}])
        diffs, _ = compare(aulica, control, tolerance=0.0)
        assert len(diffs) == 1

    def test_returns_empty_differences_when_all_match(self):
        aulica  = make_aulica([{"Legajo": 1, "Monto": 500.0}, {"Legajo": 2, "Monto": 800.0}])
        control = make_control([
            {"Legajo": 1, "Alumno": "Juan", "Total": 500.0, "Cuota_Abril": 500.0},
            {"Legajo": 2, "Alumno": "Ana",  "Total": 800.0, "Cuota_Abril": 800.0},
        ])
        diffs, _ = compare(aulica, control, tolerance=1.0)
        assert len(diffs) == 0

    def test_differences_sorted_descending(self):
        aulica  = make_aulica([
            {"Legajo": 1, "Monto": 500.0},
            {"Legajo": 2, "Monto": 100.0},
        ])
        control = make_control([
            {"Legajo": 1, "Alumno": "Juan", "Total": 300.0, "Cuota_Abril": 300.0},  # diff +200
            {"Legajo": 2, "Alumno": "Ana",  "Total":  50.0, "Cuota_Abril":  50.0},  # diff +50
        ])
        diffs, _ = compare(aulica, control, tolerance=1.0)
        diferencias = diffs["Diferencia"].tolist()
        assert diferencias == sorted(diferencias, reverse=True)

    def test_detects_negative_difference(self):
        aulica  = make_aulica([{"Legajo": 1, "Monto": 500.0}])
        control = make_control([{"Legajo": 1, "Alumno": "Juan", "Total": 1000.0, "Cuota_Abril": 1000.0}])
        diffs, _ = compare(aulica, control, tolerance=1.0)
        assert diffs.iloc[0]["Diferencia"] == pytest.approx(-500.0)

# ════════════════════════════════════════════════════════
# AGRUPACIÓN DE CUPONES
# ════════════════════════════════════════════════════════
class TestCouponGrouping:
    def test_sums_multiple_coupons_for_same_legajo(self):
        aulica  = make_aulica([
            {"Legajo": 1, "Monto": 300.0},
            {"Legajo": 1, "Monto": 200.0},
        ])
        control = make_control([{"Legajo": 1, "Alumno": "Juan", "Total": 500.0, "Cuota_Abril": 500.0}])
        diffs, _ = compare(aulica, control, tolerance=1.0)
        assert len(diffs) == 0

    def test_partial_sum_still_generates_difference(self):
        aulica  = make_aulica([
            {"Legajo": 1, "Monto": 300.0},
            {"Legajo": 1, "Monto": 100.0},
        ])
        control = make_control([{"Legajo": 1, "Alumno": "Juan", "Total": 500.0, "Cuota_Abril": 500.0}])
        diffs, _ = compare(aulica, control, tolerance=1.0)
        assert len(diffs) == 1
        assert diffs.iloc[0]["Diferencia"] == pytest.approx(-100.0)

# ════════════════════════════════════════════════════════
# SOLO EN CONTROL
# ════════════════════════════════════════════════════════
class TestControlOnly:
    def test_detects_student_missing_from_aulica(self):
        aulica  = make_aulica([{"Legajo": 1, "Monto": 500.0}])
        control = make_control([
            {"Legajo": 1, "Alumno": "Juan", "Total": 500.0, "Cuota_Abril": 500.0},
            {"Legajo": 2, "Alumno": "Ana",  "Total": 800.0, "Cuota_Abril": 800.0},
        ])
        _, control_only = compare(aulica, control, tolerance=1.0)
        assert len(control_only) == 1
        assert control_only.iloc[0]["Legajo"] == 2

    def test_returns_empty_control_only_when_all_present(self):
        aulica  = make_aulica([{"Legajo": 1, "Monto": 500.0}])
        control = make_control([{"Legajo": 1, "Alumno": "Juan", "Total": 500.0, "Cuota_Abril": 500.0}])
        _, control_only = compare(aulica, control, tolerance=1.0)
        assert len(control_only) == 0

    def test_control_only_has_correct_columns(self):
        aulica  = make_aulica([])
        control = make_control([{"Legajo": 1, "Alumno": "Juan", "Total": 500.0, "Cuota_Abril": 500.0}])
        _, control_only = compare(aulica, control, tolerance=1.0)
        assert set(control_only.columns) == {"Alumno", "Legajo", "Cuota_Abril", "Total"}

    def test_student_only_in_aulica_not_in_control_only(self):
        aulica  = make_aulica([{"Legajo": 99, "Monto": 500.0}])
        control = make_control([{"Legajo": 1, "Alumno": "Juan", "Total": 500.0, "Cuota_Abril": 500.0}])
        _, control_only = compare(aulica, control, tolerance=1.0)
        assert 99 not in control_only["Legajo"].values

# ════════════════════════════════════════════════════════
# EDGE CASES
# ════════════════════════════════════════════════════════
class TestEdgeCases:
    def test_empty_aulica_returns_all_as_control_only(self):
        aulica  = make_aulica([])
        control = make_control([
            {"Legajo": 1, "Alumno": "Juan", "Total": 500.0, "Cuota_Abril": 500.0},
            {"Legajo": 2, "Alumno": "Ana",  "Total": 800.0, "Cuota_Abril": 800.0},
        ])
        diffs, control_only = compare(aulica, control, tolerance=1.0)
        assert len(diffs) == 0
        assert len(control_only) == 2

    def test_empty_control_returns_empty_results(self):
        aulica  = make_aulica([{"Legajo": 1, "Monto": 500.0}])
        control = make_control([])
        diffs, control_only = compare(aulica, control, tolerance=1.0)
        assert len(diffs) == 0
        assert len(control_only) == 0

    def test_both_empty_returns_empty_results(self):
        aulica  = make_aulica([])
        control = make_control([])
        diffs, control_only = compare(aulica, control, tolerance=1.0)
        assert len(diffs) == 0
        assert len(control_only) == 0