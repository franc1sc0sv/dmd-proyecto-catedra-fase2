"""Transformación: aplica las reglas de limpieza (docs/reglas_limpieza.md) y arma
las tablas del esquema estrella según etl/contrato.py.

Criterios (Fase 1, sección 2.4):
  * Formato y estructura se corrigen (fechas en texto, meses con nombre, año en
    el nombre de la columna, filas vacías/nota).
  * Datos dudosos NO se modifican: se cargan y se anotan en Etl_Observaciones.
  * Lo que no se puede cargar va a Etl_Rechazos con su causa. Cada fila de origen
    queda como cargada o rechazada.
"""

import re
from dataclasses import dataclass, field
from datetime import date, datetime

import pandas as pd

from . import contrato

MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
         "Septiembre", "Octubre", "Noviembre", "Diciembre"]
MES_A_NUMERO = {m.casefold(): i for i, m in enumerate(MESES, start=1)}
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
TOLERANCIA = 0.005  # medio centavo


@dataclass
class Bitacora:
    rechazos: list[dict] = field(default_factory=list)
    observaciones: list[dict] = field(default_factory=list)
    filas_no_registro: list[dict] = field(default_factory=list)  # vacías / nota (no son registros)

    def rechazar(self, hoja, fila, llave, causa):
        self.rechazos.append(dict(hoja=hoja, fila_excel=int(fila), llave_origen=llave, causa=causa))

    def observar(self, hoja, fila, llave, tipo, detalle):
        self.observaciones.append(dict(hoja=hoja, fila_excel=int(fila), llave_origen=llave,
                                       tipo=tipo, detalle=detalle))


# ---------------------------------------------------------------- conversiones
def texto(v) -> str | None:
    if v is None or (isinstance(v, float) and pd.isna(v)) or v is pd.NA:
        return None
    s = re.sub(r"\s+", " ", str(v)).strip()
    return s or None


def fecha(v) -> date | None:
    """Acepta fecha de Excel o texto ISO AAAA-MM-DD. Otro formato -> None (rechazo)."""
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    s = texto(v)
    if s is None:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return None


def numero(v) -> float | None:
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = texto(v)
    if s is None:
        return None
    s = s.replace("$", "").replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


def llaves(valores) -> dict[str, int]:
    """Llave sustituta determinista: 1..n en orden alfabético del valor natural."""
    return {v: i for i, v in enumerate(sorted(set(valores)), start=1)}


# ---------------------------------------------------------------- hojas
def limpiar_clientes(df: pd.DataFrame, b: Bitacora) -> pd.DataFrame:
    hoja = "Clientes"
    col_visitas = next(c for c in df.columns if str(c).startswith("VisitasWeb"))
    col_conv = next(c for c in df.columns if str(c).startswith("ConversionesWeb"))
    anio_web = int(re.search(r"(\d{4})$", str(col_visitas)).group(1))  # el año está en el encabezado

    filas, vistos = [], set()
    for r in df.to_dict("records"):
        f, cid = r["fila_excel"], texto(r["ClienteID"])
        if cid is None:
            b.rechazar(hoja, f, None, "ClienteID vacío"); continue
        if cid in vistos:
            b.rechazar(hoja, f, cid, "ClienteID duplicado"); continue
        freg = fecha(r["FechaRegistro"])
        if freg is None:
            b.rechazar(hoja, f, cid, f"FechaRegistro no convertible: {r['FechaRegistro']!r}"); continue
        region = texto(r["Region"])
        if region is None:
            b.rechazar(hoja, f, cid, "Region vacía"); continue
        vis, conv = numero(r[col_visitas]), numero(r[col_conv])
        if vis is None or conv is None or vis < 0 or conv < 0:
            b.rechazar(hoja, f, cid, "Visitas o conversiones web no numéricas o negativas"); continue
        if conv > vis:
            b.observar(hoja, f, cid, "Conversiones > visitas", f"{conv:.0f} conversiones y {vis:.0f} visitas")
        vistos.add(cid)
        filas.append(dict(fila_excel=f, cliente_id=cid, nombre=texto(r["Nombre"]) or "(sin nombre)",
                          segmento=texto(r["Segmento"]) or "(sin segmento)", region=region,
                          fecha_registro=freg, visitas_web=int(vis), conversiones_web=int(conv),
                          anio=anio_web))
    return pd.DataFrame(filas)


