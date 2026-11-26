# Clases de las unidades 3, 4 y 5 → implementación

Qué concepto de cada clase (UIA3, UIA4, UIA5) aplica el proyecto, dónde está y en qué sección del informe conviene citarlo. Las unidades son teóricas: no prescriben herramientas, así que lo que sigue es cómo la implementación encaja en su vocabulario.

| Clase | Concepto | Dónde se aplica | Sección del informe |
|---|---|---|---|
| 9 · ETL | Técnica de **consolidación**: varias fuentes (3 hojas) → un destino que guarda una copia (el DW) | `etl/` | 2 |
| 9 · ETL | Extracción **pull por lotes** y **carga total**; no se requiere CDC (año fiscal cerrado, sin marcas de cambio) | `etl/run_etl.py`, `etl/load.py` | 2 |
| 9 · ETL | Motores de extracción, transformación y carga + **servicios de administración y operación** (log de errores, estadísticas) | `extract.py`, `transform.py`, `load.py`; `Etl_Rechazos`, `Etl_Observaciones`, `reporte_carga.md` | 2 |
| 9 · ETL | Tipos de ETL: *basado en motor* (Pentaho, gráfico) vs. código propio. El ETL en Python es código propio, no un ETL basado en motor; ver `decisiones.md` D4 | — | 5 |
| 10 · OLAP | Tipos: **MOLAP** (cubo SSAS multidimensional, Fase 1) y **ROLAP** (vista `vw_Cubo_Ventas` sobre las tablas relacionales) | `olap/`, `sql/olap/01_vistas_cubo.sql` | 4 |
| 10 · OLAP | Elementos: esquema, **cubo**, **jerarquía** (año → semestre → trimestre → mes → día; categoría → producto), **nivel**, **miembro**, roles, **MDX** | `olap/README.md`, `olap/ssas/kpis_calculados.mdx` | 4 y 5 |
| 10 · OLAP | **Cubo virtual**: cruzar hechos por dimensiones comunes. Ventas y Finanzas se cruzan por la dimensión conformada Dim_Mes | `Dim_Tiempo.mes_key` → `Dim_Mes` | 5 |
| 11 · Informes | Elementos de un informe: texto, tablas, gráficos, **métricas**, **alertas visuales automáticas** (margen bruto < 40 %) | `powerbi/README.md`, `alerta_margen_bruto` en `vw_KPI_Finanzas_Mensual` | 6 |
| 11 · Informes | **KPI vs. KGI**: el KPI mide; el KGI es la meta a alcanzar. La Fase 1 solo fijó una meta (margen bruto ≥ 40 %); las demás quedan **pendientes** | `docs/kpis.md` → Metas | 3 |
| 11 · Informes | Métricas *lagging* (resultado: ventas, márgenes) y *leading* (actividad: visitas web) | `docs/kpis.md` | 3 |
| 12 · Cuadro de mando | Proceso: elegir datos → formato → **boceto** → **interactividad** → implementar | `powerbi/README.md` (boceto y segmentadores) | 6 |
| 12 · Cuadro de mando | Cuadro de mando (táctico, monitoriza Ventas y Finanzas) ≠ Balanced Scorecard (estrategia). El reporte es un cuadro de mando con perspectivas financiera y de cliente | `powerbi/` | 6 |
| 13 · Minería | Proceso **KDD**: selección → preparación → minería → evaluación/interpretación → difusión | Encabezados de `mining/01_kmeans_clientes.ipynb` | 4 |
| 13 · Minería | **OLAP vs. minería**: OLAP responde "qué pasó" (KPIs, cubo); la minería descubre lo no evidente (segmentos K-means) | — | 4 y 6 |
| 14 · Algoritmos | Aprendizaje **no supervisado = agrupamiento**: K-means no necesita etiqueta (el Excel no tiene "cliente perdido") | Notebook | 4 |
| 14 · Algoritmos | K-means: inicialización, asignación al centroide más cercano, actualización; minimiza distancias cuadráticas | Notebook (`KMeans`, inercia = SSE) | 4 |
| 14 · Algoritmos | Reglas de asociación (soporte y confianza sobre **canastas**) y árboles (necesitan clase objetivo): descartados, porque cada orden tiene un producto y no hay variable objetivo | `decisiones.md` D7 | 4 |
| 15.2 · KDD | Limpieza e integración: identificación por **identificadores externos** (ClienteID, OrdenID), datos faltantes e **inconsistentes entre fuentes** | `docs/reglas_limpieza.md` | 2 |
| 15.3 · KDD | **Informe de estado de los atributos** (#total, #nulos, #distintos, media, desv., moda, mín., máx.) | `data/sample/perfil_atributos.md` (lo genera el ETL) | 2 |
| 15.4 · KDD | Operadores OLAP: **drill, roll, slice & dice, pivot** | `sql/olap/02_operadores_olap.sql` | 4 |
| 17 · BI | Preguntas de BI: ¿qué pasó? (KPIs), ¿por qué? (cubo, drill), ¿qué pasará? (fuera de alcance) | — | 6 |
| 17 · BI | **BIMM**: Andina pasa de la fase 2 ("Excel caos", datos accesibles sin BI) a las fases 4–7 (DW, OLAP, minería) | — | 1 y 6 |
| 18 · Tendencias | **Data quality** y **MDM**: una sola lista por concepto (regiones, productos), llaves maestras | Dimensiones conformadas, `reglas_limpieza.md` | 2 |
| 19 · Alcances | Niveles: **estratégico** (cuadro de mando), **táctico** (consultas OLAP), operativo (reportes); objetivos de BI en **Ventas** y **Finanzas** | Páginas del reporte, cubo | 6 |
| 20 · Tecnología | Open source (Pentaho, Python/scikit-learn) vs. propietario (SQL Server, SSAS, Power BI) | Pila elegida en la Fase 1 | 4 |
