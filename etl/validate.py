"""Validación y conciliación: Excel original ↔ transformación ↔ extracto CSV ↔ SQL Server.

El lado "Excel" se calcula de forma independiente del ETL (openpyxl directo, sin
reglas de limpieza) para que un error en transform.py no se valide a sí mismo.
Genera data/sample/reporte_carga.md y devuelve False si algo no cuadra.
"""

from datetime import datetime
from pathlib import Path

import openpyxl
import pandas as pd
import sqlalchemy as sa

from . import config, contrato

MESES = {"enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"}


def _filas(ws):
    enc = [c.value for c in ws[1]]
    for fila in ws.iter_rows(min_row=2, values_only=True):
        yield dict(zip(enc, fila))


def resumen_excel(ruta: Path) -> dict:
    """Conteos y totales leídos directamente del Excel (valores calculados por Excel)."""
    wb = openpyxl.load_workbook(ruta, data_only=True, read_only=True)
    ven = [r for r in _filas(wb["Ventas"]) if r.get("OrdenID")]
    cli = [r for r in _filas(wb["Clientes"]) if r.get("ClienteID")]
    fin = [r for r in _filas(wb["Finanzas_Mensual"]) if str(r.get("Mes") or "").strip().lower() in MESES]
    col_v = next(k for k in cli[0] if str(k).startswith("VisitasWeb"))
    col_c = next(k for k in cli[0] if str(k).startswith("ConversionesWeb"))
    ventas = sum(float(r["Total"]) if r["Total"] is not None else float(r["Cantidad"]) * float(r["PrecioUnitario"])
                 for r in ven)
    ecommerce = sum(float(r["Cantidad"]) * float(r["PrecioUnitario"]) for r in ven if r["Canal"] == "E-commerce")
    s = lambda k: sum(float(r[k]) for r in fin)  # noqa: E731
    ingresos, costo, gastos, flujo, inversion = (s(k) for k in
        ("Ingresos", "CostoVentas", "GastosOperativos", "FlujoCaja", "InversionesRealizadas"))
    utilidad = ingresos - costo - gastos
    visitas, conv = sum(int(r[col_v]) for r in cli), sum(int(r[col_c]) for r in cli)
    clientes_con_compra = len({r["ClienteID"] for r in ven})
    return {
        "filas": {"Ventas": wb["Ventas"].max_row - 1, "Clientes": wb["Clientes"].max_row - 1,
                  "Finanzas_Mensual": wb["Finanzas_Mensual"].max_row - 1},
        "registros": {"Ventas": len(ven), "Clientes": len(cli), "Finanzas_Mensual": len(fin)},
        "totales": {"ventas": round(ventas, 2), "ingresos": round(ingresos, 2),
                    "visitas_web": visitas, "conversiones_web": conv},
        "distintos": {"Dim_Cliente": len(cli), "Dim_Producto": len({r["Producto"] for r in ven}),
                      "Dim_Canal": len({r["Canal"] for r in ven}), "Dim_Vendedor": len({r["Vendedor"] for r in ven}),
                      "Dim_Region": len({r["Region"] for r in ven} | {r["Region"] for r in cli}),
                      "Dim_Mes": len(fin)},
        "kpis": {
            "margen_bruto_pct": round(100 * (ingresos - costo) / ingresos, 2),
            "margen_neto_pct": round(100 * utilidad / ingresos, 2),
            "indice_gastos_operativos_pct": round(100 * gastos / ingresos, 2),
            "roi_pct": round(100 * utilidad / inversion, 2),
            "flujo_caja_acumulado": round(flujo, 2),
            "ventas_por_cliente": round(ventas / clientes_con_compra, 2),
            "tasa_conversion_web_pct": round(100 * conv / visitas, 2),
            "ticket_promedio": round(ventas / len(ven), 2),
            "participacion_ecommerce_pct": round(100 * ecommerce / ventas, 2),
        },
    }


def resumen_tablas(t: dict[str, pd.DataFrame]) -> dict:
    return {
        "conteos": {n: len(df) for n, df in t.items()},
        "totales": {"ventas": round(float(t["Hecho_Ventas"]["total"].sum()), 2),
                    "ingresos": round(float(t["Hecho_Finanzas_Mensual"]["ingresos"].sum()), 2),
                    "visitas_web": int(t["Hecho_Trafico_Web"]["visitas_web"].sum()),
                    "conversiones_web": int(t["Hecho_Trafico_Web"]["conversiones_web"].sum())},
    }


def leer_muestra(carpeta: Path = config.SAMPLE) -> dict[str, pd.DataFrame]:
    return {t.nombre: pd.read_csv(carpeta / f"{t.nombre}.csv", encoding="utf-8-sig") for t in contrato.TABLAS}