def limpiar_ventas(df: pd.DataFrame, clientes: pd.DataFrame, b: Bitacora) -> pd.DataFrame:
    hoja = "Ventas"
    cli = clientes.set_index("cliente_id")
    filas, vistos = [], set()
    for r in df.to_dict("records"):
        f, oid = r["fila_excel"], texto(r["OrdenID"])
        if oid is None:
            b.rechazar(hoja, f, None, "OrdenID vacío"); continue
        if oid in vistos:
            b.rechazar(hoja, f, oid, "OrdenID duplicado"); continue
        fch = fecha(r["Fecha"])
        if fch is None:
            b.rechazar(hoja, f, oid, f"Fecha no convertible: {r['Fecha']!r}"); continue
        cid = texto(r["ClienteID"])
        if cid not in cli.index:
            b.rechazar(hoja, f, oid, f"ClienteID {cid!r} no existe en Clientes"); continue
        vals = {k: texto(r[k]) for k in ("Categoria", "Producto", "Canal", "Vendedor", "Region")}
        faltan = [k for k, v in vals.items() if v is None]
        if faltan:
            b.rechazar(hoja, f, oid, f"Columnas vacías: {', '.join(faltan)}"); continue
        cant, precio = numero(r["Cantidad"]), numero(r["PrecioUnitario"])
        if cant is None or precio is None or cant <= 0 or precio <= 0 or cant != int(cant):
            b.rechazar(hoja, f, oid, "Cantidad o PrecioUnitario no válidos"); continue

        total = round(cant * precio, 2)  # se recalcula siempre (en el Excel es una fórmula)
        total_excel = numero(r["Total"])
        if total_excel is None:
            b.observar(hoja, f, oid, "Total sin valor", "La celda no tenía valor calculado; se usa Cantidad × PrecioUnitario")
        elif abs(total_excel - total) > TOLERANCIA:
            b.observar(hoja, f, oid, "Total no coincide", f"Excel {total_excel:.2f} vs recalculado {total:.2f}; se carga el recalculado")
        if fch < cli.at[cid, "fecha_registro"]:
            b.observar(hoja, f, oid, "Orden anterior al registro del cliente",
                       f"{cid}: orden {fch} y registro {cli.at[cid, 'fecha_registro']}")
        vistos.add(oid)
        filas.append(dict(fila_excel=f, orden_id=oid, fecha=fch, cliente_id=cid,
                          categoria=vals["Categoria"], producto=vals["Producto"], canal=vals["Canal"],
                          equipo=vals["Vendedor"], region_venta=vals["Region"],
                          region_cliente=cli.at[cid, "region"],
                          cantidad=int(cant), precio_unitario=round(precio, 2), total=total))
    return pd.DataFrame(filas)


def limpiar_finanzas(df: pd.DataFrame, anio: int, b: Bitacora) -> pd.DataFrame:
    hoja = "Finanzas_Mensual"
    medidas = ["Ingresos", "CostoVentas", "GastosOperativos", "FlujoCaja", "InversionesRealizadas"]
    filas, vistos = [], set()
    for r in df.to_dict("records"):
        f, mes = r["fila_excel"], texto(r["Mes"])
        if mes is None or mes.casefold() not in MES_A_NUMERO:
            # Filas vacías y la nota "cifras en USD" debajo de diciembre: no son registros.
            b.filas_no_registro.append(dict(hoja=hoja, fila_excel=f, contenido=mes or "(vacía)"))
            continue
        n = MES_A_NUMERO[mes.casefold()]
        if n in vistos:
            b.rechazar(hoja, f, mes, "Mes duplicado"); continue
        v = {k: numero(r[k]) for k in medidas}
        if any(x is None for x in v.values()):
            b.rechazar(hoja, f, mes, "Medidas no numéricas"); continue
        util = round(v["Ingresos"] - v["CostoVentas"] - v["GastosOperativos"], 2)
        util_x = numero(r["UtilidadNeta"])
        if util_x is None or abs(util_x - util) > TOLERANCIA:
            b.observar(hoja, f, mes, "UtilidadNeta no coincide", f"Excel {util_x} vs recalculada {util:.2f}; se carga la recalculada")
        roi = util / v["InversionesRealizadas"] if v["InversionesRealizadas"] else None
        roi_x = numero(r["RetornoInversion"])
        if roi is not None and (roi_x is None or abs(roi_x - roi) > 1e-6):
            b.observar(hoja, f, mes, "RetornoInversion no coincide", f"Excel {roi_x} vs recalculado {roi:.6f}; se carga el recalculado")
        vistos.add(n)
        filas.append(dict(fila_excel=f, mes_key=anio * 100 + n, ingresos=v["Ingresos"],
                          costo_ventas=v["CostoVentas"], gastos_operativos=v["GastosOperativos"],
                          utilidad_neta=util, flujo_caja=v["FlujoCaja"],
                          inversiones_realizadas=v["InversionesRealizadas"],
                          retorno_inversion=None if roi is None else round(roi, 6)))
    return pd.DataFrame(filas)


# ---------------------------------------------------------------- dimensiones
def dim_calendario(anios: list[int]) -> tuple[pd.DataFrame, pd.DataFrame]:
    dias = pd.date_range(f"{min(anios)}-01-01", f"{max(anios)}-12-31", freq="D")
    t = pd.DataFrame({"fecha": dias.date})
    t["tiempo_key"] = dias.year * 10000 + dias.month * 100 + dias.day
    t["dia_semana"] = [DIAS[d] for d in dias.dayofweek]
    t["mes_numero"] = dias.month
    t["nombre_mes"] = [MESES[m - 1] for m in dias.month]
    t["trimestre"] = dias.quarter
    t["semestre"] = (dias.month > 6).astype(int) + 1
    t["anio"] = dias.year
    t["mes_key"] = dias.year * 100 + dias.month
    mes = (t.drop_duplicates("mes_key")[["mes_key", "mes_numero", "nombre_mes", "trimestre", "semestre", "anio"]]
           .reset_index(drop=True))
    return t, mes


