# Datos

**Qué es esta carpeta:** el Excel original del caso y la base ya limpia en CSV.

**Para quién:** todos. Las partes 3 y 4 trabajan directamente con `sample/` si no tienen SQL Server.

## `raw/`: el Excel original

`datos_andina_retail_corp.xlsx`, tal como vino del Aula Digital, sin modificar. Está en Git porque es pequeño (75 KB) y la propia hoja de Finanzas lo declara *"Datos simulados con fines académicos"*.

- Hojas: **Ventas** (850 filas × 11 columnas), **Clientes** (120 × 7) y **Finanzas_Mensual** (12 meses + 2 filas vacías + 1 nota). **Contexto** solo describe el caso y no se carga.
- SHA256: `7e9568e2704317a3ae3cdaaccfa0a6c8e7cdbac1d1ca922c02060578e5fa7a8a`. El ETL avisa si el archivo cambia.

**No lo edites.** Si hay que corregir algo, la corrección va en el ETL (`etl/transform.py`).

## `sample/`: la base limpia en CSV

**La genera el ETL; no se edita a mano.** Si la borras, `python -m etl.run_etl --sin-bd` la vuelve a crear.

| Archivo | Qué es |
|---|---|
| `Dim_*.csv`, `Hecho_*.csv` | Las 10 tablas del Datawarehouse, con las mismas columnas y llaves que SQL Server |
| `Etl_Rechazos.csv` | Filas del Excel que no se pudieron cargar y por qué (hoy: ninguna) |
| `Etl_Observaciones.csv` | Datos cargados que merecen revisión (hoy: 3 órdenes anteriores al registro del cliente) |
| `reporte_carga.md` | **El resumen de la última carga**: qué cuadró entre Excel, CSV y base, y los KPIs verificados |
| `perfil_atributos.md` / `.csv` | Perfilado del Excel antes de limpiar: nulos, distintos, mínimos, máximos… (Clase 15.3) |

Formato de los CSV: UTF-8 (con BOM, para que Excel y Power BI lean bien los acentos), fechas `AAAA-MM-DD` y punto decimal.