def resumen_bd(eng: sa.Engine) -> dict:
    with eng.connect() as cx:
        q = lambda sql: cx.exec_driver_sql(sql).scalar()  # noqa: E731
        conteos = {t.nombre: q(f"SELECT COUNT(*) FROM dbo.{t.nombre}") for t in contrato.TABLAS}
        totales = {"ventas": round(float(q("SELECT SUM(total) FROM dbo.Hecho_Ventas")), 2),
                   "ingresos": round(float(q("SELECT SUM(ingresos) FROM dbo.Hecho_Finanzas_Mensual")), 2),
                   "visitas_web": int(q("SELECT SUM(visitas_web) FROM dbo.Hecho_Trafico_Web")),
                   "conversiones_web": int(q("SELECT SUM(conversiones_web) FROM dbo.Hecho_Trafico_Web"))}
        kpis = dict(cx.exec_driver_sql("SELECT * FROM dbo.vw_KPI_Anual").mappings().one())
        cols = pd.read_sql("SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                           "ORDER BY TABLE_NAME, ORDINAL_POSITION", cx)
    esquema = {n: list(g["COLUMN_NAME"]) for n, g in cols.groupby("TABLE_NAME")}
    return {"conteos": conteos, "totales": totales, "kpis": {k: float(v) for k, v in kpis.items() if v is not None},
            "esquema": esquema}


def _n(x) -> str:
    return f"{x:,.2f}" if isinstance(x, float) else f"{x:,}"


def validar(tablas, bitacora, rx: dict, bd: dict | None, destino: Path = config.SAMPLE) -> bool:
    checks: list[tuple[str, bool, str]] = []

    def chk(nombre, ok, detalle):
        checks.append((nombre, bool(ok), detalle))

    tr = resumen_tablas(tablas)
    mu = resumen_tablas(leer_muestra(destino))
    rech = pd.DataFrame(bitacora.rechazos, columns=["hoja", "fila_excel", "llave_origen", "causa"])
    no_reg = pd.DataFrame(bitacora.filas_no_registro, columns=["hoja", "fila_excel", "contenido"])

    # 1. Cada fila de origen: cargada o rechazada (las filas vacías/nota no son registros).
    cargadas = {"Ventas": tr["conteos"]["Hecho_Ventas"], "Clientes": tr["conteos"]["Dim_Cliente"],
                "Finanzas_Mensual": tr["conteos"]["Hecho_Finanzas_Mensual"]}
    for hoja, leidas in rx["filas"].items():
        r = int((rech["hoja"] == hoja).sum())
        n = int((no_reg["hoja"] == hoja).sum())
        chk(f"{hoja}: leídas = cargadas + rechazadas + no-registro", leidas == cargadas[hoja] + r + n,
            f"{leidas} = {cargadas[hoja]} + {r} + {n}")
    # 2. Totales: Excel ↔ transformación ↔ muestra ↔ BD.
    for k, v in rx["totales"].items():
        fuentes = {"transformación": tr["totales"][k], "muestra": mu["totales"][k]}
        if bd:
            fuentes["BD"] = bd["totales"][k]
        ok = all(abs(x - v) < 0.01 for x in fuentes.values())
        chk(f"Total {k}", ok, f"Excel {_n(v)} · " + " · ".join(f"{a} {_n(b)}" for a, b in fuentes.items()))
    # 3. Conteos de tablas: transformación ↔ muestra ↔ BD; dimensiones ↔ valores distintos del Excel.
    for n, c in tr["conteos"].items():
        ok = c == mu["conteos"][n] and (bd is None or c == bd["conteos"][n])
        esperado = rx["distintos"].get(n)
        ok = ok and (esperado is None or c == esperado)
        chk(f"Filas {n}", ok, f"transf. {c} · muestra {mu['conteos'][n]}"
            + (f" · BD {bd['conteos'][n]}" if bd else "") + (f" · distintos Excel {esperado}" if esperado else ""))
    # 4. Esquema de la BD = contrato.
    if bd:
        for t in contrato.TABLAS:
            chk(f"Esquema {t.nombre} = contrato", bd["esquema"].get(t.nombre) == t.nombres, "")
        # 5. KPIs SQL = KPIs calculados directo del Excel.
        for k, v in rx["kpis"].items():
            chk(f"KPI {k}", abs(bd["kpis"][k] - v) < 0.011, f"SQL {_n(bd['kpis'][k])} · Excel {_n(v)}")

    ok = all(c[1] for c in checks)
    _reporte(destino / "reporte_carga.md", checks, bitacora, rx, ok, bd is not None)
    return ok


def _reporte(ruta: Path, checks, b, rx, ok, con_bd):
    obs = pd.DataFrame(b.observaciones, columns=["hoja", "fila_excel", "llave_origen", "tipo", "detalle"])
    L = ["# Reporte de carga", "",
         f"Generado: {datetime.now():%Y-%m-%d %H:%M} · Excel SHA256 `{config.EXCEL_SHA256[:12]}…` · "
         f"BD: {'sí' if con_bd else 'no (modo --sin-bd)'} · **Resultado: {'OK' if ok else 'FALLÓ'}**", "",
         "## Conciliación", "", "| Verificación | OK | Detalle |", "|---|---|---|"]
    L += [f"| {n} | {'✅' if o else '❌'} | {d} |" for n, o, d in checks]
    L += ["", "## Filas que no se cargaron", ""]
    if b.rechazos:
        L += ["| Hoja | Fila Excel | Llave | Causa |", "|---|---|---|---|"]
        L += [f"| {r['hoja']} | {r['fila_excel']} | {r['llave_origen']} | {r['causa']} |" for r in b.rechazos]
    else:
        L.append("**Rechazos: 0.** Ninguna fila de datos se descartó.")
    if b.filas_no_registro:
        L += ["", "Filas que no son registros (no se cuentan como rechazos, Fase 1 tabla 1):", "",
              "| Hoja | Fila Excel | Contenido |", "|---|---|---|"]
        L += [f"| {r['hoja']} | {r['fila_excel']} | {r['contenido']} |" for r in b.filas_no_registro]
    L += ["", "## Observaciones (se cargan, pero requieren revisión)", ""]
    if len(obs):
        L += [f"- **{t}**: {n}" for t, n in obs["tipo"].value_counts().items()]
        L += ["", "Detalle completo: `Etl_Observaciones.csv` / tabla `dbo.Etl_Observaciones`."]
    else:
        L.append("Ninguna.")
    ruta.write_text("\n".join(L) + "\n", encoding="utf-8")