def transformar(hojas: dict[str, pd.DataFrame], segmentos: pd.DataFrame | None = None):
    b = Bitacora()
    cli = limpiar_clientes(hojas["Clientes"], b)
    ven = limpiar_ventas(hojas["Ventas"], cli, b)
    anios = sorted({d.year for d in ven["fecha"]} | set(cli["anio"]))
    if len(anios) != 1:
        raise ValueError(f"Se esperaba un solo año fiscal y hay {anios}")
    fin = limpiar_finanzas(hojas["Finanzas_Mensual"], anios[0], b)

    dim_tiempo, dim_mes = dim_calendario(anios)

    k_cli = llaves(cli["cliente_id"])
    dim_cliente = cli.assign(cliente_key=cli["cliente_id"].map(k_cli)).sort_values("cliente_key")
    dim_cliente["segmento_cluster"] = pd.NA
    if segmentos is not None and len(segmentos):
        seg = segmentos.set_index("cliente_id")["segmento_cluster"]
        dim_cliente["segmento_cluster"] = dim_cliente["cliente_id"].map(seg).astype("Int64")

    # Producto -> categoría debe ser única; si un producto aparece con dos, se usa la más frecuente.
    pc = ven.groupby(["producto", "categoria"]).size().reset_index(name="n")
    pc = pc.sort_values(["producto", "n"], ascending=[True, False])
    for prod, g in pc.groupby("producto"):
        if len(g) > 1:
            b.observar("Ventas", 0, prod, "Producto con varias categorías",
                       f"Se usa {g.iloc[0]['categoria']!r}; otras: {list(g['categoria'].iloc[1:])}")
    pc = pc.drop_duplicates("producto")
    k_prod = llaves(pc["producto"])
    dim_producto = pc.assign(producto_key=pc["producto"].map(k_prod)).sort_values("producto_key")
    k_canal, k_vend = llaves(ven["canal"]), llaves(ven["equipo"])
    k_reg = llaves(list(ven["region_venta"]) + list(cli["region"]))
    dim_canal = pd.DataFrame({"canal": list(k_canal), "canal_key": list(k_canal.values())})
    dim_vendedor = pd.DataFrame({"equipo": list(k_vend), "vendedor_key": list(k_vend.values())})
    dim_region = pd.DataFrame({"region": list(k_reg), "region_key": list(k_reg.values())})

    hv = pd.DataFrame({
        "tiempo_key": [d.year * 10000 + d.month * 100 + d.day for d in ven["fecha"]],
        "mes_key": [d.year * 100 + d.month for d in ven["fecha"]],
        "cliente_key": ven["cliente_id"].map(k_cli),
        "producto_key": ven["producto"].map(k_prod),
        "canal_key": ven["canal"].map(k_canal),
        "vendedor_key": ven["equipo"].map(k_vend),
        "region_cliente_key": ven["region_cliente"].map(k_reg),
        "region_venta_key": ven["region_venta"].map(k_reg),
        "orden_id": ven["orden_id"], "cantidad": ven["cantidad"],
        "precio_unitario": ven["precio_unitario"], "total": ven["total"],
    })
    ht = pd.DataFrame({
        "cliente_key": cli["cliente_id"].map(k_cli), "region_cliente_key": cli["region"].map(k_reg),
        "anio": cli["anio"], "visitas_web": cli["visitas_web"], "conversiones_web": cli["conversiones_web"],
    }).sort_values("cliente_key")

    rech = pd.DataFrame(b.rechazos, columns=["hoja", "fila_excel", "llave_origen", "causa"])
    rech.insert(0, "rechazo_id", range(1, len(rech) + 1))
    obs = pd.DataFrame(b.observaciones, columns=["hoja", "fila_excel", "llave_origen", "tipo", "detalle"])
    obs.insert(0, "observacion_id", range(1, len(obs) + 1))

    salida = {
        "Dim_Mes": dim_mes, "Dim_Tiempo": dim_tiempo, "Dim_Cliente": dim_cliente,
        "Dim_Producto": dim_producto, "Dim_Canal": dim_canal, "Dim_Vendedor": dim_vendedor,
        "Dim_Region": dim_region, "Hecho_Ventas": hv.sort_values("orden_id"),
        "Hecho_Finanzas_Mensual": fin.sort_values("mes_key"), "Hecho_Trafico_Web": ht,
        "Etl_Rechazos": rech, "Etl_Observaciones": obs,
    }
    # Fuerza el orden de columnas del contrato (y falla si falta alguna).
    salida = {n: df[contrato.POR_NOMBRE[n].nombres].reset_index(drop=True) for n, df in salida.items()}
    return salida, b
