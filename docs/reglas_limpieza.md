# Reglas de limpieza y su justificación

Implementadas en `etl/transform.py`. Criterio de la Fase 1 (sección 2.4): **el formato y la estructura se corrigen; los datos dudosos no se modifican** (se cargan y se anotan en `Etl_Observaciones`), porque el archivo no permite saber cuál es el valor correcto. Lo que no se puede cargar va a `Etl_Rechazos` con su causa, de modo que cada fila de origen queda como cargada o rechazada.

Conteos observados en `datos_andina_retail_corp.xlsx` (SHA256 `7e9568e2…`), verificados en la Fase 2 contra el archivo.

## Correcciones de formato y estructura

| # | Problema | Hoja / columna | Regla | Observado |
|---|---|---|---|---|
| F1 | Filas vacías y una nota debajo de diciembre | Finanzas_Mensual | Solo se toman filas cuyo `Mes` es un nombre de mes; las demás no son registros (no cuentan como rechazos). La nota fija la unidad: USD | 2 vacías + 1 nota |
| F2 | Fechas guardadas como texto | Ventas.Fecha, Clientes.FechaRegistro | Se convierten a `DATE` con formato `AAAA-MM-DD`; si no se puede, la fila se **rechaza** | 970 fechas, 0 inválidas |
| F3 | Meses escritos con su nombre | Finanzas_Mensual.Mes | Se traducen a número y a `mes_key` = AAAAMM | 12 |
| F4 | El año está en el encabezado | Clientes.VisitasWeb2024, ConversionesWeb2024 | Se extrae el año del nombre de la columna → `anio`; las columnas pasan a `visitas_web` y `conversiones_web` | año 2024 |
| F5 | Columnas que son fórmulas de Excel | Ventas.Total, Finanzas.UtilidadNeta, RetornoInversion | Se **recalculan** siempre (`cantidad × precio`, `ingresos − costo − gastos`, `utilidad ÷ inversiones`) y se carga el recalculado. Si el valor del Excel difiere o falta, se anota. Así el ETL no depende de que el archivo tenga los valores ya calculados | 0 diferencias |
| F6 | Retorno mostrado como porcentaje | Finanzas.RetornoInversion | Se guarda como razón (0.94), no como 94 | 12 |
| F7 | Espacios sobrantes en textos | Todas las columnas de texto | Se recortan y se colapsan espacios dobles | 0 casos |
| F8 | Códigos repetidos | OrdenID, ClienteID, Mes | El segundo y siguientes se **rechazan** | 0 casos |
| F9 | Llave huérfana | Ventas.ClienteID | Si no existe en Clientes, la orden se **rechaza** | 0 casos |
| F10 | Valores no numéricos o ≤ 0 | Cantidad, PrecioUnitario, medidas | La fila se **rechaza** | 0 casos |

## Datos dudosos que se cargan sin cambios

| # | Situación | Tratamiento | Observado |
|---|---|---|---|
| O1 | Orden anterior al registro del cliente | Se carga y se anota (`Etl_Observaciones`) | 3 órdenes: AR-20354 y AR-20563 (CLI-0068), AR-20550 (CLI-0030) |
| O2 | Región de la venta ≠ región del cliente | No es error: son dos datos distintos. Se cargan ambos (Dim_Region con dos roles) | 638 de 850 órdenes |
| O3 | Ventas no concilian con ingresos | Cada fuente en su propio hecho; se comparan por mes, sin forzar | $705,113.80 vs. $2,331,474.57 |
| O4 | Diciembre incompleto | No se imputa. El crecimiento de diciembre se marca como parcial | Ventas hasta el 20-dic; 41 órdenes vs. 63–87 |
| O5 | Conversiones web < compras en línea | No se ajusta; la tasa de conversión usa solo la hoja Clientes | 15 clientes (6 con 0 conversiones) |
| O6 | Equipo vendedor no corresponde a canal/región | Se carga tal cual: el equipo es quien registra la venta | p. ej. "Equipo E-commerce" con ventas en tienda |
| O7 | Totales atípicos | Se conservan (son productos caros × 4–5 unidades) | 30 > $2,695.04 (rango intercuartílico) |
| O8 | Nombres de cliente repetidos | `nombre` es solo descriptivo; la llave es `cliente_id` | 89 nombres para 120 clientes |
| O9 | Conversiones > visitas | Se anotaría | 0 casos |

## Resultado de la última carga

Ver `data/sample/reporte_carga.md` (lo regenera cada ejecución del ETL): 0 rechazos, 3 observaciones (O1).
