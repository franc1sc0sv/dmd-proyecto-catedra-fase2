# Parte 4: Power BI e interpretación

**Qué es esta carpeta:** todo lo necesario para armar el reporte de Power BI de Ventas y Finanzas: consultas listas para pegar, relaciones, medidas de los KPIs y un boceto de las páginas.

**Para quién:** la persona de la parte 4. **Puedes empezar hoy**, sin SQL Server, usando los CSV de `data/sample/`. Cuando la base esté lista se cambia la fuente con un solo parámetro, sin rehacer nada.

## Qué ya está hecho

- 10 consultas de Power Query (`power_query/*.pq`), una por tabla, con los tipos correctos. Leen los CSV o SQL Server según un parámetro.
- La tabla de relaciones del modelo (paso 3).
- Las medidas DAX de los 10 KPIs (`medidas.dax`), cada una con el valor que debe dar.
- El boceto de 5 páginas (paso 5).

> ⚠️ Nada de esto se ha abierto todavía en Power BI: está escrito y revisado, pero no probado. Si una consulta da error, avisa en el grupo.

## Tus pasos

**1. Crear los parámetros.** Power BI Desktop → **Inicio → Transformar datos → Administrar parámetros → Nuevo**. Crea 4, de tipo Texto:

| Parámetro | Valor para empezar | Valor cuando la BD esté lista |
|---|---|---|
| `FuenteDatos` | `CSV` | `SQL` |
| `CarpetaMuestra` | ruta completa a `data\sample` en tu PC, p. ej. `D:\dev_tools\dmd-proyecto-catedra-fase2\data\sample` | (no se usa) |
| `Servidor` | `localhost` | `localhost` |
| `BaseDatos` | `AndinaRetailDW` | `AndinaRetailDW` |

**2. Cargar las 10 tablas.** Por cada archivo de `power_query/`: **Nueva fuente → Consulta en blanco → Editor avanzado**, pega el contenido y ponle a la consulta **el mismo nombre que el archivo** (`Hecho_Ventas`, `Dim_Cliente`, …). Luego **Cerrar y aplicar**. Modo: **Importación**.

**3. Crear las relaciones** (vista de modelo). Todas son uno a muchos, con filtro en una sola dirección (de la dimensión al hecho):

| Desde (1) | Hacia (N) | Columna | Nota |
|---|---|---|---|
| Dim_Mes | Hecho_Ventas | `mes_key` | Dimensión **compartida**: un filtro de mes afecta ventas **y** finanzas |
| Dim_Mes | Hecho_Finanzas_Mensual | `mes_key` | |
| Dim_Tiempo | Hecho_Ventas | `tiempo_key` | |
| Dim_Cliente | Hecho_Ventas | `cliente_key` | |
| Dim_Cliente | Hecho_Trafico_Web | `cliente_key` | |
| Dim_Producto | Hecho_Ventas | `producto_key` | |
| Dim_Canal | Hecho_Ventas | `canal_key` | |
| Dim_Vendedor | Hecho_Ventas | `vendedor_key` | |
| Dim_Region | Hecho_Ventas | `region_venta_key` | Región **donde se vendió** |
| Dim_Region_Cliente | Hecho_Ventas | `region_cliente_key` | Región **del cliente** (ver abajo) |
| Dim_Region_Cliente | Hecho_Trafico_Web | `region_cliente_key` | |

- **Dos regiones.** Power BI no permite dos relaciones activas entre las mismas tablas. Clic derecho en la consulta `Dim_Region` → **Referencia** y nombra la nueva `Dim_Region_Cliente`. Así tendrás un filtro "Región de la venta" y otro "Región del cliente" (son distintas en 638 de 850 órdenes).
- **Calendario.** `Dim_Tiempo` ya es el calendario: **Herramientas de tabla → Marcar como tabla de fechas → `fecha`**. Ordena `nombre_mes` por `mes_numero` en Dim_Tiempo y en Dim_Mes.
- **Mes en ejes y filtros:** usa **Dim_Mes**, porque filtra ventas y finanzas. Las medidas `Crecimiento ventas %` y `Mes parcial` están hechas para Dim_Mes en el eje. Dim_Tiempo es solo para el detalle diario.
- **No relaciones Hecho_Ventas con Hecho_Finanzas_Mensual.** No concilian (ventas $705,113.80 vs. ingresos $2,331,474.57); se comparan solo por mes con Dim_Mes.
- Oculta las columnas `*_key` en la vista de informe.

