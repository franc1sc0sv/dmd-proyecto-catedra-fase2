"""Punto de entrada del ETL.

    python -m etl.run_etl            # Excel -> limpieza -> data/sample + SQL Server + validación
    python -m etl.run_etl --sin-bd   # igual, pero sin SQL Server (solo genera data/sample)
"""

import argparse
import sys

import pandas as pd

from . import config, load, validate
from .extract import extraer, sha256
from .transform import transformar


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sin-bd", action="store_true", help="no cargar SQL Server; solo generar data/sample")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")  # consola de Windows

    hash_ = sha256(config.EXCEL)
    if hash_ != config.EXCEL_SHA256:
        print(f"AVISO: el Excel no es el original (sha256 {hash_[:12]}…). Los totales esperados pueden variar.")

    print(f"1/4 Extrayendo {config.EXCEL.name}")
    hojas = extraer(config.EXCEL)

    segmentos = None
    if config.SEGMENTOS.exists():
        segmentos = pd.read_csv(config.SEGMENTOS, encoding="utf-8-sig")
        print(f"    Usando segmentos de K-means: {config.SEGMENTOS.relative_to(config.RAIZ)}")

    print("2/4 Transformando")
    tablas, bitacora = transformar(hojas, segmentos)
    print(f"    rechazos: {len(bitacora.rechazos)} · observaciones: {len(bitacora.observaciones)}")

    print("3/4 Cargando")
    load.escribir_muestra(tablas)
    print(f"    extracto -> {config.SAMPLE.relative_to(config.RAIZ)}")
    resumen_bd = None
    if not args.sin_bd:
        eng = load.cargar_bd(tablas)
        print(f"    SQL Server -> {config.DB_SERVER}/{config.DB_NAME}")
        resumen_bd = validate.resumen_bd(eng)

    print("4/4 Validando")
    ok = validate.validar(tablas, bitacora, validate.resumen_excel(config.EXCEL), resumen_bd)
    print(f"    {'OK' if ok else 'FALLÓ'} -> data/sample/reporte_carga.md")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
