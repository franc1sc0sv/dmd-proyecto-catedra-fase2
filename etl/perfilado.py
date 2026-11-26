"""Informe de estado de los atributos del Excel (Clase 15.3, UIA4).

Una fila por columna de cada hoja, sobre los datos tal como vienen (antes de
limpiar): tipo, #total, #nulos, #distintos, media, desviación, moda, mínimo y
máximo. Es la evidencia del perfilado que justifica las reglas de limpieza.
"""

from pathlib import Path

import pandas as pd


def _tipo(s: pd.Series) -> str:
    v = s.dropna()
    return "Numérico" if len(v) and pd.to_numeric(v, errors="coerce").notna().all() else "Nominal"


def perfilar(hojas: dict[str, pd.DataFrame]) -> pd.DataFrame:
    filas = []
    for hoja, df in hojas.items():
        for col in df.columns:
            if col == "fila_excel":
                continue
            s = df[col]
            tipo = _tipo(s)
            no_nulos = s.dropna()
            fila = {"hoja": hoja, "atributo": col, "tipo": tipo, "total": len(s),
                    "nulos": int(s.isna().sum()), "distintos": int(s.nunique(dropna=False)),
                    "media": None, "desv": None,
                    "moda": no_nulos.mode().iloc[0] if len(no_nulos) else None}
            if tipo == "Numérico":
                n = pd.to_numeric(no_nulos)
                fila.update(media=round(n.mean(), 2), desv=round(n.std(), 2), minimo=n.min(), maximo=n.max())
            else:
                txt = no_nulos.astype(str)
                fila.update(minimo=txt.min() if len(txt) else None, maximo=txt.max() if len(txt) else None)
            filas.append(fila)
    return pd.DataFrame(filas)


def escribir(perfil: pd.DataFrame, destino: Path) -> None:
    perfil.to_csv(destino / "perfil_atributos.csv", index=False, encoding="utf-8-sig")
    fmt = lambda v: "" if v is None or (isinstance(v, float) and pd.isna(v)) else (  # noqa: E731
        f"{v:,.2f}" if isinstance(v, float) else str(v).replace("|", "\\|"))
    L = ["# Informe de estado de los atributos", "",
         "Perfilado del Excel **antes** de limpiar (Clase 15.3). Los mínimos y máximos de atributos nominales "
         "son alfabéticos, como en SQL. `Fecha` y `FechaRegistro` aparecen como *Nominal* porque vienen como texto "
         "(regla F2 de `docs/reglas_limpieza.md`). Las 3 filas sin datos de Finanzas_Mensual (2 vacías + nota) explican "
         "sus nulos.", ""]
    for hoja, g in perfil.groupby("hoja", sort=False):
        L += [f"## {hoja}", "", "| Atributo | Tipo | #total | #nulos | #distintos | Media | Desv. | Moda | Mín. | Máx. |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for r in g.to_dict("records"):
            L.append("| " + " | ".join(fmt(r[k]) for k in
                     ("atributo", "tipo", "total", "nulos", "distintos", "media", "desv", "moda", "minimo", "maximo")) + " |")
        L.append("")
    (destino / "perfil_atributos.md").write_text("\n".join(L), encoding="utf-8")