Es un esquema **estrella**: ninguna dimensión se relaciona con otra (Clase 3).

**4. Crear las medidas.** Crea una tabla vacía `_Medidas` (**Inicio → Especificar datos**) y agrega cada medida de `medidas.dax` (**Nueva medida**, pega una por una). Pon una tarjeta por medida **sin filtros** y compara con el valor entre corchetes del archivo. Por ejemplo, `Ventas` = 705,113.80. Para el crecimiento, haz una tabla con `Dim_Mes[nombre_mes]`: mayo debe dar −22.84 % y octubre +49.08 %, y solo diciembre debe tener `Mes parcial` = 1.

**5. Armar las páginas** (boceto; Clase 12: datos → formato → boceto → interactividad):

| Página | Pregunta de negocio | Visuales |
|---|---|---|
| **Resumen** | ¿Cómo cerró 2024? | 10 tarjetas KPI; margen bruto en rojo si < 40 % (medida `Alerta margen bruto`) |
| **Ventas** | ¿Dónde crece, quién compra y por qué canal? | Línea de ventas por mes y canal; crecimiento % mensual (diciembre marcado como parcial); barras por categoría y producto; matriz región venta × región cliente; ticket por canal |
| **Finanzas** | ¿Es rentable y hay liquidez mes a mes? | Márgenes bruto y neto por mes con línea de 40 %; flujo de caja acumulado; ROI por mes; columnas ingresos, costo y gastos |
| **Clientes** | ¿Qué segmentos pesan más? | Ventas y ticket por `segmento` y por `segmento_cluster` (K-means); tasa de conversión web por región y segmento |
| **Ventas vs. Ingresos** | ¿El crecimiento comercial acompaña al financiero? | Ventas e ingresos por mes (doble eje), con una nota de que no concilian |

Filtros comunes en todas las páginas: mes y trimestre (Dim_Mes), categoría, canal, región, segmento y grupo K-means.

**6. Guardar como proyecto.** **Archivo → Guardar como → Proyecto de Power BI (`.pbip`)** en `powerbi/AndinaRetail/`. Es texto, así que Git muestra los cambios. El `.pbix` no se sube; se exporta solo para la entrega. Que **una sola persona** edite el proyecto a la vez.

**7. Cuando la base esté lista:** cambia `FuenteDatos` a `SQL` y pulsa **Actualizar**. Si Power BI pregunta por el cifrado, acepta la conexión sin cifrar (es un servidor local).

**8. Interpretación (sección 6 del informe):** una o dos frases de negocio por página. Qué pasó, por qué y qué haría Andina (Clase 17: ¿qué pasó?, ¿por qué?).

## Archivos

| Archivo | Qué es | ¿Lo editas? |
|---|---|---|
| `power_query/*.pq` | Las 10 consultas. Se generan desde `etl/contrato.py` con `python -m etl.generar` | No |
| `medidas.dax` | Medidas de los KPIs con el valor esperado de cada una | Puedes agregar medidas |
| `AndinaRetail/` | El proyecto `.pbip` (lo creas en el paso 6) | Sí |

## Cómo sabes que terminaste

Las tarjetas sin filtros dan los valores de `medidas.dax`, las 5 páginas responden su pregunta, el proyecto está guardado como `.pbip` y cada página tiene su interpretación escrita.

## Alternativa: conexión en vivo al cubo

Es lo que propuso la Fase 1. En ese caso el modelo y las medidas viven en el cubo SSAS (`olap/`), no en Power BI: los pasos 1 a 4 no aplican y hay que esperar a que el cubo esté desplegado. Ver [`docs/decisiones.md`](../docs/decisiones.md), D5.
