"""Extracción: lee las tres hojas de datos del Excel tal como vienen.

Todo se lee como texto/objeto (sin inferir tipos) para que la conversión y sus
errores ocurran en transform.py, donde quedan registrados. La hoja Contexto
solo describe el caso y no se carga.
"""

import hashlib
from pathlib import Path

import pandas as pd

HOJAS = ("Ventas", "Clientes", "Finanzas_Mensual")


def sha256(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def extraer(ruta: Path) -> dict[str, pd.DataFrame]:
    """Devuelve {hoja: DataFrame} con la columna extra `fila_excel` (1 = encabezado)."""
    hojas = {}
    for hoja in HOJAS:
        # pandas usa openpyxl con data_only=True: las celdas con fórmula traen el
        # último valor calculado por Excel (o None si el archivo nunca se calculó).
        df = pd.read_excel(ruta, sheet_name=hoja, dtype=object)
        df.insert(0, "fila_excel", range(2, len(df) + 2))
        hojas[hoja] = df
    return hojas
