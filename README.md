# Datawarehouse Andina Retail Corp

Proyecto de Cátedra, Fase 2 · Datawarehouse y Minería de Datos (DMD 941) · Universidad Don Bosco.

**Entrega: 27 de noviembre de 2026, 11:59 p. m.** (Aula Digital): un PDF con 6 secciones + enlace al video de defensa. La defensa oral es obligatoria y su fecha aún no se ha anunciado.

El Excel `datos_andina_retail_corp.xlsx` (año fiscal 2024) pasa por un ETL a un esquema estrella en SQL Server; sobre él se calculan los KPIs, el cubo OLAP, la segmentación K-means y el reporte de Power BI. El diseño viene de la propuesta de la Fase 1.

## El contrato de datos

Todas las partes trabajan contra **las mismas tablas y columnas**, definidas en [`etl/contrato.py`](etl/contrato.py) y documentadas en [`docs/diccionario_datos.md`](docs/diccionario_datos.md):

- `data/sample/*.csv`: el extracto limpio **completo** (850 órdenes, 120 clientes, 12 meses), con las mismas llaves que la BD.
- SQL Server `AndinaRetailDW`: las mismas tablas.

Las partes 3 y 4 pueden trabajar con los CSV sin instalar SQL Server, y cambiar después a la BD sin tocar su código (`FUENTE=bd` en minería, parámetro `FuenteDatos` en Power BI).

## Levantar el entorno (Windows)

Requisitos: Python 3.12, Git. Para cargar la BD: SQL Server 2019+ con autenticación de Windows y **ODBC Driver 18 for SQL Server**.

```powershell
git clone <url-del-repo> andina-retail-dw
cd andina-retail-dw
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
copy .env.example .env                       # ajustar si el servidor no es localhost

.venv\Scripts\python -m etl.run_etl          # Excel -> limpieza -> data/sample + SQL Server + validación
.venv\Scripts\python -m etl.run_etl --sin-bd # sin SQL Server: solo regenera data/sample
```

El ETL termina con `OK` y escribe [`data/sample/reporte_carga.md`](data/sample/reporte_carga.md): conciliación de filas y totales Excel ↔ muestra ↔ BD, los 9 KPIs anuales de SQL contra un cálculo directo sobre el Excel, y las filas rechazadas u observadas. Si algo no cuadra, sale con código 1.

Ejecutar el notebook de K-means de punta a punta:

```powershell
.venv\Scripts\python -m jupyter nbconvert --to notebook --execute --inplace mining\01_kmeans_clientes.ipynb
```

## Partes y responsables

| Parte | Carpetas | Responsable | Estado de la base |
|---|---|---|---|
| 1. ETL y Datawarehouse | `etl/`, `sql/ddl/`, `docs/` | *por asignar* | ✅ ETL Python funcionando y validado. Decidir si se queda o se rehace en Pentaho (`docs/decisiones.md`, D4) |
| 2. KPIs y cubo OLAP | `sql/kpis/`, `sql/olap/`, `olap/` | *por asignar* | ✅ 10 KPIs en vistas SQL, verificados. ✅ Vista CUBE/ROLLUP. ⬜ Cubo SSAS (guía + MDX esqueleto) |
| 3. Minería de datos | `mining/` | *por asignar* | ✅ Notebook K-means ejecutable; faltan las decisiones del equipo (🟨 en el notebook) |
| 4. Power BI e interpretación | `powerbi/` | *por asignar* | ✅ Consultas M generadas, relaciones, medidas DAX, boceto. ⬜ Construir el `.pbip` |

Cada carpeta tiene un README corto con lo que falta.

## Cómo trabajar

- `main` siempre funciona: el ETL corre y da `OK`.
- Una rama por tarea (`parte3-kmeans-k`, `parte4-pagina-finanzas`, …) y un **PR con al menos un revisor** del equipo. Con el plazo actual, PRs chicos y revisión el mismo día.
- Si cambias el contrato (`etl/contrato.py`): corre `python -m etl.generar` (regenera DDL, diccionario y consultas de Power Query) y `python -m etl.run_etl`, y avisa a las partes 3 y 4 en el PR.
- No subir `.env`, `.pbix` ni respaldos `.bak` (ya están en `.gitignore`).

## Mapa del repositorio

```
data/raw/          Excel original (datos simulados con fines académicos; 75 KB)
data/sample/       Extracto limpio = contrato (CSV) + reporte_carga.md       ← generado por el ETL
etl/               contrato.py · extract · transform · load · validate · run_etl · generar
sql/ddl/           Tablas (generado desde el contrato)
sql/kpis/          Vistas de KPIs (las crea el ETL) y consultas de evidencia
sql/olap/          Vista CUBE/ROLLUP (la crea el ETL)
olap/              Guía y MDX del cubo SSAS
mining/            Notebook K-means + datos.py + output/ (segmentos que el ETL integra)
powerbi/           Guía, consultas M, medidas DAX y proyecto .pbip
docs/              Diccionario, esquema estrella, reglas de limpieza, KPIs, decisiones
```
