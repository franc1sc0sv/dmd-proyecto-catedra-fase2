# DMD · Proyecto de Cátedra Fase 2: Datawarehouse Andina Retail Corp

Datawarehouse y Minería de Datos (DMD 941) · Universidad Don Bosco.

**Entrega: 27 de noviembre de 2026, 11:59 p. m.** (Aula Digital): un PDF con 6 secciones + enlace al video de defensa. La defensa oral es obligatoria y su fecha aún no se ha anunciado.

## Qué hay aquí, en un minuto

El Excel del caso (`datos_andina_retail_corp.xlsx`) **ya está limpio y cargado** en un Datawarehouse en SQL Server, con el esquema estrella de la Fase 1. Sobre esa base ya funcionan los 10 KPIs y una segmentación K-means. Todo está verificado: los totales y los KPIs coinciden con el Excel original.

Lo más importante: **la misma base existe como archivos CSV** en `data/sample/`. Quien no tenga SQL Server puede trabajar igual con esos archivos, que tienen exactamente las mismas tablas y columnas.

| Si te toca… | Empieza aquí | Qué ya está hecho | Qué te falta |
|---|---|---|---|
| **1. ETL y DW** | `etl/README.md` | ETL completo (Excel → limpieza → SQL Server), con validación automática y reporte de filas descartadas | Decidir si se queda en Python o se rehace en Pentaho, que fue lo que se propuso (`docs/decisiones.md`, D4) |
| **2. KPIs y cubo** | `olap/README.md`, `sql/README.md` | Los 10 KPIs en vistas SQL (valores verificados), consultas de evidencia y un cubo en SQL con `ROLLUP`/`CUBE` | Construir el cubo SSAS siguiendo la guía paso a paso |
| **3. Minería** | `mining/README.md` | Notebook de K-means que corre de punta a punta | Elegir el número de grupos (k) y ponerle nombre a cada grupo (celdas 🟨) |
| **4. Power BI** | `powerbi/README.md` | Consultas listas para pegar, relaciones del modelo, medidas DAX de los 10 KPIs y boceto de las páginas | Armar el reporte en Power BI y escribir la interpretación |
| **Informe PDF** | `docs/README.md` | Textos de apoyo por sección: diccionario, reglas de limpieza, KPIs, decisiones y relación con las clases | Redactar el informe y hacer las capturas |

## Cómo se usa

Requisitos: Windows, Python 3.12 y Git. Para la BD: SQL Server con autenticación de Windows y **ODBC Driver 18 for SQL Server**.

```powershell
git clone <url-del-repo> dmd-proyecto-catedra-fase2
cd dmd-proyecto-catedra-fase2
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
copy .env.example .env                       # ajustar si el servidor no es localhost

.venv\Scripts\python -m etl.run_etl          # carga todo en SQL Server y regenera data/sample
.venv\Scripts\python -m etl.run_etl --sin-bd # sin SQL Server: solo regenera data/sample
```

Al terminar dice `OK` y deja el resultado en [`data/sample/reporte_carga.md`](data/sample/reporte_carga.md).

Para correr el notebook de K-means de punta a punta:

```powershell
.venv\Scripts\python -m jupyter nbconvert --to notebook --execute --inplace mining\01_kmeans_clientes.ipynb
```

## Números de referencia (2024)

Sirven para comprobar que lo que armes cuadra con la base:

| Concepto | Valor |
|---|---|
| Ventas | 850 órdenes · $705,113.80 |
| Ingresos (Finanzas) | $2,331,474.57 (no concilian con las ventas; está documentado) |
| Margen bruto / neto | 41.57 % / 26.90 % |
| Ticket promedio / ventas por cliente | $829.55 / $5,875.95 |
| Participación del e-commerce / conversión web | 44.00 % / 9.01 % |

Los 10 KPIs con su fórmula están en [`docs/kpis.md`](docs/kpis.md).

## Reglas del equipo

- `main` siempre funciona: el ETL corre y da `OK`.
- Una rama por tarea (`parte3-kmeans-k`, `parte4-pagina-finanzas`, …) y un **PR revisado por otra persona del equipo**. Con el plazo actual, PRs pequeños y revisados el mismo día.
- La estructura de las tablas está en un solo archivo, [`etl/contrato.py`](etl/contrato.py). Si la cambias, corre `python -m etl.generar` y `python -m etl.run_etl`, y avísale al resto en el PR.
- No subir `.env`, `.pbix` ni respaldos `.bak` (ya están en `.gitignore`).

## Mapa de carpetas

```
data/raw/      Excel original del caso
data/sample/   La base limpia en CSV + reportes de la carga        (lo genera el ETL)
etl/           Programa que limpia el Excel y carga la base
sql/           Tablas, vistas de KPIs, cubo en SQL y consultas de evidencia
olap/          Guía y cálculos para el cubo SSAS
mining/        Notebook de K-means y sus resultados
powerbi/       Guía, consultas, medidas DAX y el proyecto de Power BI
docs/          Material para el informe
```
