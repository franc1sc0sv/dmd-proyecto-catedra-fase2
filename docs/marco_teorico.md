# Clases de las unidades 1 a 5 → implementación

Qué concepto de cada clase (UIA1 a UIA5) aplica el proyecto, dónde está y en qué sección del informe conviene citarlo. Las unidades son teóricas: no prescriben herramientas, así que lo que sigue es cómo la implementación encaja en su vocabulario.

| Clase | Concepto | Dónde se aplica | Sección del informe |
|---|---|---|---|
| 1 · Soporte de decisiones | Datos operacionales vs. para soporte de decisiones: **tiempo** (año fiscal completo), **granularidad** (orden → mes → año), **dimensionalidad** | Hechos con grano de orden y de mes; vistas mensuales y anuales | 1 |
| 1 · Soporte de decisiones | Requisitos de la BD de soporte: esquema no normalizado, **extracción y filtrado** (validación, fechas en formatos distintos, mismo dato con nombres distintos), interfaz analítica | `etl/`, `reglas_limpieza.md`, Power BI | 2 |
| 2 · Almacén de datos | Inmon: integrado, **orientado a temas**, **variante en el tiempo**, **no volátil** | Tres temas (ventas, finanzas, tráfico web); Dim_Tiempo y Dim_Mes; carga total por lotes, sin actualizaciones en línea | 1 y 5 |
| 2 · Almacén de datos | Reglas de Inmon 6 (solo lectura + carga periódica por lotes), 8 (**varios niveles de detalle**), 10 (**seguimiento de fuentes y transformaciones**), 11 (**metadatos**) | 6: `run_etl`; 8: hechos + `vw_KPI_*` + cubo; 10: `reporte_carga.md`, `Etl_*`; 11: `contrato.py` → `diccionario_datos.md` (columna *Origen*) | 5 |
| 3 · Modelo multidimensional | **Estrella antes que copo de nieve**; las dimensiones solo se relacionan con los hechos | `esquema_estrella.md`; `mes_key` en el hecho y no en Dim_Tiempo (`decisiones.md` D2) | 5 |
| 3 · Modelo multidimensional | Llave del hecho = **composición de las llaves de las dimensiones**; medidas numéricas y **aditivas** | PK compuesta de `Hecho_Ventas`; `precio_unitario` y `retorno_inversion` no aditivas (se recalculan) | 5 |
| 3 · Modelo multidimensional | **Dimensión tiempo** obligatoria; **jerarquías y niveles** (mes → semestre → año) | Dim_Tiempo, Dim_Mes; jerarquías en `olap/README.md` | 5 |
| 4 · Implementación | Diseñador: criterios de integración y carga, desempeño de consulta, necesidades del usuario final | ETL validado; vistas; páginas de Power BI por pregunta de negocio | 5 y 6 |
| 5 · Data warehouse | Proceso de negocio → **hecho**; vista → **dimensión**; indicador → **métrica** | Tres procesos → tres hechos | 5 |
| 5 · Data warehouse | Tipos de hecho: **transaccional** (Ventas) y **snapshot periódico** (Finanzas mensual, Tráfico web anual) | `contrato.py` → *Clasificación* en el diccionario | 5 |
| 5 · Data warehouse | Tipos de dimensión: **SCD 0** (Tiempo), **SCD 1** (resto; la carga total sobrescribe), **degenerada** (`orden_id`, `anio`), **conformada** (Dim_Mes), **role-playing** (Dim_Region) | `contrato.py` → diccionario | 5 |
| 5 · Data warehouse | Métricas vs. **KPI** vs. **KGI** (meta) | `docs/kpis.md` | 3 |
| 6 · Ciclo de vida | **Kimball**: requisitos del negocio → rutas de tecnología, datos (modelado dimensional, diseño físico, ETL) y BI → implementación y mantenimiento | Fase 1 = requisitos y diseño; Fase 2 = las tres rutas | 1 y cronograma |
| 7 · Herramientas ETL | Funciones: definir fuentes, **asignaciones origen → destino**, transformaciones, carga y **actualización** (carga total) | Columna *Origen* del diccionario; `transform.py`; `load.py` | 2 |
| 7 · Herramientas ETL | Excel = dato **semiestructurado**; transformación = limpieza, estandarización y **datos derivados** (leyes de derivación) | `total`, `utilidad_neta` y `retorno_inversion` recalculados | 2 |
| 7 · Herramientas ETL | **Data profiling** y **data quality** como funciones del ETL | `perfil_atributos.md`, `reporte_carga.md` | 2 |
| 8 · Análisis multidimensional | Agregación por niveles, **bajar y subir** (drill/roll), tablas pivote, cálculos de negocio (márgenes, participación, comparación de periodos) | `vw_Cubo_Ventas`, `02_operadores_olap.sql`, medidas DAX/MDX | 4 |
| 9 · ETL | Técnica de **consolidación**: varias fuentes (3 hojas) → un destino que guarda una copia (el DW) | `etl/` | 2 |
| 9 · ETL | Extracción **pull por lotes** y **carga total**; no se requiere CDC (año fiscal cerrado, sin marcas de cambio) | `etl/run_etl.py`, `etl/load.py` | 2 |
| 9 · ETL | Motores de extracción, transformación y carga + **servicios de administración y operación** (log de errores, estadísticas) | `extract.py`, `transform.py`, `load.py`; `Etl_Rechazos`, `Etl_Observaciones`, `reporte_carga.md` | 2 |
| 9 · ETL | Tipos de ETL: *basado en motor* (Pentaho, gráfico) vs. código propio. El ETL en Python es código propio, no un ETL basado en motor; ver `decisiones.md` D4 | — | 5 |
| 10 · OLAP | Tipos: **MOLAP** (cubo SSAS multidimensional, Fase 1) y **ROLAP** (vista `vw_Cubo_Ventas` sobre las tablas relacionales) | `olap/`, `sql/olap/01_vistas_cubo.sql` | 4 |
| 10 · OLAP | Elementos: esquema, **cubo**, **jerarquía** (año → semestre → trimestre → mes → día; categoría → producto), **nivel**, **miembro**, roles, **MDX** | `olap/README.md`, `olap/ssas/kpis_calculados.mdx` | 4 y 5 |
| 10 · OLAP | **Cubo virtual**: cruzar hechos por dimensiones comunes. Ventas y Finanzas se cruzan por la dimensión conformada Dim_Mes | `mes_key` en ambos hechos | 5 |
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
