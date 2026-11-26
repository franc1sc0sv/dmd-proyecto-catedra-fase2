"""Carga: escribe el extracto (data/sample) y carga SQL Server.

Carga total, como define la Fase 1: crea la BD si no existe, recrea las tablas
(sql/ddl), inserta dimensiones y luego hechos, y (re)crea las vistas de KPIs y
del cubo (sql/kpis, sql/olap).
"""

import re
from pathlib import Path

import pandas as pd
import sqlalchemy as sa

from . import config, contrato


def escribir_muestra(tablas: dict[str, pd.DataFrame], destino: Path = config.SAMPLE) -> None:
    destino.mkdir(parents=True, exist_ok=True)
    for nombre, df in tablas.items():
        # utf-8-sig: Power BI y Excel detectan bien los acentos con BOM.
        df.to_csv(destino / f"{nombre}.csv", index=False, encoding="utf-8-sig", date_format="%Y-%m-%d")


def _lotes(sql: str) -> list[str]:
    return [b.strip() for b in re.split(r"^\s*GO\s*$", sql, flags=re.M | re.I) if b.strip()]


def ejecutar_script(engine: sa.Engine, ruta: Path) -> None:
    with engine.begin() as cx:
        for lote in _lotes(ruta.read_text(encoding="utf-8")):
            cx.exec_driver_sql(lote)


def crear_bd_si_falta() -> None:
    master = sa.create_engine(config.sqlalchemy_url("master"), isolation_level="AUTOCOMMIT")
    with master.connect() as cx:
        cx.exec_driver_sql(f"IF DB_ID(N'{config.DB_NAME}') IS NULL CREATE DATABASE [{config.DB_NAME}]")
    master.dispose()


def motor() -> sa.Engine:
    return sa.create_engine(config.sqlalchemy_url(), fast_executemany=True)


def cargar_bd(tablas: dict[str, pd.DataFrame]) -> sa.Engine:
    crear_bd_si_falta()
    eng = motor()
    ejecutar_script(eng, config.SQL_DIR / "ddl" / "01_tablas.sql")
    for t in contrato.TABLAS:  # orden del contrato = dimensiones antes que hechos
        df = tablas[t.nombre].astype(object).where(tablas[t.nombre].notna(), None)
        df.to_sql(t.nombre, eng, schema="dbo", if_exists="append", index=False, chunksize=1000)
    # Solo los scripts que crean vistas; las consultas sueltas de evidencia no se ejecutan aquí.
    for carpeta in ("kpis", "olap"):
        for script in sorted((config.SQL_DIR / carpeta).glob("*vistas*.sql")):
            ejecutar_script(eng, script)
    return eng
