# Parte 4: Power BI

Reporte de Ventas y Finanzas sobre el contrato de datos (`docs/diccionario_datos.md`). Se puede empezar **hoy** contra `data/sample/` y cambiar a SQL Server con un solo parámetro, sin rehacer el modelo.

## 1. Conexión (fuente intercambiable)

1. Power BI Desktop → **Inicio → Transformar datos → Administrar parámetros → Nuevo**. Crea 4 parámetros de tipo Texto:

   | Parámetro | Valor para empezar | Valor con la BD lista |
   |---|---|---|
   | `FuenteDatos` | `CSV` | `SQL` |
   | `CarpetaMuestra` | ruta absoluta a `data\sample` de tu clon, p. ej. `D:\dev_tools\dmd-proyecto-catedra-fase2\data\sample` | (no se usa) |
   | `Servidor` | `localhost` | `localhost` |
   | `BaseDatos` | `AndinaRetailDW` | `AndinaRetailDW` |

2. Para cada archivo de `power_query/` (10 tablas): **Nueva fuente → Consulta en blanco → Editor avanzado**, pega el contenido y nombra la consulta igual que el archivo (`Hecho_Ventas`, `Dim_Cliente`, …).
3. **Cerrar y aplicar.** Para pasar a SQL Server: cambia `FuenteDatos` a `SQL` y actualiza. Las columnas y tipos son idénticos (los genera `python -m etl.generar` desde el contrato).

Modo: **Importación**. SQL Server usa autenticación de Windows; si Power BI pregunta por cifrado, acepta la conexión sin cifrar (es un servidor local de desarrollo).

> Los archivos `.pq` se generan automáticamente; si cambia el contrato, se regeneran y se vuelven a pegar.

## 2. Modelo: relaciones

Todas uno a muchos, filtro en una sola dirección (dimensión → hecho). Es un esquema **estrella puro**: ninguna dimensión se relaciona con otra (Clase 3).

| Desde (1) | Hacia (N) | Columna | Nota |
|---|---|---|---|
| Dim_Mes | Hecho_Ventas | `mes_key` | Dimensión **conformada**: un segmentador de mes filtra ventas **y** finanzas |
| Dim_Mes | Hecho_Finanzas_Mensual | `mes_key` | |
| Dim_Tiempo | Hecho_Ventas | `tiempo_key` | |
| Dim_Cliente | Hecho_Ventas | `cliente_key` | |
| Dim_Cliente | Hecho_Trafico_Web | `cliente_key` | |
| Dim_Producto | Hecho_Ventas | `producto_key` | |
| Dim_Canal | Hecho_Ventas | `canal_key` | |
| Dim_Vendedor | Hecho_Ventas | `vendedor_key` | |
| Dim_Region | Hecho_Ventas | `region_venta_key` | **Región de la venta** (activa) |
| Dim_Region_Cliente | Hecho_Ventas | `region_cliente_key` | Ver abajo |
| Dim_Region_Cliente | Hecho_Trafico_Web | `region_cliente_key` | |

**Dimensión con dos roles (Dim_Region).** Power BI permite una sola relación activa entre dos tablas. Duplica la consulta: clic derecho en `Dim_Region` → **Referencia**, nómbrala `Dim_Region_Cliente`. Así hay un segmentador "Región de la venta" y otro "Región del cliente" (difieren en 638 de 850 órdenes).

**Tabla calendario.** `Dim_Tiempo` ya es el calendario (366 días de 2024): **Herramientas de tabla → Marcar como tabla de fechas → `fecha`**. Ordena `nombre_mes` por `mes_numero` (en Dim_Tiempo y Dim_Mes). Para análisis por mes usa **Dim_Mes** (filtra ambos hechos); Dim_Tiempo sirve para el detalle diario y para `DATEADD` en el crecimiento.

**Ventas vs. Finanzas.** No se concilian (ventas $705,113.80 vs. ingresos $2,331,474.57). Se comparan solo por mes usando `Dim_Mes`; no relaciones Hecho_Ventas con Hecho_Finanzas_Mensual.

Oculta las columnas `*_key` en la vista de informe.

## 3. Medidas

`medidas.dax`: las 10 de la Fase 1 más medidas base. Cada una trae su valor esperado para 2024. Comprueba que las tarjetas sin filtros den esos valores (también están en `dbo.vw_KPI_Anual` y en `data/sample/reporte_carga.md`).

## 4. Boceto de páginas

| Página | Pregunta de negocio | Visuales |
|---|---|---|
| **Resumen** | ¿Cómo cerró 2024? | 10 tarjetas KPI; margen bruto en rojo si < 40 % |
| **Ventas** | ¿Dónde crece, quién compra y por qué canal? | Línea de ventas por mes y canal; crecimiento % mensual (diciembre marcado como parcial); barras por categoría y producto; matriz región venta × región cliente; ticket por canal |
| **Finanzas** | ¿Es rentable y hay liquidez mes a mes? | Márgenes bruto/neto por mes con línea de 40 %; flujo de caja acumulado; ROI por mes; columnas ingresos/costo/gastos |
| **Clientes** | ¿Qué segmentos pesan más? | Ventas y ticket por `segmento` y `segmento_cluster` (K-means); tasa de conversión web por región y segmento; perfil de grupos (`mining/output/perfil_segmentos.csv`) |
| **Ventas vs. Ingresos** | ¿El crecimiento comercial acompaña al financiero? | Ventas e ingresos por mes (doble eje) con la nota de que no concilian |

Segmentadores comunes: Dim_Mes (mes, trimestre), categoría, canal, región, segmento, grupo K-means.

## 5. Versionado

Guarda como **Proyecto de Power BI (`.pbip`)** en `powerbi/AndinaRetail/`: **Archivo → Guardar como → tipo Proyecto de Power BI**. Es texto (TMDL/JSON), así que Git muestra diferencias y se revisa en PR. `.gitignore` excluye la caché (`.pbi/cache.abf`, `localSettings.json`) y los `.pbix`; el `.pbix` final se exporta solo para la entrega.

Una sola persona edita el `.pbip` a la vez (los cambios simultáneos en el modelo se fusionan mal).

## Alternativa: conexión en vivo al cubo (lo que propuso la Fase 1)

Con conexión en vivo a SSAS, el modelo y las medidas viven en el cubo (MDX, `olap/`) y no en Power BI: los pasos 2 y 3 no aplican, y los visuales hechos contra la muestra se deben volver a enlazar. Ver `docs/decisiones.md`.
