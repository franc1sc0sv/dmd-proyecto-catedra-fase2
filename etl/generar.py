"""Genera, desde etl/contrato.py, el DDL (sql/ddl/01_tablas.sql) y el diccionario
de datos (docs/diccionario_datos.md). Ejecutar tras cambiar el contrato:

    python -m etl.generar
"""

from . import contrato
from .config import RAIZ


def ddl() -> str:
    out = ["-- GENERADO por `python -m etl.generar` desde etl/contrato.py. No editar a mano.",
           "-- Carga total: borra y recrea todas las tablas (Fase 1, sección 2.2).", ""]
    for t in reversed(contrato.TABLAS):
        out.append(f"IF OBJECT_ID(N'dbo.{t.nombre}', N'U') IS NOT NULL DROP TABLE dbo.{t.nombre};")
    out.append("GO\n")
    for t in contrato.TABLAS:
        cols = [f"    {c.nombre} {c.tipo_sql} {'NULL' if c.nula else 'NOT NULL'}" for c in t.columnas]
        pk = [c.nombre for c in t.columnas if c.pk]
        cols.append(f"    CONSTRAINT PK_{t.nombre} PRIMARY KEY ({', '.join(pk)})")
        for c in t.columnas:
            if c.fk:
                ref_t, ref_c = c.fk.split(".")
                cols.append(f"    CONSTRAINT FK_{t.nombre}_{c.nombre} FOREIGN KEY ({c.nombre}) "
                            f"REFERENCES dbo.{ref_t} ({ref_c})")
        out.append(f"CREATE TABLE dbo.{t.nombre} (\n" + ",\n".join(cols) + "\n);\nGO\n")
    return "\n".join(out)


def diccionario() -> str:
    out = ["# Diccionario de datos", "",
           "> Generado por `python -m etl.generar` desde `etl/contrato.py`. No editar a mano.", "",
           "Convenciones: **PK** llave primaria, **FK** llave foránea, montos en USD. La columna *Origen* es el "
           "mapeo origen → destino (Clase 7) y la *Clasificación* sigue los tipos de hechos y dimensiones de la Clase 5. "
           "Diagrama y relaciones: [esquema_estrella.md](esquema_estrella.md).", ""]
    for t in contrato.TABLAS:
        out += [f"## {t.nombre}", "", f"*Tipo:* {t.tipo} · *Grano:* {t.grano}"
                + (f" · *Clasificación:* {t.clasificacion}" if t.clasificacion else ""), "",
                "| Columna | Tipo | Nulo | Llave | Origen (Excel → destino) | Descripción |", "|---|---|---|---|---|---|"]
        for c in t.columnas:
            llave = " ".join(x for x in ["PK" if c.pk else "", f"FK → {c.fk}" if c.fk else ""] if x)
            out.append(f"| `{c.nombre}` | {c.tipo_sql} | {'sí' if c.nula else 'no'} | {llave} | {c.origen or 'ETL'} | {c.descripcion} |")
        out.append("")
    return "\n".join(out)


def _tipo_m(tipo_sql: str) -> str:
    t = tipo_sql.upper()
    if t.startswith(("INT", "TINYINT", "SMALLINT")):
        return "Int64.Type"
    if t == "DECIMAL(12,6)":
        return "type number"
    if t.startswith("DECIMAL"):
        return "Currency.Type"
    if t == "DATE":
        return "type date"
    return "type text"


def power_query(t: contrato.Tabla) -> str:
    """Consulta M con la misma salida desde CSV (data/sample) o desde SQL Server.
    Usa los parámetros FuenteDatos ("CSV"|"SQL"), CarpetaMuestra, Servidor y BaseDatos."""
    tipos = ",\n        ".join(f'{{"{c.nombre}", {_tipo_m(c.tipo_sql)}}}' for c in t.columnas)
    return f"""// {t.nombre}: generado por `python -m etl.generar` desde etl/contrato.py
// Mismas columnas y mismos tipos desde CSV o desde SQL Server (los tipos se fijan al final en ambos casos).
let
    Tipos = {{
        {tipos}
    }},
    DesdeSQL = () => Sql.Database(Servidor, BaseDatos){{[Schema = "dbo", Item = "{t.nombre}"]}}[Data],
    DesdeCSV = () =>
        let
            Csv = Csv.Document(File.Contents(CarpetaMuestra & "\\{t.nombre}.csv"),
                               [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv])
        in
            Table.PromoteHeaders(Csv, [PromoteAllScalars = true]),
    Origen = if FuenteDatos = "SQL" then DesdeSQL() else DesdeCSV(),
    Resultado = Table.TransformColumnTypes(Table.SelectColumns(Origen, List.Transform(Tipos, each _{{0}})), Tipos, "en-US")
in
    Resultado
"""


if __name__ == "__main__":
    (RAIZ / "sql" / "ddl" / "01_tablas.sql").write_text(ddl(), encoding="utf-8")
    (RAIZ / "docs" / "diccionario_datos.md").write_text(diccionario(), encoding="utf-8")
    pq = RAIZ / "powerbi" / "power_query"
    pq.mkdir(parents=True, exist_ok=True)
    for t in contrato.TABLAS:
        if t.tipo != "control":
            (pq / f"{t.nombre}.pq").write_text(power_query(t), encoding="utf-8")
    print("Generados sql/ddl/01_tablas.sql, docs/diccionario_datos.md y powerbi/power_query/*.pq")
