"""Acceso a los datos del contrato para los notebooks de minería.

    from datos import cargar
    t = cargar()            # lee data/sample/*.csv (no necesita SQL Server)
    t = cargar("bd")        # lee las mismas tablas desde SQL Server (.env)

También se elige con la variable de entorno FUENTE=muestra|bd.
Ambas fuentes devuelven exactamente las mismas tablas y columnas (etl/contrato.py).
"""

import os
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from etl import config, contrato  # noqa: E402

SALIDA = RAIZ / "mining" / "output"


def cargar(fuente: str | None = None) -> dict[str, pd.DataFrame]:
    fuente = (fuente or os.getenv("FUENTE", "muestra")).lower()
    nombres = [t.nombre for t in contrato.TABLAS if t.tipo != "control"]
    if fuente == "muestra":
        return {n: pd.read_csv(config.SAMPLE / f"{n}.csv", encoding="utf-8-sig") for n in nombres}
    if fuente == "bd":
        import sqlalchemy as sa
        eng = sa.create_engine(config.sqlalchemy_url())
        with eng.connect() as cx:
            return {n: pd.read_sql(f"SELECT * FROM dbo.{n}", cx) for n in nombres}
    raise ValueError("fuente debe ser 'muestra' o 'bd'")
